# 🚀 Deployment Checklist

Gunakan checklist ini untuk memastikan deployment berjalan lancar.

## 📋 Pre-Deployment

### Server Requirements
- [ ] Ubuntu 22.04 LTS installed
- [ ] Root/sudo access available
- [ ] Minimum 2GB RAM
- [ ] Minimum 10GB free disk space
- [ ] Internet connection active
- [ ] Server IP address noted: _______________

### Network Requirements
- [ ] Server accessible from network
- [ ] Port 22 (SSH) open
- [ ] Port 80 (HTTP) can be opened
- [ ] Port 443 (HTTPS) can be opened
- [ ] Can reach OLT IP address from server

### OLT Requirements
- [ ] OLT IP address: _______________
- [ ] SNMP enabled on OLT
- [ ] SNMP community string: _______________
- [ ] SNMP version (usually 2c): _______________
- [ ] Telnet/SSH credentials (if needed):
  - Username: _______________
  - Password: _______________

## 🔧 Installation Steps

### 1. Upload Project to Server
- [ ] Connect to server via SSH
```bash
ssh user@server-ip
```

**Option A: Via Git**
- [ ] Clone repository
```bash
git clone <repository-url>
cd olt_zte_network_management_app
```

**Option B: Via SCP**
- [ ] Compress project locally
```bash
tar -czf olt_app.tar.gz olt_zte_network_management_app/
```
- [ ] Upload to server
```bash
scp olt_app.tar.gz user@server-ip:/tmp/
```
- [ ] Extract on server
```bash
ssh user@server-ip
cd /tmp
tar -xzf olt_app.tar.gz
```

### 2. Run Installation Script
- [ ] Navigate to deployment directory
```bash
cd olt_zte_network_management_app/deployment/ubuntu22
```
- [ ] Make script executable
```bash
chmod +x install.sh
```
- [ ] Run installation
```bash
sudo ./install.sh
```
- [ ] Wait for installation to complete (5-10 minutes)
- [ ] Note down generated database password: _______________
- [ ] Installation completed successfully

### 3. Verify Installation
- [ ] Check service status
```bash
olt-status
```
- [ ] All services show "active (running)"
- [ ] Check logs for errors
```bash
olt-logs
```
- [ ] No critical errors in logs

## 🌐 Post-Installation

### 1. Access Application
- [ ] Open browser
- [ ] Navigate to: http://your-server-ip
- [ ] Application loads successfully
- [ ] No console errors in browser

### 2. Initial Login
- [ ] Login with default credentials:
  - Username: `admin`
  - Password: `admin123`
- [ ] Login successful
- [ ] Dashboard loads

### 3. Change Default Password
- [ ] Click on user profile/settings
- [ ] Change password to secure password
- [ ] New password: _______________ (store securely!)
- [ ] Logout
- [ ] Login with new password
- [ ] Login successful

### 4. Add First OLT
- [ ] Go to OLT Management
- [ ] Click "Add OLT"
- [ ] Fill in OLT details:
  - Name: _______________
  - IP Address: _______________
  - SNMP Community: _______________
  - SNMP Port: 161
  - Telnet Username: _______________ (optional)
  - Telnet Password: _______________ (optional)
- [ ] Click "Test" button
- [ ] Connection test successful
- [ ] Save OLT
- [ ] OLT appears in list

### 5. Discover ONUs
- [ ] Select OLT in OLT Management
- [ ] Click "Sync" button
- [ ] Go to ONU Management
- [ ] Select OLT from dropdown
- [ ] Click "Discover ONUs"
- [ ] ONUs discovered and listed

### 6. Test All Features
- [ ] Dashboard shows statistics
- [ ] OLT list shows correct status
- [ ] ONU list shows discovered ONUs
- [ ] Can add ODP
- [ ] Cable Route visualization works
- [ ] All pages load without errors

## 🔐 Security Hardening

### 1. Firewall Configuration
- [ ] Configure UFW firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```
- [ ] Verify firewall status
```bash
sudo ufw status
```

### 2. Enable HTTPS (Recommended)
- [ ] Domain name configured (if using): _______________
- [ ] Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx
```
- [ ] Get SSL certificate
```bash
sudo certbot --nginx -d your-domain.com
```
- [ ] Certificate obtained successfully
- [ ] Auto-renewal configured

### 3. Database Backup
- [ ] Create backup directory
```bash
sudo mkdir -p /opt/backups
```
- [ ] Create backup script
```bash
sudo nano /usr/local/bin/olt-backup
# Paste backup script content
sudo chmod +x /usr/local/bin/olt-backup
```
- [ ] Test backup
```bash
sudo /usr/local/bin/olt-backup
```
- [ ] Backup file created
- [ ] Add to crontab for daily backup
```bash
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/olt-backup") | crontab -
```

### 4. System Updates
- [ ] Enable automatic security updates
```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 📊 Monitoring Setup

### 1. Log Monitoring
- [ ] Know how to view logs
```bash
olt-logs              # Application logs
sudo tail -f /var/log/nginx/access.log  # Nginx access
sudo tail -f /var/log/nginx/error.log   # Nginx errors
```

### 2. Resource Monitoring
- [ ] Install monitoring tools (optional)
```bash
sudo apt install htop
```
- [ ] Check CPU/Memory usage
```bash
htop
```

### 3. Disk Space Monitoring
- [ ] Check disk space
```bash
df -h
```
- [ ] Ensure sufficient free space

## 📝 Documentation

### 1. Document Configuration
- [ ] Record server details in secure location:
  - Server IP: _______________
  - SSH port: _______________
  - SSH user: _______________
  - Admin password: _______________
  - Database password: _______________
  - SNMP community: _______________

### 2. Create runbook
- [ ] Document common operations
- [ ] Document troubleshooting steps
- [ ] Share with team

## ✅ Final Verification

### System Health
- [ ] All services running
```bash
olt-status
```
- [ ] No errors in logs
- [ ] Application accessible
- [ ] Can login successfully
- [ ] All features working

### Functionality Test
- [ ] Can add/edit/delete OLT
- [ ] Can test OLT connection
- [ ] Can discover ONUs
- [ ] Can view ONU details
- [ ] Can add/edit/delete ODP
- [ ] Dashboard shows statistics
- [ ] Cable route visualization works

### Security
- [ ] Default password changed
- [ ] Firewall enabled
- [ ] HTTPS enabled (if applicable)
- [ ] Backups configured
- [ ] Unnecessary services disabled

### Performance
- [ ] Application loads quickly
- [ ] No timeout errors
- [ ] Database queries fast
- [ ] SNMP queries working

## 🎉 Deployment Complete!

- [ ] Deployment completed successfully
- [ ] All checklist items completed
- [ ] Documentation updated
- [ ] Team notified
- [ ] Training provided (if needed)

---

## 📞 Support Contacts

**Technical Support:**
- GitHub Issues: [Link]
- Email: support@example.com

**Emergency Contacts:**
- Server Admin: _______________
- Network Admin: _______________
- Database Admin: _______________

---

## 🔄 Maintenance Schedule

**Daily:**
- [ ] Check application logs
- [ ] Verify services running

**Weekly:**
- [ ] Review system resources
- [ ] Check disk space
- [ ] Review alerts

**Monthly:**
- [ ] System updates
- [ ] Review user accounts
- [ ] Test backup restore
- [ ] Performance review

**Quarterly:**
- [ ] Security audit
- [ ] Documentation review
- [ ] Disaster recovery test

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Verified By:** _______________  

**Notes:**
_______________________________________________
_______________________________________________
_______________________________________________
