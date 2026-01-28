from flask import Flask, jsonify, request, redirect, render_template_string
from flask_cors import CORS
from functools import wraps
import secrets
import datetime
from typing import Dict, Optional
import requests
from auth_manager import token_manager

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}})  # Enable CORS for all routes

# Use token_manager from auth_manager.py
def generate_token(user_id: str) -> Dict:
    """Generate user token"""
    return token_manager.generate_token(user_id)

def validate_token(token: str) -> Optional[Dict]:
    """Validate token - supports both user and service tokens"""
    return token_manager.validate_token(token)

def require_auth(f):
    """Authentication decorator - supports user and service tokens"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing authorization header'}), 401
        
        token = auth_header[7:]
        token_data = validate_token(token)
        if not token_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Set user info based on token type
        if token_data['type'] == 'user':
            request.current_user = token_data['user_id']
            request.auth_type = 'user'
        else:  # service token
            request.current_user = token_data['name']
            request.auth_type = 'service'
        
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
    
    def get_users(self): 
        response = self._make_request("GET", "/scim/v2/Users/")
        print(f"Django response: {response}")  # Debug log
        return response
    def get_user(self, user_id): return self._make_request("GET", f"/scim/v2/Users/{user_id}/")
    def create_user(self, data): return self._make_request("POST", "/scim/v2/Users/", data)
    def update_user(self, user_id, data): return self._make_request("PATCH", f"/scim/v2/Users/{user_id}/", data)
    def put_user(self, user_id, data): return self._make_request("PUT", f"/scim/v2/Users/{user_id}/", data)
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
        
        return jsonify({
            'valid': True,
            'type': token_data['type'],
            'user_id': token_data.get('user_id') or token_data.get('name')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/revoke', methods=['POST'])
def revoke():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header[7:]
        if token_manager.revoke_token(token):
            return jsonify({'message': 'Token revoked'})
        return jsonify({'error': 'Token not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# OAuth 2.0 endpoints
@app.route('/oauth/v2/authorize', methods=['GET'])
def oauth_authorize():
    """OAuth authorization endpoint - Step 1"""
    try:
        client_id = request.args.get('client_id')
        redirect_uri = request.args.get('redirect_uri')
        scope = request.args.get('scope', 'users:read')
        state = request.args.get('state', '')
        
        if not client_id:
            return jsonify({'error': 'client_id required'}), 400
        
        if not token_manager.validate_client(client_id, redirect_uri):
            return jsonify({'error': 'Invalid client_id or redirect_uri'}), 400
        
        scopes = scope.split(',')
        
        # Get client info
        client_info = token_manager.oauth_clients.get(client_id, {})
        app_name = client_info.get('name', client_id)
        
        # Build scope items HTML
        scope_items = ''.join([f'<div class="scope-item">✓ {s}</div>' for s in scopes])
        
        # Simple approval page
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>OAuth Authorization</title>
            <style>
                body {{ font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px; }}
                .app-info {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .scopes {{ background: #fff; border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .scope-item {{ padding: 8px; margin: 5px 0; background: #e3f2fd; border-radius: 3px; }}
                button {{ padding: 12px 30px; margin: 10px 5px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }}
                .approve {{ background: #4CAF50; color: white; }}
                .deny {{ background: #f44336; color: white; }}
            </style>
        </head>
        <body>
            <h2>🔐 Authorization Request</h2>
            <div class="app-info">
                <strong>Application:</strong> {app_name}<br>
                <strong>Client ID:</strong> {client_id}
            </div>
            
            <p>This application is requesting access to:</p>
            <div class="scopes">
                {scope_items}
            </div>
            
            <form method="POST" action="/oauth/v2/authorize">
                <input type="hidden" name="client_id" value="{client_id}">
                <input type="hidden" name="redirect_uri" value="{redirect_uri or ''}">
                <input type="hidden" name="scope" value="{scope}">
                <input type="hidden" name="state" value="{state}">
                <button type="submit" name="action" value="approve" class="approve">✓ Approve</button>
                <button type="submit" name="action" value="deny" class="deny">✗ Deny</button>
            </form>
        </body>
        </html>
        '''
        return html
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/oauth/v2/authorize', methods=['POST'])
def oauth_authorize_post():
    """OAuth authorization approval - Step 2"""
    try:
        action = request.form.get('action')
        client_id = request.form.get('client_id')
        redirect_uri = request.form.get('redirect_uri')
        scope = request.form.get('scope', 'users:read')
        state = request.form.get('state', '')
        
        if action != 'approve':
            error_url = f"{redirect_uri}?error=access_denied&state={state}"
            return redirect(error_url)
        
        scopes = scope.split(',')
        code = token_manager.generate_auth_code(client_id, scopes)
        
        callback_url = f"{redirect_uri}?code={code}&state={state}"
        return redirect(callback_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/oauth/v2/access', methods=['POST'])
def oauth_access():
    """OAuth token exchange - Step 3"""
    try:
        data = request.get_json() or request.form.to_dict()
        code = data.get('code')
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        
        if not all([code, client_id, client_secret]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        token_data = token_manager.exchange_code_for_token(code, client_id, client_secret)
        
        if not token_data:
            return jsonify({'error': 'Invalid authorization code or client credentials'}), 401
        
        return jsonify(token_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    """OAuth callback endpoint - displays the code"""
    code = request.args.get('code')
    state = request.args.get('state', '')
    error = request.args.get('error')
    
    if error:
        return f'''
        <html>
        <body style="font-family: Arial; max-width: 500px; margin: 50px auto; padding: 20px;">
            <h2 style="color: #f44336;">❌ Authorization Denied</h2>
            <p>The authorization request was denied.</p>
        </body>
        </html>
        '''
    
    return f'''
    <html>
    <head>
        <title>OAuth Success</title>
        <style>
            body {{ font-family: Arial; max-width: 600px; margin: 50px auto; padding: 20px; }}
            .code-box {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; word-break: break-all; }}
            .success {{ color: #4CAF50; }}
        </style>
    </head>
    <body>
        <h2 class="success">✓ Authorization Successful</h2>
        <p>Your authorization code:</p>
        <div class="code-box"><strong>{code}</strong></div>
        <p>Use this code to exchange for an access token at:</p>
        <code>POST http://127.0.0.1:9000/oauth/v2/access</code>
        <p style="margin-top: 20px; color: #666;">State: {state}</p>
    </body>
    </html>
    '''

# Service token management endpoints
@app.route('/auth/service-tokens', methods=['GET'])
@require_auth
def list_service_tokens():
    """List all service tokens (admin only)"""
    try:
        tokens_data = token_manager.list_service_tokens()
        # Convert datetime objects to strings
        result = {}
        for token, data in tokens_data.items():
            result[token] = {
                'name': data['name'],
                'description': data['description'],
                'permissions': data['permissions'],
                'created_at': data['created_at'].isoformat() if hasattr(data['created_at'], 'isoformat') else str(data['created_at'])
            }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/service-tokens', methods=['POST'])
@require_auth
def create_service_token():
    """Create new service token (admin only)"""
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        permissions = data.get('permissions', ['users:read', 'users:write'])
        
        token = token_manager.add_service_token(name, description, permissions)
        return jsonify({
            'token': token,
            'name': name,
            'description': description,
            'permissions': permissions,
            'message': 'Service token created successfully'
        }), 201
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

@app.route('/users/<user_id>', methods=['PUT'])
@require_auth
def put_user(user_id):
    return jsonify(scim_client.put_user(user_id, request.get_json()))

@app.route('/users/<user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    return jsonify(scim_client.delete_user(user_id))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Authenticated SCIM Client with OAuth 2.0 Support")
    print("="*60)
    print("\n📍 Server: http://0.0.0.0:9000")
    print("\n👤 User Login:")
    print("   - admin/password123")
    print("   - user1/pass123")
    print("\n🔑 Service Tokens (Pre-configured):")
    for token, data in token_manager.service_tokens.items():
        print(f"   - {data['name']}: {token}")
    print("\n🔐 OAuth 2.0 Clients:")
    for client_id, client_data in token_manager.oauth_clients.items():
        print(f"   - {client_data['name']}: {client_id}")
        print(f"     Secret: {client_data['client_secret']}")
    print("\n📚 Endpoints:")
    print("   Auth: /auth/login, /auth/validate, /auth/revoke")
    print("   OAuth: /oauth/v2/authorize, /oauth/v2/access")
    print("   Service: /auth/service-tokens (GET/POST)")
    print("   SCIM: /users (GET/POST/PATCH/DELETE)")
    print("\n🎯 OAuth Flow:")
    print("   1. GET /oauth/v2/authorize?client_id=scim_client_001&redirect_uri=http://127.0.0.1:9000/oauth/callback&scope=users:read,users:write")
    print("   2. User approves → receives code")
    print("   3. POST /oauth/v2/access with code + client credentials")
    print("\n" + "="*60 + "\n")
    app.run(host='0.0.0.0', port=9000, debug=True)