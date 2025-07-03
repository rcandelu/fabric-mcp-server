import aiohttp
from typing import Dict, List, Any
import pandas as pd
from datetime import datetime, timedelta
import json

class FabricClient:
    """Client for Microsoft Fabric API interactions"""
    
    def __init__(self, tenant_id: str, client_id: str, client_secret: str,
                 workspace_id: str, lakehouse_id: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.workspace_id = workspace_id
        self.lakehouse_id = lakehouse_id
        self.base_url = "https://api.fabric.microsoft.com/v1"
        self.token = None
        self.token_expires = None
    
    async def _get_token(self) -> str:
        """Get or refresh access token"""
        if self.token and self.token_expires > datetime.now():
            return self.token
        
        async with aiohttp.ClientSession() as session:
            url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": "https://api.fabric.microsoft.com/.default",
                "grant_type": "client_credentials"
            }
            
            async with session.post(url, data=data) as response:
                result = await response.json()
                self.token = result["access_token"]
                self.token_expires = datetime.now() + timedelta(seconds=result["expires_in"] - 60)
                return self.token
    
    async def list_tables(self) -> List[Dict[str, Any]]:
        """List all tables in the lakehouse"""
        token = await self._get_token()
        
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{self.base_url}/workspaces/{self.workspace_id}/lakehouses/{self.lakehouse_id}/tables"
            
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                return data.get("value", [])
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a SQL query using Fabric SQL endpoint"""
        # Validate query is read-only
        if not self._is_safe_query(query):
            raise ValueError("Only SELECT queries are allowed")
        
        token = await self._get_token()
        
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Use Fabric SQL Analytics endpoint
            url = f"{self.base_url}/workspaces/{self.workspace_id}/datamarts/query"
            data = {
                "query": query,
                "lakehouseId": self.lakehouse_id
            }
            
            async with session.post(url, headers=headers, json=data) as response:
                if response.status != 200:
                    error = await response.text()
                    raise Exception(f"Query failed: {error}")
                
                result = await response.json()
                return {
                    "columns": result.get("columns", []),
                    "rows": result.get("rows", []),
                    "row_count": len(result.get("rows", []))
                }
    
    def _is_safe_query(self, query: str) -> bool:
        """Validate query is read-only"""
        dangerous_keywords = [
            "INSERT", "UPDATE", "DELETE", "DROP", "CREATE", 
            "ALTER", "TRUNCATE", "EXEC", "EXECUTE"
        ]
        
        query_upper = query.upper()
        return not any(keyword in query_upper for keyword in dangerous_keywords)