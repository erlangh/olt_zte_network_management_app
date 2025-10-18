# 🚀 Quick Start Guide

## For Ubuntu 22.04 (Production)

### One-Command Install

```bash
# SSH to your Ubuntu 22.04 server, then:
cd /tmp
git clone <repository-url>
cd olt_zte_network_management_app/deployment/ubuntu22
chmod +x install.sh
sudo ./install.sh
```

⏱️ Installation takes ~5-10 minutes

🌐 Access: `http://your-server-ip`

🔐 Login: `admin` / `admin123`

⚠️ **Change password after first login!**

---

## For Windows (Development)

### Prerequisites
- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Node.js 18+ ([Download](https://nodejs.org/))
- PostgreSQL ([Download](https://www.postgresql.org/download/windows/))

### Setup

1. **Clone or extract the project**
```powershell
cd C:\path\to\olt_zte_network_management_app
```

2. **Setup Backend**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure Database**
```powershell
# Create database in PostgreSQL
# Then copy .env.example to .env and edit:
copy .env.example .env
notepad .env
```

Edit `.env`:
```env
DATABASE_URL=postgresql://your_user:your_pass@localhost:5432/olt_management
```

4. **Initialize Database**
```powershell
python init_db.py
```

5. **Setup Frontend**
```powershell
cd ..\frontend
npm install
copy .env.example .env
```

6. **Start Application**
```powershell
# Option 1: Use start script (opens 2 terminals)
cd ..
.\start.ps1

# Option 2: Manual (open 2 terminals)
# Terminal 1 - Backend:
cd backend
.venv\Scripts\activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend:
cd frontend
npm run dev
```

7. **Access Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

---

## For Linux/Mac (Development)

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL

### Setup

1. **Clone project**
```bash
cd ~/projects
git clone <repository-url>
cd olt_zte_network_management_app
```

2. **Setup Backend**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. **Configure Database**
```bash
# Create PostgreSQL database
sudo -u postgres createdb olt_management
sudo -u postgres createuser olt_user -P

# Configure .env
cp .env.example .env
nano .env
```

4. **Initialize Database**
```bash
python init_db.py
```

5. **Setup Frontend**
```bash
cd ../frontend
npm install
cp .env.example .env
```

6. **Start Application**
```bash
# Option 1: Use start script
cd ..
chmod +x start.sh
./start.sh

# Option 2: Manual (open 2 terminals)
# Terminal 1 - Backend:
cd backend
source .venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend:
cd frontend
npm run dev
```

7. **Access Application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs

---

## First Steps After Login

### 1. Change Default Password
- Click on user icon or settings
- Change password
- Logout and login again

### 2. Add Your First OLT
1. Go to **OLT Management**
2. Click **Add OLT**
3. Fill in:
   - Name: e.g., "OLT-Central-01"
   - IP Address: Your OLT IP
   - SNMP Community: Usually "public"
4. Click **Test** to verify connection
5. Click **Sync** to discover ONUs

### 3. View Dashboard
- Go to **Dashboard** to see statistics
- View online/offline devices
- Check alerts

### 4. Manage ONUs
1. Go to **ONU Management**
2. Select OLT from dropdown
3. Click **Discover ONUs**
4. View ONU details and signal strength

### 5. Add ODPs
1. Go to **ODP Management**
2. Click **Add ODP**
3. Fill in ODP details
4. Add location coordinates for mapping

### 6. View Cable Routes
- Go to **Cable Route** page
- See network topology visualization
- Drag nodes to rearrange

---

## Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# Check database connection
# Verify DATABASE_URL in .env
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules
npm install
```

### Can't connect to OLT
```bash
# Test SNMP connection
snmpwalk -v2c -c public <olt-ip> 1.3.6.1.2.1.1

# Check network connectivity
ping <olt-ip>
```

### Database error
```bash
# Recreate database
python init_db.py
```

---

## Need Help?

📖 Full Documentation: [README.md](README.md)

🚀 Deployment Guide: [deployment/ubuntu22/README.md](deployment/ubuntu22/README.md)

📧 Support: Create an issue on GitHub

---

**Happy Monitoring! 🎉**
