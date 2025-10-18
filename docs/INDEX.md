# 📚 Documentation Index

Complete documentation for OLT ZTE C320 Management System.

## 🚀 Getting Started

### For Beginners
1. **[QUICK_START.md](../QUICK_START.md)** - Quick start guide for all platforms
   - Ubuntu 22.04 installation
   - Windows development setup
   - Linux/Mac development setup
   - First steps after login

2. **[README.md](../README.md)** - Main documentation
   - Features overview
   - Requirements
   - Installation instructions
   - Usage guide
   - Troubleshooting

### For Deployment
3. **[Deployment Guide](../deployment/ubuntu22/README.md)** - Ubuntu 22.04 deployment
   - Pre-requisites
   - Step-by-step installation
   - Post-installation configuration
   - Security hardening
   - Backup and restore
   - Troubleshooting

4. **[DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md)** - Deployment checklist
   - Pre-deployment checks
   - Installation steps
   - Post-installation verification
   - Security configuration
   - Maintenance schedule

## 📖 Technical Documentation

### Architecture & Design
5. **[PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md)** - Complete project overview
   - Architecture
   - Technology stack
   - Features list
   - Database schema
   - API endpoints

6. **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference
   - All endpoints documented
   - Request/response examples
   - Error codes
   - Authentication

### Development
7. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contributing guidelines
   - Development setup
   - Code style
   - Commit messages
   - Pull request process
   - Testing guidelines

8. **[CHANGELOG.md](../CHANGELOG.md)** - Version history
   - Release notes
   - Feature additions
   - Bug fixes
   - Breaking changes

## 🔧 Scripts & Tools

### Backend Scripts
- **init_db.py** - Initialize database and create admin user
- **create_sample_data.py** - Create sample data for testing
- **test_connection.py** - Test database connection
- **test_snmp.py** - Test SNMP connection to OLT

### Deployment Scripts
- **install.sh** - Automated Ubuntu 22.04 installation
- **update.sh** - Update to new version
- **uninstall.sh** - Complete removal

### Development Scripts
- **start.sh** - Start development servers (Linux/Mac)
- **start.ps1** - Start development servers (Windows)

## 📝 Reference Materials

### ZTE C320 Specific
- SNMP Configuration
- Common OIDs
- Telnet commands
- Firmware versions

### Technologies Used
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React, Vite, Ant Design
- **Communication**: pysnmp, netmiko
- **Deployment**: Ubuntu, Nginx, Systemd

## 🎯 Use Cases

### Network Administrator
- Managing OLT devices
- Monitoring network status
- Customer management
- Troubleshooting

### Field Technician
- ODP location tracking
- Remote ONU status check
- Signal quality verification

### Management
- Dashboard statistics
- Network health monitoring
- Reports and analytics

## 🔍 How-To Guides

### Common Tasks

#### How to Add an OLT
1. Go to OLT Management page
2. Click "Add OLT"
3. Fill in details (IP, SNMP community)
4. Click "Test" to verify
5. Save

#### How to Discover ONUs
1. Add OLT first
2. Test OLT connection
3. Click "Sync" on OLT
4. Go to ONU Management
5. Select OLT and click "Discover ONUs"

#### How to Add ODP
1. Go to ODP Management
2. Click "Add ODP"
3. Fill in details including coordinates
4. Specify splitter ratio and ports
5. Save

#### How to View Network Topology
1. Go to Cable Route page
2. Interactive diagram shows connections
3. Drag nodes to rearrange
4. Zoom and pan to navigate

#### How to Deploy to Ubuntu
1. Upload project to server
2. Run `sudo ./deployment/ubuntu22/install.sh`
3. Wait for completion (5-10 min)
4. Access via http://server-ip
5. Login and change default password

#### How to Backup Database
```bash
# Create backup
sudo -u postgres pg_dump olt_management > backup.sql

# Restore backup
sudo -u postgres psql olt_management < backup.sql
```

#### How to Update Application
```bash
cd /opt/olt_management/deployment/ubuntu22
sudo ./update.sh
```

#### How to View Logs
```bash
# Application logs
olt-logs

# Nginx logs
sudo tail -f /var/log/nginx/error.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

## 🐛 Troubleshooting

### Common Issues

#### Can't Connect to OLT
- Check network connectivity: `ping <olt-ip>`
- Test SNMP: `snmpwalk -v2c -c public <olt-ip> 1.3.6.1.2.1.1`
- Verify SNMP community string
- Check firewall on OLT side

#### Application Won't Start
- Check service: `sudo systemctl status olt_management`
- Check logs: `olt-logs`
- Verify port 8000 is free
- Check database connection

#### Frontend Won't Load
- Check Nginx: `sudo systemctl status nginx`
- Test Nginx config: `sudo nginx -t`
- Check browser console for errors
- Verify frontend build exists

#### Database Connection Error
- Check PostgreSQL: `sudo systemctl status postgresql`
- Verify credentials in .env
- Test connection: `sudo -u postgres psql -d olt_management`

## 📞 Support

### Getting Help
1. Check documentation
2. Search closed issues
3. Review troubleshooting section
4. Create new issue with details

### Reporting Bugs
Use the bug report template in CONTRIBUTING.md:
- Description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Logs and screenshots

### Feature Requests
Submit via GitHub issues:
- Feature description
- Use case
- Proposed solution
- Alternatives considered

## 🔐 Security

### Best Practices
- Change default password immediately
- Use strong passwords
- Enable HTTPS
- Configure firewall
- Regular backups
- Keep system updated

### Security Features
- JWT authentication
- Password hashing
- SQL injection prevention
- CORS configuration
- Firewall rules

## 📊 Monitoring & Maintenance

### Daily Tasks
- Check application logs
- Verify services running
- Monitor disk space

### Weekly Tasks
- Review system resources
- Check for updates
- Review alerts

### Monthly Tasks
- System updates
- Review user accounts
- Test backup restore
- Performance review

### Quarterly Tasks
- Security audit
- Documentation review
- Disaster recovery test

## 📄 License

MIT License - See [LICENSE](../LICENSE)

## 🙏 Credits

Built with open source technologies:
- FastAPI
- React
- Ant Design
- ReactFlow
- PostgreSQL
- And many more

---

**Version:** 1.0.0  
**Last Updated:** 2025-10-19

**Quick Links:**
- [GitHub Repository](#)
- [Issue Tracker](#)
- [Discussions](#)
- [Wiki](#)
