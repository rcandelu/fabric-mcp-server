from typing import Dict, Any, List
import json
import asyncio
from datetime import datetime

class FabricTools:
    """Tools for interacting with Fabric data"""
    
    def __init__(self, fabric_client):
        self.fabric_client = fabric_client
        self.query_timeout = 30  # seconds
    
    async def list_tables(self) -> Dict[str, Any]:
        """List all available tables"""
        try:
            tables = await self.fabric_client.list_tables()
            
            # Format response
            formatted_tables = []
            for table in tables:
                formatted_tables.append({
                    "name": table["name"],
                    "schema": table.get("schema", "dbo"),
                    "type": table.get("type", "TABLE"),
                    "row_count": table.get("properties", {}).get("rowCount", "Unknown")
                })
            
            return {
                "success": True,
                "tables": formatted_tables,
                "count": len(formatted_tables)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a read-only query with timeout"""
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                self.fabric_client.execute_query(query),
                timeout=self.query_timeout
            )
            
            # Convert to JSON-serializable format
            rows = []
            for row in result["rows"]:
                row_dict = {}
                for i, col in enumerate(result["columns"]):
                    row_dict[col["name"]] = row[i]
                rows.append(row_dict)
            
            return {
                "success": True,
                "columns": [col["name"] for col in result["columns"]],
                "data": rows,
                "row_count": result["row_count"],
                "query": query,
                "executed_at": datetime.now().isoformat()
            }
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Query timeout after {self.query_timeout} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }