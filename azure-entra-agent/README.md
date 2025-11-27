# Azure Entra User Lookup Agent

A Python agent for searching Microsoft Entra (Azure AD) user accounts using the Microsoft Graph API with secure Windows environment variable storage.

## Features

- Search users by full or partial name
- Retrieve detailed user information including:
  - Display name
  - Email address
  - User Principal Name
  - Job title
  - Department
  - Office location
  - Phone numbers
- Secure authentication using Azure App Registration
- Credentials stored in Windows environment variables (more secure than .env files)
- Async/await support for efficient API calls

## Prerequisites

1. Python 3.13 or higher
2. Azure Active Directory tenant
3. Azure App Registration with:
   - `User.Read.All` and `Group.Read.All` permissions (or `Directory.Read.All` for broader access)
   - A client secret

## Setup

### 1. Install Dependencies

```bash
uv sync
# or
pip install -r requirements.txt
```

### 2. Set Up Azure App Registration

Follow the [Quick Start Guide](QUICKSTART.md) to:
1. Create an Azure App Registration
2. Add API permissions
3. Generate a client secret
4. Note your credentials

### 3. Configure Windows Environment Variables

Choose one of these methods to set your Azure credentials:

#### Option A: PowerShell Script (Recommended)

Run as Administrator for system-wide (all users) or as regular user for current user only:

```powershell
# For current user (recommended)
.\setup_env.ps1

# For system-wide (requires Admin)
.\setup_env.ps1 -System

# To see current values
.\setup_env.ps1 -ShowCurrent
```

#### Option B: Command Prompt Script

```cmd
setup_env.bat
```

#### Option C: Manual Setup

Follow the detailed instructions in [setup_env_manual.md](setup_env_manual.md)

#### Option D: Quick PowerShell Commands

```powershell
# Set for current user (permanent)
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_ID", "your-client-id", "User")
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", "your-client-secret", "User")
[Environment]::SetEnvironmentVariable("AZURE_TENANT_ID", "your-tenant-id", "User")
[Environment]::SetEnvironmentVariable("USER_AGENT_NAME", "EntraUserLookupAgent", "User")

# Set for current session only (immediate effect)
$env:AZURE_CLIENT_ID = "your-client-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID = "your-tenant-id"
$env:USER_AGENT_NAME = "EntraUserLookupAgent"
```

### 4. Verify Setup

```bash
.venv\Scripts\python test_setup.py
```

## Usage

### Interactive Mode

```bash
.venv\Scripts\python entra_agent.py
```

### Programmatic Usage

```python
import asyncio
from entra_agent import EntraUserLookupAgent

async def main():
    # Initialize the agent
    agent = EntraUserLookupAgent()
    
    # Search for users by name
    users = await agent.search_users_by_name("john")
    
    for user in users:
        print(f"Name: {user['display_name']}")
        print(f"Email: {user['email']}")
        print(f"Title: {user.get('job_title', 'N/A')}")
        print("---")

# Run the async function
asyncio.run(main())
```

### Using the Example

```bash
.venv\Scripts\python example_usage.py
```

## API Reference

### `EntraUserLookupAgent`

Main agent class for interacting with Entra users.

#### Methods

##### `search_users_by_name(name: str) -> List[Dict[str, Any]]`

Search for users by full or partial name.

**Parameters:**
- `name` (str): Full or partial name to search for

**Returns:**
- List of user dictionaries with user details

**Raises:**
- `ValueError`: If search name is empty
- `ODataError`: If Graph API call fails

**Example:**
```python
users = await agent.search_users_by_name("Smith")
```

##### `get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]`

Get a specific user by their Entra ID.

**Parameters:**
- `user_id` (str): The Entra user ID (GUID)

**Returns:**
- User dictionary or None if not found

**Example:**
```python
user = await agent.get_user_by_id("12345678-1234-1234-1234-123456789012")
```

## Environment Variables

The agent reads these Windows environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `AZURE_CLIENT_ID` | Yes | Azure App Registration client ID |
| `AZURE_CLIENT_SECRET` | Yes | Azure App Registration client secret |
| `AZURE_TENANT_ID` | Yes | Azure AD tenant ID |
| `USER_AGENT_NAME` | No | User agent name for Graph API calls (default: "EntraUserLookupAgent") |

### Setting Environment Variables

**Windows Settings:**
1. Search for "Edit the system environment variables"
2. Click "Environment Variables..."
3. Under "User variables", click "New..."
4. Add each variable

**PowerShell:**
```powershell
# Permanent (User scope)
[Environment]::SetEnvironmentVariable("VARIABLE_NAME", "value", "User")

# Current session only
$env:VARIABLE_NAME = "value"
```

**Command Prompt:**
```cmd
# Permanent (User scope)
setx VARIABLE_NAME "value"

# Current session only
set VARIABLE_NAME=value
```

## Azure App Registration Setup

### Required API Permissions

- `User.Read.All` (Application permission)

### Steps to Register App

1. Go to Azure Portal > Azure Active Directory
2. Navigate to "App registrations"
3. Click "New registration"
4. Name: "Entra User Lookup Agent"
5. Select account types
6. Click "Register"
7. Note Application (client) ID and Directory (tenant) ID
8. Go to "Certificates & secrets" > "New client secret"
9. Add description, select expiration
10. Click "Add" and **copy the secret value immediately**
11. Go to "API permissions" > "Add a permission"
12. Select "Microsoft Graph" > "Application permissions"
13. Add `User.Read.All`
14. Click "Grant admin consent for [organization]"

## Error Handling

The agent includes comprehensive error handling for:
- Missing environment variables
- Invalid credentials
- Graph API errors
- Rate limiting
- Network issues

## Security Best Practices

1. **Use User Environment Variables** instead of System variables
2. **Never commit secrets** to version control
3. **Regularly rotate** client secrets
4. **Use least privilege** principle for API permissions
5. **Consider Azure Key Vault** for production environments
6. **Monitor access** to the Azure App Registration
7. **Use secure deployment** pipelines for production

## Troubleshooting

### Environment Variables Not Accessible

- Restart your terminal/command prompt
- Restart your IDE (VS Code, PyCharm, etc.)
- Log out and back into Windows
- Check variable scope (User vs System)

### Common Errors

**"Missing required Azure credentials"**
- Environment variables not set correctly
- Restart your session after setting variables

**"Insufficient privileges" or "Authorization_RequestDenied"**
- Verify API permissions in Azure Portal
- Ensure admin consent granted
- Check User.Read.All permission added

**"Invalid client secret"**
- Verify client secret is correct
- Check if secret expired
- Regenerate if necessary

**No users found when searching**
- Verify search name spelling
- Check users exist in tenant
- Ensure service principal has user access

## Development

### Running Tests (when implemented)
```bash
python -m unittest discover -s . -p "test_*.py"
```

### Project Structure
```
azure-entra-agent/
├── entra_agent.py          # Main agent class
├── example_usage.py        # Example usage
├── test_setup.py          # Setup verification
├── setup_env.ps1          # PowerShell setup script
├── setup_env.bat          # Batch setup script
├── setup_env_manual.md    # Manual setup instructions
├── QUICKSTART.md          # Quick start guide
├── pyproject.toml         # Project configuration
├── requirements.txt       # Python dependencies
└── .venv/                 # Virtual environment
```

## Support

For Azure-specific issues:
- [Microsoft Graph Documentation](https://docs.microsoft.com/en-us/graph/)
- [Azure Identity Python SDK](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity)
- [Microsoft Graph Python SDK](https://github.com/microsoftgraph/msgraph-sdk-python)

For issues with this agent:
- Check the troubleshooting section
- Verify your Azure App Registration setup
- Ensure all required permissions are granted

## Contributing

When adding new features:
1. Follow existing code patterns
2. Add appropriate error handling
3. Update documentation
4. Test with both existing and new functionality

## License

This project is provided as-is for educational and development purposes.