#!/usr/bin/env python3
"""
Test Railway deployment connectivity and debug issues
"""
import requests
import json
import sys

def test_railway_deployment():
    """Test the Railway deployment URL"""
    base_url = "https://scim-identity-management.up.railway.app"
    
    print("Testing Railway deployment...")
    print(f"Base URL: {base_url}")
    
    # Test endpoints
    endpoints = [
        "/",
        "/scim/v2/Users/",
        "/admin/",
        "/api/health/"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\nTesting: {url}")
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")
                if 'json' in response.headers.get('content-type', ''):
                    try:
                        data = response.json()
                        print(f"JSON Response: {json.dumps(data, indent=2)[:200]}...")
                    except:
                        print("Invalid JSON response")
                else:
                    print(f"Content preview: {response.text[:100]}...")
            else:
                print(f"Error: {response.text[:200]}")
                
        except requests.exceptions.ConnectionError:
            print(f"Connection Error: Cannot connect to {url}")
        except requests.exceptions.Timeout:
            print(f"Timeout: Request to {url} timed out")
        except Exception as e:
            print(f"Error: {str(e)}")
    
    # Test SCIM endpoints specifically
    print(f"\nTesting SCIM API endpoints...")
    scim_endpoints = [
        "/scim/v2/Users/",
        "/scim/v2/Users/1/",
    ]
    
    for endpoint in scim_endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\nSCIM Test: {url}")
            headers = {
                'Content-Type': 'application/scim+json',
                'Accept': 'application/scim+json'
            }
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            if response.status_code in [200, 404]:
                print(f"Response: {response.text[:300]}...")
            else:
                print(f"Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"SCIM Error: {str(e)}")

if __name__ == "__main__":
    test_railway_deployment()