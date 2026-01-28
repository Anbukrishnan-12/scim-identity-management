import uuid
import datetime
from typing import Dict, Optional
import secrets

class TokenManager:
    def __init__(self):
        self.tokens: Dict[str, Dict] = {}
        self.revoked_tokens: set = set()
        # OAuth authorization codes
        self.auth_codes: Dict[str, Dict] = {}
        # OAuth clients
        self.oauth_clients: Dict[str, Dict] = {
            'scim_client_001': {
                'client_secret': 'secret_scim_001',
                'redirect_uris': ['http://127.0.0.1:9000/oauth/callback', 'http://localhost:9000/oauth/callback'],
                'name': 'SCIM Application'
            }
        }
        # Service tokens - long-lived tokens for automation
        self.service_tokens: Dict[str, Dict] = {
            'sk_service_scim_sync_001': {
                'name': 'SCIM Sync Service',
                'description': 'Automated user synchronization',
                'permissions': ['users:read', 'users:write'],
                'created_at': datetime.datetime.utcnow()
            },
            'sk_service_hr_integration_002': {
                'name': 'HR Integration Service',
                'description': 'HR system integration',
                'permissions': ['users:read', 'users:write'],
                'created_at': datetime.datetime.utcnow()
            }
        }
    
    def generate_token(self, user_id: str, expires_in: int = 3600) -> Dict[str, str]:
        """Generate new access token"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        
        self.tokens[token] = {
            'user_id': user_id,
            'created_at': datetime.datetime.utcnow(),
            'expires_at': expires_at,
            'active': True
        }
        
        return {
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': expires_in,
            'expires_at': expires_at.isoformat()
        }
    
    def validate_token(self, token: str) -> Optional[Dict]:
        """Validate token - supports both user tokens and service tokens"""
        if not token:
            return None
        
        # Check if it's a service token
        if token.startswith('sk_service_'):
            return self.validate_service_token(token)
        
        # Check user token
        if token in self.revoked_tokens:
            return None
        
        token_data = self.tokens.get(token)
        if not token_data or datetime.datetime.utcnow() > token_data['expires_at']:
            return None
        
        return {
            'type': 'user',
            'user_id': token_data['user_id'],
            'expires_at': token_data['expires_at']
        }
    
    def validate_service_token(self, token: str) -> Optional[Dict]:
        """Validate service token"""
        service_data = self.service_tokens.get(token)
        if not service_data:
            return None
        
        return {
            'type': 'service',
            'name': service_data['name'],
            'permissions': service_data['permissions'],
            'description': service_data['description']
        }
    
    def revoke_token(self, token: str) -> bool:
        """Revoke specific token"""
        if token in self.tokens:
            self.tokens[token]['active'] = False
            self.revoked_tokens.add(token)
            return True
        return False
    
    def add_service_token(self, name: str, description: str, permissions: list) -> str:
        """Generate new service token"""
        token = f"sk_service_{secrets.token_urlsafe(16)}"
        self.service_tokens[token] = {
            'name': name,
            'description': description,
            'permissions': permissions,
            'created_at': datetime.datetime.utcnow()
        }
        return token
    
    def list_service_tokens(self) -> Dict:
        """List all service tokens"""
        return {k: v for k, v in self.service_tokens.items()}
    
    def generate_auth_code(self, client_id: str, scopes: list, user_id: str = None) -> str:
        """Generate OAuth authorization code"""
        code = secrets.token_urlsafe(32)
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        
        self.auth_codes[code] = {
            'client_id': client_id,
            'scopes': scopes,
            'user_id': user_id,
            'created_at': datetime.datetime.utcnow(),
            'expires_at': expires_at,
            'used': False
        }
        return code
    
    def exchange_code_for_token(self, code: str, client_id: str, client_secret: str) -> Optional[Dict]:
        """Exchange authorization code for access token"""
        code_data = self.auth_codes.get(code)
        
        if not code_data or code_data['used']:
            return None
        
        if datetime.datetime.utcnow() > code_data['expires_at']:
            return None
        
        if code_data['client_id'] != client_id:
            return None
        
        client = self.oauth_clients.get(client_id)
        if not client or client['client_secret'] != client_secret:
            return None
        
        code_data['used'] = True
        
        token = secrets.token_urlsafe(32)
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        
        self.tokens[token] = {
            'user_id': code_data.get('user_id', 'oauth_user'),
            'scopes': code_data['scopes'],
            'client_id': client_id,
            'created_at': datetime.datetime.utcnow(),
            'expires_at': expires_at,
            'active': True
        }
        
        return {
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': 3600,
            'scope': ','.join(code_data['scopes'])
        }
    
    def validate_client(self, client_id: str, redirect_uri: str = None) -> bool:
        """Validate OAuth client"""
        client = self.oauth_clients.get(client_id)
        if not client:
            return False
        
        if redirect_uri and redirect_uri not in client['redirect_uris']:
            return False
        
        return True

# Global instance
token_manager = TokenManager()