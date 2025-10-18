# Ubuntu 22.04 Deployment Guide

Complete guide untuk deploy OLT Management System di Ubuntu 22.04 LTS.

## 📋 Pre-requisites

### Server Requirements
- Ubuntu 22.04 LTS (fresh install recommended)
- Minimum 2GB RAM
- 10GB free disk space
- Internet connection
- Root/sudo access

### Network Requirements
- Server harus bisa diakses dari network
- Port 80 (HTTP) dan 443 (HTTPS) terbuka
- Koneksi ke OLT ZTE C320 (untuk SNMP/Telnet)

## 🚀 Quick Start

### Method 1: Via SSH

```bash
# 1. Connect to your Ubuntu server
ssh user@your-server-ip

# 2. Download the project
git clone <repository-url>
cd olt_zte_network_management_app/deployment/ubuntu22

# 3. Make script executable
chmod +x install.sh

# 4. Run installation
sudo ./install.sh

# 5. Wait for installation to complete (5-10 minutes)
# You'll see the application URL and credentials when done
```

### Method 2: Via SCP (Upload from local)

```bash
# 1. Compress the project locally
tar -czf olt_app.tar.gz olt_zte_network_management_app/

# 2. Upload to server
scp olt_app.tar.gz user@your-server:/tmp/

# 3. SSH to server and extract
ssh user@your-server
cd /tmp
tar -xzf olt_app.tar.gz
cd olt_zte_network_management_app/deployment/ubuntu22

# 4. Run installation
chmod +x install.sh
sudo ./install.sh
```

## 📦 What Gets Installed

The installation script will install and configure:

1. **System Packages:**
   - Python 3.11
   - PostgreSQL database
   - Node.js 18.x
   - Nginx web server
   - SNMP tools

2. **Application Components:**
   - Backend API (FastAPI)
   - Frontend (React)
   - Database with initial schema
   - Default admin user

3. **System Services:**
   - systemd service for backend
   - Nginx reverse proxy
   - PostgreSQL database

4. **Utility Commands:**
   - `olt-start` - Start application
   - `olt-stop` - Stop application
   - `olt-restart` - Restart application
   - `olt-logs` - View logs
   - `olt-status` - Check status

## 🔍 Installation Process Details

### Step-by-Step Breakdown

1. **System Update** (1-2 min)
   - Updates package lists
   - Upgrades existing packages

2. **Dependencies Installation** (3-5 min)
   - Installs Python, Node.js, PostgreSQL, Nginx
   - Downloads and installs all required libraries

3. **User & Database Setup** (30 sec)
   - Creates application user `oltuser`
   - Creates PostgreSQL database
   - Generates secure passwords

4. **Application Setup** (2-3 min)
   - Copies files to `/opt/olt_management`
   - Installs Python dependencies
   - Installs Node.js dependencies
   - Builds frontend

5. **Configuration** (30 sec)
   - Configures environment variables
   - Sets up Nginx
   - Creates systemd service

6. **Initialization** (1 min)
   - Creates database tables
   - Creates default admin user
   - Starts services

**Total Time: 5-10 minutes**

## 🎯 Post-Installation

### 1. Verify Installation

```bash
# Check all services
olt-status

# You should see all services as "active (running)"
```

### 2. Access Application

Open browser and navigate to:
```
http://your-server-ip
```

Login with:
- Username: `admin`
- Password: `admin123`

### 3. Change Default Password

**IMPORTANT:** Change the default password immediately!

1. Login with default credentials
2. Go to Settings (or User Profile)
3. Change password
4. Logout and login with new password

### 4. Add First OLT

1. Go to **OLT Management**
2. Click **Add OLT**
3. Fill in OLT details:
   - Name: e.g., "OLT-Jakarta-01"
   - IP: e.g., "192.168.1.100"
   - SNMP Community: "public" (or your custom community)
4. Click **Test** to verify connection
5. Click **Sync** to discover ONUs

## 🔧 Configuration

### Environment Variables

Backend configuration is stored in:
```
/opt/olt_management/backend/.env
```

To edit:
```bash
sudo nano /opt/olt_management/backend/.env
```

Common settings:
```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Security
SECRET_KEY=<your-secret-key>
ACCESS_TOKEN_EXPIRE_MINUTES=30

# SNMP Settings
DEFAULT_SNMP_VERSION=2c
SNMP_TIMEOUT=5
```

After editing, restart the application:
```bash
sudo olt-restart
```

### Nginx Configuration

Nginx config is at:
```
/etc/nginx/sites-available/olt_management
```

To edit:
```bash
sudo nano /etc/nginx/sites-available/olt_management
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## 🔒 Security Hardening

### 1. Enable HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate (replace with your domain)
sudo certbot --nginx -d olt.yourdomain.com

# Certificate will auto-renew
```

### 2. Configure Firewall

```bash
# Reset firewall
sudo ufw --force reset

# Allow SSH (IMPORTANT!)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw --force enable

# Check status
sudo ufw status
```

### 3. Secure PostgreSQL

```bash
# Edit PostgreSQL config
sudo nano /etc/postgresql/14/main/postgresql.conf

# Change:
listen_addresses = 'localhost'  # Only local connections

# Restart PostgreSQL
sudo systemctl restart postgresql
```

### 4. Regular Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update application
cd /opt/olt_management/deployment/ubuntu22
sudo ./update.sh
```

## 📊 Monitoring & Logs

### Application Logs

```bash
# Real-time logs
olt-logs

# Last 100 lines
sudo journalctl -u olt_management -n 100

# Today's logs
sudo journalctl -u olt_management --since today
```

### Nginx Logs

```bash
# Access logs
sudo tail -f /var/log/nginx/access.log

# Error logs
sudo tail -f /var/log/nginx/error.log
```

### Database Logs

```bash
# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### System Resources

```bash
# CPU and Memory usage
htop

# Disk usage
df -h

# Network connections
sudo netstat -tulpn
```

## 🔄 Backup & Restore

### Backup Database

```bash
# Create backup directory
sudo mkdir -p /opt/backups

# Backup database
sudo -u postgres pg_dump olt_management > /opt/backups/olt_db_$(date +%Y%m%d).sql

# Compress backup
gzip /opt/backups/olt_db_$(date +%Y%m%d).sql
```

### Automated Backup Script

```bash
# Create backup script
sudo nano /usr/local/bin/olt-backup

# Add:
#!/bin/bash
BACKUP_DIR="/opt/backups"
DATE=$(date +%Y%m%d_%H%M%S)
sudo -u postgres pg_dump olt_management | gzip > $BACKUP_DIR/olt_db_$DATE.sql.gz
# Keep only last 7 days
find $BACKUP_DIR -name "olt_db_*.sql.gz" -mtime +7 -delete

# Make executable
sudo chmod +x /usr/local/bin/olt-backup

# Add to crontab (daily at 2 AM)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/olt-backup") | crontab -
```

### Restore Database

```bash
# Stop application
sudo olt-stop

# Restore from backup
gunzip < /opt/backups/olt_db_20250119.sql.gz | sudo -u postgres psql olt_management

# Start application
sudo olt-start
```

## 🐛 Troubleshooting

### Issue: Application won't start

```bash
# Check service status
sudo systemctl status olt_management

# Check if port 8000 is free
sudo netstat -tulpn | grep 8000

# If port is in use, kill the process
sudo kill -9 $(sudo lsof -t -i:8000)

# Restart
sudo olt-restart
```

### Issue: Can't access web interface

```bash
# Check if Nginx is running
sudo systemctl status nginx

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Check firewall
sudo ufw status

# Check if port 80 is open
sudo netstat -tulpn | grep :80
```

### Issue: Database connection error

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
sudo -u postgres psql -c "SELECT version();"

# Restart PostgreSQL
sudo systemctl restart postgresql

# Check database exists
sudo -u postgres psql -l | grep olt_management
```

### Issue: SNMP connection failed

```bash
# Test SNMP from server
snmpget -v2c -c public <olt-ip> 1.3.6.1.2.1.1.1.0

# Check network connectivity
ping <olt-ip>

# Check firewall on OLT
# Make sure SNMP (UDP 161) is allowed
```

## 🔄 Updating

### Update to New Version

```bash
cd /opt/olt_management/deployment/ubuntu22
sudo ./update.sh
```

The update script will:
1. Backup current installation
2. Update backend dependencies
3. Rebuild frontend
4. Restart services

If something goes wrong, backup can be restored:
```bash
sudo systemctl stop olt_management
sudo rm -rf /opt/olt_management
sudo mv /opt/olt_backup_YYYYMMDD_HHMMSS /opt/olt_management
sudo systemctl start olt_management
```

## 🗑️ Uninstallation

To completely remove the application:

```bash
cd /opt/olt_management/deployment/ubuntu22
sudo ./uninstall.sh
```

You'll be asked:
- Confirm uninstallation
- Remove database? (yes/no)
- Remove user? (yes/no)

## 📞 Support

If you encounter issues:

1. Check logs: `olt-logs`
2. Check status: `olt-status`
3. Review troubleshooting section
4. Create issue on GitHub with logs

## ✅ Checklist

After installation, verify:

- [ ] Application accessible via browser
- [ ] Can login with admin credentials
- [ ] Changed default password
- [ ] Added at least one OLT
- [ ] OLT connection test successful
- [ ] Can discover ONUs
- [ ] Dashboard shows statistics
- [ ] All services running (`olt-status`)
- [ ] Firewall configured
- [ ] Backup script set up (optional)
- [ ] HTTPS enabled (recommended)

---

**Installation support: support@example.com**
