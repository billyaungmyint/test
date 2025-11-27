"""
Azure Entra User Lookup Agent

This module provides functionality to search for Microsoft Entra (Azure AD) users
by full or partial name using the Microsoft Graph API.

Security Note: This agent reads credentials from Windows environment variables
for better security. Set these in System Properties > Environment Variables:
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder
from msgraph.generated.models.o_data_errors.o_data_error import ODataError
from kiota_abstractions.base_request_configuration import RequestConfiguration


class EntraUserLookupAgent:
    """
    Agent for looking up Microsoft Entra user accounts by name.
    
    Uses Azure App Registration with Client ID and Secret for authentication.
    """
    
    def __init__(self):
        """Initialize the agent with Azure credentials from Windows environment variables."""
        self.client_id = os.environ.get('AZURE_CLIENT_ID')
        self.client_secret = os.environ.get('AZURE_CLIENT_SECRET')
        self.tenant_id = os.environ.get('AZURE_TENANT_ID')
        self.user_agent = os.environ.get('USER_AGENT_NAME', 'EntraUserLookupAgent')
        
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise ValueError(
                "Missing required Azure credentials. Please set Windows environment variables:\n"
                "AZURE_CLIENT_ID - Your Azure App Registration client ID\n"
                "AZURE_CLIENT_SECRET - Your Azure App Registration client secret\n"
                "AZURE_TENANT_ID - Your Azure AD tenant ID\n\n"
                "Set these in: Control Panel > System > Advanced system settings > Environment Variables"
            )
        
        # Initialize the credential and Graph client
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        
        self.graph_client = GraphServiceClient(
            credentials=self.credential,
            scopes=['https://graph.microsoft.com/.default']
        )
    
    async def search_users_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Search for users by full or partial name.
        
        Args:
            name: Full or partial name to search for
            
        Returns:
            List of user dictionaries containing user details
            
        Raises:
            ODataError: If Graph API call fails
        """
        if not name or not name.strip():
            raise ValueError("Search name cannot be empty")
        
        # Build the search query - search across displayName and mail properties
        # Using $search parameter for better matching across multiple fields
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            search=f'"displayName:{name}" OR "mail:{name}"',
            select=["id", "displayName", "mail", "userPrincipalName", "givenName", "surname", "jobTitle", "department", "officeLocation", "mobilePhone", "businessPhones"],
            orderby=["displayName"],
            top=50  # Limit results to prevent timeouts
        )
        
        request_config = RequestConfiguration(query_parameters=query_params)
        request_config.headers.add('ConsistencyLevel', 'eventual')
        
        try:
            # Execute the search
            users_response = await self.graph_client.users.get(request_configuration=request_config)
            
            users = []
            if users_response and users_response.value:
                for user in users_response.value:
                    user_data = {
                        'id': user.id,
                        'display_name': user.display_name,
                        'email': user.mail,
                        'user_principal_name': user.user_principal_name,
                        'first_name': user.given_name,
                        'last_name': user.surname,
                        'job_title': user.job_title,
                        'department': user.department,
                        'office_location': user.office_location,
                        'mobile_phone': user.mobile_phone,
                        'business_phones': user.business_phones
                    }
                    # Remove None values for cleaner output
                    user_data = {k: v for k, v in user_data.items() if v is not None}
                    users.append(user_data)
            
            return users
            
        except ODataError as e:
            print(f"Graph API Error: {e.error.message if e.error else str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific user by their Entra ID.
        
        Args:
            user_id: The Entra user ID (GUID)
            
        Returns:
            User dictionary or None if not found
            
        Raises:
            ODataError: If Graph API call fails
        """
        if not user_id:
            raise ValueError("User ID cannot be empty")
        
        try:
            user = await self.graph_client.users.by_user_id(user_id).get()
            
            if user:
                user_data = {
                    'id': user.id,
                    'display_name': user.display_name,
                    'email': user.mail,
                    'user_principal_name': user.user_principal_name,
                    'first_name': user.given_name,
                    'last_name': user.surname,
                    'job_title': user.job_title,
                    'department': user.department,
                    'office_location': user.office_location,
                    'mobile_phone': user.mobile_phone,
                    'business_phones': user.business_phones
                }
                # Remove None values for cleaner output
                return {k: v for k, v in user_data.items() if v is not None}
            
            return None
            
        except ODataError as e:
            if e.error and e.error.code == "Request_ResourceNotFound":
                return None
            print(f"Graph API Error: {e.error.message if e.error else str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

    async def search_groups_by_name(self, name: str) -> List[Dict[str, Any]]:
        """
        Search for groups by name.
        
        Args:
            name: Full or partial group name to search for
            
        Returns:
            List of group dictionaries containing group details
            
        Raises:
            ODataError: If Graph API call fails
        """
        if not name or not name.strip():
            raise ValueError("Search name cannot be empty")
        
        # Build the search query - search across displayName and mail properties
        query_params = GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
            search=f'"displayName:{name}" OR "mail:{name}"',
            select=["id", "displayName", "description", "mail", "groupTypes", "securityEnabled", "mailEnabled", "visibility"],
            orderby=["displayName"],
            top=50
        )
        
        request_config = RequestConfiguration(query_parameters=query_params)
        request_config.headers.add('ConsistencyLevel', 'eventual')
        
        try:
            # Execute the search
            groups_response = await self.graph_client.groups.get(request_configuration=request_config)
            
            groups = []
            if groups_response and groups_response.value:
                for group in groups_response.value:
                    group_data = {
                        'id': group.id,
                        'display_name': group.display_name,
                        'description': group.description,
                        'email': group.mail,
                        'group_types': group.group_types,
                        'security_enabled': group.security_enabled,
                        'mail_enabled': group.mail_enabled,
                        'visibility': group.visibility
                    }
                    # Remove None values for cleaner output
                    group_data = {k: v for k, v in group_data.items() if v is not None}
                    groups.append(group_data)
            
            return groups
            
        except ODataError as e:
            print(f"Graph API Error: {e.error.message if e.error else str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise


async def main():
    """
    Interactive menu for searching Azure Entra users and groups.
    """
    try:
        # Initialize the agent
        agent = EntraUserLookupAgent()
        
        print("=" * 60)
        print("Azure Entra Search Agent")
        print("=" * 60)
        
        while True:
            print("\nPlease select an option:")
            print("1. Search for Users")
            print("2. Search for Groups")
            print("3. Get User by ID")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == '1':
                # Search for users
                search_name = input("\nEnter user name to search (or press Enter to go back): ").strip()
                
                if search_name:
                    print(f"\nSearching for users matching '{search_name}'...")
                    users = await agent.search_users_by_name(search_name)
                    
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
                        print("No users found matching the search criteria.")
            
            elif choice == '2':
                # Search for groups
                search_name = input("\nEnter group name to search (or press Enter to go back): ").strip()
                
                if search_name:
                    print(f"\nSearching for groups matching '{search_name}'...")
                    groups = await agent.search_groups_by_name(search_name)
                    
                    if groups:
                        print(f"\nFound {len(groups)} group(s):\n")
                        for i, group in enumerate(groups, 1):
                            print(f"{i}. {group.get('display_name', 'N/A')}")
                            if 'description' in group:
                                print(f"   Description: {group['description']}")
                            if 'email' in group:
                                print(f"   Email: {group['email']}")
                            if 'group_types' in group:
                                print(f"   Types: {', '.join(group['group_types']) if group['group_types'] else 'Security/No type'}")
                            if 'security_enabled' in group:
                                security = "Yes" if group['security_enabled'] else "No"
                                print(f"   Security Group: {security}")
                            if 'visibility' in group:
                                print(f"   Visibility: {group['visibility']}")
                            print()
                    else:
                        print("No groups found matching the search criteria.")
            
            elif choice == '3':
                # Get specific user by ID
                user_id = input("\nEnter user ID to lookup (or press Enter to go back): ").strip()
                
                if user_id:
                    print(f"\nLooking up user with ID: {user_id}")
                    user = await agent.get_user_by_id(user_id)
                    
                    if user:
                        print("\nUser details:")
                        for key, value in user.items():
                            print(f"  {key}: {value}")
                    else:
                        print("User not found.")
            
            elif choice == '4':
                # Exit
                print("\nExiting...")
                break
            
            else:
                print("\nInvalid choice. Please enter 1, 2, 3, or 4.")
                
            # Give user a moment to see results
            if choice in ['1', '2', '3']:
                input("\nPress Enter to continue...")
    
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())