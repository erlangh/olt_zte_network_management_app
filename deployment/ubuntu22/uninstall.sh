#!/bin/bash

# Uninstall script for OLT Management System

set -e

APP_DIR="/opt/olt_management"
APP_USER="oltuser"
DB_NAME="olt_management"
DB_USER="olt_user"

echo "================================================"
echo "OLT Management System - Uninstall Script"
echo "================================================"
echo ""
echo "WARNING: This will remove the application and all its data!"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Uninstall cancelled."
    exit 0
fi

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "Step 1: Stopping services..."
systemctl stop olt_management || true
systemctl disable olt_management || true

echo "Step 2: Removing systemd service..."
rm -f /etc/systemd/system/olt_management.service
systemctl daemon-reload

echo "Step 3: Removing Nginx configuration..."
rm -f /etc/nginx/sites-enabled/olt_management
rm -f /etc/nginx/sites-available/olt_management
systemctl restart nginx

echo "Step 4: Removing application directory..."
rm -rf $APP_DIR

echo "Step 5: Removing database..."
read -p "Remove PostgreSQL database? (yes/no): " remove_db
if [ "$remove_db" = "yes" ]; then
        sudo -u postgres bash -c "cd ~; psql -c \"DROP DATABASE IF EXISTS $DB_NAME;\""
        sudo -u postgres bash -c "cd ~; psql -c \"DROP USER IF EXISTS $DB_USER;\""
        echo "Database removed"
    fi

echo "Step 6: Removing user..."
read -p "Remove application user ($APP_USER)? (yes/no): " remove_user
if [ "$remove_user" = "yes" ]; then
    userdel -r $APP_USER || true
    echo "User removed"
fi

echo "Step 7: Removing utility scripts..."
rm -f /usr/local/bin/olt-*

echo ""
echo "================================================"
echo "Uninstall Complete!"
echo "================================================"
