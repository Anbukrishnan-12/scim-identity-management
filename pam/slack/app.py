from flask import Flask, jsonify, request
import logging
from scim_client import SCIMClient

# Setup logging
logging.basicConfig(level=logging.INFO)
app_logger = logging.getLogger(__name__)

app = Flask(__name__)
scim_client = SCIMClient()

@app.route('/')
def home():
    return jsonify({
        "message": "PAM Slack SCIM Client API",
        "port": 9000,
        "scim_server": "http://127.0.0.1:8000"
    })

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users from SCIM server"""
    filter_param = request.args.get('filter')
    result = scim_client.get_users(filter_param)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user from SCIM server"""
    result = scim_client.get_user(user_id)
    return jsonify(result)

@app.route('/users', methods=['POST'])
def create_user():
    """Create new user in SCIM server"""
    user_data = request.get_json()
    result = scim_client.create_user(user_data)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user in SCIM server"""
    user_data = request.get_json()
    result = scim_client.update_user(user_id, user_data)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['PATCH'])
def patch_user(user_id):
    """Partial update user in SCIM server"""
    user_data = request.get_json()
    result = scim_client.patch_user(user_id, user_data)
    return jsonify(result)

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user from SCIM server"""
    result = scim_client.delete_user(user_id)
    return jsonify(result)

@app.route('/test', methods=['GET'])
def test_connection():
    """Test connection to SCIM server"""
    try:
        result = scim_client.get_users()
        return jsonify({
            "status": "success",
            "message": "Connection to SCIM server successful",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Connection failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("Starting PAM Slack SCIM Client on port 9000...")
    print("SCIM Server: http://127.0.0.1:8000")
    print("Client API: http://127.0.0.1:9000")
    app.run(host='127.0.0.1', port=9000, debug=True)