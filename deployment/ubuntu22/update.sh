#!/bin/bash

# Update script for OLT Management System

set -e

APP_DIR="/opt/olt_management"
APP_USER="oltuser"

echo "================================================"
echo "OLT Management System - Update Script"
echo "================================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "Step 1: Stopping application..."
systemctl stop olt_management

echo "Step 2: Backing up current installation..."
BACKUP_DIR="/opt/olt_backup_$(date +%Y%m%d_%H%M%S)"
cp -r $APP_DIR $BACKUP_DIR
echo "Backup created at: $BACKUP_DIR"

echo "Step 3: Updating backend..."
cd $APP_DIR/backend
sudo -u $APP_USER git pull || echo "Skipping git pull"
sudo -u $APP_USER .venv/bin/pip install -r requirements.txt --upgrade

echo "Step 4: Running database migrations..."
# Add migration commands here if using Alembic

echo "Step 5: Updating frontend..."
cd $APP_DIR/frontend
sudo -u $APP_USER npm install
sudo -u $APP_USER npm run build

echo "Step 6: Restarting application..."
systemctl start olt_management
systemctl status olt_management

echo ""
echo "================================================"
echo "Update Complete!"
echo "================================================"
echo ""
echo "If you encounter any issues, restore from backup:"
echo "  sudo systemctl stop olt_management"
echo "  sudo rm -rf $APP_DIR"
echo "  sudo mv $BACKUP_DIR $APP_DIR"
echo "  sudo systemctl start olt_management"
echo "================================================"
