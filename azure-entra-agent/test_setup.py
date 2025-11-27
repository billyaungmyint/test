#!/usr/bin/env python3
"""
Simple test script to verify the Azure Entra Agent setup with Windows environment variables
"""

import os
import sys
from pathlib import Path

def check_windows_env_variables():
    """Check if Windows environment variables are set correctly."""
    print("Checking Windows Environment Variables...")
    
    required_vars = ['AZURE_CLIENT_ID', 'AZURE_CLIENT_SECRET', 'AZURE_TENANT_ID']
    missing_vars = []
    placeholder_vars = []
    
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
        elif 'your-' in value.lower() or 'example' in value.lower() or value.strip() == '':
            placeholder_vars.append(var)
    
    if missing_vars:
        print(f"ERROR: Missing environment variables: {', '.join(missing_vars)}")
        print("   Set these Windows environment variables:")
        print("   - AZURE_CLIENT_ID")
        print("   - AZURE_CLIENT_SECRET")
        print("   - AZURE_TENANT_ID")
        print("\n   Use one of these methods:")
        print("   1. Run setup_env.ps1 (PowerShell)")
        print("   2. Run setup_env.bat (Command Prompt)")
        print("   3. Manual setup: See setup_env_manual.md")
        print("\n   Or set temporarily for this session:")
        print("   PowerShell:") 
        print('     $env:AZURE_CLIENT_ID="your-client-id"')
        print("   CMD:")
        print('     set AZURE_CLIENT_ID=your-client-id')
        return False
    
    if placeholder_vars:
        print(f"ERROR: Placeholder values found in: {', '.join(placeholder_vars)}")
        print("   Please replace 'your-client-id-here' with actual Azure credentials")
        return False
    
    print("OK: All required Windows environment variables are set")
    return True

def check_optional_vars():
    """Check optional environment variables."""
    user_agent = os.environ.get('USER_AGENT_NAME')
    if not user_agent:
        print("INFO: USER_AGENT_NAME not set, using default: 'EntraUserLookupAgent'")
    else:
        print(f"OK: USER_AGENT_NAME is set to: {user_agent}")
    
    # Show current values (hide secrets)
    print("\nCurrent environment variable values:")
    for var in ['AZURE_CLIENT_ID', 'AZURE_TENANT_ID', 'USER_AGENT_NAME']:
        value = os.environ.get(var, 'Not Set')
        if var == 'AZURE_CLIENT_SECRET':
            print(f"  {var} = {'*encrypted*' if value != 'Not Set' else 'Not Set'}")
        else:
            print(f"  {var} = {value}")
    
    return True

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import azure.identity
        import msgraph
        print("OK: All required packages are installed")
        return True
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}")
        print("   Please run: uv sync")
        return False

def check_agent_import():
    """Check if the agent can be imported."""
    try:
        from entra_agent import EntraUserLookupAgent
        print("OK: Agent module can be imported successfully")
        return True
    except ImportError as e:
        print(f"ERROR: Cannot import EntraUserLookupAgent: {e}")
        return False
    except ValueError as e:
        if "Missing required Azure credentials" in str(e):
            print("ERROR: Azure credentials not available for agent initialization")
            print("   This is expected if environment variables are not set.")
        else:
            print(f"ERROR: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Error importing agent: {e}")
        return False

def main():
    """Run all setup checks."""
    print("= Azure Entra Agent Setup Verification")
    print("========================================")
    
    checks = [
        ("Windows Environment Variables", check_windows_env_variables),
        ("Optional Variables", check_optional_vars),
        ("Dependencies", check_dependencies),
        ("Agent Module", check_agent_import)
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"ERROR: Unexpected error during {name}: {e}")
    
    print("\n" + "=" * 40)
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\nSetup verification successful!")
        print("\nNext steps:")
        print("1. Ensure your Azure App has 'User.Read.All' permission")
        print("2. Grant admin consent for the permission")
        print("3. Run: .venv\\Scripts\\python entra_agent.py")
        print("4. Search for users by name!")
        
        print("\nTo test immediately:")
        print(".venv\\Scripts\\python example_usage.py")
        return 0
    else:
        print("\nSome checks failed. Please fix the issues above.")
        print("\nQuick fix options:")
        print("1. Run setup_env.ps1 in PowerShell to set variables")
        print("2. Run setup_env.bat in Command Prompt")
        print("3. Follow setup_env_manual.md for GUI instructions")
        return 1

if __name__ == "__main__":
    sys.exit(main())