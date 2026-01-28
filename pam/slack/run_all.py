"""
Master Script - Start Servers and Run Tests
Automatically starts Django + Flask servers and runs API tests
"""

import subprocess
import time
import requests
import json
import sys
import os

BASE_URL = "http://127.0.0.1:9000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}\n")

def print_response(title, response):
    print(f"\n📍 {title}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def check_server(url, name):
    """Check if server is running"""
    try:
        requests.get(url, timeout=2)
        print(f"✅ {name} is running")
        return True
    except:
        print(f"❌ {name} is not running")
        return False

def start_servers():
    """Start Django and Flask servers"""
    print_header("Starting Servers")
    print("\n⚠️  Please start servers manually in separate terminals:")
    print("\n  Terminal 1:")
    print("    cd c:\\iga project")
    print("    python manage.py runserver")
    print("\n  Terminal 2:")
    print("    cd c:\\iga project\\pam\\slack")
    print("    python auth_scim_server.py")
    print("\n⏳ Waiting 10 seconds for you to start servers...")
    time.sleep(10)
    
    # Check if servers are running
    django_ok = check_server("http://127.0.0.1:8000", "Django Server")
    flask_ok = check_server("http://127.0.0.1:9000", "Flask Server")
    
    if not django_ok or not flask_ok:
        print("\n❌ Servers not running!")
        return None, None
    
    return True, True

def run_tests():
    """Run API tests"""
    print_header("Running API Tests")
    
    # Test 1: User Login
    print("\n🔐 TEST 1: User Login")
    try:
        login_response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"username": "admin", "password": "password123"}
        )
        print_response("User Login", login_response)
        
        if login_response.status_code == 200:
            user_token = login_response.json()['access_token']
            
            # Test 2: Get Users
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
                    "user_name": f"test.{int(time.time())}@example.com",
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
        
        print_header("✅ All Tests Completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    print_header("SCIM OAuth System - Master Script")
    
    # Check if servers are already running
    django_running = check_server("http://127.0.0.1:8000", "Django Server")
    flask_running = check_server("http://127.0.0.1:9000", "Flask Server")
    
    if django_running and flask_running:
        print("\n✅ Servers are already running!")
        run_tests()
    else:
        print("\n⚠️  Servers not running.")
        result = start_servers()
        
        if result[0] and result[1]:
            run_tests()
        else:
            print("\n❌ Servers not running. Please start manually and run again.")
