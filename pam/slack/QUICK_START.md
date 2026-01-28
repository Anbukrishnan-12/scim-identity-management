# 🚀 Quick Start: User Token + Service Token

## ✅ Implementation Complete!

Your SCIM system now supports **TWO** types of tokens:

### 1️⃣ User Token (Login Required)
```bash
# Login
POST http://127.0.0.1:9000/auth/login
{
    "username": "admin",
    "password": "password123"
}

# Get token → Use for 1 hour → Expires
```

### 2️⃣ Service Token (No Login!)
```bash
# Just use directly - no login needed!
Authorization: Bearer sk_service_scim_sync_001

# Never expires!
```

---

## 🎯 Pre-configured Service Tokens

Copy-paste these tokens directly:

```
sk_service_scim_sync_001
sk_service_hr_integration_002
```

---

## 🧪 Test It Now!

### Start Servers:
```bash
# Terminal 1
cd "c:\iga project"
python manage.py runserver

# Terminal 2
cd "c:\iga project\pam\slack"
python auth_scim_server.py
```

### Run Test:
```bash
cd "c:\iga project\pam\slack"
python test_tokens.py
```

---

## 📝 Example: Get Users

### With User Token:
```bash
# Step 1: Login
curl -X POST http://127.0.0.1:9000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'

# Step 2: Copy token from response

# Step 3: Use token
curl http://127.0.0.1:9000/users \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### With Service Token:
```bash
# One step only!
curl http://127.0.0.1:9000/users \
  -H "Authorization: Bearer sk_service_scim_sync_001"
```

---

## 🎨 Postman Examples

### User Token:
1. **Login:**
   - Method: POST
   - URL: `http://127.0.0.1:9000/auth/login`
   - Body: `{"username":"admin","password":"password123"}`
   
2. **Use Token:**
   - Method: GET
   - URL: `http://127.0.0.1:9000/users`
   - Headers: `Authorization: Bearer <paste_token>`

### Service Token:
1. **Direct Use:**
   - Method: GET
   - URL: `http://127.0.0.1:9000/users`
   - Headers: `Authorization: Bearer sk_service_scim_sync_001`

---

## 📚 Files Modified

✅ `auth_manager.py` - Added service token support
✅ `auth_scim_server.py` - Updated to use both tokens
✅ `test_tokens.py` - Test script
✅ `TOKEN_GUIDE.md` - Full documentation

---

## 🔥 Key Benefits

| Feature | User Token | Service Token |
|---------|-----------|---------------|
| Login Required | ✅ Yes | ❌ No |
| Expires | ✅ 1 hour | ❌ Never |
| Use Case | Web apps | Automation |
| Security | High | Medium |

---

## 💡 When to Use

**User Token:**
- Web application login
- User-specific actions
- Short-term access

**Service Token:**
- Automated scripts
- Background jobs
- CI/CD pipelines
- Cron jobs

---

## ✨ Next Steps

1. Start both servers
2. Run `test_tokens.py`
3. Try both token types in Postman
4. Read `TOKEN_GUIDE.md` for details

**Happy coding! 🎉**
