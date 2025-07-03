import azure.functions as func
import json
from fastmcp import FastMCP
from src.server import create_fabric_mcp_server

app = func.FunctionApp()

# Initialize MCP server
mcp_server = create_fabric_mcp_server()

@app.route(route="mcp/{*path}", methods=["GET", "POST"])
async def mcp_handler(req: func.HttpRequest) -> func.HttpResponse:
    """Handle MCP protocol requests"""
    try:
        # Get the path after /mcp/
        path = req.route_params.get('path', '')
        
        # Handle different MCP endpoints
        if req.method == "POST":
            body = req.get_json()
            
            if path == "initialize":
                result = await mcp_server.handle_initialize(body)
            elif path == "tools/list":
                result = await mcp_server.handle_list_tools()
            elif path == "tools/call":
                result = await mcp_server.handle_call_tool(body)
            elif path == "resources/list":
                result = await mcp_server.handle_list_resources()
            elif path == "resources/read":
                result = await mcp_server.handle_read_resource(body)
            elif path == "prompts/list":
                result = await mcp_server.handle_list_prompts()
            elif path == "prompts/get":
                result = await mcp_server.handle_get_prompt(body)
            else:
                return func.HttpResponse(
                    json.dumps({"error": "Unknown endpoint"}),
                    status_code=404,
                    mimetype="application/json"
                )
            
            return func.HttpResponse(
                json.dumps(result),
                status_code=200,
                mimetype="application/json"
            )
        
        # GET request for health check
        return func.HttpResponse(
            json.dumps({"status": "healthy", "service": "Fabric MCP Server"}),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )