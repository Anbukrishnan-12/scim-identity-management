from flask import Flask, jsonify, request
from functools import wraps
import secrets
import datetime
from typing import Dict, Optional
import requests

app = Flask(__name__)

# Simple token storage
tokens = {}
revoked_tokens = set()

def generate_token(user_id: str) -> Dict:
    """Generate token"""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    tokens[token] = {
        'user_id': user_id,
        'expires_at': expires_at,
        'active': True
    }
    
    return {
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': 3600
    }

def validate_token(token: str) -> Optional[Dict]:
    """Validate token"""
    if not token or token in revoked_tokens:
        return None
    
    token_data = tokens.get(token)
    if not token_data or datetime.datetime.utcnow() > token_data['expires_at']:
        return None
    
    return token_data

def require_auth(f):
    """Authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing authorization header'}), 401
        
        token = auth_header[7:]
        token_data = validate_token(token)
        if not token_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.current_user = token_data['user_id']
        return f(*args, **kwargs)
    return decorated_function

# SCIM Client
class SCIMClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}
    
    def _make_request(self, method: str, endpoint: str, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=data)
            response.raise_for_status()
            if response.status_code == 204:
                return {"status": "success", "message": "Resource deleted"}
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_users(self): return self._make_request("GET", "/scim/v2/Users/")
    def get_user(self, user_id): return self._make_request("GET", f"/scim/v2/Users/{user_id}/")
    def create_user(self, data): return self._make_request("POST", "/scim/v2/Users/", data)
    def update_user(self, user_id, data): return self._make_request("PATCH", f"/scim/v2/Users/{user_id}/", data)
    def delete_user(self, user_id): return self._make_request("DELETE", f"/scim/v2/Users/{user_id}/")

scim_client = SCIMClient()

# Users
USERS = {
    "admin": "password123",
    "user1": "pass123"
}

@app.route('/')
def home():
    return jsonify({
        "message": "PAM Slack SCIM Client API with Authentication",
        "port": 9000,
        "auth_endpoints": ["/auth/login", "/auth/revoke", "/auth/validate"],
        "scim_endpoints": ["/users (GET/POST)", "/users/<id> (GET/PATCH/DELETE)"]
    })

# Auth endpoints
@app.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username not in USERS or USERS[username] != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify(generate_token(username))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/validate', methods=['GET'])
def validate():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing authorization header'}), 401
        
        token = auth_header[7:]
        token_data = validate_token(token)
        
        if not token_data:
            return jsonify({'error': 'Invalid token'}), 401
        
        return jsonify({'valid': True, 'user_id': token_data['user_id']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/revoke', methods=['POST'])
def revoke():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header[7:]
        if token in tokens:
            tokens[token]['active'] = False
            revoked_tokens.add(token)
            return jsonify({'message': 'Token revoked'})
        return jsonify({'error': 'Token not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Protected SCIM endpoints
@app.route('/users', methods=['GET'])
@require_auth
def get_users():
    return jsonify(scim_client.get_users())

@app.route('/users/<user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    return jsonify(scim_client.get_user(user_id))

@app.route('/users', methods=['POST'])
@require_auth
def create_user():
    return jsonify(scim_client.create_user(request.get_json()))

@app.route('/users/<user_id>', methods=['PATCH'])
@require_auth
def update_user(user_id):
    return jsonify(scim_client.update_user(user_id, request.get_json()))

@app.route('/users/<user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    return jsonify(scim_client.delete_user(user_id))

if __name__ == '__main__':
    print("Starting Authenticated SCIM Client on port 9000...")
    print("Users: admin/password123, user1/pass123")
    print("1. Login: POST /auth/login")
    print("2. Use token: Authorization: Bearer <token>")
    app.run(host='127.0.0.1', port=9000, debug=True)