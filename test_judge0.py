"""
Quick test script for Judge0 service
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.portfolio.services.judge0_service import get_judge0_service

print("="*50)
print("  JUDGE0 SERVICE TEST")
print("="*50)
print()

# Get service
judge0 = get_judge0_service()

print("1. Service available:", judge0.is_available())
print()

if not judge0.is_available():
    print("❌ Judge0 service not available!")
    print("   Install: pip install requests")
    sys.exit(1)

# Test 1: Python Hello World
print("2. Testing Python execution...")
result = judge0.execute_code('print("Hello from Python!")', 'python')

print(f"   Success: {result.get('success')}")
print(f"   Message: {result.get('message')}")
print(f"   Output: {result.get('stdout', 'N/A')}")
print(f"   Errors: {result.get('stderr', 'None')}")
print()

# Test 2: C++ Hello World
print("3. Testing C++ execution...")
cpp_code = '''#include <iostream>
using namespace std;

int main() {
    cout << "Hello from C++" << endl;
    return 0;
}'''

result = judge0.execute_code(cpp_code, 'cpp')

print(f"   Success: {result.get('success')}")
print(f"   Message: {result.get('message')}")
print(f"   Output: {result.get('stdout', 'N/A')}")
print(f"   Compile: {result.get('compile_output', 'None')}")
print()

print("="*50)
print("  TEST COMPLETED")
print("="*50)


