@echo off
echo Starting SCIM Identity Management System...
echo.

echo Starting Django SCIM Server on port 8000...
start "Django SCIM Server" cmd /k "cd /d "%~dp0" && python manage.py runserver 127.0.0.1:8000"

echo Waiting 3 seconds for Django server to initialize...
timeout /t 3 /nobreak >nul

echo Starting Flask Authentication Server on port 9000...
start "Flask Auth Server" cmd /k "cd /d "%~dp0pam\slack" && python auth_scim_server.py"

echo.
echo Both servers are starting...
echo Django SCIM Server: http://127.0.0.1:8000
echo Flask Auth Server: http://127.0.0.1:9000
echo.
echo Press any key to exit...
pause >nul