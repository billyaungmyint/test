"""
Example usage of the Azure Entra Agent for searching users

Security Note: This example uses Windows environment variables.
Set these in System Properties > Environment Variables:
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID
"""

import asyncio
from entra_agent import EntraUserLookupAgent

async def search_users_example():
    """Example: Search for users by name"""
    try:
        # Initialize the agent
        agent = EntraUserLookupAgent()
        
        # Search for users by name
        search_term = "smith"  # You can change this
        print(f"Searching for users matching '{search_term}'...")
        
        users = await agent.search_users_by_name(search_term)
        
        if users:
            print(f"\nFound {len(users)} user(s):\n")
            for i, user in enumerate(users, 1):
                print(f"{i}. {user.get('display_name', 'N/A')}")
                print(f"   Email: {user.get('email', 'N/A')}")
                print(f"   Username: {user.get('user_principal_name', 'N/A')}")
                if 'job_title' in user:
                    print(f"   Title: {user['job_title']}")
                if 'department' in user:
                    print(f"   Department: {user['department']}")
                print()
        else:
            print("No users found.")
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with your Azure credentials")
        print("2. Granted User.Read.All permission to your Azure App")
        print("3. Granted admin consent")

async def get_specific_user_example():
    """Example: Get a specific user by ID"""
    try:
        agent = EntraUserLookupAgent()
        
        # You would typically get this ID from a previous search
        # user_id = "some-guid-here"
        # user = await agent.get_user_by_id(user_id)
        
        print("Use get_user_by_id() to retrieve a specific user by their Entra ID")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Run the search example
    asyncio.run(search_users_example())