# ===============================================
# SQL Server Connection Examples
# ===============================================
# This file demonstrates various ways to use the connect_sql_database.ps1 script
# DO NOT commit actual credentials to version control!

# ===============================================
# Example 1: Basic Connection Test (SQL Auth)
# ===============================================
Write-Host "`n=== Example 1: Basic Connection Test ===" -ForegroundColor Cyan
# NOTE: Replace with your actual server, database, username, and password
$serverName = "localhost"
$databaseName = "master"
$username = "sa"
# IMPORTANT: Never hardcode passwords in production!
# $password = "***SECURE_PASSWORD***"  # Replace with actual password

# Uncomment to run:
# .\connect_sql_database.ps1 -ServerName $serverName -DatabaseName $databaseName -Username $username -Password $password


# ===============================================
# Example 2: Connection Test (Windows Auth)
# ===============================================
Write-Host "`n=== Example 2: Windows Authentication ===" -ForegroundColor Cyan
# This uses your current Windows credentials

# Uncomment to run:
# .\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -UseWindowsAuth


# ===============================================
# Example 3: Execute Simple Query
# ===============================================
Write-Host "`n=== Example 3: Execute Query ===" -ForegroundColor Cyan
# Check SQL Server version

# Uncomment to run:
# .\connect_sql_database.ps1 `
#     -ServerName "localhost" `
#     -DatabaseName "master" `
#     -UseWindowsAuth `
#     -Query "SELECT @@VERSION AS SQLServerVersion"


# ===============================================
# Example 4: List All Databases
# ===============================================
Write-Host "`n=== Example 4: List Databases ===" -ForegroundColor Cyan

# Uncomment to run:
# .\connect_sql_database.ps1 `
#     -ServerName "localhost" `
#     -DatabaseName "master" `
#     -UseWindowsAuth `
#     -Query "SELECT name, database_id, create_date FROM sys.databases ORDER BY name"


# ===============================================
# Example 5: Secure Password Input
# ===============================================
Write-Host "`n=== Example 5: Secure Password Prompt ===" -ForegroundColor Cyan
# Prompt user for password securely (password not visible while typing)

# Uncomment to run:
# $server = "localhost"
# $database = "master"
# $user = "sa"
# $securePassword = Read-Host "Enter SQL Password" -AsSecureString
# $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
# $plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
# .\connect_sql_database.ps1 -ServerName $server -DatabaseName $database -Username $user -Password $plainPassword
# Remove password from memory
# $plainPassword = $null
# [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)


# ===============================================
# Example 6: Using Environment Variables
# ===============================================
Write-Host "`n=== Example 6: Environment Variables ===" -ForegroundColor Cyan
# Set environment variables (do this once in your session or profile)
# $env:SQL_SERVER = "localhost"
# $env:SQL_DATABASE = "TestDB"
# $env:SQL_USERNAME = "sa"
# $env:SQL_PASSWORD = "YourPassword"  # NOT recommended for production!

# Then use them:
# Uncomment to run:
# .\connect_sql_database.ps1 `
#     -ServerName $env:SQL_SERVER `
#     -DatabaseName $env:SQL_DATABASE `
#     -Username $env:SQL_USERNAME `
#     -Password $env:SQL_PASSWORD `
#     -Query "SELECT GETDATE() AS CurrentDateTime"


# ===============================================
# Example 7: Azure SQL Database
# ===============================================
Write-Host "`n=== Example 7: Azure SQL Database ===" -ForegroundColor Cyan
# Connect to Azure SQL Database
# NOTE: Azure SQL requires username in format: username@servername

# Uncomment to run:
# $azureServer = "myserver.database.windows.net"
# $azureDatabase = "MyDatabase"
# $azureUsername = "sqladmin"
# $azurePassword = "***SECURE_PASSWORD***"  # Replace with actual password
#
# .\connect_sql_database.ps1 `
#     -ServerName $azureServer `
#     -DatabaseName $azureDatabase `
#     -Username $azureUsername `
#     -Password $azurePassword `
#     -Query "SELECT GETDATE() AS CurrentDateTime"


# ===============================================
# Example 8: Query with Results Processing
# ===============================================
Write-Host "`n=== Example 8: Process Query Results ===" -ForegroundColor Cyan
# Execute query and capture output for further processing

# Uncomment to run:
# $output = .\connect_sql_database.ps1 `
#     -ServerName "localhost" `
#     -DatabaseName "master" `
#     -UseWindowsAuth `
#     -Query "SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')"
#
# Write-Host "Query executed. Check output above for results."


# ===============================================
# Example 9: Error Handling in Scripts
# ===============================================
Write-Host "`n=== Example 9: Error Handling ===" -ForegroundColor Cyan
# Handle connection failures gracefully

# Uncomment to run:
# try {
#     .\connect_sql_database.ps1 `
#         -ServerName "localhost" `
#         -DatabaseName "TestDB" `
#         -UseWindowsAuth `
#         -Query "SELECT 1 AS Test"
#     
#     if ($LASTEXITCODE -eq 0) {
#         Write-Host "✓ Database operation successful" -ForegroundColor Green
#     } else {
#         Write-Host "✗ Database operation failed" -ForegroundColor Red
#     }
# }
# catch {
#     Write-Host "✗ Script execution error: $($_.Exception.Message)" -ForegroundColor Red
# }


# ===============================================
# Example 10: Automated Health Check
# ===============================================
Write-Host "`n=== Example 10: Database Health Check ===" -ForegroundColor Cyan
# Check if database is accessible and responsive

# Uncomment to run:
# $healthCheckQuery = @"
# SELECT 
#     SERVERPROPERTY('ProductVersion') AS Version,
#     SERVERPROPERTY('ProductLevel') AS ServicePack,
#     SERVERPROPERTY('Edition') AS Edition,
#     GETDATE() AS CurrentDateTime
# "@
#
# .\connect_sql_database.ps1 `
#     -ServerName "localhost" `
#     -DatabaseName "master" `
#     -UseWindowsAuth `
#     -Query $healthCheckQuery


# ===============================================
# SECURITY BEST PRACTICES
# ===============================================
Write-Host "`n=== Security Best Practices ===" -ForegroundColor Yellow
Write-Host "1. Never hardcode passwords in scripts" -ForegroundColor Gray
Write-Host "2. Use Windows Authentication when possible" -ForegroundColor Gray
Write-Host "3. Store credentials securely (e.g., Azure Key Vault, Windows Credential Manager)" -ForegroundColor Gray
Write-Host "4. Use least-privilege database accounts" -ForegroundColor Gray
Write-Host "5. Enable SSL/TLS for remote connections" -ForegroundColor Gray
Write-Host "6. Regularly rotate passwords and review access" -ForegroundColor Gray
Write-Host "7. Never commit credentials to version control" -ForegroundColor Gray
Write-Host "8. Use environment-specific configuration files (.gitignore them!)" -ForegroundColor Gray

Write-Host "`nUncomment the examples above to try them out!" -ForegroundColor Cyan
Write-Host "Remember to update server names, databases, and credentials as needed.`n" -ForegroundColor Cyan
