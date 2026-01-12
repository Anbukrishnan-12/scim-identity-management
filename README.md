# SCIM Identity Management System with Authentication

A complete SCIM 2.0 compliant Identity Governance & Administration system with token-based authentication.

## 🏗️ Architecture

```
Postman/Client → Flask Auth Server (Port 9000) → Django SCIM Server (Port 8000) → Database
                        ↓
                Token Authentication
                - Login/Logout
                - Token Validation
                - Token Revocation
```

## 🚀 Features

### Django SCIM Server (Port 8000)
- ✅ Full SCIM 2.0 API compliance
- ✅ Complete CRUD operations for users
- ✅ Enterprise & Slack schema extensions
- ✅ Proper HTTP status codes and error handling
- ✅ SQLite database integration

### Flask Authentication Client (Port 9000)
- ✅ Token-based authentication system
- ✅ JWT-like token generation and validation
- ✅ Token revocation capability
- ✅ Protected SCIM endpoints
- ✅ 1-hour token expiry

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository:
```bash
git clone <your-repo-url>
cd iga-project
```

2. Install Django dependencies:
```bash
pip install django djangorestframework
```

3. Install Flask dependencies:
```bash
cd pam/slack
pip install -r requirements.txt
```

4. Initialize database:
```bash
cd ../..
python manage.py migrate
```

## 🖥️ Running the Servers

### Method 1: Two Terminals
**Terminal 1 (Django SCIM Server):**
```bash
cd iga-project
python manage.py runserver
```

**Terminal 2 (Flask Auth Client):**
```bash
cd iga-project/pam/slack
python auth_scim_server.py
```

### Method 2: Batch Script (Windows)
```bash
cd iga-project
start_servers.bat
```

## 🔐 Authentication

### Default Users
- Username: `admin`, Password: `password123`
- Username: `user1`, Password: `pass123`

### Login Process
1. **Get Token:**
```bash
POST http://127.0.0.1:9000/auth/login
Content-Type: application/json

{
    "username": "admin",
    "password": "password123"
}
```

2. **Use Token:**
```bash
GET http://127.0.0.1:9000/users
Authorization: Bearer <your_access_token>
```

3. **Revoke Token:**
```bash
POST http://127.0.0.1:9000/auth/revoke
Authorization: Bearer <your_access_token>
```

## 📡 API Endpoints

### Authentication Endpoints (Port 9000)
- `POST /auth/login` - Get access token
- `GET /auth/validate` - Validate current token
- `POST /auth/revoke` - Revoke current token

### Protected SCIM Endpoints (Port 9000)
- `GET /users` - List all users
- `GET /users/{id}` - Get specific user
- `POST /users` - Create new user
- `PATCH /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Direct SCIM Endpoints (Port 8000)
- `GET /scim/v2/Users/` - List users (no auth)
- `POST /scim/v2/Users/` - Create user (no auth)
- `GET /scim/v2/Users/{id}/` - Get user (no auth)
- `PUT/PATCH /scim/v2/Users/{id}/` - Update user (no auth)
- `DELETE /scim/v2/Users/{id}/` - Delete user (no auth)

## 📝 Example Usage

### Create User
```json
POST http://127.0.0.1:9000/users
Authorization: Bearer <token>
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
    ]
}
```

### Update User
```json
PATCH http://127.0.0.1:9000/users/{user_id}
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "Senior Developer"
}
```

## 🗂️ Project Structure

```
iga-project/
├── django_scim/              # Django project settings
│   ├── settings.py
│   └── urls.py
├── slack_scim/               # SCIM app
│   ├── models.py            # Database models
│   ├── serializers.py       # SCIM JSON serialization
│   ├── views.py             # API endpoints
│   └── urls.py              # URL routing
├── pam/slack/               # Flask authentication client
│   ├── auth_scim_server.py  # Main Flask app with auth
│   ├── scim_client.py       # SCIM client library
│   └── requirements.txt     # Python dependencies
├── manage.py                # Django management
├── start_servers.bat        # Windows batch script
└── README.md               # This file
```

## 🧪 Testing

### Using Postman
1. Import the provided Postman collection
2. Set up environment variables for tokens
3. Test authentication flow
4. Test CRUD operations

### Using Python Script
```bash
cd pam/slack
python scim_client.py
```

## 🔧 Configuration

### Token Expiry
Default: 1 hour (3600 seconds)
```python
# In auth_scim_server.py
expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
```

### Database
- Development: SQLite (`scim.db`)
- Production: Configure in `django_scim/settings.py`

## 🛡️ Security Features

- Token-based authentication
- Token expiration (1 hour)
- Token revocation capability
- Protected API endpoints
- Proper error handling
- Input validation

## 📋 SCIM Compliance

- SCIM 2.0 Core Schema
- Enterprise User Schema Extension
- Slack Profile Schema Extension
- Proper HTTP status codes
- Standard error responses
- Pagination support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed information

---

**Built with Django REST Framework, Flask, and SCIM 2.0 standards** 🚀