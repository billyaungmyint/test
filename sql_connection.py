"""
SQL Server Connection Module

This module demonstrates various ways to connect to SQL Server databases.
Follows PEP 8 conventions and project guidelines.
DO NOT commit actual credentials to version control!
"""

import pyodbc
import os
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect_sql_auth(server: str, database: str, username: str, password: str) -> Optional[pyodbc.Connection]:
    """
    Connect to SQL Server using SQL Server authentication.
    
    Args:
        server: SQL Server instance name or IP address
        database: Database name to connect to
        username: SQL Server username
        password: SQL Server password
        
    Returns:
        Connection object if successful, None otherwise
    """
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password}"
        )
        connection = pyodbc.connect(connection_string)
        logger.info(f"Successfully connected to {database} on {server} using SQL authentication")
        return connection
    except pyodbc.Error as e:
        logger.error(f"SQL authentication connection failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during SQL authentication: {e}")
        return None


def connect_windows_auth(server: str, database: str) -> Optional[pyodbc.Connection]:
    """
    Connect to SQL Server using Windows authentication.
    
    Args:
        server: SQL Server instance name or IP address
        database: Database name to connect to
        
    Returns:
        Connection object if successful, None otherwise
    """
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes"
        )
        connection = pyodbc.connect(connection_string)
        logger.info(f"Successfully connected to {database} on {server} using Windows authentication")
        return connection
    except pyodbc.Error as e:
        logger.error(f"Windows authentication connection failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during Windows authentication: {e}")
        return None


def test_connection(connection: pyodbc.Connection) -> Dict[str, Any]:
    """
    Test a database connection by executing a simple query.
    
    Args:
        connection: Active database connection
        
    Returns:
        Dictionary with test results
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION as version, GETDATE() as current_time")
        row = cursor.fetchone()
        
        result = {
            "success": True,
            "version": row.version if row else "Unknown",
            "current_time": row.current_time if row else "Unknown"
        }
        logger.info("Connection test successful")
        return result
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return {"success": False, "error": str(e)}


def get_connection_from_env() -> Optional[pyodbc.Connection]:
    """
    Create a database connection using environment variables.
    
    Environment variables:
        SQL_SERVER: Server name or IP (default: localhost)
        SQL_DATABASE: Database name (default: master)
        SQL_USERNAME: Username for SQL auth (optional)
        SQL_PASSWORD: Password for SQL auth (optional)
        
    Returns:
        Connection object if successful, None otherwise
    """
    server = os.getenv("SQL_SERVER", "localhost")
    database = os.getenv("SQL_DATABASE", "master")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")
    
    if username and password:
        logger.info("Using SQL Server authentication from environment")
        return connect_sql_auth(server, database, username, password)
    else:
        logger.info("Using Windows authentication (no SQL credentials in environment)")
        return connect_windows_auth(server, database)


def main():
    """
    Main function to demonstrate SQL Server connections.
    Uses environment variables for configuration.
    """
    print("=== SQL Server Connection Examples ===")
    
    # Get connection parameters
    server = os.getenv("SQL_SERVER", "localhost")
    database = os.getenv("SQL_DATABASE", "master")
    
    print(f"Target server: {server}")
    print(f"Target database: {database}")
    print()
    
    # Example 1: Try Windows Authentication
    print("=== Example 1: Windows Authentication ===")
    conn = connect_windows_auth(server, database)
    if conn:
        print("✓ Windows authentication successful!")
        test_result = test_connection(conn)
        if test_result["success"]:
            print(f"  Server version: {test_result['version'][:50]}...")
            print(f"  Current time: {test_result['current_time']}")
        conn.close()
        print("  Connection closed.")
    else:
        print("✗ Windows authentication failed")
    
    print()
    
    # Example 2: Try SQL Authentication (if credentials available)
    print("=== Example 2: SQL Server Authentication ===")
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")
    
    if username and password:
        conn = connect_sql_auth(server, database, username, password)
        if conn:
            print("✓ SQL authentication successful!")
            test_result = test_connection(conn)
            if test_result["success"]:
                print(f"  Server version: {test_result['version'][:50]}...")
                print(f"  Current time: {test_result['current_time']}")
            conn.close()
            print("  Connection closed.")
        else:
            print("✗ SQL authentication failed")
    else:
        print("SQL_USERNAME and SQL_PASSWORD environment variables not set")
        print("Skipping SQL authentication example")
    
    print()
    print("=== Environment-based Connection ===")
    conn = get_connection_from_env()
    if conn:
        print("✓ Environment-based connection successful!")
        conn.close()
    else:
        print("✗ Environment-based connection failed")


if __name__ == "__main__":
    main()