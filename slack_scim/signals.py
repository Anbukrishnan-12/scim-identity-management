from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SlackUser
import requests
import json
import threading

RAILWAY_URL = "https://scim-identity-management.up.railway.app"

def sync_to_railway(action, user_data=None, user_id=None):
    """Sync changes to Railway in background"""
    def sync():
        try:
            if action == 'create':
                response = requests.post(f"{RAILWAY_URL}/scim/v2/Users/", json=user_data, timeout=5)
                print(f"Railway sync - Created user: {user_data.get('display_name', 'Unknown')}")
            
            elif action == 'update':
                response = requests.patch(f"{RAILWAY_URL}/scim/v2/Users/{user_id}/", json=user_data, timeout=5)
                print(f"Railway sync - Updated user: {user_data.get('display_name', 'Unknown')}")
            
            elif action == 'delete':
                response = requests.delete(f"{RAILWAY_URL}/scim/v2/Users/{user_id}/", timeout=5)
                print(f"Railway sync - Deleted user: {user_id}")
                
        except Exception as e:
            print(f"Railway sync error: {e}")
    
    # Run in background thread
    thread = threading.Thread(target=sync)
    thread.daemon = True
    thread.start()

@receiver(post_save, sender=SlackUser)
def sync_user_create_update(sender, instance, created, **kwargs):
    """Auto-sync when user is created or updated"""
    user_data = {
        "user_name": instance.user_name,
        "display_name": instance.display_name or "",
        "given_name": instance.given_name or "",
        "family_name": instance.family_name or "",
        "active": instance.active,
        "emails": [{"value": instance.user_name, "type": "work", "primary": True}] if instance.user_name else []
    }
    
    if created:
        sync_to_railway('create', user_data)
    else:
        sync_to_railway('update', user_data, str(instance.scim_id))

@receiver(post_delete, sender=SlackUser)
def sync_user_delete(sender, instance, **kwargs):
    """Auto-sync when user is deleted"""
    sync_to_railway('delete', user_id=str(instance.scim_id))