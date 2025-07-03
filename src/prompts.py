from datetime import datetime
from typing import Dict, Any

class FabricPrompts:
    """Predefined prompts for BI analysis"""
    
    def get_sales_analysis_prompt(self) -> str:
        """Generate comprehensive sales analysis prompt"""
        return """Perform a comprehensive sales data analysis with the following components:

1. **Monthly Trends Analysis**
   - Calculate month-over-month growth rates
   - Identify seasonal patterns
   - Highlight significant changes or anomalies

2. **Top Performing Products**
   - List top 10 products by revenue
   - Calculate contribution percentage to total sales
   - Show growth trends for each top product

3. **Year-over-Year Comparison**
   - Compare current year performance vs previous year
   - Calculate YoY growth percentages
   - Identify biggest gainers and decliners

4. **Category Analysis**
   - Break down sales by product category
   - Identify fastest growing categories
   - Show category contribution to overall revenue

5. **Key Insights**
   - Summarize 3-5 key findings
   - Provide actionable recommendations
   - Highlight areas of concern or opportunity

Please format the analysis in a clear, executive-friendly manner with:
- Visual indicators (↑↓) for trends
- Percentage changes clearly marked
- Key numbers highlighted
- Brief, actionable recommendations

After completing the analysis, use the append_insight tool to save the key findings to the company insights memo."""
    
    def get_bi_report_prompt(self, report_type: str, time_period: str) -> str:
        """Generate BI report prompt based on type and period"""
        
        report_templates = {
            "executive": self._get_executive_report_template,
            "operational": self._get_operational_report_template,
            "financial": self._get_financial_report_template,
            "marketing": self._get_marketing_report_template
        }
        
        template_func = report_templates.get(report_type, self._get_executive_report_template)
        return template_func(time_period)
    
    def _get_executive_report_template(self, time_period: str) -> str:
        """Executive dashboard report template"""
        return f"""Generate an executive dashboard report for {time_period} with:

**Executive Summary**
- Overall business performance scorecard
- Revenue and profitability metrics
- Key performance indicators (KPIs) status
- Critical issues requiring attention

**Financial Highlights**
- Revenue: Total, by segment, by region
- Costs and margins analysis
- Cash flow summary
- Budget vs actual comparison

**Operational Metrics**
- Production/service delivery efficiency
- Customer satisfaction scores
- Employee productivity metrics
- Quality indicators

**Strategic Initiatives**
- Progress on key projects
- Milestone achievements
- Risk assessment
- Resource allocation

**Market Position**
- Market share analysis
- Competitive positioning
- Customer acquisition/retention
- Brand health metrics

**Recommendations**
- Top 3 priorities for next period
- Resource reallocation suggestions
- Risk mitigation strategies
- Growth opportunities

Format as a concise, visual report suitable for C-level executives.
Save key insights using the append_insight tool with category 'executive'."""
    
    def _get_operational_report_template(self, time_period: str) -> str:
        """Operational efficiency report template"""
        return f"""Generate an operational efficiency report for {time_period} focusing on:

**Production/Service Metrics**
- Output volumes and trends
- Capacity utilization rates
- Downtime analysis
- Quality metrics (defect rates, returns)

**Process Efficiency**
- Cycle time analysis
- Bottleneck identification
- Process improvement opportunities
- Automation potential

**Resource Utilization**
- Labor productivity
- Equipment efficiency (OEE)
- Material usage variance
- Energy consumption trends

**Supply Chain Performance**
- Supplier performance scores
- Inventory turnover
- Order fulfillment rates
- Lead time analysis

**Cost Analysis**
- Cost per unit trends
- Overhead allocation
- Waste reduction opportunities
- Cost saving initiatives

Provide specific, actionable recommendations for operational improvements.
Save insights using append_insight with category 'operational'."""
    
    def _get_financial_report_template(self, time_period: str) -> str:
        """Financial analysis report template"""
        return f"""Generate a detailed financial analysis report for {time_period} including:

**Income Statement Analysis**
- Revenue breakdown by stream
- Gross margin analysis
- Operating expense trends
- EBITDA and net profit margins

**Balance Sheet Review**
- Asset utilization metrics
- Working capital analysis
- Debt-to-equity ratios
- Liquidity positions

**Cash Flow Analysis**
- Operating cash flow trends
- Free cash flow generation
- Capital expenditure review
- Cash conversion cycle

**Financial Ratios**
- Profitability ratios (ROE, ROA, ROS)
- Efficiency ratios
- Leverage ratios
- Market value ratios

**Variance Analysis**
- Budget vs actual comparison
- Forecast accuracy review
- Significant variance explanations
- Corrective action plans

**Risk Assessment**
- Currency exposure
- Credit risk analysis
- Market risk factors
- Mitigation strategies

Provide forward-looking guidance and recommendations.
Save critical findings using append_insight with category 'financial'."""
    
    def _get_marketing_report_template(self, time_period: str) -> str:
        """Marketing performance report template"""
        return f"""Generate a marketing performance report for {time_period} covering:

**Campaign Performance**
- Campaign ROI analysis
- Conversion rate trends
- Cost per acquisition (CPA)
- Channel performance comparison

**Customer Analytics**
- Customer acquisition trends
- Retention and churn rates
- Customer lifetime value (CLV)
- Segmentation analysis

**Digital Marketing Metrics**
- Website traffic and engagement
- SEO performance
- Social media metrics
- Email marketing effectiveness

**Brand Health**
- Brand awareness metrics
- Net Promoter Score (NPS)
- Market share trends
- Competitive positioning

**Sales Funnel Analysis**
- Lead generation metrics
- Conversion rates by stage
- Sales cycle length
- Pipeline health

**Budget Efficiency**
- Marketing spend by channel
- ROI by marketing activity
- Budget utilization rate
- Optimization opportunities

Provide data-driven recommendations for marketing strategy optimization.
Save key insights using append_insight with category 'marketing'."""
    
    def get_custom_prompt(self, analysis_type: str, parameters: Dict[str, Any]) -> str:
        """Generate custom analysis prompt based on parameters"""
        base_prompt = f"Perform a {analysis_type} analysis with the following parameters:\n\n"
        
        for key, value in parameters.items():
            base_prompt += f"- {key}: {value}\n"
        
        base_prompt += "\nProvide clear visualizations and actionable insights."
        base_prompt += "\nSave important findings using the append_insight tool."
        
        return base_prompt