#!/usr/bin/env python3
import subprocess
import requests
import json

def get_railway_domain():
    """Get current Railway domain"""
    try:
        result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
        if result.returncode == 0:
            domain = result.stdout.strip()
            print(f"Current Railway domain: {domain}")
            return domain
        else:
            print(f"Error getting domain: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_domain(domain):
    """Test if domain is working"""
    if not domain:
        return
    
    if not domain.startswith('http'):
        domain = f"https://{domain}"
    
    print(f"Testing: {domain}")
    
    try:
        response = requests.get(domain, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Domain is working!")
        else:
            print(f"❌ Domain returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("=== Railway Domain Check ===")
    
    # Get current domain
    domain = get_railway_domain()
    
    # Test domain
    test_domain(domain)
    
    # Also test SCIM endpoint
    if domain:
        if not domain.startswith('http'):
            domain = f"https://{domain}"
        scim_url = f"{domain}/scim/v2/Users/"
        print(f"\nTesting SCIM endpoint: {scim_url}")
        try:
            response = requests.get(scim_url, timeout=10)
            print(f"SCIM Status: {response.status_code}")
            if response.status_code == 200:
                print("✅ SCIM API is working!")
                print(f"Response: {response.text[:200]}...")
        except Exception as e:
            print(f"❌ SCIM Error: {e}")

if __name__ == "__main__":
    main()