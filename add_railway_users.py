import requests
import json

# Railway deployed API endpoint
BASE_URL = "https://scim-identity-management.up.railway.app"

# Sample users to create
users = [
    {
        "user_name": "admin@company.com",
        "display_name": "System Admin",
        "given_name": "System",
        "family_name": "Admin",
        "active": True,
        "emails": [{"value": "admin@company.com", "type": "work", "primary": True}]
    },
    {
        "user_name": "john.doe@company.com",
        "display_name": "John Doe",
        "given_name": "John",
        "family_name": "Doe",
        "active": True,
        "emails": [{"value": "john.doe@company.com", "type": "work", "primary": True}]
    },
    {
        "user_name": "jane.smith@company.com",
        "display_name": "Jane Smith", 
        "given_name": "Jane",
        "family_name": "Smith",
        "active": True,
        "emails": [{"value": "jane.smith@company.com", "type": "work", "primary": True}]
    },
    {
        "user_name": "mike.wilson@company.com",
        "display_name": "Mike Wilson",
        "given_name": "Mike", 
        "family_name": "Wilson",
        "active": True,
        "emails": [{"value": "mike.wilson@company.com", "type": "work", "primary": True}]
    },
    {
        "user_name": "sarah.johnson@company.com",
        "display_name": "Sarah Johnson",
        "given_name": "Sarah", 
        "family_name": "Johnson",
        "active": True,
        "emails": [{"value": "sarah.johnson@company.com", "type": "work", "primary": True}]
    }
]

# Create users via direct SCIM API (no auth needed)
for user in users:
    try:
        response = requests.post(f"{BASE_URL}/scim/v2/Users/", json=user)
        if response.status_code == 201:
            print(f"Created user: {user['display_name']}")
        else:
            print(f"Failed to create {user['display_name']}: {response.text}")
    except Exception as e:
        print(f"Error creating {user['display_name']}: {e}")

print("\nChecking total users...")
try:
    response = requests.get(f"{BASE_URL}/scim/v2/Users/")
    if response.status_code == 200:
        data = response.json()
        print(f"Total Users: {data.get('totalResults', 0)}")
    else:
        print(f"Failed to get users: {response.text}")
except Exception as e:
    print(f"Error getting users: {e}")