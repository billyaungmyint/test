@echo off
REM Batch script to set Windows environment variables for Azure Entra Agent
REM Run this in Command Prompt to set variables for the current session only
REM For permanent variables, use the PowerShell script or set them manually
REM in Control Panel > System > Advanced system settings > Environment Variables

echo ========================================================================
echo Azure Entra Agent - Environment Variable Setup
echo ========================================================================
echo.

REM Check if running as administrator (optional check)
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Note: Running as Administrator not required for current session variables.
    echo To set permanent system variables, use PowerShell script or Control Panel.
) else (
    echo Running as non-administrator (current session only).
)
echo.

REM Get user input
set /p CLIENT_ID="Enter Azure Client ID: "
set /p TENANT_ID="Enter Azure Tenant ID: "
set /p CLIENT_SECRET="Enter Azure Client Secret: "

REM Set environment variables for current session only
setx AZURE_CLIENT_ID "%CLIENT_ID%" >nul 2>&1
setx AZURE_TENANT_ID "%TENANT_ID%" >nul 2>&1
setx AZURE_CLIENT_SECRET "%CLIENT_SECRET%" >nul 2>&1
setx USER_AGENT_NAME "EntraUserLookupAgent" >nul 2>&1

REM Also set for current session
set AZURE_CLIENT_ID=%CLIENT_ID%
set AZURE_TENANT_ID=%TENANT_ID%
set AZURE_CLIENT_SECRET=%CLIENT_SECRET%
set USER_AGENT_NAME=EntraUserLookupAgent

echo.
echo ========================================================================
echo Variables set successfully!
echo ========================================================================
echo Note: These variables are set for your USER account (permanent)
echo and for the CURRENT session (immediate).
echo.
echo You may need to restart your terminal or IDE for changes to take effect.
echo.
echo Variables set:
echo AZURE_CLIENT_ID = %CLIENT_ID%
echo AZURE_TENANT_ID = %TENANT_ID%
echo AZURE_CLIENT_SECRET = ***** (hidden for security)
echo USER_AGENT_NAME = EntraUserLookupAgent
echo.
echo To verify in a NEW terminal:
echo   echo %%AZURE_CLIENT_ID%%
echo   echo %%AZURE_TENANT_ID%%
echo   echo %%USER_AGENT_NAME%%
echo ========================================================================

pause