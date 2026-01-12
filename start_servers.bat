@echo off
echo Starting Django SCIM Server and Flask Auth Client...
echo.

start "Django SCIM Server" cmd /k "cd /d \"c:\iga project\" && python manage.py runserver"
timeout /t 3 /nobreak >nul
start "Flask Auth Client" cmd /k "cd /d \"c:\iga project\pam\slack\" && python auth_scim_server.py"

echo Both servers started!
echo Django: http://127.0.0.1:8000
echo Flask: http://127.0.0.1:9000
pause