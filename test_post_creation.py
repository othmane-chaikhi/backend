#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour la création de posts
"""
import os
import sys
import django

# Fix encoding on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.portfolio.models import Post

# Vérifier l'utilisateur admin
try:
    admin = User.objects.get(username='admin')
    print(f"[OK] Admin user found: {admin.username}")
    print(f"     Email: {admin.email}")
    print(f"     Is staff: {admin.is_staff}")
    print(f"     Is superuser: {admin.is_superuser}")
except User.DoesNotExist:
    print("[ERROR] Admin user not found!")
    exit(1)

# Test de création de post
try:
    test_post = Post.objects.create(
        title="Test Post - Created via Script",
        content="This is a test post to verify creation works.",
        author=admin,
        is_published=False  # Brouillon pour test
    )
    print(f"\n[OK] Test post created successfully!")
    print(f"     ID: {test_post.id}")
    print(f"     Title: {test_post.title}")
    print(f"     Author: {test_post.author.username}")
    print(f"     Published: {test_post.is_published}")
    
    # Supprimer le post de test
    test_post.delete()
    print(f"\n[OK] Test post deleted (cleanup)")
    
except Exception as e:
    print(f"\n[ERROR] Error creating post: {e}")
    import traceback
    traceback.print_exc()

# Afficher les posts existants
print("\n[INFO] Existing posts:")
posts = Post.objects.all()
if posts:
    for post in posts:
        print(f"       - [{post.id}] {post.title} by {post.author.username}")
else:
    print("       No posts found")

print("\n[OK] Diagnostic complete!")

