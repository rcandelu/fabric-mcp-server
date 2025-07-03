"""Fabric MCP Server - Microsoft Fabric integration for Model Context Protocol"""

__version__ = "1.0.0"
__author__ = "Fabric MCP Team"

from .server import create_fabric_mcp_server
from .fabric_client import FabricClient
from .tools import FabricTools
from .resources import InsightsMemo
from .prompts import FabricPrompts

__all__ = [
    "create_fabric_mcp_server",
    "FabricClient",
    "FabricTools",
    "InsightsMemo",
    "FabricPrompts"
]