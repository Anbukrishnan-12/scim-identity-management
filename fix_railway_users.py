import requests
import json

RAILWAY_URL = "https://scim-identity-management.up.railway.app"

# Get all users
response = requests.get(f"{RAILWAY_URL}/scim/v2/Users/")
data = response.json()

print(f"Current users: {len(data['Resources'])}")

# Delete all users first
for user in data['Resources']:
    user_id = user.get('id')
    if user_id:
        try:
            del_response = requests.delete(f"{RAILWAY_URL}/scim/v2/Users/{user_id}/")
            if del_response.status_code == 204:
                print(f"Deleted: {user.get('userName', 'Unknown')}")
        except Exception as e:
            print(f"Error deleting {user.get('userName', 'Unknown')}: {e}")

# Create fresh 12 users
fresh_users = [
    {"user_name": "admin@company.com", "display_name": "System Admin", "given_name": "System", "family_name": "Admin", "active": True},
    {"user_name": "john.doe@company.com", "display_name": "John Doe", "given_name": "John", "family_name": "Doe", "active": True},
    {"user_name": "jane.smith@company.com", "display_name": "Jane Smith", "given_name": "Jane", "family_name": "Smith", "active": True},
    {"user_name": "mike.wilson@company.com", "display_name": "Mike Wilson", "given_name": "Mike", "family_name": "Wilson", "active": True},
    {"user_name": "sarah.johnson@company.com", "display_name": "Sarah Johnson", "given_name": "Sarah", "family_name": "Johnson", "active": True},
    {"user_name": "david.brown@company.com", "display_name": "David Brown", "given_name": "David", "family_name": "Brown", "active": True},
    {"user_name": "lisa.davis@company.com", "display_name": "Lisa Davis", "given_name": "Lisa", "family_name": "Davis", "active": True},
    {"user_name": "tom.miller@company.com", "display_name": "Tom Miller", "given_name": "Tom", "family_name": "Miller", "active": True},
    {"user_name": "anna.garcia@company.com", "display_name": "Anna Garcia", "given_name": "Anna", "family_name": "Garcia", "active": True},
    {"user_name": "james.taylor@company.com", "display_name": "James Taylor", "given_name": "James", "family_name": "Taylor", "active": True},
    {"user_name": "emma.white@company.com", "display_name": "Emma White", "given_name": "Emma", "family_name": "White", "active": True},
    {"user_name": "robert.lee@company.com", "display_name": "Robert Lee", "given_name": "Robert", "family_name": "Lee", "active": True}
]

# Add emails to each user
for user in fresh_users:
    user["emails"] = [{"value": user["user_name"], "type": "work", "primary": True}]

# Create users
for user in fresh_users:
    try:
        response = requests.post(f"{RAILWAY_URL}/scim/v2/Users/", json=user)
        if response.status_code == 201:
            print(f"Created: {user['display_name']}")
        else:
            print(f"Failed to create {user['display_name']}: {response.text}")
    except Exception as e:
        print(f"Error creating {user['display_name']}: {e}")

# Final count check
response = requests.get(f"{RAILWAY_URL}/scim/v2/Users/")
if response.status_code == 200:
    data = response.json()
    print(f"\nFinal count - Total: {data.get('totalResults', 0)}, Resources: {len(data.get('Resources', []))}")
else:
    print("Error checking final count")