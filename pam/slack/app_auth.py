from flask import Flask, jsonify, request
from functools import wraps
import logging
try:
    from scim_client import SCIMClient
    scim_client = SCIMClient()
except ImportError:
    print("Warning: scim_client not found, using mock")
    scim_client = None
logging.basicConfig(level=logging.INFO)
app_logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simple user store (use database in production)
USERS = {
    "admin": "password123",
    "user1": "pass123"
}

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header[7:]  # Remove 'Bearer '
        token_data = token_manager.validate_token(token)
        if not token_data:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.current_user = token_data['user_id']
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return jsonify({
        "message": "PAM Slack SCIM Client API with Authentication",
        "port": 9000,
        "auth_endpoints": ["/auth/login", "/auth/revoke", "/auth/validate"]
    })

# Authentication endpoints
@app.route('/auth/login', methods=['POST'])
def login():
    """Login and get access token"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    if username not in USERS or USERS[username] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token_info = token_manager.generate_token(username)
    return jsonify(token_info)

@app.route('/auth/revoke', methods=['POST'])
@require_auth
def revoke_token():
    """Revoke current token"""
    auth_header = request.headers.get('Authorization')
    token = auth_header[7:]  # Remove 'Bearer '
    
    if token_manager.revoke_token(token):
        return jsonify({'message': 'Token revoked successfully'})
    else:
        return jsonify({'error': 'Token not found'}), 404

@app.route('/auth/validate', methods=['GET'])
@require_auth
def validate_token():
    """Validate current token"""
    return jsonify({
        'valid': True,
        'user_id': request.current_user,
        'message': 'Token is valid'
    })

# Protected SCIM endpoints
@app.route('/users', methods=['GET'])
@require_auth
def get_users():
    """Get all users (protected)"""
    filter_param = request.args.get('filter')
    result = scim_client.get_users(filter_param)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['GET'])
@require_auth
def get_user(user_id):
    """Get specific user (protected)"""
    result = scim_client.get_user(user_id)
    return jsonify(result)

@app.route('/users', methods=['POST'])
@require_auth
def create_user():
    """Create new user (protected)"""
    user_data = request.get_json()
    result = scim_client.create_user(user_data)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['PUT'])
@require_auth
def update_user(user_id):
    """Update user (protected)"""
    user_data = request.get_json()
    result = scim_client.update_user(user_id, user_data)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['PATCH'])
@require_auth
def patch_user(user_id):
    """Partial update user (protected)"""
    user_data = request.get_json()
    result = scim_client.patch_user(user_id, user_data)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['DELETE'])
@require_auth
def delete_user(user_id):
    """Delete user (protected)"""
    result = scim_client.delete_user(user_id)
    return jsonify(result)

# Public test endpoint (no auth required)
@app.route('/test', methods=['GET'])
def test_connection():
    """Test connection (public)"""
    return jsonify({
        "status": "success",
        "message": "Server is running",
        "auth_required": "Use /auth/login to get token"
    })

if __name__ == '__main__':
    print("Starting PAM Slack SCIM Client with Authentication on port 9000...")
    print("Login: POST /auth/login with username/password")
    print("Users: admin/password123, user1/pass123")
    app.run(host='127.0.0.1', port=9000, debug=True)