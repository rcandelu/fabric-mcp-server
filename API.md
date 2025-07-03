# Fabric MCP Server API Documentation

## Base URL

```
https://fabric-mcp-server.azurewebsites.net/mcp
```

## Authentication

All requests must include an API key in the headers:

```
x-api-key: your-api-key
```

## Endpoints

### Health Check

**GET** `/mcp`

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "service": "Fabric MCP Server"
}
```

### Initialize

**POST** `/mcp/initialize`

Initialize the MCP session.

**Request:**
```json
{
  "protocol_version": "1.0",
  "capabilities": {
    "tools": true,
    "resources": true,
    "prompts": true
  }
}
```

### List Tools

**POST** `/mcp/tools/list`

Get available tools.

**Response:**
```json
{
  "tools": [
    {
      "name": "list_tables",
      "description": "List all available tables in the Fabric lakehouse",
      "parameters": {}
    },
    {
      "name": "read_query",
      "description": "Execute a read-only SQL query on Fabric data",
      "parameters": {
        "query": {
          "type": "string",
          "required": true
        }
      }
    },
    {
      "name": "append_insight",
      "description": "Append a new insight to the company insights memo",
      "parameters": {
        "title": {
          "type": "string",
          "required": true
        },
        "content": {
          "type": "string",
          "required": true
        },
        "category": {
          "type": "string",
          "default": "general"
        },
        "tags": {
          "type": "array",
          "items": "string",
          "default": []
        }
      }
    }
  ]
}
```

### Call Tool

**POST** `/mcp/tools/call`

Execute a tool.

**Request:**
```json
{
  "tool": "read_query",
  "arguments": {
    "query": "SELECT TOP 10 * FROM sales_data ORDER BY revenue DESC"
  }
}
```

**Response:**
```json
{
  "success": true,
  "columns": ["product_id", "product_name", "revenue"],
  "data": [
    {
      "product_id": "P001",
      "product_name": "Widget Pro",
      "revenue": 125000
    }
  ],
  "row_count": 10,
  "query": "SELECT TOP 10 * FROM sales_data ORDER BY revenue DESC",
  "executed_at": "2024-07-03T15:30:00Z"
}
```

### List Resources

**POST** `/mcp/resources/list`

Get available resources.

**Response:**
```json
{
  "resources": [
    {
      "name": "insights-memo",
      "description": "Company insights memo document",
      "mime_type": "text/markdown"
    }
  ]
}
```

### Read Resource

**POST** `/mcp/resources/read`

Read a resource.

**Request:**
```json
{
  "resource": "insights-memo"
}
```

**Response:**
```json
{
  "content": "# Company Insights Memo\n\n...",
  "metadata": {
    "total_insights": 42,
    "categories": ["general", "financial", "operational"],
    "last_updated": "2024-07-03T15:00:00Z"
  }
}
```

### List Prompts

**POST** `/mcp/prompts/list`

Get available prompts.

**Response:**
```json
{
  "prompts": [
    {
      "name": "analyze-sales-data",
      "description": "Comprehensive sales data analysis prompt"
    },
    {
      "name": "generate-bi-report",
      "description": "Generate a BI report based on current data",
      "parameters": {
        "report_type": {
          "type": "string",
          "default": "executive",
          "enum": ["executive", "operational", "financial", "marketing"]
        },
        "time_period": {
          "type": "string",
          "default": "last_month"
        }
      }
    }
  ]
}
```

### Get Prompt

**POST** `/mcp/prompts/get`

Get a specific prompt.

**Request:**
```json
{
  "prompt": "analyze-sales-data"
}
```

**Response:**
```json
{
  "prompt": "Perform a comprehensive sales data analysis with the following components...\n",
  "name": "analyze-sales-data"
}
```

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "details": "Additional context if available"
}
```

### Common Error Codes

- `400` - Bad Request (invalid parameters)
- `401` - Unauthorized (missing or invalid API key)
- `404` - Not Found (unknown endpoint or resource)
- `500` - Internal Server Error

## Rate Limiting

- 100 requests per minute per API key
- 1000 requests per hour per API key
- Query execution limited to 30 seconds

## Best Practices

1. **Query Optimization**
   - Use appropriate WHERE clauses
   - Limit result sets with TOP or LIMIT
   - Avoid SELECT * on large tables

2. **Error Handling**
   - Implement retry logic for transient errors
   - Handle timeout errors gracefully
   - Log errors for debugging

3. **Security**
   - Keep API keys secure
   - Use environment variables
   - Rotate keys regularly

4. **Performance**
   - Cache frequently used data
   - Batch operations when possible
   - Monitor usage metrics