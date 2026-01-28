# SCIM Identity Management System - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Server Commands](#server-commands)
4. [Authentication Methods](#authentication-methods)
5. [CRUD Operations](#crud-operations)
6. [API Reference](#api-reference)
7. [Testing](#testing)

---

## Project Overview

A complete SCIM 2.0 compliant Identity Governance & Administration system with three authentication methods:
- User Token Authentication (Login-based)
- Service Token Authentication (Pre-configured)
- OAuth 2.0 Authentication (User approval-based)

**Technology Stack:**
- Django 4.2.7 (SCIM Server - Port 8000)
- Flask (Authentication Server - Port 9000)
- SQLite Database
- Python 3.8+

---

## Architecture

```
Client (Postman/Browser/Script)
    ↓
Flask Auth Server (Port 9000)
    ↓ (Validates Token)
Django SCIM Server (Port 8000)
    ↓
SQLite Database
```

**Two Servers:**
1. **Django SCIM Server** (Port 8000) - Handles SCIM operations and database
2. **Flask Auth Server** (Port 9000) - Handles authentication and proxies SCIM requests

---

## Server Commands

### Start Servers

#### Method 1: Batch File (Recommended)
```bash
cd c:\iga project
start_servers.bat
```
**Result:** Opens 2 terminal windows automatically

#### Method 2: Manual (2 Terminals)

**Terminal 1 - Django Server:**
```bash
cd c:\iga project
python manage.py runserver
```
**Output:**
```
Starting development server at http://127.0.0.1:8000/
```

**Terminal 2 - Flask Server:**
```bash
cd c:\iga project\pam\slack
python auth_scim_server.py
```
**Output:**
```
🚀 Authenticated SCIM Client with OAuth 2.0 Support
📍 Server: http://127.0.0.1:9000
```

### Stop Servers

**Windows:**
- Press `Ctrl + C` in each terminal
- Or close the terminal windows

**Verify Servers Running:**
```bash
# Check Django
curl http://127.0.0.1:8000

# Check Flask
curl http://127.0.0.1:9000
```

---

## Authentication Methods

### 1. User Token Authentication

**Step 1: Login**

**Request:**
```http
POST http://127.0.0.1:9000/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "password123"
}
```

**Response:**
```json
{
    "access_token": "abc123xyz...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "expires_at": "2024-01-15T10:30:00.000000"
}
```

**Step 2: Use Token**
```http
GET http://127.0.0.1:9000/users
Authorization: Bearer abc123xyz...
```

**Available Users:**
- Username: `admin`, Password: `password123`
- Username: `user1`, Password: `pass123`

**Token Properties:**
- Expires: 1 hour (3600 seconds)
- Revocable: Yes
- Use Case: Web applications

---

### 2. Service Token Authentication

**Pre-configured Tokens:**
```
sk_service_scim_sync_001
sk_service_hr_integration_002
```

**Request:**
```http
GET http://127.0.0.1:9000/users
Authorization: Bearer sk_service_scim_sync_001
```

**Token Properties:**
- Expires: Never
- Revocable: No
- Use Case: Automation, scripts, background jobs

---

### 3. OAuth 2.0 Authentication

**Step 1: Authorization Request (Browser)**
```
http://127.0.0.1:9000/oauth/v2/authorize?client_id=scim_client_001&redirect_uri=http://127.0.0.1:9000/oauth/callback&scope=users:read,users:write
```

**Step 2: User Approves → Receives Code**
```
http://127.0.0.1:9000/oauth/callback?code=f16-NxUCa1pkFn-B99s4NxEpHLJ36-OAqfmJElSqBVo
```

**Step 3: Exchange Code for Token**

**Request:**
```http
POST http://127.0.0.1:9000/oauth/v2/access
Content-Type: application/json

{
    "code": "f16-NxUCa1pkFn-B99s4NxEpHLJ36-OAqfmJElSqBVo",
    "client_id": "scim_client_001",
    "client_secret": "secret_scim_001"
}
```

**Response:**
```json
{
    "access_token": "icx2F0um1CC17su-RjaC6tyoJaJMxItNS--Vr5gZl1I",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "users:read,users:write"
}
```

**OAuth Client Credentials:**
- Client ID: `scim_client_001`
- Client Secret: `secret_scim_001`
- Redirect URIs: `http://127.0.0.1:9000/oauth/callback`

**Token Properties:**
- Authorization Code Expires: 10 minutes
- Access Token Expires: 1 hour
- Use Case: Third-party applications

---

## CRUD Operations

### CREATE - Add New User

**Request:**
```http
POST http://127.0.0.1:9000/users
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "user_name": "john.doe@example.com",
    "display_name": "John Doe",
    "given_name": "John",
    "family_name": "Doe",
    "active": true,
    "emails": [
        {
            "value": "john.doe@example.com",
            "type": "work",
            "primary": true
        }
    ],
    "phone_numbers": [
        {
            "value": "+1-555-1234",
            "type": "work"
        }
    ],
    "title": "Software Engineer",
    "user_type": "Employee"
}
```

**Response (201 Created):**
```json
{
    "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User",
        "urn:scim:schemas:extension:slack:2.0:User"
    ],
    "id": "1",
    "user_name": "john.doe@example.com",
    "display_name": "John Doe",
    "name": {
        "given_name": "John",
        "family_name": "Doe"
    },
    "active": true,
    "emails": [
        {
            "value": "john.doe@example.com",
            "type": "work",
            "primary": true
        }
    ],
    "phone_numbers": [
        {
            "value": "+1-555-1234",
            "type": "work"
        }
    ],
    "title": "Software Engineer",
    "user_type": "Employee",
    "meta": {
        "resourceType": "User",
        "created": "2024-01-15T10:00:00.000000Z",
        "lastModified": "2024-01-15T10:00:00.000000Z"
    }
}
```

**Minimal Create Request:**
```json
{
    "user_name": "jane@example.com",
    "display_name": "Jane Smith",
    "active": true
}
```

---

### READ - Get Users

#### Get All Users

**Request:**
```http
GET http://127.0.0.1:9000/users
Authorization: Bearer <your_token>
```

**Response (200 OK):**
```json
{
    "schemas": ["urn:ietf:params:scim:api:messages:2.0:ListResponse"],
    "totalResults": 2,
    "startIndex": 1,
    "itemsPerPage": 2,
    "Resources": [
        {
            "id": "1",
            "user_name": "john.doe@example.com",
            "display_name": "John Doe",
            "active": true,
            "emails": [
                {
                    "value": "john.doe@example.com",
                    "type": "work",
                    "primary": true
                }
            ]
        },
        {
            "id": "2",
            "user_name": "jane@example.com",
            "display_name": "Jane Smith",
            "active": true
        }
    ]
}
```

#### Get Single User

**Request:**
```http
GET http://127.0.0.1:9000/users/1
Authorization: Bearer <your_token>
```

**Response (200 OK):**
```json
{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "id": "1",
    "user_name": "john.doe@example.com",
    "display_name": "John Doe",
    "name": {
        "given_name": "John",
        "family_name": "Doe"
    },
    "active": true,
    "emails": [
        {
            "value": "john.doe@example.com",
            "type": "work",
            "primary": true
        }
    ],
    "title": "Software Engineer"
}
```

---

### UPDATE - Modify User

#### Partial Update (PATCH)

**Request:**
```http
PATCH http://127.0.0.1:9000/users/1
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "title": "Senior Software Engineer",
    "active": true
}
```

**Response (200 OK):**
```json
{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "id": "1",
    "user_name": "john.doe@example.com",
    "display_name": "John Doe",
    "title": "Senior Software Engineer",
    "active": true
}
```

#### Full Update (PUT)

**Request:**
```http
PUT http://127.0.0.1:9000/users/1
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "user_name": "john.doe@example.com",
    "display_name": "John Doe",
    "given_name": "John",
    "family_name": "Doe",
    "active": true,
    "title": "Lead Engineer"
}
```

**Response (200 OK):**
```json
{
    "schemas": ["urn:ietf:params:scim:schemas:core:2.0:User"],
    "id": "1",
    "user_name": "john.doe@example.com",
    "display_name": "John Doe",
    "title": "Lead Engineer",
    "active": true
}
```

---

### DELETE - Remove User

**Request:**
```http
DELETE http://127.0.0.1:9000/users/1
Authorization: Bearer <your_token>
```

**Response (204 No Content):**
```json
{
    "status": "success",
    "message": "Resource deleted"
}
```

---

## API Reference

### Authentication Endpoints (Port 9000)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | User login | No |
| GET | `/auth/validate` | Validate token | Yes |
| POST | `/auth/revoke` | Revoke token | Yes |
| GET | `/auth/service-tokens` | List service tokens | Yes |
| POST | `/auth/service-tokens` | Create service token | Yes |

### OAuth Endpoints (Port 9000)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/oauth/v2/authorize` | Authorization page | No |
| POST | `/oauth/v2/authorize` | Handle approval | No |
| POST | `/oauth/v2/access` | Exchange code for token | No |
| GET | `/oauth/callback` | OAuth callback | No |

### SCIM Endpoints (Port 9000 - Protected)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/users` | List all users | Yes |
| GET | `/users/{id}` | Get specific user | Yes |
| POST | `/users` | Create user | Yes |
| PATCH | `/users/{id}` | Partial update | Yes |
| PUT | `/users/{id}` | Full update | Yes |
| DELETE | `/users/{id}` | Delete user | Yes |

### Direct SCIM Endpoints (Port 8000 - No Auth)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/scim/v2/Users/` | List users |
| GET | `/scim/v2/Users/{id}/` | Get user |
| POST | `/scim/v2/Users/` | Create user |
| PATCH | `/scim/v2/Users/{id}/` | Update user |
| DELETE | `/scim/v2/Users/{id}/` | Delete user |

---

## Testing

### Test with Python Script

**Run API Tests:**
```bash
cd c:\iga project\pam\slack
python api_test.py
```

**Run OAuth Tests:**
```bash
cd c:\iga project\pam\slack
python test_oauth.py
```

**Run Token Tests:**
```bash
cd c:\iga project\pam\slack
python test_tokens.py
```

### Test with Postman

**Import Collection:**
1. Create new collection
2. Add requests from API Reference
3. Set environment variable for token

**Example Postman Workflow:**

1. **Login:**
   - POST `http://127.0.0.1:9000/auth/login`
   - Body: `{"username": "admin", "password": "password123"}`
   - Save `access_token` to variable

2. **Get Users:**
   - GET `http://127.0.0.1:9000/users`
   - Header: `Authorization: Bearer {{access_token}}`

3. **Create User:**
   - POST `http://127.0.0.1:9000/users`
   - Header: `Authorization: Bearer {{access_token}}`
   - Body: User JSON

4. **Update User:**
   - PATCH `http://127.0.0.1:9000/users/1`
   - Header: `Authorization: Bearer {{access_token}}`
   - Body: `{"title": "New Title"}`

5. **Delete User:**
   - DELETE `http://127.0.0.1:9000/users/1`
   - Header: `Authorization: Bearer {{access_token}}`

---

## Error Responses

### 401 Unauthorized
```json
{
    "error": "Invalid or expired token"
}
```

### 400 Bad Request
```json
{
    "error": "Missing required parameters"
}
```

### 404 Not Found
```json
{
    "error": "User not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error message"
}
```

---

## Database Commands

### View Database
```bash
cd c:\iga project
sqlite3 scim.db
```

### SQL Queries
```sql
-- List all users
SELECT * FROM slack_scim_slackuser;

-- Count users
SELECT COUNT(*) FROM slack_scim_slackuser;

-- Find user by email
SELECT * FROM slack_scim_slackuser WHERE user_name = 'john.doe@example.com';
```

### Migrations
```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

---

## Project Structure

```
c:\iga project\
├── django_scim/              # Django settings
│   ├── settings.py
│   └── urls.py
├── slack_scim/               # SCIM app
│   ├── models.py            # Database models
│   ├── serializers.py       # SCIM serialization
│   ├── views.py             # API views
│   └── urls.py              # URL routing
├── pam/slack/               # Authentication
│   ├── auth_manager.py      # Token management
│   ├── auth_scim_server.py  # Flask server
│   ├── api_test.py          # API tests
│   ├── test_oauth.py        # OAuth tests
│   ├── test_tokens.py       # Token tests
│   ├── OAUTH_GUIDE.md       # OAuth docs
│   └── TOKEN_GUIDE.md       # Token docs
├── manage.py                # Django CLI
├── start_servers.bat        # Start script
├── scim.db                  # SQLite database
└── README.md               # Project readme
```

---

## Quick Reference

### Start Everything
```bash
cd c:\iga project
start_servers.bat
```

### Test Everything
```bash
cd c:\iga project\pam\slack
python api_test.py
```

### Service Token (Quick Test)
```bash
curl -H "Authorization: Bearer sk_service_scim_sync_001" http://127.0.0.1:9000/users
```

### User Login (Quick Test)
```bash
curl -X POST http://127.0.0.1:9000/auth/login -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"password123\"}"
```

---

## Support

For issues:
1. Check server logs in terminal windows
2. Verify both servers are running
3. Check token expiration
4. Review error messages

**Built with Django, Flask, and SCIM 2.0 standards** 🚀
