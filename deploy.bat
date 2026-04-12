@echo off
echo Deploying genesis-to-quantum to Cloudflare Pages...
cd /d D:\GitHub\genesis-to-quantum
npx wrangler pages deploy . --project-name genesis-to-quantum --branch main --commit-dirty=true
echo.
echo Done! Check above for deployment URL.
pause
