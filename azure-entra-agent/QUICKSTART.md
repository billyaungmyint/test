# Quick Start Guide

## Step 1: Configure Azure App Registration

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **"New registration"**
   - Name: `Entra User Lookup Agent`
   - Supported account types: Choose based on your needs
   - Click **"Register"**

4. Note your **Application (client) ID** and **Directory (tenant) ID**

5. Create a client secret:
   - Go to **"Certificates & secrets"**
   - Click **"New client secret"**
   - Add description: `Agent secret`
   - Choose expiration
   - Click **"Add"**
   - **Copy the secret value immediately!**

6. Add API permissions:
   - Go to **"API permissions"**
   - Click **"Add a permission"**
   - Select **"Microsoft Graph"**
   - Select **"Application permissions"**
   - Search for and add **"User.Read.All"**
   - Click **"Grant admin consent for [organization]"**

## Step 2: Set Windows Environment Variables

Choose one of these methods:

### Option A: PowerShell Script (Easiest)

```powershell
# Run in the project directory
.\setup_env.ps1

# Enter your credentials when prompted
# Use -System switch to set for all users (requires Admin)
```

### Option B: Command Prompt

```cmd
# Run in the project directory
setup_env.bat

# Enter your credentials when prompted
```

### Option C: Quick PowerShell Commands

```powershell
# Set permanent User variables
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_ID", "your-client-id", "User")
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", "your-client-secret", "User")
[Environment]::SetEnvironmentVariable("AZURE_TENANT_ID", "your-tenant-id", "User")

# Set for current session (immediately available)
$env:AZURE_CLIENT_ID = "your-client-id"
$env:AZURE_CLIENT_SECRET = "your-client-secret"
$env:AZURE_TENANT_ID = "your-tenant-id"
```

### Option D: Manual Setup

1. Search for "Edit the system environment variables"
2. Click "Environment Variables..."
3. Under "User variables", click "New..."
4. Add each variable:
   - **AZURE_CLIENT_ID**: Your application client ID
   - **AZURE_CLIENT_SECRET**: Your client secret
   - **AZURE_TENANT_ID**: Your tenant ID
   - **USER_AGENT_NAME**: EntraUserLookupAgent (optional)

## Step 3: Verify Setup

**Important: Restart your terminal or IDE after setting environment variables!**

```bash
.venv\Scripts\python test_setup.py
```

You should see all checks passing. If you see errors about missing variables:

1. **Restart your terminal/command prompt**
2. **Restart your IDE if using one**
3. **Log out and back in if needed**
4. **Run the verification again**

## Step 4: Test the Agent

### Interactive Test

```bash
.venv\Scripts\python entra_agent.py
```

This will prompt you to enter a name to search.

### Automated Test

```bash
.venv\Scripts\python example_usage.py
```

This searches for users with "smith" in their name.

## Step 5: Use in Your Code

```python
import asyncio
from entra_agent import EntraUserLookupAgent

async def main():
    agent = EntraUserLookupAgent()
    
    # Search for users
    users = await agent.search_users_by_name("John")
    
    for user in users:
        print(f"{user['display_name']} - {user['email']}")

asyncio.run(main())
```

## Troubleshooting

### "Missing required Azure credentials"

**Cause:** Environment variables not accessible

**Solution:**
1. Verify variables are set:
   ```powershell
   # In PowerShell
   $env:AZURE_CLIENT_ID
   $env:AZURE_TENANT_ID
   ```

2. If empty, restart your terminal and try again

3. If still empty, re-run the setup script or check manual setup

### "Insufficient privileges" or "Authorization_RequestDenied"

**Cause:** Missing API permissions or admin consent

**Solution:**
1. Go to Azure Portal
2. Check App Registration > API permissions
3. Ensure User.Read.All is added
4. Click "Grant admin consent for [organization]"
5. Wait a few minutes and try again

### "Invalid client secret"

**Cause:** Wrong secret or expired secret

**Solution:**
1. Verify the secret in your environment variable matches Azure
2. Check if secret expired in Azure Portal
3. Regenerate secret if needed and update environment variable
4. Restart terminal after updating

### No users found

**Cause:** Search criteria too narrow or permissions issue

**Solution:**
1. Try a broader search term
2. Verify users exist in your Azure AD
3. Check that User.Read.All permission is granted
4. Ensure admin consent was successful

## Security Notes

- **User variables** are recommended over System variables
- Keep client secret secure and rotate regularly
- Use least privilege permissions
- Monitor app registration usage in Azure Portal
- Consider Azure Key Vault for production

## Next Steps

- Explore the full [README.md](README.md) for API reference
- Customize search parameters
- Add logging and monitoring
- Integrate with your applications
- Add error handling and retries

## Need Help?

- Check [README.md](README.md) troubleshooting section
- Review [setup_env_manual.md](setup_env_manual.md) for detailed setup
- Verify Azure App Registration configuration
- Ensure environment variables are set and accessible