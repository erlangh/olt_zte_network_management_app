# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-19

### Initial Release 🎉

#### Added
- **OLT Management**
  - Add, edit, delete OLT devices
  - Test SNMP connection to OLT
  - Sync OLT data
  - Monitor OLT status
  - Store OLT configuration (IP, SNMP, Telnet credentials)

- **ONU Management**
  - List and filter ONUs by OLT and Port
  - Discover ONUs via SNMP
  - Monitor ONU status (online/offline)
  - View signal strength (RX/TX power in dBm)
  - View distance and optical metrics
  - Refresh individual ONU data
  - Track customer information
  - Service plan management

- **ODP Management**
  - Add, edit, delete ODPs
  - GPS coordinates tracking
  - Splitter configuration (1:2, 1:4, 1:8, 1:16, 1:32)
  - Port capacity management
  - View location on Google Maps
  - Status tracking

- **Cable Route Visualization**
  - Interactive network topology diagram
  - Visual representation of OLT → ODP → ONU flow
  - Color-coded status indicators
  - Drag and drop node positioning
  - Zoom and pan controls
  - Mini-map for navigation
  - Real-time status updates

- **Dashboard**
  - Real-time statistics display
  - OLT, ONU, ODP counts
  - Online/Offline status indicators
  - Port utilization metrics
  - Recent ONUs list
  - System alerts
  - Auto-refresh every 30 seconds

- **Authentication & Security**
  - JWT-based authentication
  - Login/Logout functionality
  - Password hashing with bcrypt
  - Protected routes
  - Default admin user
  - Token expiration handling

- **SNMP Communication**
  - SNMP v2c support
  - Custom OID configuration
  - Connection testing
  - System information retrieval
  - ONU discovery
  - Signal level monitoring

- **Backend API**
  - RESTful API with FastAPI
  - PostgreSQL database support
  - SQLAlchemy ORM
  - Pydantic data validation
  - Automatic API documentation (Swagger/OpenAPI)
  - CORS support

- **Frontend**
  - React 18 with Vite
  - Ant Design UI components
  - Dark theme by default
  - Responsive design
  - State management with Zustand
  - React Router for navigation
  - ReactFlow for network visualization

- **Deployment**
  - One-command installation script for Ubuntu 22.04
  - Automated dependency installation
  - PostgreSQL database setup
  - Nginx reverse proxy configuration
  - Systemd service creation
  - Firewall configuration
  - SSL certificate support (Let's Encrypt)
  - Utility commands (olt-start, olt-stop, olt-restart, olt-logs, olt-status)
  - Update script
  - Uninstall script

- **Documentation**
  - Comprehensive README
  - Quick Start Guide
  - Deployment Guide
  - Project Summary
  - Deployment Checklist
  - Contributing Guidelines
  - API Documentation
  - Troubleshooting Guide

- **Development Tools**
  - Database initialization script
  - Sample data creation script
  - SNMP connection test script
  - Database connection test script
  - Development start scripts (Windows/Linux)

### Technical Details

#### Backend Stack
- FastAPI 0.104.1
- Python 3.11+
- PostgreSQL 15+
- SQLAlchemy 2.0.23
- pysnmp 4.4.12
- netmiko 4.3.0
- python-jose (JWT)
- passlib (password hashing)

#### Frontend Stack
- React 18
- Vite 5
- Ant Design 5
- React Router 6
- Zustand (state management)
- Axios (HTTP client)
- ReactFlow (visualization)
- Recharts (charts)
- Leaflet (maps)

#### Database Schema
- users (authentication)
- olts (OLT devices)
- slots (card slots)
- ports (PON ports)
- onus (ONUs with customer data)
- odps (Optical Distribution Points)
- cable_routes (routing information)

#### API Endpoints
- `/api/v1/auth/*` - Authentication
- `/api/v1/olt/*` - OLT management
- `/api/v1/onu/*` - ONU management
- `/api/v1/odp/*` - ODP management
- `/api/v1/cable-route/*` - Cable routes
- `/api/v1/dashboard/*` - Dashboard data

### Security
- JWT token authentication
- Password hashing with bcrypt
- SQL injection prevention (ORM)
- CORS configuration
- Secure credential storage
- Firewall configuration included

### Known Issues
- SNMP OIDs may need adjustment for different ZTE C320 firmware versions
- Telnet CLI commands may vary by firmware
- Cable visualization limited to 20 ONUs for performance

### Future Enhancements
Planned for future releases:
- VLAN configuration management
- Bulk ONU provisioning
- Email/SMS alerts
- Historical data and graphs
- PDF/Excel report export
- Multi-OLT vendor support
- Advanced troubleshooting tools
- Mobile app
- API rate limiting
- Advanced user roles

---

## Release Notes

### Version 1.0.0 Highlights

This is the first production-ready release of the OLT ZTE C320 Management System. The system provides a complete solution for managing and monitoring GPON networks with ZTE C320 OLT devices.

**Key Features:**
- Full OLT, ONU, and ODP management
- Real-time SNMP monitoring
- Interactive network visualization
- Easy deployment to Ubuntu 22.04
- Comprehensive documentation

**Installation:**
```bash
cd deployment/ubuntu22
sudo ./install.sh
```

**Default Credentials:**
- Username: admin
- Password: admin123
- ⚠️ Change after first login!

**System Requirements:**
- Ubuntu 22.04 LTS
- 2GB RAM minimum
- 10GB disk space
- PostgreSQL 15+
- Python 3.11+
- Node.js 18+

**Tested With:**
- ZTE C320 OLT with GPON cards
- SNMP v2c
- Various ONU models (ZTE F660, etc.)

---

[1.0.0]: https://github.com/username/repo/releases/tag/v1.0.0
