# Plan: OLT ZTE C320 Management & Monitoring System

**Created**: 2025-10-19 01:41:51
**Project**: OLT ZTE Network Management Application

## Objective
Membangun aplikasi web management dan monitoring untuk OLT ZTE C320 yang mencakup:
- Management OLT ZTE C320
- Management ODP (Optical Distribution Point)
- Management ONU (Optical Network Unit)  
- Visualisasi alur kabel route
- Deployment di Ubuntu 22 via SSH

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **OLT Communication**: 
  - SNMP (pysnmp)
  - Telnet/SSH (netmiko)
- **Authentication**: JWT
- **API Documentation**: Swagger/OpenAPI

### Frontend
- **Framework**: React 18 + Vite
- **UI Library**: Ant Design / Material-UI
- **State Management**: Zustand / React Query
- **Visualization**: React Flow (untuk cable routing diagram)
- **Charts**: Recharts / Chart.js
- **Maps**: Leaflet (untuk ODP location mapping)

### Deployment
- **OS**: Ubuntu 22.04 LTS
- **Web Server**: Nginx (reverse proxy)
- **Process Manager**: Systemd
- **Database**: PostgreSQL
- **SSL**: Let's Encrypt (optional)

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Frontend (React)                    │
│  - Dashboard monitoring                          │
│  - OLT management                                │
│  - ODP management                                │
│  - ONU management                                │
│  - Cable route visualization                     │
└────────────────┬────────────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────────────┐
│           Backend (FastAPI)                      │
│  - API endpoints                                 │
│  - Authentication & authorization                │
│  - Business logic                                │
│  - SNMP/Telnet client                           │
└────────────┬─────────────────┬──────────────────┘
             │                 │
             ▼                 ▼
┌──────────────────┐  ┌──────────────────┐
│   PostgreSQL     │  │   OLT ZTE C320   │
│   - OLT data     │  │   - SNMP         │
│   - ODP data     │  │   - Telnet/SSH   │
│   - ONU data     │  │                  │
│   - Cable routes │  │                  │
└──────────────────┘  └──────────────────┘
```

## Database Schema

### Tables
1. **olts** - OLT devices
2. **slots** - OLT card slots
3. **ports** - PON ports
4. **odps** - Optical Distribution Points
5. **onus** - ONUs registered
6. **cable_routes** - Cable routing data
7. **users** - System users
8. **logs** - Activity logs

## Features

### MVP (Phase 1)
1. **OLT Management**
   - Add/edit/delete OLT devices
   - Connection testing (SNMP/Telnet)
   - Basic monitoring (status, uptime)
   
2. **ONU Management**
   - List ONUs per port
   - ONU status monitoring (online/offline)
   - ONU registration/deregistration
   - Signal level monitoring (rx/tx power)
   
3. **ODP Management**
   - Add/edit/delete ODP
   - ODP location (coordinates)
   - Assign ODP to ports
   
4. **Basic Dashboard**
   - Total OLT/ODP/ONU statistics
   - Online/offline status
   - Recent activities

### Phase 2 (Enhancement)
1. **Cable Route Visualization**
   - Interactive cable routing diagram
   - OLT -> ODP -> ONU flow
   - Drag & drop interface
   
2. **Advanced Monitoring**
   - Real-time bandwidth monitoring
   - Historical data & graphs
   - Alerts & notifications
   
3. **Provisioning**
   - Bulk ONU provisioning
   - Configuration templates
   - VLAN management
   
4. **Reports**
   - Export to PDF/Excel
   - Custom reports
   - SLA monitoring

### Phase 3 (Advanced)
1. **Map Integration**
   - Geographic ODP mapping
   - Coverage area visualization
   
2. **Troubleshooting Tools**
   - Ping test
   - ONT discovery
   - Port diagnostics
   
3. **Multi-tenant**
   - User roles & permissions
   - Department separation

## Implementation Steps

### Section 1: Project Setup
- [1.1] Initialize project structure
- [1.2] Setup Python virtual environment
- [1.3] Install backend dependencies
- [1.4] Setup database schema
- [1.5] Create base models & migrations

### Section 2: Backend Core
- [2.1] Implement database models
- [2.2] Create OLT SNMP client
- [2.3] Create Telnet/SSH client
- [2.4] Implement authentication (JWT)
- [2.5] Build REST API endpoints

### Section 3: API Endpoints
- [3.1] OLT endpoints (CRUD)
- [3.2] ONU endpoints (list, register, monitoring)
- [3.3] ODP endpoints (CRUD)
- [3.4] Dashboard endpoints (statistics)
- [3.5] Cable route endpoints

### Section 4: Frontend Setup
- [4.1] Initialize React + Vite project
- [4.2] Setup routing & layout
- [4.3] Configure API client
- [4.4] Implement authentication flow

### Section 5: Frontend Pages
- [5.1] Login page
- [5.2] Dashboard page
- [5.3] OLT management page
- [5.4] ONU management page
- [5.5] ODP management page
- [5.6] Cable route visualization page

### Section 6: Deployment
- [6.1] Create installation script for Ubuntu 22
- [6.2] Setup Nginx configuration
- [6.3] Create systemd service files
- [6.4] Database initialization script
- [6.5] Create deployment documentation

## Installation Script Features
- Automated dependency installation
- PostgreSQL setup & database creation
- Python environment setup
- Frontend build
- Nginx configuration
- Systemd service creation
- Firewall configuration
- SSL certificate setup (optional)

## Testing Strategy
- Unit tests for backend logic
- Integration tests for API endpoints
- E2E tests for critical flows
- Manual testing for OLT communication

## Security Considerations
- JWT token authentication
- Password hashing (bcrypt)
- Input validation & sanitization
- SQL injection prevention (ORM)
- Rate limiting
- HTTPS enforcement
- Secure credential storage

## Success Criteria
- [ ] Aplikasi dapat terhubung ke OLT ZTE C320 via SNMP
- [ ] Dapat membaca data ONU dari OLT
- [ ] CRUD ODP berhasil
- [ ] Visualisasi cable route berfungsi
- [ ] Install script berhasil di Ubuntu 22
- [ ] Dashboard menampilkan statistik real-time
- [ ] Dokumentasi lengkap

## Timeline Estimate
- Phase 1 (MVP): 2-3 hari
- Phase 2: 2-3 hari
- Phase 3: 2-3 hari
- Testing & Polish: 1-2 hari

**Total**: 7-11 hari development time

## Notes
- OLT ZTE C320 menggunakan SNMP v2c secara default
- Perlu credential Telnet untuk konfigurasi
- Frontend akan responsive untuk desktop & mobile
- Semua data sensitif (password, community string) di-encrypt di database
