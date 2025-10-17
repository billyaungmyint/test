"""
Unit tests for SQL Server connection module.

Follows project testing guidelines with unittest framework.
Tests validate both functionality and clean up any side effects.
"""

import unittest
from unittest.mock import patch, MagicMock, call
import os
import logging

# Import the module to test
import sql_connection


class TestSQLConnection(unittest.TestCase):
    """Test cases for SQL Server connection functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Disable logging during tests to reduce noise
        logging.disable(logging.CRITICAL)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Re-enable logging
        logging.disable(logging.NOTSET)
    
    @patch('sql_connection.pyodbc.connect')
    def test_connect_sql_auth_success(self, mock_connect):
        """Test successful SQL Server authentication connection."""
        # Arrange
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        # Act
        result = sql_connection.connect_sql_auth("localhost", "testdb", "testuser", "testpass")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result, mock_connection)
        mock_connect.assert_called_once()
        
        # Verify connection string format
        call_args = mock_connect.call_args[0][0]
        self.assertIn("DRIVER={ODBC Driver 17 for SQL Server}", call_args)
        self.assertIn("SERVER=localhost", call_args)
        self.assertIn("DATABASE=testdb", call_args)
        self.assertIn("UID=testuser", call_args)
        self.assertIn("PWD=testpass", call_args)
    
    @patch('sql_connection.pyodbc.connect')
    def test_connect_sql_auth_failure(self, mock_connect):
        """Test SQL Server authentication connection failure."""
        # Arrange
        mock_connect.side_effect = Exception("Connection failed")
        
        # Act
        result = sql_connection.connect_sql_auth("badserver", "baddb", "baduser", "badpass")
        
        # Assert
        self.assertIsNone(result)
        mock_connect.assert_called_once()
    
    @patch('sql_connection.pyodbc.connect')
    def test_connect_windows_auth_success(self, mock_connect):
        """Test successful Windows authentication connection."""
        # Arrange
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        # Act
        result = sql_connection.connect_windows_auth("localhost", "testdb")
        
        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result, mock_connection)
        mock_connect.assert_called_once()
        
        # Verify connection string format
        call_args = mock_connect.call_args[0][0]
        self.assertIn("DRIVER={ODBC Driver 17 for SQL Server}", call_args)
        self.assertIn("SERVER=localhost", call_args)
        self.assertIn("DATABASE=testdb", call_args)
        self.assertIn("Trusted_Connection=yes", call_args)
    
    @patch('sql_connection.pyodbc.connect')
    def test_connect_windows_auth_failure(self, mock_connect):
        """Test Windows authentication connection failure."""
        # Arrange
        mock_connect.side_effect = Exception("Authentication failed")
        
        # Act
        result = sql_connection.connect_windows_auth("badserver", "baddb")
        
        # Assert
        self.assertIsNone(result)
        mock_connect.assert_called_once()
    
    def test_test_connection_success(self):
        """Test successful connection testing."""
        # Arrange
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_row = MagicMock()
        mock_row.version = "Microsoft SQL Server 2019"
        mock_row.current_time = "2025-10-17 10:00:00"
        
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = mock_row
        
        # Act
        result = sql_connection.test_connection(mock_connection)
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["version"], "Microsoft SQL Server 2019")
        self.assertEqual(result["current_time"], "2025-10-17 10:00:00")
        mock_cursor.execute.assert_called_once_with("SELECT @@VERSION as version, GETDATE() as current_time")
    
    def test_test_connection_failure(self):
        """Test connection testing failure."""
        # Arrange
        mock_connection = MagicMock()
        mock_connection.cursor.side_effect = Exception("Query failed")
        
        # Act
        result = sql_connection.test_connection(mock_connection)
        
        # Assert
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    @patch.dict(os.environ, {"SQL_SERVER": "envserver", "SQL_DATABASE": "envdb", 
                             "SQL_USERNAME": "envuser", "SQL_PASSWORD": "envpass"})
    @patch('sql_connection.connect_sql_auth')
    def test_get_connection_from_env_sql_auth(self, mock_connect_sql_auth):
        """Test environment-based connection with SQL authentication."""
        # Arrange
        mock_connection = MagicMock()
        mock_connect_sql_auth.return_value = mock_connection
        
        # Act
        result = sql_connection.get_connection_from_env()
        
        # Assert
        self.assertEqual(result, mock_connection)
        mock_connect_sql_auth.assert_called_once_with("envserver", "envdb", "envuser", "envpass")
    
    @patch.dict(os.environ, {"SQL_SERVER": "envserver", "SQL_DATABASE": "envdb"}, clear=True)
    @patch('sql_connection.connect_windows_auth')
    def test_get_connection_from_env_windows_auth(self, mock_connect_windows_auth):
        """Test environment-based connection with Windows authentication."""
        # Arrange
        mock_connection = MagicMock()
        mock_connect_windows_auth.return_value = mock_connection
        
        # Act
        result = sql_connection.get_connection_from_env()
        
        # Assert
        self.assertEqual(result, mock_connection)
        mock_connect_windows_auth.assert_called_once_with("envserver", "envdb")
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('sql_connection.connect_windows_auth')
    def test_get_connection_from_env_defaults(self, mock_connect_windows_auth):
        """Test environment-based connection with default values."""
        # Arrange
        mock_connection = MagicMock()
        mock_connect_windows_auth.return_value = mock_connection
        
        # Act
        result = sql_connection.get_connection_from_env()
        
        # Assert
        self.assertEqual(result, mock_connection)
        mock_connect_windows_auth.assert_called_once_with("localhost", "master")
    
    @patch('sql_connection.get_connection_from_env')
    @patch('sql_connection.connect_windows_auth')
    @patch('sql_connection.connect_sql_auth')
    @patch('builtins.print')
    def test_main_function_execution(self, mock_print, mock_connect_sql_auth, 
                                   mock_connect_windows_auth, mock_get_connection_from_env):
        """Test main function executes without errors."""
        # Arrange
        mock_connection = MagicMock()
        mock_connect_windows_auth.return_value = mock_connection
        mock_connect_sql_auth.return_value = None
        mock_get_connection_from_env.return_value = mock_connection
        
        # Mock test_connection to avoid database calls
        with patch('sql_connection.test_connection') as mock_test:
            mock_test.return_value = {
                "success": True, 
                "version": "Microsoft SQL Server 2019 Test Version",
                "current_time": "2025-10-17 10:00:00"
            }
            
            # Act
            sql_connection.main()
        
        # Assert - verify main function ran and made expected calls
        mock_connect_windows_auth.assert_called()
        mock_get_connection_from_env.assert_called_once()
        
        # Verify print statements were made (output was generated)
        mock_print.assert_called()
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        header_found = any("SQL Server Connection Examples" in call for call in print_calls)
        self.assertTrue(header_found, "Expected header not found in print output")


class TestConnectionStringFormats(unittest.TestCase):
    """Test connection string formatting and edge cases."""
    
    @patch('sql_connection.pyodbc.connect')
    def test_connection_string_special_characters(self, mock_connect):
        """Test connection strings handle special characters correctly."""
        # Arrange
        mock_connect.return_value = MagicMock()
        
        # Act
        sql_connection.connect_sql_auth("server\\instance", "test-db", "user@domain", "pass{word}")
        
        # Assert
        call_args = mock_connect.call_args[0][0]
        self.assertIn("SERVER=server\\instance", call_args)
        self.assertIn("DATABASE=test-db", call_args)
        self.assertIn("UID=user@domain", call_args)
        self.assertIn("PWD=pass{word}", call_args)
    
    @patch('sql_connection.pyodbc.connect')
    def test_empty_parameters_handling(self, mock_connect):
        """Test handling of empty string parameters."""
        # Arrange
        mock_connect.return_value = MagicMock()
        
        # Act
        sql_connection.connect_sql_auth("", "", "", "")
        
        # Assert
        mock_connect.assert_called_once()
        call_args = mock_connect.call_args[0][0]
        self.assertIn("SERVER=", call_args)
        self.assertIn("DATABASE=", call_args)


if __name__ == "__main__":
    unittest.main()