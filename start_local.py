import subprocess
import sys

print("Starting Django SCIM server on http://localhost:8000")
print("SCIM API will be available at: http://localhost:8000/scim/v2/Users/")
print("Press Ctrl+C to stop")

try:
    subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'])
except KeyboardInterrupt:
    print("\nServer stopped")