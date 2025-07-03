from fastmcp import FastMCP
from typing import Any, Dict, List
import os
from .fabric_client import FabricClient
from .tools import FabricTools
from .resources import InsightsMemo
from .prompts import FabricPrompts

def create_fabric_mcp_server() -> FastMCP:
    """Create and configure the Fabric MCP server"""
    
    # Initialize FastMCP server
    mcp = FastMCP(
        name="fabric-mcp-server",
        version="1.0.0",
        description="Microsoft Fabric MCP Server with BI capabilities"
    )
    
    # Initialize Fabric client
    fabric_client = FabricClient(
        tenant_id=os.getenv("FABRIC_TENANT_ID"),
        client_id=os.getenv("FABRIC_CLIENT_ID"),
        client_secret=os.getenv("FABRIC_CLIENT_SECRET"),
        workspace_id=os.getenv("FABRIC_WORKSPACE_ID"),
        lakehouse_id=os.getenv("FABRIC_LAKEHOUSE_ID")
    )
    
    # Initialize components
    tools = FabricTools(fabric_client)
    insights_memo = InsightsMemo()
    prompts = FabricPrompts()
    
    # Register tools
    @mcp.tool()
    async def list_tables() -> Dict[str, Any]:
        """List all available tables in the Fabric lakehouse"""
        return await tools.list_tables()
    
    @mcp.tool()
    async def read_query(query: str) -> Dict[str, Any]:
        """Execute a read-only SQL query on Fabric data"""
        return await tools.execute_query(query)
    
    @mcp.tool()
    async def append_insight(
        title: str,
        content: str,
        category: str = "general",
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """Append a new insight to the company insights memo"""
        return await insights_memo.append_insight(
            title=title,
            content=content,
            category=category,
            tags=tags or []
        )
    
    # Register resources
    @mcp.resource("insights-memo")
    async def get_insights_memo() -> Dict[str, Any]:
        """Get the current insights memo document"""
        return {
            "content": insights_memo.get_markdown(),
            "metadata": {
                "total_insights": insights_memo.count(),
                "categories": insights_memo.get_categories(),
                "last_updated": insights_memo.last_updated
            }
        }
    
    # Register prompts
    @mcp.prompt("analyze-sales-data")
    async def analyze_sales_prompt() -> str:
        """Comprehensive sales data analysis prompt"""
        return prompts.get_sales_analysis_prompt()
    
    @mcp.prompt("generate-bi-report")
    async def bi_report_prompt(
        report_type: str = "executive",
        time_period: str = "last_month"
    ) -> str:
        """Generate a BI report based on current data"""
        return prompts.get_bi_report_prompt(report_type, time_period)
    
    return mcp