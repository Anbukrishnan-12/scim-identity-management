#!/usr/bin/env python3
"""
Simple Railway Deployment Script
"""
import subprocess
import sys
import os

def install_railway_cli():
    """Install Railway CLI using npm"""
    try:
        print("Installing Railway CLI...")
        result = subprocess.run(['npm', 'install', '-g', '@railway/cli'], 
                              capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print("Railway CLI installed successfully")
            return True
        else:
            print(f"Failed to install Railway CLI: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("Installation timed out")
        return False
    except FileNotFoundError:
        print("npm not found. Please install Node.js first")
        return False

def deploy_to_railway():
    """Deploy to Railway"""
    try:
        # Login (this will open browser)
        print("Please login to Railway in the browser that opens...")
        subprocess.run(['railway', 'login'], check=True)
        
        # Link project
        print("Linking to Railway project...")
        subprocess.run(['railway', 'link'], check=True)
        
        # Deploy
        print("Deploying to Railway...")
        result = subprocess.run(['railway', 'up'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Deployment successful!")
            print(result.stdout)
            
            # Get the new URL
            url_result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
            if url_result.returncode == 0:
                print(f"New URL: {url_result.stdout}")
        else:
            print(f"Deployment failed: {result.stderr}")
            
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("=== Railway Deployment Fix ===")
    
    # Check if npm is available
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
    except:
        print("Node.js/npm not found. Please install Node.js first from https://nodejs.org/")
        return
    
    # Install Railway CLI
    if not install_railway_cli():
        return
    
    # Deploy
    deploy_to_railway()

if __name__ == "__main__":
    main()