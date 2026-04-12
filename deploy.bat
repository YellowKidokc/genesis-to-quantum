@echo off
echo.
echo Deploying genesis-to-quantum to Cloudflare Pages...
echo.
cd /d D:\GitHub\genesis-to-quantum
call npx wrangler pages deploy . --project-name genesis-to-quantum --branch main --commit-dirty=true
echo.
if %errorlevel% neq 0 (
    echo *** DEPLOY FAILED - error code %errorlevel% ***
) else (
    echo *** DEPLOY SUCCESSFUL ***
)
echo.
pause
