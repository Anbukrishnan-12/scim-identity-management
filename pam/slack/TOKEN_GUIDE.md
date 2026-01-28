# 🔐 Token Authentication Guide

## Token Types

### 1. User Token (Short-lived)
**Use Case:** Web applications, interactive users

**Features:**
- ✅ Requires login (username/password)
- ✅ Expires in 1 hour
- ✅ Can be revoked
- ✅ User-specific tracking

**How to Get:**
```bash
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
    "access_token": "abc123...",
    "token_type": "Bearer",
    "expires_in": 3600
}
```

---

### 2. Service Token (Long-lived)
**Use Case:** Automation, background jobs, scripts

**Features:**
- ✅ No login required
- ✅ Never expires
- ✅ Pre-configured
- ✅ Service-specific tracking

**Pre-configured Tokens:**
```
sk_service_scim_sync_001        - SCIM Sync Service
sk_service_hr_integration_002   - HR Integration Service
```

---

## Usage Examples

### User Token Flow
```bash
# 1. Login
curl -X POST http://127.0.0.1:9000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# 2. Use token
curl http://127.0.0.1:9000/users \
  -H "Authorization: Bearer YOUR_USER_TOKEN"
```

### Service Token Flow
```bash
# Direct use - no login needed!
curl http://127.0.0.1:9000/users \
  -H "Authorization: Bearer sk_service_scim_sync_001"
```

---

## API Endpoints

### Authentication
- `POST /auth/login` - Get user token
- `GET /auth/validate` - Validate any token
- `POST /auth/revoke` - Revoke user token

### Service Token Management
- `GET /auth/service-tokens` - List all service tokens
- `POST /auth/service-tokens` - Create new service token

### SCIM Operations (Both tokens work)
- `GET /users` - List users
- `POST /users` - Create user
- `GET /users/{id}` - Get user
- `PATCH /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

---

## Testing

Run the test script:
```bash
cd "c:\iga project\pam\slack"
python test_tokens.py
```

---

## When to Use Which Token?

| Scenario | Token Type |
|----------|-----------|
| Web application login | User Token |
| Automated sync script | Service Token |
| Background job | Service Token |
| User-specific actions | User Token |
| CI/CD pipeline | Service Token |
| Admin dashboard | User Token |
| Cron job | Service Token |

---

## Security Notes

⚠️ **User Tokens:**
- Expire after 1 hour
- Require re-authentication
- Can be revoked anytime

⚠️ **Service Tokens:**
- Never expire
- Keep them secret!
- Store in environment variables
- Rotate periodically

---

## Creating New Service Token

```bash
# Login first with user token
curl -X POST http://127.0.0.1:9000/auth/service-tokens \
  -H "Authorization: Bearer YOUR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Automation Service",
    "description": "Automated user provisioning",
    "permissions": ["users:read", "users:write"]
  }'
```

**Response:**
```json
{
    "token": "sk_service_abc123xyz789",
    "name": "My Automation Service",
    "message": "Service token created successfully"
}
```

---

## Environment Variables (Recommended)

```bash
# .env file
USER_TOKEN=your_user_token_here
SERVICE_TOKEN=sk_service_scim_sync_001
```

```python
# Python script
import os
token = os.getenv('SERVICE_TOKEN')
```

---

## Troubleshooting

**Error: "Invalid or expired token"**
- User token expired → Login again
- Service token invalid → Check spelling

**Error: "Missing authorization header"**
- Add: `Authorization: Bearer YOUR_TOKEN`

**Error: "Invalid credentials"**
- Check username/password for user login
