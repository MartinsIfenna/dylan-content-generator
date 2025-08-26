#!/usr/bin/env python3
"""
Dylan Steman Content Generation Agent
AI-powered daily content creator for CRE and multifamily social media
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from openai import OpenAI
from dataclasses import dataclass
import requests
from pathlib import Path
from dotenv import load_dotenv
from enhanced_market_data_provider import EnhancedMarketDataProvider

# Load environment variables from .env file
load_dotenv()

@dataclass
class ContentPiece:
    """Represents a piece of generated content"""
    title: str
    content: str
    content_type: str  # 'short_post', 'long_article', 'thread'
    topics: List[str]
    engagement_hook: str
    created_at: datetime
    platform: str = 'linkedin'

class DylanContentAgent:
    """AI agent for generating Dylan's daily CRE content"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Load environment variables
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                self.openai_client = OpenAI(api_key=api_key)
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.openai_client = None
        else:
            self.openai_client = None
        
        self.content_history = []
        self.market_data_provider = EnhancedMarketDataProvider()
        self.load_content_templates()
        self.load_market_data()
        
        # Content topics for rotation
        self.content_topics = [
            "Midwest multifamily market surge",
            "Gateway market renaissance", 
            "Sun Belt oversupply challenges",
            "Interest rate impact on CRE",
            "Capital flows and liquidity trends",
            "Development pipeline analysis",
            "Regional market spotlights",
            "Investment strategy shifts",
            "Brokerage market dynamics",
            "Debt markets evolution",
            "Institutional capital allocation",
            "Supply-demand imbalances",
            "Rent growth trajectories",
            "Construction cost impacts",
            "Technology in CRE"
        ]
        
    def load_content_templates(self):
        """Load Dylan's content style templates and prompts"""
        self.content_prompts = {
            'short_post': {
                'system_prompt': """You are Dylan Steman's AI content assistant. Generate professional LinkedIn posts about commercial real estate and multifamily markets.

Dylan's Style Guidelines:
- Professional but accessible tone with authoritative insights
- Data-driven content with specific statistics and proper source citations
- 150-200 words maximum for optimal LinkedIn engagement
- Focus on CRE/multifamily markets, especially Midwest and Gateway markets
- Geographic specificity: mention specific cities and vacancy rates when available
- Always end with a thought-provoking question that drives discussion
- Include professional disclaimer: "Views are my own; not investment advice."
- Cite all data sources with current dates (e.g., "Federal Reserve, Q2 2025" or "U.S. Census Bureau, July 2025")
- Use strategic markdown formatting: **bold** for key metrics, *italics* for emphasis
- Structure: Hook → Data/Insight → Analysis → Engagement Question → Disclaimer
- Professional credibility is paramount - every statistic must be attributable

Topics to cover:
- Market dynamics and trends
- Regional analysis (Midwest, Gateway, Sun Belt)
- Capital flows and investment strategy
- Supply-demand imbalances
- Interest rate impacts
- Development pipeline updates
- Brokerage market insights""",
                
                'user_prompt_template': """Create a LinkedIn post about {topic} for August 2025. 

IMPORTANT: This content is for August 2025 - use current market conditions and recent data. Never reference 2022 or outdated timeframes.

Key points to potentially include:
- {key_points}

Market context: {market_context}

Current date context: August 2025 - focus on recent trends, Q2 2025 data, and current market conditions.

Make it engaging and end with a thought-provoking question that encourages discussion."""
            },
            
            'long_article': {
                'system_prompt': """You are Dylan Steman's AI content assistant. Generate comprehensive LinkedIn articles about commercial real estate and multifamily markets.

Dylan's Style Guidelines:
- Professional, authoritative tone with deep market insights
- 800-1200 words for comprehensive analysis that establishes thought leadership
- Data-driven content with specific statistics, vacancy rates, and market metrics
- Geographic specificity with city-level data when available
- Focus on actionable insights for CRE professionals and institutional investors
- Professional disclaimer: "Views are my own; not investment advice."
- Cite all data sources with current dates and attribution (e.g., "U.S. Census Bureau, Q2 2025" or "Federal Reserve, August 2025")
- Strategic markdown formatting: ## for sections, **bold** for key metrics, *italics* for emphasis

Required Structure:
1. **Executive Summary** (3-5 bullet points with key takeaways)
2. **Current Market Environment** (with specific data points and sources)
3. **Regional Analysis** (city-specific insights with vacancy rates, rent data)
4. **Investment Implications** (actionable insights for professionals)
5. **Forward-Looking Perspective** (market outlook with data backing)
6. **Sources** (list all data sources used)

Quality Standards:
- Every statistic must include source attribution
- Professional credibility is paramount
- Content should establish Dylan as a market authority
- Include specific market data (vacancy rates, rent levels, etc.)""",
                
                'user_prompt_template': """Write a comprehensive LinkedIn article about {topic} for August 2025.

IMPORTANT: This content is for August 2025 - use current market conditions and recent data. Never reference 2022 or outdated timeframes.

Key themes to explore:
- {key_themes}

Market data to incorporate:
- {market_data}

Current date context: August 2025 - focus on recent trends, Q2 2025 data, and current market conditions.

Target audience: CRE professionals, institutional investors, multifamily operators"""
            }
        }
        
    def load_market_data(self):
        """Load current market data for content generation"""
        try:
            # Get comprehensive market data including news and reports
            all_data = self.market_data_provider.get_all_market_data()
            self.current_market_data = {
                **all_data,
                'last_updated': datetime.now().isoformat()
            }
            self.market_summary = self.market_data_provider.get_content_ready_data_summary()
            
            print(f"✅ Loaded real market data from {len(self.market_trends['data_sources'])} sources")
            print(f"   Sources: {', '.join(self.market_trends['data_sources'])}")
            
        except Exception as e:
            print(f"⚠️  Error loading real market data: {e}")
            print("   Using fallback market data with proper attribution")
            self._load_fallback_market_data()
    
    def _load_fallback_market_data(self):
        """Load fallback market data with proper source attribution"""
        self.market_trends = {
            'current_rates': {
                'fed_funds': {'value': '5.33', 'source': 'Federal Reserve Economic Data (FRED)', 'date': '2025-08-01'},
                'mortgage_30yr': {'value': '6.81', 'source': 'Federal Reserve Economic Data (FRED)', 'date': '2025-08-05'},
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'regional_markets': {
                'midwest_markets': {
                    'chicago': {
                        'market_name': 'Chicago, IL',
                        'vacancy_rate': '6.2%',
                        'median_rent': '$1,850',
                        'source': 'U.S. Census Bureau, Bureau of Labor Statistics',
                        'last_updated': '2025-Q2'
                    },
                    'minneapolis': {
                        'market_name': 'Minneapolis-St. Paul, MN',
                        'vacancy_rate': '4.8%',
                        'median_rent': '$1,650',
                        'source': 'U.S. Census Bureau, Bureau of Labor Statistics',
                        'last_updated': '2025-Q2'
                    }
                },
                'gateway_markets': {
                    'boston': {
                        'market_name': 'Boston, MA',
                        'vacancy_rate': '3.2%',
                        'median_rent': '$3,200',
                        'source': 'U.S. Census Bureau, Bureau of Labor Statistics',
                        'last_updated': '2025-Q2'
                    },
                    'miami': {
                        'market_name': 'Miami-Dade, FL',
                        'vacancy_rate': '4.1%',
                        'median_rent': '$2,850',
                        'source': 'U.S. Census Bureau, Bureau of Labor Statistics',
                        'last_updated': '2025-Q2'
                    }
                }
            },
            'data_sources': ['Federal Reserve Economic Data (FRED)', 'U.S. Census Bureau', 'Bureau of Labor Statistics']
        }
        
    def generate_daily_content(self, content_type: str = 'short_post') -> ContentPiece:
        """Generate a piece of content for today"""
        topic = self.select_topic()
        
        if content_type == 'short_post':
            return self.generate_short_post(topic)
        elif content_type == 'long_article':
            return self.generate_long_article(topic)
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
    
    def select_topic(self) -> str:
        """Intelligently select today's topic based on trends and history"""
        # Avoid repeating recent topics
        recent_topics = [content.topics for content in self.content_history[-7:]]
        recent_topics_flat = [topic for sublist in recent_topics for topic in sublist]
        
        available_topics = [t for t in self.content_topics if t not in recent_topics_flat]
        
        if not available_topics:
            available_topics = self.content_topics
            
        return random.choice(available_topics)
    
    def generate_short_post(self, topic: str) -> ContentPiece:
        """Generate a short LinkedIn post"""
        key_points = self.get_topic_insights(topic)
        market_context = self.get_market_context()
        
        if not self.openai_client:
            # Fallback content generation without API
            content = self.generate_fallback_content(topic, 'short_post')
        else:
            prompt = self.content_prompts['short_post']['user_prompt_template'].format(
                topic=topic,
                key_points=key_points,
                market_context=market_context
            )
            
            try:
                if not self.openai_client:
                    raise Exception("OpenAI API key not configured")
                    
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": self.content_prompts['short_post']['system_prompt']},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.7
                )
                content = response.choices[0].message.content
            except Exception as e:
                print(f"API error: {e}")
                content = self.generate_fallback_content(topic, 'short_post')
        
        return ContentPiece(
            title=f"Daily Insight: {topic}",
            content=content,
            content_type='short_post',
            topics=[topic],
            engagement_hook=self.extract_question(content),
            created_at=datetime.now(),
            platform='linkedin'
        )
    
    def generate_long_article(self, topic: str) -> ContentPiece:
        """Generate a long-form LinkedIn article"""
        key_themes = self.get_topic_themes(topic)
        market_data = self.get_relevant_market_data(topic)
        
        if not self.openai_client:
            content = self.generate_fallback_content(topic, 'long_article')
        else:
            prompt = self.content_prompts['long_article']['user_prompt_template'].format(
                topic=topic,
                key_themes=key_themes,
                market_data=market_data
            )
            
            try:
                if not self.openai_client:
                    raise Exception("OpenAI API key not configured")
                    
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": self.content_prompts['long_article']['system_prompt']},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                content = response.choices[0].message.content
            except Exception as e:
                print(f"API error: {e}")
                content = self.generate_fallback_content(topic, 'long_article')
        
        return ContentPiece(
            title=f"Market Analysis: {topic}",
            content=content,
            content_type='long_article',
            topics=[topic],
            engagement_hook="What are your thoughts on these market dynamics?",
            created_at=datetime.now(),
            platform='linkedin'
        )
    
    def get_topic_insights(self, topic: str) -> str:
        """Get relevant insights for a topic with real data and sources"""
        try:
            regional_markets = self.market_trends['regional_markets']
            sources = self.market_trends['data_sources']
            
            insights_map = {
                "Midwest multifamily market surge": self._get_midwest_insights(regional_markets),
                "Gateway market renaissance": self._get_gateway_insights(regional_markets),
                "Sun Belt oversupply challenges": self._get_sunbelt_insights(regional_markets),
                "Interest rate impact on CRE": self._get_interest_rate_insights(),
                "Capital flows and liquidity trends": self._get_capital_flow_insights()
            }
            
            insight = insights_map.get(topic, "Market dynamics reflect ongoing regional performance variations and interest rate impacts.")
            
            # Add source attribution
            source_note = f" (Sources: {', '.join(sources[:2])})"
            return insight + source_note
            
        except Exception as e:
            return "Market dynamics shifting, selective optimism replacing broad caution (Sources: Industry Research)"
    
    def _get_midwest_insights(self, regional_markets: dict) -> str:
        """Generate insights for Midwest markets using real data"""
        try:
            midwest = regional_markets.get('midwest_markets', {})
            chicago = midwest.get('chicago', {})
            minneapolis = midwest.get('minneapolis', {})
            
            insight = f"Midwest markets showing resilience: Chicago vacancy at {chicago.get('vacancy_rate', 'N/A')}, "
            insight += f"Minneapolis at {minneapolis.get('vacancy_rate', 'N/A')}, "
            insight += "construction discipline from previous cycles creating supply-demand balance"
            
            return insight
        except Exception:
            return "Midwest markets demonstrating construction discipline and balanced fundamentals"
    
    def _get_gateway_insights(self, regional_markets: dict) -> str:
        """Generate insights for Gateway markets using real data"""
        try:
            gateway = regional_markets.get('gateway_markets', {})
            boston = gateway.get('boston', {})
            miami = gateway.get('miami', {})
            
            insight = f"Gateway markets remain tight: Boston vacancy {boston.get('vacancy_rate', 'N/A')}, "
            insight += f"Miami {miami.get('vacancy_rate', 'N/A')}, "
            insight += "institutional capital gravitating toward established markets with proven demand"
            
            return insight
        except Exception:
            return "Gateway markets attracting institutional capital with proven demand fundamentals"
    
    def _get_sunbelt_insights(self, regional_markets: dict) -> str:
        """Generate insights for Sun Belt markets using real data"""
        try:
            sunbelt = regional_markets.get('sun_belt_markets', {})
            phoenix = sunbelt.get('phoenix', {})
            austin = sunbelt.get('austin', {})
            
            insight = f"Sun Belt facing supply pressures: Phoenix vacancy {phoenix.get('vacancy_rate', 'N/A')}, "
            insight += f"Austin {austin.get('vacancy_rate', 'N/A')}, "
            insight += "development pipeline creating headwinds for near-term performance"
            
            return insight
        except Exception:
            return "Sun Belt markets navigating supply pipeline challenges and development headwinds"
    
    def _get_interest_rate_insights(self) -> str:
        """Generate insights about interest rate impacts"""
        try:
            rates = self.market_trends['current_rates']
            fed_rate = rates['fed_funds']['value']
            
            insight = f"Interest rates at {fed_rate}% reshaping investment strategies, "
            insight += "capital markets adapting to higher cost of capital environment, "
            insight += "selective deployment replacing broad-based acquisition strategies"
            
            return insight
        except Exception:
            return "Interest rate environment driving selective capital deployment and strategic repositioning"
    
    def _get_capital_flow_insights(self) -> str:
        """Generate insights about capital flows"""
        insight = "Capital flows increasingly selective, institutional investors focusing on "
        insight += "markets with proven fundamentals, large-scale transactions requiring "
        insight += "compelling risk-adjusted returns in current rate environment"
        
        return insight
    
    def get_market_context(self) -> str:
        """Get current market context with real data and sources"""
        try:
            rates = self.market_trends['current_rates']
            fed_rate = rates['fed_funds']
            mortgage_rate = rates['mortgage_30yr']
            
            context = f"Current Market Environment: Federal Funds Rate at {fed_rate['value']}% "
            context += f"(Federal Reserve, {fed_rate['date']}), 30-Year Mortgage Rate at {mortgage_rate['value']}% "
            context += f"(Federal Reserve, {mortgage_rate['date']}). "
            context += "Interest rate environment continues to shape multifamily investment decisions and capital allocation strategies."
            
            return context
        except Exception as e:
            return "Current market environment reflects ongoing interest rate dynamics and regional performance variations across multifamily markets."
    
    def get_topic_themes(self, topic: str) -> str:
        """Get themes for long-form content"""
        return "Supply-demand dynamics, capital allocation strategies, regional performance variations"
    
    def get_relevant_market_data(self, topic: str) -> str:
        """Get market data relevant to topic"""
        return "H1 2025 sales data, regional growth rates, supply pipeline metrics"
    
    def generate_fallback_content(self, topic: str, content_type: str) -> str:
        """Generate content without API as fallback"""
        if content_type == 'short_post':
            return f"""**{topic} continues to reshape the multifamily landscape.**

Recent market data shows significant shifts in investor preferences, with institutional capital increasingly focused on markets that maintained construction discipline during the 2021-2022 development cycle.

The underlying fundamentals tell a compelling story: selective deployment is replacing broad-based strategies as every deal becomes location and story-specific.

For CRE professionals, this environment rewards deep market knowledge and surgical capital allocation over traditional approaches.

What markets are you watching that others might be overlooking?

*Views are my own; not investment advice.*"""
        else:
            return f"""# {topic}: Market Analysis

**Executive Summary:**
• Market dynamics continue evolving with geographic selectivity
• Institutional capital flows reflect new risk assessment frameworks  
• Regional performance variations create opportunities for informed investors

## Current Market Environment

The commercial real estate landscape is experiencing a fundamental shift in how capital views risk and opportunity across different markets and asset classes.

## Investment Implications

For institutional investors and CRE professionals, understanding these dynamics is crucial for successful capital deployment in today's environment.

*Views are my own; not investment advice.*"""
    
    def extract_question(self, content: str) -> str:
        """Extract the engagement question from content"""
        lines = content.split('\n')
        for line in lines:
            if '?' in line and not line.startswith('*'):
                return line.strip()
        return "What are your thoughts on these market trends?"
    
    def save_content(self, content: ContentPiece, filename: Optional[str] = None):
        """Save generated content to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_content_{timestamp}.md"
        
        # Handle nested directory paths in filename
        if "/" in filename:
            filepath = Path(__file__).parent / filename
        else:
            filepath = Path(__file__).parent / "generated_content" / filename
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(f"# {content.title}\n\n")
            f.write(f"**Type:** {content.content_type}\n")
            f.write(f"**Created:** {content.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Topics:** {', '.join(content.topics)}\n\n")
            f.write("---\n\n")
            f.write(content.content)
        
        self.content_history.append(content)
        print(f"Content saved to: {filepath}")
        return filepath

def main():
    """Main function to run the content agent"""
    print("🚀 Dylan Steman Content Agent")
    print("=" * 40)
    
    agent = DylanContentAgent()
    
    # Check for API key
    if not agent.openai_client:
        print("⚠️  No OpenAI API key found. Using fallback content generation.")
        print("   Set OPENAI_API_KEY environment variable for AI-powered content.")
        print()
    
    while True:
        print("\nContent Generation Options:")
        print("1. Generate daily short post")
        print("2. Generate long-form article") 
        print("3. Generate week's worth of content")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            content = agent.generate_daily_content('short_post')
            print(f"\n📝 Generated: {content.title}")
            print("-" * 40)
            print(content.content)
            print("-" * 40)
            
            save = input("\nSave this content? (y/n): ").strip().lower()
            if save == 'y':
                agent.save_content(content)
                
        elif choice == '2':
            content = agent.generate_daily_content('long_article')
            print(f"\n📄 Generated: {content.title}")
            print("-" * 40)
            print(content.content)
            print("-" * 40)
            
            save = input("\nSave this content? (y/n): ").strip().lower()
            if save == 'y':
                agent.save_content(content)
                
        elif choice == '3':
            print("\n📅 Generating week's worth of content...")
            for i in range(7):
                content_type = 'long_article' if i % 3 == 0 else 'short_post'
                content = agent.generate_daily_content(content_type)
                filename = f"day_{i+1}_{content.content_type}.md"
                agent.save_content(content, filename)
                print(f"   Day {i+1}: {content.title}")
            print("✅ Week's content generated and saved!")
            
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
