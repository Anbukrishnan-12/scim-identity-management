@echo off
echo Getting Railway domain...
echo.

echo Login to Railway (browser will open):
railway login

echo.
echo Getting current domain:
railway domain

echo.
echo If no domain exists, generating one:
railway domain --generate

echo.
echo Final domain:
railway domain

pause