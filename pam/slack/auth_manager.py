import uuid
import datetime
from typing import Dict, Optional
import secrets

class TokenManager:
    def __init__(self):
        self.tokens: Dict[str, Dict] = {}
        self.revoked_tokens: set = set()
    
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
        """Validate token"""
        if not token or token in self.revoked_tokens:
            return None
        
        token_data = self.tokens.get(token)
        if not token_data or datetime.datetime.utcnow() > token_data['expires_at']:
            return None
        
        return token_data
    
    def revoke_token(self, token: str) -> bool:
        """Revoke specific token"""
        if token in self.tokens:
            self.tokens[token]['active'] = False
            self.revoked_tokens.add(token)
            return True
        return False

# Global instance
token_manager = TokenManager()