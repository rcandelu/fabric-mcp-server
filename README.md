# Fabric MCP Server

🚀 Remote MCP Server for Microsoft Fabric with BI capabilities - Integrates with OneLake semantic models and provides read-only query access with insights management.

## 🎯 Features

- **Microsoft Fabric Integration**: Direct connection to OneLake semantic models
- **Read-Only SQL Access**: Secure query execution with validation
- **BI Insights Management**: Capture and store analysis insights
- **Pre-built Prompts**: Sales analysis and BI report generation
- **Azure Functions Hosting**: Serverless architecture for scalability
- **Claude Desktop Compatible**: Works seamlessly with Claude AI

## 🏗️ Architecture

```
Claude Desktop <-> Azure Functions (MCP Server) <-> Microsoft Fabric
                            |
                            v
                   Azure Blob Storage
                    (Insights Memo)
```

## 🛠️ Tools Available

### 1. `list_tables`
List all available tables in your Fabric lakehouse.

### 2. `read_query`
Execute read-only SQL queries on your Fabric data with:
- Query validation (SELECT only)
- 30-second timeout protection
- Formatted JSON response

### 3. `append_insight`
Save important findings to the company insights memo:
- Categorized insights (general, financial, operational, marketing)
- Tagging system for easy retrieval
- Persistent storage in Azure Blob

## 📝 Resources

### `insights-memo`
Markdown document containing all captured insights:
- Organized by category
- Timestamped entries
- Full history of analysis findings

## 💡 Prompts

### `analyze-sales-data`
Comprehensive sales analysis including:
- Monthly trends
- Top performers
- YoY comparisons
- Category breakdowns

### `generate-bi-report`
Customizable BI reports:
- Executive dashboards
- Operational efficiency
- Financial analysis
- Marketing performance

## 🚀 Deployment

### Prerequisites

1. Azure Subscription
2. Microsoft Fabric workspace with lakehouse
3. Azure Storage Account
4. Azure Functions Core Tools (for local development)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/rcandelu/fabric-mcp-server.git
   cd fabric-mcp-server
   ```

2. **Configure Azure Resources**
   
   Create an Azure Function App:
   ```bash
   az functionapp create \
     --resource-group myResourceGroup \
     --consumption-plan-location westeurope \
     --runtime python \
     --runtime-version 3.11 \
     --functions-version 4 \
     --name fabric-mcp-server \
     --storage-account mystorageaccount
   ```

3. **Set Environment Variables**
   
   In Azure Portal, add these Application Settings:
   - `FABRIC_TENANT_ID`: Your Azure AD tenant ID
   - `FABRIC_CLIENT_ID`: Service principal client ID
   - `FABRIC_CLIENT_SECRET`: Service principal secret
   - `FABRIC_WORKSPACE_ID`: Fabric workspace ID
   - `FABRIC_LAKEHOUSE_ID`: Lakehouse ID
   - `STORAGE_ACCOUNT_NAME`: Azure Storage account name
   - `STORAGE_ACCOUNT_KEY`: Storage account key

4. **Configure GitHub Secrets**
   
   Add these secrets to your GitHub repository:
   - `AZURE_CREDENTIALS`: Service principal JSON
   - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`: Download from Azure Portal

5. **Deploy**
   
   Push to main branch to trigger automatic deployment:
   ```bash
   git push origin main
   ```

## 💻 Local Development

1. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure local settings**
   
   Copy `local.settings.json` and fill in your values.

3. **Run locally**
   ```bash
   func start
   ```

## 🔧 Claude Desktop Configuration

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "fabric-bi": {
      "url": "https://fabric-mcp-server.azurewebsites.net/mcp",
      "headers": {
        "x-api-key": "your-api-key"
      },
      "capabilities": {
        "tools": true,
        "resources": true,
        "prompts": true
      }
    }
  }
}
```

## 🔐 Security Considerations

- **Read-Only Access**: Only SELECT queries are allowed
- **Query Validation**: Dangerous SQL keywords are blocked
- **Timeout Protection**: 30-second query timeout
- **Authentication**: Service principal with minimal permissions
- **API Key**: Additional layer of security for endpoints

## 📊 Usage Examples

### List Available Tables
```
User: Show me what tables are available in our Fabric lakehouse
Claude: I'll list all the available tables for you...
[Uses list_tables tool]
```

### Execute Analysis Query
```
User: What were our top 10 products by revenue last quarter?
Claude: I'll query the sales data to find your top performing products...
[Uses read_query tool with appropriate SQL]
```

### Save Insights
```
User: That's interesting, please save these findings
Claude: I'll save these insights to your company memo...
[Uses append_insight tool]
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🔗 Resources

- [Microsoft Fabric Documentation](https://docs.microsoft.com/fabric)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Azure Functions Python Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)

## 👥 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Consult Microsoft Fabric and Azure documentation

---

*Built with ❤️ for the Microsoft Fabric and MCP communities*