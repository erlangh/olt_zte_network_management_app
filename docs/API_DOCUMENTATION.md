# API Documentation

Complete API documentation for OLT ZTE C320 Management System.

**Base URL:** `http://your-server/api/v1`

**Interactive Docs:** `http://your-server/api/v1/docs`

## Authentication

All endpoints except `/auth/login` and `/auth/register` require JWT authentication.

### Headers
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

---

## 🔐 Authentication Endpoints

### Register User
```http
POST /auth/register
```

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2025-10-19T10:30:00Z"
}
```

### Login
```http
POST /auth/login
```

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User
```http
GET /auth/me
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@localhost",
  "full_name": "System Administrator",
  "is_active": true,
  "is_superuser": true,
  "created_at": "2025-10-19T10:00:00Z"
}
```

---

## 🖥️ OLT Management

### List All OLTs
```http
GET /olt/?skip=0&limit=100
```

**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum records to return (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "OLT-Central-01",
    "ip_address": "192.168.1.100",
    "description": "Main OLT at central office",
    "snmp_community": "public",
    "snmp_version": "2c",
    "snmp_port": 161,
    "telnet_enabled": true,
    "telnet_port": 23,
    "telnet_username": "admin",
    "location": "Central Office",
    "latitude": -6.2088,
    "longitude": 106.8456,
    "is_active": true,
    "status": "online",
    "last_seen": "2025-10-19T10:45:00Z",
    "vendor": "ZTE",
    "model": "C320",
    "firmware_version": "V2.2.0",
    "serial_number": "ZTE123456789",
    "uptime": 3600000,
    "created_at": "2025-10-19T09:00:00Z",
    "updated_at": "2025-10-19T10:45:00Z"
  }
]
```

### Get OLT by ID
```http
GET /olt/{olt_id}
```

**Response:** `200 OK` (same structure as list)

### Create OLT
```http
POST /olt/
```

**Request Body:**
```json
{
  "name": "OLT-East-01",
  "ip_address": "192.168.1.101",
  "description": "OLT at eastern district",
  "snmp_community": "public",
  "snmp_version": "2c",
  "snmp_port": 161,
  "telnet_enabled": true,
  "telnet_port": 23,
  "telnet_username": "admin",
  "telnet_password": "password123",
  "location": "Eastern District Office",
  "latitude": -6.2000,
  "longitude": 106.8500
}
```

**Response:** `200 OK` (created OLT object)

### Update OLT
```http
PUT /olt/{olt_id}
```

**Request Body:** (all fields optional)
```json
{
  "name": "OLT-East-Updated",
  "description": "Updated description",
  "location": "New Location"
}
```

**Response:** `200 OK` (updated OLT object)

### Delete OLT
```http
DELETE /olt/{olt_id}
```

**Response:** `200 OK`
```json
{
  "message": "OLT deleted successfully"
}
```

### Test OLT Connection
```http
POST /olt/{olt_id}/test
```

**Response:** `200 OK`
```json
{
  "olt_id": 1,
  "status": "online",
  "is_reachable": true,
  "response_time": 0.125,
  "uptime": 3600000,
  "total_onus": 45,
  "online_onus": 42,
  "offline_onus": 3
}
```

### Sync OLT Data
```http
POST /olt/{olt_id}/sync
```

**Response:** `200 OK`
```json
{
  "message": "OLT data synced successfully",
  "system_info": {
    "description": "ZTE C320 GPON OLT",
    "uptime": "3600000",
    "name": "OLT-Central-01"
  },
  "onus_discovered": 45
}
```

---

## 📡 ONU Management

### List ONUs
```http
GET /onu/?skip=0&limit=100&olt_id=1&port_id=5&status=online
```

**Query Parameters:**
- `skip` (optional): Records to skip
- `limit` (optional): Max records
- `olt_id` (optional): Filter by OLT
- `port_id` (optional): Filter by port
- `status` (optional): Filter by status (online/offline)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "olt_id": 1,
    "port_id": 5,
    "odp_id": 2,
    "sn": "ZTEG12345678",
    "mac_address": "00:11:22:33:44:55",
    "onu_id": 1,
    "customer_name": "John Doe",
    "customer_phone": "081234567890",
    "customer_address": "Jl. Sudirman No. 123",
    "service_plan": "100 Mbps",
    "status": "online",
    "auth_status": "authorized",
    "rx_power": -25.5,
    "tx_power": 2.3,
    "olt_rx_power": -24.8,
    "distance": 1500,
    "temperature": 45.2,
    "voltage": 3.3,
    "vendor": "ZTE",
    "model": "F660",
    "firmware_version": "V9.0.10",
    "hardware_version": "V6.0",
    "vlan": 100,
    "bandwidth_profile": "100M",
    "description": "Customer ONU",
    "uptime": 86400,
    "last_online": "2025-10-19T10:45:00Z",
    "last_offline": null,
    "is_active": true,
    "created_at": "2025-10-15T08:00:00Z",
    "updated_at": "2025-10-19T10:45:00Z"
  }
]
```

### Get ONU by ID
```http
GET /onu/{onu_id}
```

### Create/Register ONU
```http
POST /onu/
```

**Request Body:**
```json
{
  "sn": "ZTEG12345678",
  "olt_id": 1,
  "port_id": 5,
  "odp_id": 2,
  "customer_name": "John Doe",
  "customer_phone": "081234567890",
  "customer_address": "Jl. Sudirman No. 123",
  "service_plan": "100 Mbps",
  "vlan": 100,
  "description": "New customer"
}
```

### Update ONU
```http
PUT /onu/{onu_id}
```

**Request Body:** (all fields optional)
```json
{
  "customer_name": "John Updated",
  "customer_phone": "081234567891",
  "service_plan": "200 Mbps",
  "vlan": 200
}
```

### Delete ONU
```http
DELETE /onu/{onu_id}
```

### Refresh ONU Status
```http
POST /onu/{onu_id}/refresh
```

**Response:** Updated ONU object with fresh SNMP data

### Discover ONUs on OLT
```http
GET /onu/olt/{olt_id}/discover
```

**Response:** `200 OK`
```json
{
  "olt_id": 1,
  "onus_discovered": 45,
  "onus": [
    {
      "slot": 1,
      "port": 1,
      "onu_id": 1,
      "status": "1",
      "oid_suffix": "1.1.1"
    }
  ]
}
```

---

## 📍 ODP Management

### List ODPs
```http
GET /odp/?skip=0&limit=100
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "port_id": 5,
    "name": "ODP-001",
    "code": "ODP001",
    "address": "Jl. Sudirman No. 123",
    "latitude": -6.2088,
    "longitude": 106.8456,
    "total_ports": 8,
    "used_ports": 5,
    "available_ports": 3,
    "splitter_ratio": "1:8",
    "status": "active",
    "installation_date": "2025-01-15T00:00:00Z",
    "description": "Main ODP for area A",
    "notes": "Near the main road",
    "is_active": true,
    "created_at": "2025-01-15T08:00:00Z",
    "updated_at": "2025-10-19T10:00:00Z"
  }
]
```

### Create ODP
```http
POST /odp/
```

**Request Body:**
```json
{
  "name": "ODP-002",
  "code": "ODP002",
  "port_id": 6,
  "address": "Jl. Thamrin No. 456",
  "latitude": -6.1951,
  "longitude": 106.8230,
  "total_ports": 16,
  "splitter_ratio": "1:16",
  "description": "Secondary ODP",
  "notes": "Next to the school"
}
```

### Update ODP
```http
PUT /odp/{odp_id}
```

### Delete ODP
```http
DELETE /odp/{odp_id}
```

---

## 🔗 Cable Route Management

### List Cable Routes
```http
GET /cable-route/?skip=0&limit=100
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "source_type": "olt",
    "source_id": 1,
    "destination_type": "odp",
    "destination_id": 2,
    "cable_type": "Single Mode",
    "fiber_count": 12,
    "cable_length": 500.5,
    "route_coordinates": [
      {"lat": -6.2088, "lng": 106.8456},
      {"lat": -6.2090, "lng": 106.8460}
    ],
    "status": "active",
    "installation_date": "2025-01-20T00:00:00Z",
    "description": "Main fiber route",
    "notes": "Underground cable",
    "created_at": "2025-01-20T08:00:00Z",
    "updated_at": null
  }
]
```

### Create Cable Route
```http
POST /cable-route/
```

**Request Body:**
```json
{
  "source_type": "olt",
  "source_id": 1,
  "destination_type": "odp",
  "destination_id": 2,
  "cable_type": "Single Mode",
  "fiber_count": 12,
  "cable_length": 500.5,
  "route_coordinates": [
    {"lat": -6.2088, "lng": 106.8456},
    {"lat": -6.2090, "lng": 106.8460}
  ],
  "description": "Main route",
  "notes": "Underground"
}
```

### Delete Cable Route
```http
DELETE /cable-route/{route_id}
```

---

## 📊 Dashboard

### Get Statistics
```http
GET /dashboard/stats
```

**Response:** `200 OK`
```json
{
  "olts": {
    "total": 5,
    "online": 4,
    "offline": 1
  },
  "onus": {
    "total": 234,
    "online": 220,
    "offline": 14
  },
  "odps": {
    "total": 45,
    "active": 42
  },
  "port_utilization": 78.5
}
```

### Get Recent ONUs
```http
GET /dashboard/recent-onus?limit=10
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "sn": "ZTEG12345678",
    "customer_name": "John Doe",
    "status": "online",
    "created_at": "2025-10-19T09:00:00Z"
  }
]
```

### Get Alerts
```http
GET /dashboard/alerts
```

**Response:** `200 OK`
```json
[
  {
    "type": "error",
    "title": "OLT Offline",
    "message": "OLT OLT-East-01 is offline",
    "timestamp": "2025-10-19T10:30:00Z"
  },
  {
    "type": "warning",
    "title": "Low Signal ONUs",
    "message": "5 ONUs have low signal strength",
    "timestamp": null
  }
]
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

## Pagination

Most list endpoints support pagination:
- `skip`: Number of records to skip (offset)
- `limit`: Maximum number of records to return

Example:
```
GET /onu/?skip=20&limit=10  # Get records 21-30
```

## Filtering

Some endpoints support filtering via query parameters. Check individual endpoint documentation.

---

**Need more details?** Check the interactive API docs at `/api/v1/docs`
