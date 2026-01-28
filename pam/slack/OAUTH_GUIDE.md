# OAuth 2.0 Implementation Guide

## Overview
Complete OAuth 2.0 authorization flow implementation for SCIM API access.

## Flow Diagram
```
User → Authorization Request → Approval Page → Authorization Code → Access Token → API Access
```

## Pre-configured OAuth Client

**Client ID:** `scim_client_001`  
**Client Secret:** `secret_scim_001`  
**Redirect URIs:**
- `http://127.0.0.1:9000/oauth/callback`
- `http://localhost:9000/oauth/callback`

## Available Scopes

- `users:read` - Read user information
- `users:write` - Create and update users
- `users:delete` - Delete users

## OAuth Endpoints

### 1. Authorization Endpoint
**GET** `/oauth/v2/authorize`

Request user authorization and display approval page.

**Parameters:**
- `client_id` (required) - OAuth client identifier
- `redirect_uri` (required) - Callback URL after authorization
- `scope` (optional) - Comma-separated scopes (default: `users:read`)
- `state` (optional) - State parameter for CSRF protection

**Example:**
```
GET http://127.0.0.1:9000/oauth/v2/authorize?client_id=scim_client_001&redirect_uri=http://127.0.0.1:9000/oauth/callback&scope=users:read,users:write&state=xyz123
```

**Response:**
- HTML approval page with requested scopes
- User can approve or deny the request

### 2. Token Exchange Endpoint
**POST** `/oauth/v2/access`

Exchange authorization code for access token.

**Parameters:**
- `code` (required) - Authorization code from step 1
- `client_id` (required) - OAuth client identifier
- `client_secret` (required) - OAuth client secret

**Example:**
```bash
POST http://127.0.0.1:9000/oauth/v2/access
Content-Type: application/json

{
    "code": "authorization_code_here",
    "client_id": "scim_client_001",
    "client_secret": "secret_scim_001"
}
```

**Response:**
```json
{
    "access_token": "token_here",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "users:read,users:write"
}
```

### 3. Callback Endpoint
**GET** `/oauth/callback`

Receives authorization code after user approval.

**Parameters:**
- `code` - Authorization code (on success)
- `error` - Error code (on denial)
- `state` - State parameter from authorization request

## Complete Flow Example

### Step 1: Request Authorization

Open in browser:
```
http://127.0.0.1:9000/oauth/v2/authorize?client_id=scim_client_001&redirect_uri=http://127.0.0.1:9000/oauth/callback&scope=users:read,users:write
```

### Step 2: User Approves

User sees approval page and clicks "Approve" button.

Browser redirects to:
```
http://127.0.0.1:9000/oauth/callback?code=ABC123XYZ&state=xyz123
```

### Step 3: Exchange Code for Token

```bash
POST http://127.0.0.1:9000/oauth/v2/access
Content-Type: application/json

{
    "code": "ABC123XYZ",
    "client_id": "scim_client_001",
    "client_secret": "secret_scim_001"
}
```

Response:
```json
{
    "access_token": "your_access_token_here",
    "token_type": "Bearer",
    "expires_in": 3600,
    "scope": "users:read,users:write"
}
```

### Step 4: Use Access Token

```bash
GET http://127.0.0.1:9000/users
Authorization: Bearer your_access_token_here
```

## Python Example

```python
import requests
import webbrowser

# Step 1: Open authorization URL
auth_url = "http://127.0.0.1:9000/oauth/v2/authorize?client_id=scim_client_001&redirect_uri=http://127.0.0.1:9000/oauth/callback&scope=users:read,users:write"
webbrowser.open(auth_url)

# Step 2: Get code from callback (user copies it)
code = input("Enter authorization code: ")

# Step 3: Exchange for token
response = requests.post(
    "http://127.0.0.1:9000/oauth/v2/access",
    json={
        "code": code,
        "client_id": "scim_client_001",
        "client_secret": "secret_scim_001"
    }
)

token_data = response.json()
access_token = token_data['access_token']

# Step 4: Use token
headers = {"Authorization": f"Bearer {access_token}"}
users = requests.get("http://127.0.0.1:9000/users", headers=headers)
print(users.json())
```

## Testing with Script

Run the automated test script:
```bash
cd pam\slack
python test_oauth.py
```

The script will:
1. Open browser for authorization
2. Prompt for authorization code
3. Exchange code for token
4. Test token with SCIM API

## Postman Collection

### Request 1: Authorization (Manual)
Open in browser:
```
GET http://127.0.0.1:9000/oauth/v2/authorize?client_id=scim_client_001&redirect_uri=http://127.0.0.1:9000/oauth/callback&scope=users:read,users:write
```

### Request 2: Token Exchange
```
POST http://127.0.0.1:9000/oauth/v2/access
Content-Type: application/json

{
    "code": "{{auth_code}}",
    "client_id": "scim_client_001",
    "client_secret": "secret_scim_001"
}
```

### Request 3: Use Token
```
GET http://127.0.0.1:9000/users
Authorization: Bearer {{access_token}}
```

## Security Notes

- Authorization codes expire in 10 minutes
- Authorization codes are single-use only
- Access tokens expire in 1 hour
- Always use HTTPS in production
- Validate redirect_uri to prevent open redirects
- Use state parameter to prevent CSRF attacks

## Token Comparison

| Feature | User Token | Service Token | OAuth Token |
|---------|-----------|---------------|-------------|
| Login Required | Yes | No | User approval |
| Expiry | 1 hour | Never | 1 hour |
| Use Case | Web apps | Automation | Third-party apps |
| Scopes | All | Pre-defined | User-approved |

## Troubleshooting

**Invalid client_id:**
- Check client ID matches `scim_client_001`

**Invalid redirect_uri:**
- Must be exactly `http://127.0.0.1:9000/oauth/callback`

**Code expired:**
- Authorization codes expire in 10 minutes
- Request new authorization

**Invalid code:**
- Codes are single-use only
- Cannot reuse the same code

**Token expired:**
- Access tokens expire in 1 hour
- Request new authorization to get new token
