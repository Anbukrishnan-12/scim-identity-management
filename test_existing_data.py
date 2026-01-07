import requests

def test_get_existing_data():
    base_url = "https://iga-system-production-c44b.up.railway.app"
    headers = {"X-User-Role": "hr"}
    
    print("Testing existing data retrieval...")
    
    # Test role-based endpoint
    try:
        response = requests.get(f"{base_url}/api/v1/identity/role/developer", headers=headers, timeout=10)
        print(f"Role endpoint status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} developers")
            for emp in data:
                print(f"  - ID: {emp.get('id')}, Name: {emp.get('display_name')}, Employee ID: {emp.get('employee_id')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    # Test individual employee
    try:
        response = requests.get(f"{base_url}/api/v1/identity/1", headers=headers, timeout=10)
        print(f"\nIndividual employee (ID:1) status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Employee: {data.get('display_name')} ({data.get('employee_id')})")
            print(f"Role: {data.get('business_role')}")
            print(f"Entitlements: {len(data.get('entitlements', {}))}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_get_existing_data()