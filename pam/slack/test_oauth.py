"""
OAuth 2.0 Flow Test Script
Tests the complete OAuth authorization flow
"""

import requests
import webbrowser
from urllib.parse import urlparse, parse_qs

BASE_URL = "http://127.0.0.1:9000"

# OAuth Client Credentials
CLIENT_ID = "scim_client_001"
CLIENT_SECRET = "secret_scim_001"
REDIRECT_URI = "http://127.0.0.1:9000/oauth/callback"
SCOPES = "users:read,users:write"

def test_oauth_flow():
    print("\n" + "="*60)
    print("🔐 OAuth 2.0 Flow Test")
    print("="*60)
    
    # Step 1: Generate authorization URL
    auth_url = f"{BASE_URL}/oauth/v2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}&state=test123"
    
    print("\n📍 Step 1: Authorization URL")
    print(f"   {auth_url}")
    print("\n   Opening browser for user approval...")
    print("   After approval, copy the 'code' from the callback page")
    
    # Open browser
    webbrowser.open(auth_url)
    
    # Get code from user
    code = input("\n✏️  Enter the authorization code: ").strip()
    
    # Step 2: Exchange code for token
    print("\n📍 Step 2: Exchange code for access token")
    token_response = requests.post(
        f"{BASE_URL}/oauth/v2/access",
        json={
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
    )
    
    if token_response.status_code == 200:
        token_data = token_response.json()
        access_token = token_data['access_token']
        
        print("✅ Token received successfully!")
        print(f"   Access Token: {access_token}")
        print(f"   Token Type: {token_data['token_type']}")
        print(f"   Expires In: {token_data['expires_in']} seconds")
        print(f"   Scope: {token_data['scope']}")
        
        # Step 3: Test the token
        print("\n📍 Step 3: Test access token with SCIM API")
        headers = {"Authorization": f"Bearer {access_token}"}
        
        users_response = requests.get(f"{BASE_URL}/users", headers=headers)
        
        if users_response.status_code == 200:
            print("✅ Successfully accessed SCIM API!")
            users = users_response.json()
            print(f"   Found {users.get('totalResults', 0)} users")
        else:
            print(f"❌ Failed to access SCIM API: {users_response.text}")
    else:
        print(f"❌ Token exchange failed: {token_response.text}")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_oauth_flow()
