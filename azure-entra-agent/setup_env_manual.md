# Manual Environment Variable Setup

This guide shows you how to set Windows environment variables manually through the GUI.

## Method 1: Using Windows Settings (Windows 10/11)

1. **Open Environment Variables Settings:**
   - Press `Win + S` and search for "Edit the system environment variables"
   - Click on the result
   - Or go to: Settings > System > About > Advanced system settings > Environment Variables

2. **Create User Variables (Recommended):**
   - In the "User variables for [your username]" section, click "New..."
   - Add each variable:

### Variables to Add

**For User Variables (recommended for security):**

1. **AZURE_CLIENT_ID**
   - Variable name: `AZURE_CLIENT_ID`
   - Variable value: `[your-application-client-id]`
   - Click OK

2. **AZURE_CLIENT_SECRET**
   - Variable name: `AZURE_CLIENT_SECRET`
   - Variable value: `[your-client-secret]`
   - Click OK

3. **AZURE_TENANT_ID**
   - Variable name: `AZURE_TENANT_ID`
   - Variable value: `[your-tenant-id]`
   - Click OK

4. **USER_AGENT_NAME** (optional)
   - Variable name: `USER_AGENT_NAME`
   - Variable value: `EntraUserLookupAgent`
   - Click OK

### For System Variables (requires Admin)

If you want the variables to be available to all users:

1. Follow steps above but add to "System variables" section
2. Requires Administrator privileges
3. Less secure - secrets visible to all users

## Method 2: Using Command Prompt

**For Current Session Only (not permanent):**
```cmd
set AZURE_CLIENT_ID=your-client-id
set AZURE_CLIENT_SECRET=your-client-secret
set AZURE_TENANT_ID=your-tenant-id
set USER_AGENT_NAME=EntraUserLookupAgent
```

**Permanent (for current user):**
```cmd
setx AZURE_CLIENT_ID "your-client-id"
setx AZURE_CLIENT_SECRET "your-client-secret"
setx AZURE_TENANT_ID "your-tenant-id"
setx USER_AGENT_NAME "EntraUserLookupAgent"
```

**Note:** After using `setx`, you must open a new Command Prompt for changes to take effect.

## Method 3: Using PowerShell

**For Current Session Only:**
```powershell
$env:AZURE_CLIENT_ID="your-client-id"
$env:AZURE_CLIENT_SECRET="your-client-secret"
$env:AZURE_TENANT_ID="your-tenant-id"
$env:USER_AGENT_NAME="EntraUserLookupAgent"
```

**Permanent (for current user):**
```powershell
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_ID", "your-client-id", "User")
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", "your-client-secret", "User")
[Environment]::SetEnvironmentVariable("AZURE_TENANT_ID", "your-tenant-id", "User")
[Environment]::SetEnvironmentVariable("USER_AGENT_NAME", "EntraUserLookupAgent", "User")
```

**Permanent (system-wide, requires Admin):**
```powershell
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_ID", "your-client-id", "Machine")
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", "your-client-secret", "Machine")
[Environment]::SetEnvironmentVariable("AZURE_TENANT_ID", "your-tenant-id", "Machine")
[Environment]::SetEnvironmentVariable("USER_AGENT_NAME", "EntraUserLookupAgent", "Machine")
```

## Verification

After setting the variables, verify they are accessible:

**Command Prompt:**
```cmd
echo %AZURE_CLIENT_ID%
echo %AZURE_TENANT_ID%
```

**PowerShell:**
```powershell
$env:AZURE_CLIENT_ID
$env:AZURE_TENANT_ID
```

**Python:**
```python
import os
print(os.environ.get('AZURE_CLIENT_ID'))
print(os.environ.get('AZURE_TENANT_ID'))
```

## Security Best Practices

1. **Use User Variables** instead of System Variables when possible
2. **Never commit secrets** to version control
3. **Regularly rotate** client secrets
4. **Use least privilege** principle for API permissions
5. **Consider Azure Key Vault** for production environments
6. **Monitor access** to the Azure App Registration

## Troubleshooting

**Variables not accessible:**
- Restart your terminal/command prompt
- Restart your IDE (VS Code, PyCharm, etc.)
- Log out and back into Windows
- Check you added to correct scope (User vs System)

**Permission denied for System variables:**
- Run as Administrator
- Or use User variables instead

**Secrets visible in process list:**
- This is normal for environment variables
- Consider using a secure vault for higher security requirements