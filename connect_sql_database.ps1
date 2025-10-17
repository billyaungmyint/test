<#
.SYNOPSIS
    Connect to Microsoft SQL Server Database and execute queries.

.DESCRIPTION
    This PowerShell script provides functionality to connect to a Microsoft SQL Server database
    using different authentication methods (SQL Server Authentication or Windows Authentication).
    It includes basic query execution capabilities with error handling.

.PARAMETER ServerName
    The SQL Server instance name (e.g., "localhost" or "server.database.windows.net")

.PARAMETER DatabaseName
    The name of the database to connect to

.PARAMETER Username
    SQL Server authentication username (optional - use for SQL Server Authentication)

.PARAMETER Password
    SQL Server authentication password (optional - use for SQL Server Authentication)

.PARAMETER UseWindowsAuth
    Switch to use Windows Authentication instead of SQL Server Authentication

.PARAMETER Query
    SQL query to execute (optional - if not provided, only tests the connection)

.EXAMPLE
    # Connect using SQL Server Authentication and test connection
    .\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "master" -Username "sadmin" -Password "YourPassword123"

.EXAMPLE
    # Connect using Windows Authentication
    .\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -UseWindowsAuth

.EXAMPLE
    # Execute a query using SQL Server Authentication
    .\connect_sql_database.ps1 -ServerName "localhost" -DatabaseName "TestDB" -Username "sadmin" -Password "Pass123" -Query "SELECT @@VERSION"

.NOTES
    Author: Generated for SQL Database Connection
    Date: 2025-10-17
    Requires: .NET Framework with System.Data.SqlClient
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerName,
    
    [Parameter(Mandatory=$true)]
    [string]$DatabaseName,
    
    [Parameter(Mandatory=$false)]
    [string]$Username,
    
    [Parameter(Mandatory=$false)]
    [string]$Password,
    
    [Parameter(Mandatory=$false)]
    [switch]$UseWindowsAuth,
    
    [Parameter(Mandatory=$false)]
    [string]$Query = ""
)

# Function to build connection string
function Get-ConnectionString {
    param(
        [string]$Server,
        [string]$Database,
        [string]$User,
        [string]$Pass,
        [bool]$WindowsAuth
    )
    
    if ($WindowsAuth) {
        return "Server=$Server;Database=$Database;Integrated Security=True;TrustServerCertificate=True;"
    } else {
        if ([string]::IsNullOrEmpty($User) -or [string]::IsNullOrEmpty($Pass)) {
            throw "Username and Password are required for SQL Server Authentication. Use -UseWindowsAuth for Windows Authentication."
        }
        return "Server=$Server;Database=$Database;User Id=$User;Password=$Pass;TrustServerCertificate=True;"
    }
}

# Function to test database connection
function Test-DatabaseConnection {
    param(
        [string]$ConnectionString
    )
    
    try {
        Write-Host "Attempting to connect to SQL Server..." -ForegroundColor Cyan
        
        # Create connection object
        $connection = New-Object System.Data.SqlClient.SqlConnection
        $connection.ConnectionString = $ConnectionString
        
        # Open connection
        $connection.Open()
        
        Write-Host "✓ Successfully connected to database!" -ForegroundColor Green
        Write-Host "Server: $($connection.DataSource)" -ForegroundColor Gray
        Write-Host "Database: $($connection.Database)" -ForegroundColor Gray
        Write-Host "Server Version: $($connection.ServerVersion)" -ForegroundColor Gray
        
        return $connection
    }
    catch {
        Write-Host "✗ Connection failed!" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Function to execute SQL query
function Invoke-SqlQuery {
    param(
        [System.Data.SqlClient.SqlConnection]$Connection,
        [string]$QueryText
    )
    
    try {
        Write-Host "`nExecuting query..." -ForegroundColor Cyan
        Write-Host "Query: $QueryText" -ForegroundColor Gray
        
        # Create command object
        $command = $Connection.CreateCommand()
        $command.CommandText = $QueryText
        $command.CommandTimeout = 30
        
        # Execute query and get results
        $adapter = New-Object System.Data.SqlClient.SqlDataAdapter $command
        $dataset = New-Object System.Data.DataSet
        $rowCount = $adapter.Fill($dataset)
        
        Write-Host "✓ Query executed successfully!" -ForegroundColor Green
        Write-Host "Rows returned: $rowCount" -ForegroundColor Gray
        
        # Display results
        if ($dataset.Tables.Count -gt 0 -and $dataset.Tables[0].Rows.Count -gt 0) {
            Write-Host "`nResults:" -ForegroundColor Cyan
            $dataset.Tables[0] | Format-Table -AutoSize
        }
        
        return $dataset
    }
    catch {
        Write-Host "✗ Query execution failed!" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Main script execution
try {
    Write-Host "=== SQL Server Database Connection Script ===" -ForegroundColor Yellow
    Write-Host ""
    
    # Build connection string
    $connectionString = Get-ConnectionString -Server $ServerName -Database $DatabaseName -User $Username -Pass $Password -WindowsAuth $UseWindowsAuth
    
    # Test connection
    $connection = Test-DatabaseConnection -ConnectionString $connectionString
    
    if ($connection -ne $null) {
        # Execute query if provided
        if (-not [string]::IsNullOrEmpty($Query)) {
            $result = Invoke-SqlQuery -Connection $connection -QueryText $Query
        } else {
            Write-Host "`nNo query provided. Connection test completed successfully." -ForegroundColor Yellow
            Write-Host "Use -Query parameter to execute SQL statements." -ForegroundColor Yellow
        }
        
        # Close connection
        $connection.Close()
        Write-Host "`nConnection closed." -ForegroundColor Gray
        
        Write-Host "`n✓ Script completed successfully!" -ForegroundColor Green
        exit 0
    } else {
        Write-Host "`n✗ Script failed - could not establish connection." -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "`n✗ Unexpected error occurred!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Stack Trace: $($_.Exception.StackTrace)" -ForegroundColor DarkGray
    exit 1
}
finally {
    # Ensure connection is closed
    if ($connection -ne $null -and $connection.State -eq 'Open') {
        $connection.Close()
        Write-Host "Connection cleanup completed." -ForegroundColor Gray
    }
}
