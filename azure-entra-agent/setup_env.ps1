# PowerShell script to set Windows environment variables for Azure Entra Agent
# Run this script as Administrator to persist the variables system-wide
# Or run without Administrator to set them for the current user only

param(
    [string]$ClientId = "",
    [string]$ClientSecret = "",
    [string]$TenantId = "",
    [switch]$System,  # Set as system-wide environment variables (requires Admin)
    [switch]$ShowCurrent  # Show current values
)

function Show-CurrentValues {
    Write-Host "`nCurrent Azure Environment Variables:" -ForegroundColor Cyan
    $vars = @("AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID", "USER_AGENT_NAME")
    
    foreach ($var in $vars) {
        $value = [Environment]::GetEnvironmentVariable($var, "User")
        if (-not $value) {
            $value = [Environment]::GetEnvironmentVariable($var, "Machine")
        }
        if (-not $value) {
            $value = [Environment]::GetEnvironmentVariable($var, "Process")
        }
        
        if ($value) {
            if ($var -like "*SECRET*") {
                Write-Host "$var = *encrypted* (length: $($value.Length))" -ForegroundColor Green
            } else {
                Write-Host "$var = $value" -ForegroundColor Green
            }
        } else {
            Write-Host "$var = Not Set" -ForegroundColor Yellow
        }
    }
}

if ($ShowCurrent) {
    Show-CurrentValues
    exit
}

# Prompt for values if not provided
if (-not $ClientId) {
    $ClientId = Read-Host "Enter your Azure Client ID"
}

if (-not $ClientSecret) {
    $ClientSecret = Read-Host "Enter your Azure Client Secret" -AsSecureString
    # Convert secure string to plain text
    $ClientSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ClientSecret)
    )
}

if (-not $TenantId) {
    $TenantId = Read-Host "Enter your Azure Tenant ID"
}

# Determine the scope
$scope = if ($System) { "Machine" } else { "User" }

if ($System -and -not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Error: System-wide environment variables require Administrator privileges!" -ForegroundColor Red
    Write-Host "Either run as Administrator or remove -System to set user variables." -ForegroundColor Yellow
    exit 1
}

Write-Host "`nSetting Azure environment variables ($scope scope)..." -ForegroundColor Cyan

try {
    # Set the environment variables
    [Environment]::SetEnvironmentVariable("AZURE_CLIENT_ID", $ClientId, $scope)
    Write-Host "✓ AZURE_CLIENT_ID set" -ForegroundColor Green
    
    [Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", $ClientSecret, $scope)
    Write-Host "✓ AZURE_CLIENT_SECRET set (encrypted)" -ForegroundColor Green
    
    [Environment]::SetEnvironmentVariable("AZURE_TENANT_ID", $TenantId, $scope)
    Write-Host "✓ AZURE_TENANT_ID set" -ForegroundColor Green
    
    [Environment]::SetEnvironmentVariable("USER_AGENT_NAME", "EntraUserLookupAgent", $scope)
    Write-Host "✓ USER_AGENT_NAME set" -ForegroundColor Green
    
    Write-Host "`n✅ Environment variables set successfully!" -ForegroundColor Cyan
    Write-Host "Note: You may need to restart your terminal or IDE for changes to take effect." -ForegroundColor Yellow
    
    # Show what we just set (without showing secrets)
    Write-Host "`nVariables set:" -ForegroundColor Cyan
    Write-Host "AZURE_CLIENT_ID = $ClientId" -ForegroundColor Gray
    Write-Host "AZURE_CLIENT_SECRET = *encrypted* (length: $($ClientSecret.Length))" -ForegroundColor Gray
    Write-Host "AZURE_TENANT_ID = $TenantId" -ForegroundColor Gray
    Write-Host "USER_AGENT_NAME = EntraUserLookupAgent" -ForegroundColor Gray
    
} catch {
    Write-Host "Error setting environment variables: $_" -ForegroundColor Red
    exit 1
}

# Also set for current process so we can test immediately
$env:AZURE_CLIENT_ID = $ClientId
$env:AZURE_CLIENT_SECRET = $ClientSecret
$env:AZURE_TENANT_ID = $TenantId
$env:USER_AGENT_NAME = "EntraUserLookupAgent"

Write-Host "`nVariables also set for current PowerShell session." -ForegroundColor Green