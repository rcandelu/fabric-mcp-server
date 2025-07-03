from typing import Dict, List, Any
from datetime import datetime
import json
from azure.storage.blob import BlobServiceClient
import os

class InsightsMemo:
    """Manage company insights memo"""
    
    def __init__(self):
        # Use Azure Blob Storage for persistence
        self.storage_account = os.getenv("STORAGE_ACCOUNT_NAME")
        self.storage_key = os.getenv("STORAGE_ACCOUNT_KEY")
        self.container_name = "insights"
        self.blob_name = "company_insights.json"
        
        self.insights = []
        self.last_updated = None
        self._load_insights()
    
    def _load_insights(self):
        """Load insights from Azure Blob Storage"""
        try:
            blob_service = BlobServiceClient(
                account_url=f"https://{self.storage_account}.blob.core.windows.net",
                credential=self.storage_key
            )
            
            blob_client = blob_service.get_blob_client(
                container=self.container_name,
                blob=self.blob_name
            )
            
            if blob_client.exists():
                data = blob_client.download_blob().readall()
                stored_data = json.loads(data)
                self.insights = stored_data.get("insights", [])
                self.last_updated = stored_data.get("last_updated")
        except Exception as e:
            print(f"Error loading insights: {e}")
            self.insights = []
    
    async def append_insight(self, title: str, content: str, 
                           category: str, tags: List[str]) -> Dict[str, Any]:
        """Append a new insight"""
        try:
            insight = {
                "id": len(self.insights) + 1,
                "title": title,
                "content": content,
                "category": category,
                "tags": tags,
                "created_at": datetime.now().isoformat(),
                "author": "MCP Analysis"
            }
            
            self.insights.append(insight)
            self.last_updated = datetime.now().isoformat()
            
            # Save to blob storage
            await self._save_insights()
            
            return {
                "success": True,
                "insight_id": insight["id"],
                "message": "Insight added successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _save_insights(self):
        """Save insights to Azure Blob Storage"""
        blob_service = BlobServiceClient(
            account_url=f"https://{self.storage_account}.blob.core.windows.net",
            credential=self.storage_key
        )
        
        blob_client = blob_service.get_blob_client(
            container=self.container_name,
            blob=self.blob_name
        )
        
        data = {
            "insights": self.insights,
            "last_updated": self.last_updated
        }
        
        blob_client.upload_blob(
            data=json.dumps(data, indent=2),
            overwrite=True
        )
    
    def get_markdown(self) -> str:
        """Generate markdown document of all insights"""
        md = "# Company Insights Memo\n\n"
        md += f"*Last Updated: {self.last_updated or 'Never'}*\n\n"
        md += f"**Total Insights: {len(self.insights)}**\n\n"
        
        # Group by category
        categories = {}
        for insight in self.insights:
            cat = insight["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(insight)
        
        # Generate sections
        for category, insights in categories.items():
            md += f"## {category.title()}\n\n"
            
            for insight in insights:
                md += f"### {insight['title']}\n"
                md += f"*{insight['created_at']} - {insight['author']}*\n\n"
                md += f"{insight['content']}\n\n"
                
                if insight['tags']:
                    md += f"**Tags:** {', '.join(insight['tags'])}\n\n"
                
                md += "---\n\n"
        
        return md
    
    def count(self) -> int:
        """Get total number of insights"""
        return len(self.insights)
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        return list(set(insight["category"] for insight in self.insights))