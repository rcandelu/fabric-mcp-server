import pytest
import asyncio
from src.server import create_fabric_mcp_server
from src.fabric_client import FabricClient

@pytest.mark.asyncio
async def test_server_creation():
    """Test that MCP server can be created"""
    server = create_fabric_mcp_server()
    assert server is not None
    assert server.name == "fabric-mcp-server"
    assert server.version == "1.0.0"

@pytest.mark.asyncio
async def test_query_validation():
    """Test that dangerous queries are rejected"""
    client = FabricClient(
        tenant_id="test",
        client_id="test",
        client_secret="test",
        workspace_id="test",
        lakehouse_id="test"
    )
    
    # Test dangerous queries
    dangerous_queries = [
        "DELETE FROM users",
        "DROP TABLE accounts",
        "UPDATE products SET price = 0",
        "INSERT INTO logs VALUES ('hack')"
    ]
    
    for query in dangerous_queries:
        assert not client._is_safe_query(query)
    
    # Test safe queries
    safe_queries = [
        "SELECT * FROM products",
        "SELECT COUNT(*) FROM users WHERE active = true",
        "SELECT name, price FROM products ORDER BY price DESC"
    ]
    
    for query in safe_queries:
        assert client._is_safe_query(query)