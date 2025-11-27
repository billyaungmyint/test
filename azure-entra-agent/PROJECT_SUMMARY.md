# Project Summary: Azure Entra User Lookup Agent

## Overview

A secure Python agent for searching Microsoft Entra (Azure AD) users with Windows environment variable-based credential storage.

## 🎯 Key Security Feature

**Uses Windows Environment Variables instead of .env files** for Azure credentials - significantly more secure!

## 📁 Final Project Structure

```
azure-entra-agent/
├── entra_agent.py              # Main agent class
├── example_usage.py            # Example usage script
├── test_setup.py              # Setup verification script
├── setup_env.ps1              # PowerShell setup script
├── setup_env.bat              # Command Prompt setup script
├── setup_env_manual.md        # Manual setup instructions
├── QUICKSTART.md              # Quick start guide
├── README.md                  # Comprehensive documentation
├── SECURITY.md                # Security guide
├── SECURITY_ADVANTAGES.md     # Why env vars are more secure
├── .env.example               # Legacy .env example (not used)
├── .env.windows.example       # Windows env var example
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── .venv/                     # Virtual environment
```

## 🛠️ Libraries Installed

- **azure-identity**: Azure authentication via client credentials
- **msgraph-sdk**: Official Microsoft Graph API SDK
- **python-dotenv**: (kept for compatibility but not used)

## 🔐 Security Improvements

### Before (.env file approach):
```
Project Directory/
├── entra_agent.py
├── .env  ⚠️  DANGEROUS - can be committed to git!
└── .gitignore
```

### After (Windows env vars):
```
Project Directory/
├── entra_agent.py
└── .env.example  ✓ Safe - just an example file

# Actual secrets stored in Windows Registry:
# HKEY_CURRENT_USER\Environment
# Or: Control Panel > System > Environment Variables
```

## 🚀 Quick Start

### 1. Set Up Azure App (One Time)
- Create App Registration in Azure Portal
- Add `User.Read.All` permission
- Grant admin consent
- Copy credentials

### 2. Set Environment Variables (One Time)

**Option A - PowerShell (Recommended):**
```powershell
.\setup_env.ps1
# Enter your Azure credentials when prompted
```

**Option B - Quick PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_ID", "your-client-id", "User")
[Environment]::SetEnvironmentVariable("AZURE_CLIENT_SECRET", "your-secret", "User")
[Environment]::SetEnvironmentVariable("AZURE_TENANT_ID", "your-tenant-id", "User")
```

**Option C - Manual:**
- See [setup_env_manual.md](setup_env_manual.md)

**Important:** Restart your terminal/IDE after setting variables!

### 3. Verify Setup
```bash
.venv\Scripts\python test_setup.py
```

### 4. Run the Agent
```bash
.venv\Scripts\python entra_agent.py
```

## 💻 API Usage Examples

### Search Users by Name
```python
import asyncio
from entra_agent import EntraUserLookupAgent

async def main():
    agent = EntraUserLookupAgent()
    users = await agent.search_users_by_name("John")
    
    for user in users:
        print(f"{user['display_name']} - {user['email']}")

asyncio.run(main())
```

### Get User by ID
```python
user = await agent.get_user_by_id("user-guid-here")
print(user['display_name'], user['job_title'])
```

## 📋 Documentation Files

1. **QUICKSTART.md** - Get started in 5 minutes
2. **README.md** - Complete API documentation
3. **setup_env_manual.md** - Manual environment variable setup
4. **SECURITY.md** - Security best practices
5. **SECURITY_ADVANTAGES.md** - Why this approach is more secure

## ✅ Features

- 🔍 Search users by partial/full name
- 📊 Get detailed user information (name, email, title, dept, phone, location)
- 🔐 Secure credential storage (Windows environment variables)
- ⚡ Async/await for efficient API calls
- 🎯 Type hints for better development experience
- 🛡️ Comprehensive error handling
- 📦 Easy setup with helper scripts

## 🔑 Environment Variables Required

Set these in Windows environment variables:

| Variable | Example Value | Scope |
|----------|--------------|-------|
| `AZURE_CLIENT_ID` | `12345678-1234-1234-1234-123456789012` | User |
| `AZURE_CLIENT_SECRET` | `abc123...` | User |
| `AZURE_TENANT_ID` | `98765432-1234-1234-1234-123456789012` | User |
| `USER_AGENT_NAME` | `EntraUserLookupAgent` | User (optional) |

## 🎯 User Data Retrieved

The agent can retrieve:
- ✓ User ID
- ✓ Display Name
- ✓ Email Address
- ✓ User Principal Name
- ✓ First Name
- ✓ Last Name
- ✓ Job Title
- ✓ Department
- ✓ Office Location
- ✓ Mobile Phone
- ✓ Business Phones

## 🛡️ Security Benefits

1. **No .env file in project** - Can't be committed to git
2. **User-based access control** - Only accessible to your Windows user
3. **Windows security integration** - Protected by your Windows password
4. **Not visible in file system** - Stored in registry, not plain files
5. **Enterprise-ready** - Works with Group Policy, can be audited

## 🚀 Next Steps

1. Set up your Azure App Registration if not done
2. Run setup script to configure environment variables
3. Restart terminal/IDE
4. Run test_setup.py to verify configuration
5. Run entra_agent.py to search for users!

## 📞 Troubleshooting

**"Missing required Azure credentials"**
- Environment variables not set → Run setup script
- Variables not accessible → Restart terminal

**"Invalid client secret"**
- Check secret in Azure Portal
- May need to regenerate

**"Insufficient privileges"**
- Check User.Read.All permission
- Grant admin consent in Azure

**No users found**
- Try broader search term
- Verify users exist in directory
- Check Azure App permissions

## 🎓 Good to Know

- Environment variables are stored in `HKEY_CURRENT_USER\Environment` in Windows registry
- User scope variables don't require Administrator privileges
- Changes require terminal/IDE restart to take effect
- Secrets are encrypted at rest in Windows registry
- Each Windows user can have their own set of variables

## 💡 Tips

- Use PowerShell for easier environment variable management
- Take note of your Azure credentials before closing the Azure Portal
- Test with a small search first to verify connectivity
- The agent automatically removes `None` values from results
- Use the example_usage.py as a template for your needs

---

**Setup Time:** ~10-15 minutes
**Security Level:** High (Windows-integrated)
**Azure Permissions Required:** User.Read.All (Application)
**Platform:** Windows with Python 3.13+