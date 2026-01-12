from flask import Flask, jsonify, request
from functools import wraps
import secrets
import datetime
from typing import Dict, Optional

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
        "auth_endpoints": ["/auth/login", "/auth/revoke", "/auth/validate"]
    })

@app.route('/auth/login', methods=['POST'])
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if username not in USERS or USERS[username] != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token_info = generate_token(username)
        return jsonify(token_info)
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/auth/validate', methods=['GET'])
def validate():
    """Validate token"""
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
            'user_id': token_data['user_id']
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/auth/revoke', methods=['POST'])
def revoke():
    """Revoke token"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing authorization header'}), 401
        
        token = auth_header[7:]
        if token in tokens:
            tokens[token]['active'] = False
            revoked_tokens.add(token)
            return jsonify({'message': 'Token revoked'})
        else:
            return jsonify({'error': 'Token not found'}), 404
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting Simple Auth Server on port 9000...")
    print("Test users: admin/password123, user1/pass123")
    app.run(host='127.0.0.1', port=9000, debug=True)