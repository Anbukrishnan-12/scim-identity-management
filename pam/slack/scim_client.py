import requests
import logging
from typing import Dict, Any, Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
app_logger = logging.getLogger(__name__)

class SCIMClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None):
        """Make HTTP request to SCIM API"""
        url = f"{self.base_url}{endpoint}"
        
        app_logger.info(f'Method: {method}')
        app_logger.info(f'Endpoint: {url}')
        if params:
            app_logger.info(f'Request params: {params}')
        if data:
            app_logger.info(f'Request data: {data}')
        
        try:
            response = requests.request(
                method=method.upper(), 
                url=url, 
                headers=self.headers, 
                json=data,
                params=params
            )
            
            app_logger.info(f'Response status: {response.status_code}')
            app_logger.info(f'Response text: {response.text[:200]}...')
            
            response.raise_for_status()
            
            if response.status_code == 204:  # No Content for DELETE
                return {"status": "success", "message": "Resource deleted"}
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            app_logger.error(f"Request failed: {str(e)}")
            app_logger.error(f"Response content: {response.text if 'response' in locals() else 'No response'}")
            return {"error": str(e), "details": response.text if 'response' in locals() else None}
    
    def get_users(self, filter_param: Optional[str] = None):
        """GET /scim/v2/Users/ - List all users"""
        params = {"filter": filter_param} if filter_param else None
        return self._make_request("GET", "/scim/v2/Users/", params=params)
    
    def get_user(self, user_id: str):
        """GET /scim/v2/Users/{id}/ - Get specific user"""
        return self._make_request("GET", f"/scim/v2/Users/{user_id}/")
    
    def create_user(self, user_data: Dict[str, Any]):
        """POST /scim/v2/Users/ - Create new user"""
        return self._make_request("POST", "/scim/v2/Users/", data=user_data)
    
    def update_user(self, user_id: str, user_data: Dict[str, Any]):
        """PUT /scim/v2/Users/{id}/ - Update user"""
        return self._make_request("PUT", f"/scim/v2/Users/{user_id}/", data=user_data)
    
    def patch_user(self, user_id: str, user_data: Dict[str, Any]):
        """PATCH /scim/v2/Users/{id}/ - Partial update user"""
        return self._make_request("PATCH", f"/scim/v2/Users/{user_id}/", data=user_data)
    
    def delete_user(self, user_id: str):
        """DELETE /scim/v2/Users/{id}/ - Delete user"""
        return self._make_request("DELETE", f"/scim/v2/Users/{user_id}/")

def main():
    # Initialize SCIM client
    client = SCIMClient()
    
    # Example usage
    print("=== SCIM API Client Demo ===")
    
    # 1. Get all users
    print("\n1. Getting all users...")
    users = client.get_users()
    print(f"Users: {users}")
    
    # 2. Create new user
    print("\n2. Creating new user...")
    new_user = {
        "user_name": "demo.user@example.com",
        "display_name": "Demo User",
        "given_name": "Demo",
        "family_name": "User",
        "active": True,
        "emails": [
            {
                "value": "demo.user@example.com",
                "type": "work",
                "primary": True
            }
        ]
    }
    
    created_user = client.create_user(new_user)
    print(f"Created user: {created_user}")
    
    if 'id' in created_user:
        user_id = created_user['id']
        
        # 3. Get specific user
        print(f"\n3. Getting user {user_id}...")
        user = client.get_user(user_id)
        print(f"User details: {user}")
        
        # 4. Update user
        print(f"\n4. Updating user {user_id}...")
        update_data = {"title": "Senior Developer"}
        updated_user = client.patch_user(user_id, update_data)
        print(f"Updated user: {updated_user}")
        
        # 5. Delete user
        print(f"\n5. Deleting user {user_id}...")
        delete_result = client.delete_user(user_id)
        print(f"Delete result: {delete_result}")

if __name__ == "__main__":
    main()