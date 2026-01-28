#!/usr/bin/env python3
"""
Quick Local SCIM Server Test
Run this to test your SCIM API locally while fixing Railway deployment
"""

import os
import sys
import subprocess
import threading
import time

def run_django_server():
    """Run Django SCIM server"""
    print("Starting Django SCIM server on port 8000...")
    try:
        # Run migrations first
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        
        # Create sample users
        if os.path.exists('create_sample_users.py'):
            subprocess.run([sys.executable, 'create_sample_users.py'], check=True)
        
        # Start server
        subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("Django server stopped")
    except Exception as e:
        print(f"Error running Django server: {e}")

def run_flask_auth_server():
    """Run Flask authentication server"""
    print("Starting Flask auth server on port 9000...")
    try:
        os.chdir('pam/slack')
        subprocess.run([sys.executable, 'auth_scim_server.py'])
    except KeyboardInterrupt:
        print("Flask server stopped")
    except Exception as e:
        print(f"Error running Flask server: {e}")

def main():
    print("=== Local SCIM Server Test ===")
    print("This will start both Django (port 8000) and Flask (port 9000) servers")
    print("Press Ctrl+C to stop")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("Error: Not in Django project directory")
        return
    
    choice = input("\\nStart servers? (y/n): ").strip().lower()
    if choice != 'y':
        return
    
    try:
        # Start Django server in a thread
        django_thread = threading.Thread(target=run_django_server)
        django_thread.daemon = True
        django_thread.start()
        
        # Wait a bit for Django to start
        time.sleep(3)
        
        # Start Flask server in main thread
        run_flask_auth_server()
        
    except KeyboardInterrupt:
        print("\\nStopping servers...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()