#!/bin/bash

# OLT ZTE C320 Management System - Ubuntu 22.04 Installation Script
# This script will install all dependencies and configure the system

set -e

echo "================================================"
echo "OLT ZTE C320 Management System Installer"
echo "Ubuntu 22.04 LTS"
echo "================================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Variables
APP_DIR="/opt/olt_management"
APP_USER="oltuser"
DB_NAME="olt_management"
DB_USER="olt_user"
DB_PASS=$(openssl rand -base64 32)
SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')

echo "Step 1: Updating system packages..."
apt update
apt upgrade -y

echo "Step 2: Installing system dependencies..."
apt install -y \
    software-properties-common \
    curl \
    git \
    build-essential \
    nginx \
    postgresql \
    postgresql-contrib \
    snmp \
    snmpd

echo "Step 2.1: Enabling Python 3.11 repository..."
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.11 python3.11-venv python3-pip

# Install Node.js 18.x
echo "Step 3: Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

echo "Step 4: Creating application user..."
if ! id "$APP_USER" &>/dev/null; then
    useradd -r -m -s /bin/bash $APP_USER
    echo "User $APP_USER created"
else
    echo "User $APP_USER already exists"
fi

echo "Step 5: Setting up PostgreSQL database..."
# Create role if not exists (robust check, quiet CWD warnings)
if ! sudo -u postgres bash -c "cd ~; psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'\" | grep -q 1"; then
    sudo -u postgres bash -c "cd ~; psql -c \"CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';\""
fi
# Create database if not exists and set owner
if ! sudo -u postgres bash -c "cd ~; psql -tAc \"SELECT 1 FROM pg_database WHERE datname='$DB_NAME'\" | grep -q 1"; then
    sudo -u postgres bash -c "cd ~; psql -c \"CREATE DATABASE $DB_NAME OWNER $DB_USER;\""
fi
# Ensure privileges
sudo -u postgres bash -c "cd ~; psql -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;\"" || true
# Ensure password matches the .env configuration
sudo -u postgres bash -c "cd ~; psql -c \"ALTER USER $DB_USER WITH PASSWORD '$DB_PASS';\"" || true

echo "Step 6: Creating application directory..."
mkdir -p $APP_DIR
# Navigate to project root (2 levels up from deployment/ubuntu22)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cp -r $PROJECT_ROOT/backend $APP_DIR/
cp -r $PROJECT_ROOT/frontend $APP_DIR/

# Set ownership
chown -R $APP_USER:$APP_USER $APP_DIR

echo "Step 7: Setting up Python backend..."
cd $APP_DIR/backend
sudo -u $APP_USER python3.11 -m venv .venv
sudo -u $APP_USER .venv/bin/pip install --upgrade pip
sudo -u $APP_USER .venv/bin/pip install -r requirements.txt

echo "Step 8: Configuring backend environment..."
SERVER_IP=$(hostname -I | awk '{print $1}')
# URL-encode DB_PASS for use in DATABASE_URL (requires Python 3.11 installed above)
ENC_DB_PASS=$(python3.11 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$DB_PASS")
cat > $APP_DIR/backend/.env << EOF
DATABASE_URL=postgresql://$DB_USER:$ENC_DB_PASS@localhost:5432/$DB_NAME
APP_NAME=OLT ZTE C320 Management System
APP_VERSION=1.0.0
DEBUG=False
API_PREFIX=/api/v1
SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["http://$SERVER_IP","http://localhost","http://127.0.0.1"]
DEFAULT_SNMP_VERSION=2c
DEFAULT_SNMP_PORT=161
DEFAULT_TELNET_PORT=23
SNMP_TIMEOUT=5
TELNET_TIMEOUT=10
EOF

chown $APP_USER:$APP_USER $APP_DIR/backend/.env
chmod 600 $APP_DIR/backend/.env

echo "Step 9: Initializing database..."
cd $APP_DIR/backend
sudo -u $APP_USER .venv/bin/python -c "from app.db.database import init_db; init_db()"

echo "Step 10: Creating default admin user..."
sudo -u $APP_USER .venv/bin/python << PYEOF
from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()
admin_user = db.query(User).filter(User.username == "admin").first()
if not admin_user:
    admin = User(
        username="admin",
        email="admin@localhost",
        full_name="System Administrator",
        hashed_password=get_password_hash("admin123"),
        is_active=True,
        is_superuser=True
    )
    db.add(admin)
    db.commit()
    print("Admin user created: username=admin, password=admin123")
else:
    print("Admin user already exists")
db.close()
PYEOF

echo "Step 11: Building frontend..."
cd $APP_DIR/frontend
sudo -u $APP_USER npm install
SERVER_IP=$(hostname -I | awk '{print $1}')
cat > $APP_DIR/frontend/.env << EOF
VITE_API_URL=http://$SERVER_IP/api/v1
EOF
sudo -u $APP_USER npm run build

echo "Step 12: Configuring Nginx..."
cat > /etc/nginx/sites-available/olt_management << 'EOF'
server {
    listen 80;
    server_name _;

    # Frontend
    location / {
        root /opt/olt_management/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/olt_management /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

echo "Step 13: Creating systemd service..."
cat > /etc/systemd/system/olt_management.service << EOF
[Unit]
Description=OLT ZTE C320 Management System Backend
After=network.target postgresql.service

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR/backend
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:$APP_DIR/backend/.venv/bin"
ExecStart=$APP_DIR/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable olt_management
systemctl start olt_management

echo "Step 14: Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo "y" | ufw enable || true

echo "Step 15: Creating start/stop scripts..."
cat > /usr/local/bin/olt-start << 'EOF'
#!/bin/bash
systemctl start olt_management
systemctl status olt_management
EOF

cat > /usr/local/bin/olt-stop << 'EOF'
#!/bin/bash
systemctl stop olt_management
EOF

cat > /usr/local/bin/olt-restart << 'EOF'
#!/bin/bash
systemctl restart olt_management
systemctl status olt_management
EOF

cat > /usr/local/bin/olt-logs << 'EOF'
#!/bin/bash
journalctl -u olt_management -f
EOF

cat > /usr/local/bin/olt-status << 'EOF'
#!/bin/bash
echo "=== Backend Status ==="
systemctl status olt_management --no-pager
echo ""
echo "=== Nginx Status ==="
systemctl status nginx --no-pager
echo ""
echo "=== PostgreSQL Status ==="
systemctl status postgresql --no-pager
EOF

chmod +x /usr/local/bin/olt-*

echo ""
echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo ""
echo "Application URL: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "Default Login:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Database Credentials (saved in $APP_DIR/backend/.env):"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASS"
echo ""
echo "Useful Commands:"
echo "  olt-start    - Start the application"
echo "  olt-stop     - Stop the application"
echo "  olt-restart  - Restart the application"
echo "  olt-logs     - View application logs"
echo "  olt-status   - Check services status"
echo ""
echo "IMPORTANT: Please change the default admin password after first login!"
echo "================================================"
