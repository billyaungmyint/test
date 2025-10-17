# PowerShell SQL Server Database Connection Script

## Overview

`connect_sql_database.ps1` is a PowerShell script that provides a simple and robust way to connect to Microsoft SQL Server databases. It supports both SQL Server Authentication and Windows Authentication, with built-in error handling and query execution capabilities.

## Features

- **Multiple Authentication Methods**
  - SQL Server Authentication (username/password)
  - Windows Authentication (integrated security)
  
- **Connection Testing**
  - Validates connection before executing queries
  - Displays server information upon successful connection
  
- **Query Execution**
  - Execute SELECT, INSERT, UPDATE, DELETE statements
  - Returns and displays query results in a formatted table
  
- **Error Handling**
  - Comprehensive error messages
  - Automatic connection cleanup
  - Exit codes for scripting integration

## Prerequisites

- Windows PowerShell 5.1+ or PowerShell Core 7+
- .NET Framework with System.Data.SqlClient
- Access to a Microsoft SQL Server instance
- Appropriate database permissions

## Installation

1. Download the `connect_sql_database.ps1` file
2. Ensure PowerShell execution policy allows script execution:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

## Usage

### Basic Connection Test (SQL Server Authentication)

```powershell
.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "master" -Username "sadmin" -Password "YourPassword123"
```

### Connection Test (Windows Authentication)

```powershell
.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -UseWindowsAuth
```

### Execute a Query (SQL Server Authentication)

```powershell
.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -Username "sadmin" -Password "Pass123" -Query "SELECT @@VERSION"
```

### Execute a Query (Windows Authentication)

```powershell
.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -UseWindowsAuth -Query "SELECT TOP 10 * FROM Users"
```

### Azure SQL Database Connection

```powershell
.\connect_sql_database.ps1 -ServerName "myserver.database.windows.net" -DatabaseName "MyDatabase" -Username "sqladmin" -Password "SecurePassword123!" -Query "SELECT COUNT(*) as TableCount FROM INFORMATION_SCHEMA.TABLES"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `ServerName` | Yes | SQL Server instance name (e.g., "localhost", "server.database.windows.net") |
| `DatabaseName` | Yes | Name of the database to connect to |
| `Username` | No* | SQL Server authentication username |
| `Password` | No* | SQL Server authentication password |
| `UseWindowsAuth` | No | Switch to use Windows Authentication |
| `Query` | No | SQL query to execute (if omitted, only tests connection) |

*Required when not using Windows Authentication

## Examples

### 1. Check Database Version

```powershell
.\connect_sql_database.ps1 `
    -ServerName "localhost" `
    -DatabaseName "master" `
    -Username "sadmin" `
    -Password "YourPassword" `
    -Query "SELECT @@VERSION AS SQLServerVersion"
```

### 2. List All Tables

```powershell
.\connect_sql_database.ps1 `
    -ServerName "localhost" `
    -DatabaseName "MyDB" `
    -UseWindowsAuth `
    -Query "SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
```

### 3. Count Records in a Table

```powershell
.\connect_sql_database.ps1 `
    -ServerName "localhost" `
    -DatabaseName "MyDB" `
    -Username "appuser" `
    -Password "AppPassword123" `
    -Query "SELECT COUNT(*) AS TotalRecords FROM Customers"
```

### 4. Insert Data (Use with Caution)

```powershell
.\connect_sql_database.ps1 `
    -ServerName "localhost" `
    -DatabaseName "TestDB" `
    -Username "sadmin" `
    -Password "Pass123" `
    -Query "INSERT INTO Logs (Message, LogDate) VALUES ('Test Entry', GETDATE())"
```

## Connection String Details

The script automatically builds connection strings based on the authentication method:

**SQL Server Authentication:**
```
Server={ServerName};Database={DatabaseName};User Id={Username};Password={Password};TrustServerCertificate=True;
```

**Windows Authentication:**
```
Server={ServerName};Database={DatabaseName};Integrated Security=True;TrustServerCertificate=True;
```

## Error Handling

The script includes comprehensive error handling:

- **Connection Failures**: Displays detailed error messages if connection cannot be established
- **Query Failures**: Reports SQL execution errors with error messages
- **Parameter Validation**: Ensures required parameters are provided
- **Automatic Cleanup**: Closes connections even if errors occur
- **Exit Codes**: Returns 0 for success, 1 for failure (useful in automation)

## Security Considerations

⚠️ **Important Security Notes:**

1. **Never hardcode passwords** in scripts or commit them to version control
2. Use secure methods to pass credentials:
   - Prompt for credentials at runtime
   - Use environment variables
   - Use secure credential storage (Windows Credential Manager, Azure Key Vault)
3. Consider using Windows Authentication when possible
4. Use least-privilege database accounts
5. Enable SSL/TLS for connections to remote servers

### Example: Using Secure String for Password

```powershell
$securePassword = Read-Host "Enter SQL Password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -Username "sadmin" -Password $plainPassword
```

## Troubleshooting

### Common Issues

**"Connection failed"**
- Verify SQL Server is running
- Check server name and port (default is 1433)
- Ensure SQL Server Authentication is enabled (if not using Windows Auth)
- Check firewall settings

**"Login failed for user"**
- Verify username and password are correct
- Ensure the user has access to the specified database
- Check if the SQL Server login is enabled

**"Cannot open database"**
- Verify database name is correct
- Ensure user has permissions to access the database

**"TrustServerCertificate"**
- The script includes `TrustServerCertificate=True` for development/testing
- For production, configure proper SSL certificates

### Enable SQL Server Authentication

If you need to enable SQL Server Authentication:

1. Open SQL Server Management Studio (SSMS)
2. Right-click on the server → Properties
3. Select "Security" page
4. Choose "SQL Server and Windows Authentication mode"
5. Restart SQL Server service

## Integration with CI/CD

The script can be integrated into automated workflows:

```powershell
# Run script and check exit code
.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -UseWindowsAuth -Query "SELECT 1"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Database connection successful"
} else {
    Write-Host "Database connection failed"
    exit 1
}
```

## Advanced Usage

### Execute Multiple Queries

For multiple queries, you can call the script multiple times or modify it to accept a query file:

```powershell
# Query 1
.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -UseWindowsAuth -Query "SELECT * FROM Table1"

# Query 2
.\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -UseWindowsAuth -Query "SELECT * FROM Table2"
```

### Save Results to File

```powershell
.\connect_sql_database.ps1 `
    -ServerName "localhost" `
    -DatabaseName "TestDB" `
    -UseWindowsAuth `
    -Query "SELECT * FROM Users" `
    | Out-File -FilePath "query_results.txt"
```

## License

This script is provided as-is for connecting to Microsoft SQL Server databases. Use at your own risk and ensure you comply with your organization's security policies.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review PowerShell and SQL Server documentation
3. Verify your SQL Server configuration and permissions

## Version History

- **v1.0** (2025-10-17): Initial release with basic connection and query functionality
