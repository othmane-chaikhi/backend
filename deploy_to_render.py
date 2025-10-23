#!/usr/bin/env python3
"""
Script to help prepare Django backend for Render deployment
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'requirements.txt',
        'Procfile',
        'config/settings.py',
        'manage.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def check_requirements_txt():
    """Check if requirements.txt has necessary packages"""
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required_packages = [
            'gunicorn',
            'whitenoise',
            'django',
            'djangorestframework',
            'psycopg2-binary'
        ]
        
        missing_packages = []
        for package in required_packages:
            if package not in content:
                missing_packages.append(package)
        
        if missing_packages:
            print("❌ Missing packages in requirements.txt:")
            for package in missing_packages:
                print(f"   - {package}")
            return False
        
        print("✅ All required packages found in requirements.txt")
        return True
        
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def check_settings():
    """Check if settings.py has production configurations"""
    try:
        with open('config/settings.py', 'r') as f:
            content = f.read()
        
        required_settings = [
            'STATIC_ROOT',
            'STATIC_URL',
            'MEDIA_ROOT',
            'MEDIA_URL',
            'whitenoise.middleware.WhiteNoiseMiddleware'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if setting not in content:
                missing_settings.append(setting)
        
        if missing_settings:
            print("❌ Missing settings in config/settings.py:")
            for setting in missing_settings:
                print(f"   - {setting}")
            return False
        
        print("✅ Production settings configured")
        return True
        
    except FileNotFoundError:
        print("❌ config/settings.py not found")
        return False

def main():
    """Main deployment check"""
    print("🚀 Django Backend Deployment Check")
    print("=" * 40)
    
    all_good = True
    
    # Check files
    if not check_requirements():
        all_good = False
    
    # Check requirements.txt
    if not check_requirements_txt():
        all_good = False
    
    # Check settings
    if not check_settings():
        all_good = False
    
    print("\n" + "=" * 40)
    
    if all_good:
        print("🎉 Your backend is ready for Render deployment!")
        print("\nNext steps:")
        print("1. Push your code to GitHub")
        print("2. Go to https://dashboard.render.com")
        print("3. Create a new Web Service")
        print("4. Connect your GitHub repository")
        print("5. Set environment variables")
        print("6. Deploy!")
    else:
        print("❌ Please fix the issues above before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()
