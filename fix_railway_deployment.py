#!/usr/bin/env python3
"""
Railway Deployment Fix Script
This script helps diagnose and fix Railway deployment issues
"""

import os
import subprocess
import sys

def check_railway_cli():
    """Check if Railway CLI is installed"""
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Railway CLI found: {result.stdout.strip()}")
            return True
        else:
            print("Railway CLI not found")
            return False
    except FileNotFoundError:
        print("Railway CLI not installed")
        return False

def check_deployment_status():
    """Check Railway deployment status"""
    try:
        print("Checking Railway deployment status...")
        result = subprocess.run(['railway', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Deployment Status:")
            print(result.stdout)
        else:
            print("Error checking status:")
            print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")

def redeploy_to_railway():
    """Redeploy to Railway"""
    try:
        print("Redeploying to Railway...")
        result = subprocess.run(['railway', 'up'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Deployment successful!")
            print(result.stdout)
        else:
            print("Deployment failed:")
            print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")

def get_railway_url():
    """Get the current Railway URL"""
    try:
        print("Getting Railway URL...")
        result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Railway URL:")
            print(result.stdout)
        else:
            print("Error getting URL:")
            print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("=== Railway Deployment Fix Script ===")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("Error: Not in Django project directory")
        print("Please run this script from the iga-project directory")
        return
    
    # Check Railway CLI
    if not check_railway_cli():
        print("\nTo fix this issue, you need to:")
        print("1. Install Railway CLI: npm install -g @railway/cli")
        print("2. Login: railway login")
        print("3. Link project: railway link")
        print("4. Deploy: railway up")
        return
    
    print("\nWhat would you like to do?")
    print("1. Check deployment status")
    print("2. Get current Railway URL")
    print("3. Redeploy to Railway")
    print("4. All of the above")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        check_deployment_status()
    elif choice == '2':
        get_railway_url()
    elif choice == '3':
        redeploy_to_railway()
    elif choice == '4':
        check_deployment_status()
        get_railway_url()
        redeploy_to_railway()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()