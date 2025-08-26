#!/usr/bin/env python3
"""
Demo script for Dylan's Content Agent
Shows the system in action with sample content generation
"""

from dylan_content_agent import DylanContentAgent
from datetime import datetime
import os

def demo_content_generation():
    """Demonstrate the content generation capabilities"""
    print("🎬 Dylan Steman Content Agent Demo")
    print("=" * 50)
    
    # Initialize agent
    agent = DylanContentAgent()
    
    # Check API status
    api_status = "✅ AI-Powered" if agent.openai_client else "⚡ Template-Based"
    print(f"Status: {api_status}")
    print()
    
    # Demo 1: Generate short post
    print("📝 Demo 1: Generating Short LinkedIn Post")
    print("-" * 40)
    
    short_content = agent.generate_daily_content('short_post')
    print(f"Title: {short_content.title}")
    print(f"Topics: {', '.join(short_content.topics)}")
    print(f"Word Count: {len(short_content.content.split())} words")
    print()
    print("Content Preview:")
    print(short_content.content[:200] + "..." if len(short_content.content) > 200 else short_content.content)
    print()
    
    # Demo 2: Generate long article
    print("📄 Demo 2: Generating Long-Form Article")
    print("-" * 40)
    
    long_content = agent.generate_daily_content('long_article')
    print(f"Title: {long_content.title}")
    print(f"Topics: {', '.join(long_content.topics)}")
    print(f"Word Count: {len(long_content.content.split())} words")
    print()
    print("Content Preview:")
    print(long_content.content[:300] + "..." if len(long_content.content) > 300 else long_content.content)
    print()
    
    # Demo 3: Show topic rotation
    print("🔄 Demo 3: Topic Rotation (Next 5 Days)")
    print("-" * 40)
    
    for i in range(5):
        topic = agent.select_topic()
        print(f"Day {i+1}: {topic}")
        # Simulate adding to history
        agent.content_history.append(type('obj', (object,), {'topics': [topic]})())
    print()
    
    # Demo 4: Market data integration
    print("📊 Demo 4: Market Data Integration")
    print("-" * 40)
    
    print("Current Market Trends:")
    if hasattr(agent, 'market_trends') and isinstance(agent.market_trends, dict):
        for region, markets in agent.market_trends.items():
            print(f"  {region.replace('_', ' ').title()}:")
            if isinstance(markets, dict):
                for market, data in markets.items():
                    if isinstance(data, dict) and 'sales_growth' in data:
                        print(f"    • {market.title()}: {data['sales_growth']} growth")
                    elif isinstance(data, dict) and 'trend' in data:
                        print(f"    • {market.title()}: {data['trend'].replace('_', ' ')}")
    else:
        print("  Market data loaded successfully from multiple sources")
    print()
    
    # Demo 5: Save sample content
    print("💾 Demo 5: Saving Content")
    print("-" * 40)
    
    # Create demo directory
    demo_dir = "demo_output"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Save both pieces of content
    short_file = agent.save_content(short_content, f"{demo_dir}/demo_short_post.md")
    long_file = agent.save_content(long_content, f"{demo_dir}/demo_long_article.md")
    
    print(f"✅ Short post saved: {short_file}")
    print(f"✅ Long article saved: {long_file}")
    print()
    
    print("🎉 Demo Complete!")
    print("=" * 50)
    print("Next Steps:")
    print("1. Review generated content in demo_output/")
    print("2. Set up your OpenAI API key for AI-powered generation")
    print("3. Run 'python daily_scheduler.py' for automated scheduling")
    print("4. Customize topics and style in dylan_content_agent.py")

if __name__ == "__main__":
    demo_content_generation()
