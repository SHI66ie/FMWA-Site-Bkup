@echo off
echo Testing common web server ports...
echo ================================

for %%p in (80, 3000, 3001, 3002, 3003, 4000, 5000, 8000, 8080, 8081) do (
    echo Testing port %%p...
    netstat -ano | findstr :%%p
    echo --------------------------------
)

echo.
echo Checking Node.js processes...
tasklist /FI "IMAGENAME eq node.exe"

echo.
echo Testing network connectivity...
ping -n 3 localhost

pause
