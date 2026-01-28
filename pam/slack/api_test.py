"""
Simple API Test Script
Test all authentication methods and SCIM operations
"""

import requests
import json

BASE_URL = "http://127.0.0.1:9000"

def print_response(title, response):
    print(f"\n{'='*60}")
    print(f"📍 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

# Test 1: User Login
print("\n🔐 TEST 1: User Login")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"username": "admin", "password": "password123"}
)
print_response("User Login", login_response)

if login_response.status_code == 200:
    user_token = login_response.json()['access_token']
    
    # Test 2: Get Users with User Token
    print("\n👥 TEST 2: Get Users (User Token)")
    users_response = requests.get(
        f"{BASE_URL}/users",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    print_response("Get Users", users_response)
    
    # Test 3: Create User
    print("\n➕ TEST 3: Create User")
    create_response = requests.post(
        f"{BASE_URL}/users",
        headers={"Authorization": f"Bearer {user_token}"},
        json={
            "user_name": "test.user@example.com",
            "display_name": "Test User",
            "active": True
        }
    )
    print_response("Create User", create_response)
    
    if create_response.status_code == 201:
        user_id = create_response.json().get('id')
        
        # Test 4: Update User
        print("\n✏️ TEST 4: Update User")
        update_response = requests.patch(
            f"{BASE_URL}/users/{user_id}",
            headers={"Authorization": f"Bearer {user_token}"},
            json={"title": "Senior Developer"}
        )
        print_response("Update User", update_response)

# Test 5: Service Token
print("\n🔑 TEST 5: Service Token")
service_token = "sk_service_scim_sync_001"
service_response = requests.get(
    f"{BASE_URL}/users",
    headers={"Authorization": f"Bearer {service_token}"}
)
print_response("Get Users (Service Token)", service_response)

# Test 6: OAuth Token (if you have one)
print("\n🔐 TEST 6: OAuth Token")
print("To test OAuth:")
print("1. Open: http://127.0.0.1:9000/oauth/v2/authorize?client_id=scim_client_001&redirect_uri=http://127.0.0.1:9000/oauth/callback&scope=users:read,users:write")
print("2. Approve and copy the code")
print("3. Run: python test_oauth.py")

print("\n" + "="*60)
print("✅ Tests Completed!")
print("="*60 + "\n")
