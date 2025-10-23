#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick script to create an admin user for testing
"""
import os
import sys
import django

# Fix encoding issues on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser if it doesn't exist
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('[SUCCESS] Superuser created successfully!')
    print('   Username: admin')
    print('   Password: admin123')
    print('   Email: admin@example.com')
    print('\n[WARNING] IMPORTANT: Change this password in production!')
else:
    print('[INFO] Admin user already exists')
    print('   Username: admin')

