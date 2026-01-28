@echo off
echo === Railway Redeploy Script ===
echo.

echo Step 1: Login to Railway
railway login
if %errorlevel% neq 0 (
    echo Failed to login
    pause
    exit /b 1
)

echo.
echo Step 2: Link project
railway link
if %errorlevel% neq 0 (
    echo Failed to link project
    pause
    exit /b 1
)

echo.
echo Step 3: Check status
railway status

echo.
echo Step 4: Get current domain
railway domain

echo.
echo Step 5: Redeploy
railway up --detach

echo.
echo Step 6: Get new domain
railway domain

echo.
echo Deployment complete!
pause