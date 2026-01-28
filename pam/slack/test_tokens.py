"""
Test script to demonstrate User Token vs Service Token
"""
import requests
import json

BASE_URL = "http://127.0.0.1:9000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

# Test 1: User Token Authentication
print_section("🔐 TEST 1: User Token (Login Required)")

# Login to get user token
print("1️⃣ Login with username/password...")
login_response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "password123"
})
user_token = login_response.json()['access_token']
print(f"✅ User Token: {user_token[:20]}...")
print(f"   Expires in: 3600 seconds (1 hour)")

# Validate user token
print("\n2️⃣ Validate user token...")
validate_response = requests.get(
    f"{BASE_URL}/auth/validate",
    headers={"Authorization": f"Bearer {user_token}"}
)
print(f"✅ Token Info: {json.dumps(validate_response.json(), indent=2)}")

# Use user token to get users
print("\n3️⃣ Get users with user token...")
users_response = requests.get(
    f"{BASE_URL}/users",
    headers={"Authorization": f"Bearer {user_token}"}
)
print(f"✅ Response: {users_response.status_code}")

# Test 2: Service Token Authentication
print_section("🤖 TEST 2: Service Token (No Login Required)")

# Use pre-configured service token
service_token = "sk_service_scim_sync_001"
print(f"1️⃣ Using service token: {service_token}")
print(f"   No login required!")
print(f"   Never expires!")

# Validate service token
print("\n2️⃣ Validate service token...")
validate_response = requests.get(
    f"{BASE_URL}/auth/validate",
    headers={"Authorization": f"Bearer {service_token}"}
)
print(f"✅ Token Info: {json.dumps(validate_response.json(), indent=2)}")

# Use service token to get users
print("\n3️⃣ Get users with service token...")
users_response = requests.get(
    f"{BASE_URL}/users",
    headers={"Authorization": f"Bearer {service_token}"}
)
print(f"✅ Response: {users_response.status_code}")

# Test 3: Create new user with service token
print_section("➕ TEST 3: Create User with Service Token")

new_user = {
    "userName": "service.bot@example.com",
    "displayName": "Service Bot",
    "active": True,
    "emails": [{
        "value": "service.bot@example.com",
        "type": "work",
        "primary": True
    }]
}

print("Creating user with service token...")
create_response = requests.post(
    f"{BASE_URL}/users",
    headers={"Authorization": f"Bearer {service_token}"},
    json=new_user
)
print(f"✅ Status: {create_response.status_code}")
if create_response.status_code == 201:
    print(f"✅ User created: {create_response.json()['id']}")

# Test 4: List all service tokens
print_section("📋 TEST 4: List Service Tokens")

print("Listing all service tokens (requires user token)...")
tokens_response = requests.get(
    f"{BASE_URL}/auth/service-tokens",
    headers={"Authorization": f"Bearer {user_token}"}
)
print(f"✅ Service Tokens:")
for token, data in tokens_response.json().items():
    print(f"   - {data['name']}")
    print(f"     Token: {token}")
    print(f"     Permissions: {', '.join(data['permissions'])}")

# Summary
print_section("📊 SUMMARY")
print("✅ User Token:")
print("   - Requires login (username/password)")
print("   - Expires in 1 hour")
print("   - Good for: Web applications, user-specific actions")
print()
print("✅ Service Token:")
print("   - No login required")
print("   - Never expires")
print("   - Good for: Automation, background jobs, scripts")
print()
print("🎯 Both tokens work with all SCIM endpoints!")
print()
