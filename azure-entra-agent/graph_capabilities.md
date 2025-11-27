# Microsoft Graph API Capabilities - Extended Search Options

## Current Agent: Entra Users Only

The current `entra_agent.py` searches **Microsoft Entra ID Users** using:
- Microsoft Graph API endpoint: `/users`
- Search properties: displayName, mail, userPrincipalName

## What Microsoft Graph API Can Search

### ✅ Available Search Resources

| Resource | Graph API Endpoint | Use Case | Required Permissions |
|----------|-------------------|----------|---------------------|
| **Users** | `/users` | Search people by name/email | User.Read.All |
| **Groups** | `/groups` | Find M365/Security groups | Group.Read.All |
| **Devices** | `/devices` | Search managed devices | Device.Read.All |
| **Applications** | `/applications` | Find Azure AD apps | Application.Read.All |
| **Service Principals** | `/servicePrincipals` | Search enterprise apps | Application.Read.All |
| **Audit Logs** | `/auditLogs/signIns` | Search sign-in history | AuditLog.Read.All |
| **Directory Roles** | `/directoryRoles` | List admin roles | RoleManagement.Read.Directory |
| **Administrative Units** | `/administrativeUnits` | Search org structure | AdministrativeUnit.Read.All |

### ❌ NOT Available in Graph API (Requires Azure Resource Manager)

| Resource | Correct API | Python SDK Package |
|----------|-------------|-------------------|
| Virtual Machines | Azure Resource Manager | `azure-mgmt-compute` |
| Storage Accounts | Azure Resource Manager | `azure-mgmt-storage` |
| Virtual Networks | Azure Resource Manager | `azure-mgmt-network` |
| Resource Groups | Azure Resource Manager | `azure-mgmt-resource` |
| SQL Databases | Azure Resource Manager | `azure-mgmt-sql` |
| Key Vaults | Azure Resource Manager | `azure-mgmt-keyvault` |

## Example: Extended Agent Code

Here's how to add **Group Search** to your agent:

```python
# Add to imports
from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder

class EntraUserLookupAgent:
    # ... existing user methods ...
    
    async def search_groups_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search for groups by name"""
        if not name or not name.strip():
            raise ValueError("Search name cannot be empty")
        
        query_params = GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
            search=f'"displayName:{name}" OR "mail:{name}"',
            select=["id", "displayName", "description", "mail", "groupTypes", "securityEnabled"],
            orderby=["displayName"],
            top=50
        )
        
        request_config = RequestConfiguration(query_parameters=query_params)
        request_config.headers.add('ConsistencyLevel', 'eventual')
        
        try:
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
                        'members': []  # Would need separate call to get members
                    }
                    group_data = {k: v for k, v in group_data.items() if v is not None}
                    groups.append(group_data)
            
            return groups
            
        except ODataError as e:
            print(f"Graph API Error: {e.error.message if e.error else str(e)}")
            raise
```

## Quick Reference: Common Queries

### Users
```python
# Search by name/email
search=f'"displayName:{name}" OR "mail:{name}"'

# Get user's manager
GET /users/{id}/manager

# Get user's groups
GET /users/{id}/memberOf
```

### Groups
```python
# Search groups
search=f'"displayName:{name}" OR "mail:{name}"'

# Get group members
GET /groups/{id}/members

# Get group owners
GET /groups/{id}/owners
```

### Devices
```python
# Search devices
GET /devices?$filter=startswith(displayName,'LAPTOP')

# Get device owner
GET /devices/{id}/registeredUsers
```

### Audit Logs
```python
# Search sign-ins from last 7 days
GET /auditLogs/signIns?$filter=createdDateTime ge 2025-11-20

# Search by user
GET /auditLogs/signIns?$filter=userPrincipalName eq 'john@contoso.com'
```

## Permissions Required

Add these to your Azure App Registration:

| Permission | Admin Consent Needed | Description |
|-----------|---------------------|-------------|
| User.Read.All | Yes | Read all users' profiles |
| Group.Read.All | Yes | Read all groups |
| Device.Read.All | Yes | Read all devices |
| Application.Read.All | Yes | Read all applications |
| AuditLog.Read.All | Yes | Read audit logs |
| Directory.Read.All | Yes | Read all directory data (broad) |

## Next Steps

To extend your agent:

1. **Add new methods** for each resource type (groups, devices, etc.)
2. **Update imports** for the specific request builders
3. **Add required permissions** in Azure App Registration
4. **Grant admin consent** for new permissions
5. **Test with small queries** before scaling up

For Azure infrastructure (VMs, storage, etc.), you would need a separate agent using:
```python
from azure.mgmt.compute import ComputeManagementClient
```

Would you like me to implement group search functionality or any other specific resource?