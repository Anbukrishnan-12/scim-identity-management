@echo off
echo ============================================================
echo Starting SCIM OAuth System Servers
echo ============================================================
echo.

echo Starting Django Server (Port 8000)...
start "Django SCIM Server" cmd /k "cd /d c:\iga project && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo Starting Flask Auth Server (Port 9000)...
start "Flask Auth Server" cmd /k "cd /d c:\iga project\pam\slack && python auth_scim_server.py"

echo.
echo ============================================================
echo Both servers are starting in separate windows
echo Wait 5 seconds, then run tests:
echo   cd c:\iga project\pam\slack
echo   python api_test.py
echo ============================================================
