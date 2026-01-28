import os
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_scim.settings')
django.setup()

from slack_scim.models import SlackUser

# Get all local users
local_users = SlackUser.objects.all()
print(f"Found {local_users.count()} users in local database")

# Railway API endpoint
RAILWAY_URL = "https://scim-identity-management.up.railway.app"

# Upload each user to Railway
for user in local_users:
    user_data = {
        "user_name": user.user_name,
        "display_name": user.display_name or "",
        "given_name": user.given_name or "",
        "family_name": user.family_name or "",
        "active": user.active,
        "emails": []
    }
    
    # Add email if exists
    if user.user_name and "@" in user.user_name:
        user_data["emails"] = [{
            "value": user.user_name,
            "type": "work", 
            "primary": True
        }]
    
    try:
        response = requests.post(f"{RAILWAY_URL}/scim/v2/Users/", json=user_data)
        if response.status_code == 201:
            print(f"Uploaded: {user.display_name or user.user_name}")
        elif response.status_code == 409:
            print(f"Already exists: {user.display_name or user.user_name}")
        else:
            print(f"Failed: {user.display_name or user.user_name} - {response.text}")
    except Exception as e:
        print(f"Error: {user.display_name or user.user_name} - {e}")

# Check final count
try:
    response = requests.get(f"{RAILWAY_URL}/scim/v2/Users/")
    if response.status_code == 200:
        data = response.json()
        print(f"\nRailway Total Users: {data.get('totalResults', 0)}")
    else:
        print(f"Failed to get Railway users: {response.text}")
except Exception as e:
    print(f"Error checking Railway users: {e}")