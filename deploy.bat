@echo off
:: Deployment script for FMWA Website (Windows)

:: Set color variables
FOR /F "tokens=1,2 delims=#" %%a IN ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') DO (
  SET "DEL=%%a"
)

:init
set "GREEN=%DEL%[32m"
set "YELLOW=%DEL%[33m"
set "RED=%DEL%[31m"
set "NC=%DEL%[0m"

:: Enable colors
call :colorEcho %GREEN% "=== FMWA Website Deployment Script ==="

:: Check for required commands
where psftp >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :colorEcho %RED% "Error: PSFTP is not installed or not in PATH. Please install PuTTY tools."
    pause
    exit /b 1
)

where plink >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    call :colorEcho %RED% "Error: PLINK is not installed or not in PATH. Please install PuTTY tools."
    pause
    exit /b 1
)

:: Get deployment details
set /p remote_host=Enter remote host (e.g., example.com): 
set /p remote_user=Enter SSH username: 
set /p remote_path=Enter remote path (e.g., /var/www/fmwa): 
set /p ssh_port=Enter SSH port [22]: 

:: Set default port if not provided
if "%ssh_port%"=="" set ssh_port=22

:: Create SFTP script
echo cd %remote_path%> sftp_commands.tmp
echo put -r .\*>> sftp_commands.tmp
echo quit>> sftp_commands.tmp

:: Upload files
call :colorEcho %YELLOW% "Uploading files..."
psftp -P %ssh_port% %remote_user%@%remote_host% -b sftp_commands.tmp
if %ERRORLEVEL% NEQ 0 (
    call :colorEcho %RED% "Error: File upload failed"
    del sftp_commands.tmp
    pause
    exit /b 1
)
del sftp_commands.tmp
call :colorEcho %GREEN% "Files uploaded successfully!"

:: Set permissions
call :colorEcho %YELLOW% "Setting file permissions..."
plink -P %ssh_port% %remote_user%@%remote_host% "
    cd '%remote_path%' && \
    find . -type d -exec chmod 755 {} \; && \
    find . -type f -exec chmod 644 {} \; && \
    chmod -R 775 images/uploads/ storage/ bootstrap/cache/ && \
    chmod 775 database/database.sqlite"
if %ERRORLEVEL% NEQ 0 (
    call :colorEcho %RED% "Warning: Failed to set some permissions. You may need to set them manually."
) else (
    call :colorEcho %GREEN% "Permissions set successfully!"
)

:: Run deployment commands
call :colorEcho %YELLOW% "Running deployment commands..."
plink -P %ssh_port% %remote_user%@%remote_host% "
    cd '%remote_path%' && \
    composer install --no-dev --optimize-autoloader && \
    php artisan config:cache && \
    php artisan route:cache && \
    php artisan view:cache"
if %ERRORLEVEL% NEQ 0 (
    call :colorEcho %RED% "Warning: Some deployment commands failed. Check the output above for details."
) else (
    call :colorEcho %GREEN% "Deployment completed successfully!"
)

:: Clean up
call :colorEcho %GREEN% "\n🎉 Deployment process completed!"
call :colorEcho %YELLOW% "Your application should now be live at: http://%remote_host%/"
pause
exit /b 0

:colorEcho
echo off
set "str=%~1"
set "str=%str:"="^%"%"
set "str=%str:\=\\%"
findstr /a:%1 /R "^" "%~2"
<nul set /p "=%str%"
if not "%~2"=="" echo %~2
if not "%~3"=="" echo %~3
exit /b 0
