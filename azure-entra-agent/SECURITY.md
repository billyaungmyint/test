# Security Guide

## Environment Variable Security

This application uses **Windows Environment Variables** instead of .env files for storing Azure credentials. This provides several security advantages:

### Advantages Over .env Files

1. **Not in Project Directory**
   - Secrets are not stored in the codebase
   - Cannot be accidentally committed to version control
   - Not exposed in file system backups

2. **Access Control**
   - User-scoped variables: Only accessible to the current Windows user
   - System-scoped variables: Require Administrator privileges to set
   - Permissions inherited from Windows user account security

3. **No Plain Text Files**
   - No `.env` file that could be read by any process
   - Not visible in project directory listings
   - Not included in zip archives or file shares

4. **Windows Security Integration**
   - Protected by Windows user account security
   - Subject to Windows security policies
   - Can be audited through Windows event logs

## Environment Variable Scopes

### User Scope (Recommended)
```powershell
[Environment]::SetEnvironmentVariable("VAR_NAME", "value", "User")
```
- **Pros**: Secure, only accessible to current user, no admin required
- **Cons**: Only available to current user account
- **Use for**: Development, individual user deployments

### System Scope (Requires Admin)
```powershell
[Environment]::SetEnvironmentVariable("VAR_NAME", "value", "Machine")
```
- **Pros**: Available to all users on the machine
- **Cons**: Requires Administrator, less secure (broader access)
- **Use for**: Shared servers, system-wide applications

### Process Scope (Not Persistent)
```powershell
$env:VAR_NAME = "value"
```
- **Pros**: Immediate effect, no persistence
- **Cons**: Lost when process/terminal closes
- **Use for**: Testing, temporary sessions

## Best Practices

### 1. Use User Variables
```powershell
# Good - User scope
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", "secret", "User")

# Avoid - System scope unless necessary
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", "secret", "Machine")
```

### 2. Separate Credentials from Code
```bash
# DON'T do this:
echo "AZURE_SECRET=abc123" > .env

# DO this:
# Set in Windows Environment Variables
# Code reads from os.environ['AZURE_SECRET']
```

### 3. Regular Secret Rotation

**Recommended Rotation Schedule:**
- Development: Every 90 days
- Staging: Every 60 days  
- Production: Every 30 days

**Rotation Process:**
1. Generate new secret in Azure Portal
2. Update environment variable
3. Restart application/service
4. Remove old secret from Azure

### 4. Principle of Least Privilege

**Required Permissions:**
- `User.Read.All` (Application permission)

**Avoid granting:**
- `Directory.Read.All` (unless absolutely necessary)
- `User.ReadWrite.All` (not needed for read-only operations)
- Any admin-level permissions

### 5. Monitoring and Auditing

**Enable in Azure Portal:**
1. Go to Azure AD > Monitoring > Sign-ins
2. Filter by your application ID
3. Set up alerts for:
   - Failed authentication attempts
   - Unusual access patterns
   - Rate limit exceeded

**Monitor in Windows:**
- Check Event Viewer for security events
- Review who can access user environment variables

### 6. Secure Development Practices

**In your code:**
```python
# GOOD - Use environment variables
import os
secret = os.environ.get('AZURE_CLIENT_SECRET')

# AVOID - Hardcoded secrets
secret = "abc123"  # NEVER DO THIS

# AVOID - Configuration files with secrets
with open('config.json') as f:  # Don't store secrets here
    config = json.load(f)
```

### 7. Development vs Production

**Development:**
```powershell
# Use User environment variables
$env:AZURE_CLIENT_SECRET = "dev-secret"
```

**Production:**
```powershell
# Use managed identity or Key Vault when possible
# If using environment variables, use User scope
# Or better: Azure Key Vault with managed identity
```

## Production Security

### For Production Deployments

**Preferred Options (in order):**

1. **Azure Managed Identity** (if running on Azure)
   ```python
   # No secrets needed!
   from azure.identity import DefaultAzureCredential
   credential = DefaultAzureCredential()
   ```

2. **Azure Key Vault**
   ```python
   from azure.keyvault.secrets import SecretClient
   from azure.identity import DefaultAzureCredential
   
   credential = DefaultAzureCredential()
   client = SecretClient(vault_url="https://your-vault.vault.azure.net/", credential=credential)
   secret = client.get_secret("azure-client-secret").value
   ```

3. **Windows Environment Variables** (on-premise Windows servers)
   - Use User scope
   - Secure the Windows server
   - Regular rotation

4. **Container Secrets** (Docker/Kubernetes)
   ```yaml
   # Kubernetes secret
   apiVersion: v1
   kind: Secret
   metadata:
     name: azure-credentials
   type: Opaque
   stringData:
     AZURE_CLIENT_SECRET: your-secret
   ```

### Avoid in Production

❌ **NEVER use in production:**
- `.env` files
- Configuration files with secrets
- Hardcoded credentials
- Command line arguments with secrets
- Environment variables in Docker images

## Security Checklist

- [ ] User-scope environment variables used
- [ ] Client secret not in code or .env files
- [ ] .gitignore excludes `.env` if it exists
- [ ] Azure App has minimum required permissions
- [ ] Admin consent granted in Azure
- [ ] Client secret rotated regularly
- [ ] Application usage monitored in Azure
- [ ] Windows account securing variables is protected
- [ ] Backup systems don't capture environment variables
- [ ] Team members know not to share secrets

## Incident Response

**If you suspect credential compromise:**

1. Immediately revoke the client secret in Azure Portal
2. Generate a new client secret
3. Update environment variables
4. Restart all applications/services
5. Review Azure AD sign-in logs
6. Check for unauthorized access
7. Notify security team if required

## Additional Resources

- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/)
- [Microsoft Identity Platform](https://docs.microsoft.com/en-us/azure/active-directory/develop/)
- [Windows Security Fundamentals](https://docs.microsoft.com/en-us/windows/security/)

## Reporting Security Issues

If you discover a security vulnerability:

1. Do NOT open a public issue
2. Email security details to your security team
3. Include steps to reproduce if possible
4. Allow time for investigation before disclosure

Remember: Security is everyone's responsibility!