# OLT ZTE C320 Management & Monitoring System

Aplikasi web management dan monitoring untuk OLT ZTE C320 yang lengkap dengan management ODP, ONU, dan visualisasi alur kabel route.

## 🚀 Features

### Core Features
- ✅ **OLT Management** - Add, edit, delete, dan monitor OLT devices
- ✅ **ONU Management** - List, register, dan monitor ONUs 
- ✅ **ODP Management** - Manage Optical Distribution Points
- ✅ **Cable Route Visualization** - Interactive network topology diagram
- ✅ **Real-time Monitoring** - SNMP-based monitoring
- ✅ **Dashboard** - Comprehensive statistics dan alerts
- ✅ **User Authentication** - JWT-based authentication

### Technical Features
- 🔌 **SNMP Communication** - Connect to ZTE C320 via SNMP v2c
- 📡 **Telnet/SSH Support** - Configuration management
- 📊 **Signal Monitoring** - RX/TX power, distance, status
- 🗺️ **Geographic Mapping** - ODP location tracking
- 📈 **Statistics & Reports** - Real-time network statistics
- 🎨 **Dark Theme UI** - Modern, responsive interface

## 🏗️ Architecture

```
Frontend (React + Vite + Ant Design)
    ↓
Backend API (FastAPI + Python)
    ↓
    ├── PostgreSQL Database
    └── OLT ZTE C320 (SNMP/Telnet)
```

## 📋 Requirements

### Production (Ubuntu 22.04)
- Ubuntu 22.04 LTS
- Python 3.11+
- PostgreSQL 15+
- Node.js 18+
- Nginx
- 2GB RAM minimum
- 10GB disk space

### Development
- Python 3.11+
- Node.js 18+
- PostgreSQL (or use SQLite for development)

## 🔧 Installation

### Quick Install (Ubuntu 22.04)

1. **Download the project to your Ubuntu server:**
```bash
# Via git
git clone <repository-url>
cd olt_zte_network_management_app

# Or upload via SCP
scp -r olt_zte_network_management_app user@server:/tmp/
```

2. **Run the installation script:**
```bash
cd deployment/ubuntu22
chmod +x install.sh
sudo ./install.sh
```

3. **Access the application:**
```
http://your-server-ip
```

Default credentials:
- Username: `admin`
- Password: `admin123`

**IMPORTANT: Change the default password immediately after first login!**

## 🎮 Management Commands

After installation, you can use these commands:

```bash
# Start application
olt-start

# Stop application  
olt-stop

# Restart application
olt-restart

# View logs
olt-logs

# Check status
olt-status
```

## 📱 Usage Guide

### 1. Adding OLT Device

1. Go to **OLT Management** page
2. Click **Add OLT** button
3. Fill in the form:
   - Name: Friendly name for the OLT
   - IP Address: OLT IP address
   - SNMP Community: Default is "public"
   - Telnet Username/Password: For configuration access
4. Click **Test** to verify connection
5. Click **Sync** to discover ONUs

### 2. Managing ONUs

1. Go to **ONU Management** page
2. Select OLT from dropdown
3. Click **Discover ONUs** to find all connected ONUs
4. View ONU details:
   - Serial Number
   - Customer information
   - Status (Online/Offline)
   - Signal strength (RX/TX power)
   - Distance
5. Click **Refresh** to update individual ONU status

### 3. Managing ODPs

1. Go to **ODP Management** page
2. Click **Add ODP**
3. Fill in ODP information:
   - Name and code
   - Address and coordinates
   - Splitter ratio (1:8, 1:16, etc.)
   - Total ports
4. View ODP location on map

### 4. Cable Route Visualization

1. Go to **Cable Route** page
2. View interactive network topology:
   - 🖥️ Green = Online OLT
   - 📍 Blue = ODP
   - 📡 Green = Online ONU
   - 📡 Red = Offline ONU
3. Drag nodes to rearrange layout
4. Use controls to zoom and pan

## 🔐 Security

### Default Settings
- JWT authentication enabled
- HTTPS recommended for production
- Database credentials randomly generated during installation

### Securing Your Installation

1. **Change default admin password:**
   - Login with admin/admin123
   - Go to user settings
   - Change password

2. **Enable HTTPS (recommended):**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

3. **Firewall configuration:**
```bash
# Only allow necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

4. **Database backup:**
```bash
# Backup database
sudo -u postgres pg_dump olt_management > backup.sql

# Restore database
sudo -u postgres psql olt_management < backup.sql
```

## 🛠️ Troubleshooting

### Application won't start

```bash
# Check service status
sudo systemctl status olt_management

# Check logs
sudo journalctl -u olt_management -n 50

# Check if port is already in use
sudo netstat -tulpn | grep 8000
```

### Can't connect to OLT

1. Verify network connectivity:
```bash
ping <olt-ip>
```

2. Test SNMP:
```bash
snmpget -v2c -c public <olt-ip> 1.3.6.1.2.1.1.1.0
```

3. Check SNMP community string in OLT configuration

### Database connection error

```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql

# Check connection
sudo -u postgres psql -d olt_management
```

### Nginx error

```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Check logs
sudo tail -f /var/log/nginx/error.log
```

## 🔄 Updating

To update to a new version:

```bash
cd deployment/ubuntu22
sudo ./update.sh
```

## 🗑️ Uninstallation

To completely remove the application:

```bash
cd deployment/ubuntu22
sudo ./uninstall.sh
```

## 📚 API Documentation

After installation, API documentation is available at:
- Swagger UI: `http://your-server/api/v1/docs`
- ReDoc: `http://your-server/api/v1/redoc`

## 🏗️ Development Setup

### Backend Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run development server
python -m uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install

# Create .env file
cp .env.example .env

# Run development server
npm run dev
```

## 📖 ZTE C320 Configuration

### Enable SNMP on ZTE C320

```
# Login to OLT
telnet <olt-ip>

# Enter config mode
configure terminal

# Enable SNMP
snmp-agent
snmp-agent community read public
snmp-agent community write private
snmp-agent sys-info version v2c

# Save configuration
write
exit
```

### Common OIDs for ZTE C320

```
System Description: 1.3.6.1.2.1.1.1.0
System Uptime: 1.3.6.1.2.1.1.3.0
ONU Status: 1.3.6.1.4.1.3902.1012.3.28.1.1.3
ONU RX Power: 1.3.6.1.4.1.3902.1012.3.28.2.1.5
ONU TX Power: 1.3.6.1.4.1.3902.1012.3.28.2.1.6
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👥 Support

For support:
- Create an issue in the repository
- Email: support@example.com

## 📝 Changelog

### Version 1.0.0 (2025-10-19)
- Initial release
- OLT, ONU, ODP management
- Cable route visualization
- Dashboard with statistics
- Ubuntu 22.04 deployment scripts

## 🙏 Acknowledgments

- FastAPI - Modern Python web framework
- React - Frontend framework
- Ant Design - UI components
- ReactFlow - Network visualization
- ZTE - OLT equipment

---

**Made with ❤️ for Network Administrators**
