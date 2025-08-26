# Dylan Steman AI Content Agent 🚀

An AI-powered content generation system that creates daily social media content for Dylan Steman, focusing on commercial real estate (CRE) and multifamily markets.

## 🎯 Features

- **Daily Content Generation**: Automated creation of LinkedIn posts and articles
- **CRE Market Focus**: Specialized in multifamily, commercial real estate, and investment insights
- **Dylan's Voice**: Maintains Dylan's professional, data-driven content style
- **Flexible Scheduling**: Daily posts, weekly articles, and batch content generation
- **Content History**: Tracks topics to avoid repetition
- **Fallback Mode**: Works without API keys using template-based generation

## 📋 Content Types

### Short-Form Posts (150-200 words)
- Daily LinkedIn posts
- Market insights and trends
- Data-driven observations
- Engagement questions
- Professional disclaimers

### Long-Form Articles (800-1200 words)
- Weekly in-depth analysis
- Market research pieces
- Executive summaries
- Sectioned analysis
- Forward-looking insights

## 🛠 Installation

1. **Clone and Setup**
   ```bash
   cd /Users/mac/CascadeProjects/Dylan_Steman_Content
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Required API Keys** (Optional)
   - OpenAI API key for AI-powered content generation
   - LinkedIn API for automated posting (future feature)

## 🚀 Quick Start

### Generate Content Manually
```bash
python dylan_content_agent.py
```

### Run Automated Scheduler
```bash
python daily_scheduler.py
```

## 📊 Content Strategy

### Topics Covered
- **Market Analysis**: Midwest surge, Gateway renaissance, Sun Belt challenges
- **Investment Insights**: Capital flows, liquidity trends, strategy shifts
- **Regional Spotlights**: Minneapolis, Chicago, Boston, Miami markets
- **Industry Trends**: Interest rates, development pipeline, supply-demand
- **Professional Insights**: Brokerage dynamics, institutional capital

### Dylan's Content Style
- ✅ Professional but accessible tone
- ✅ Data-driven with specific statistics
- ✅ Cites sources and dates
- ✅ Ends with engaging questions
- ✅ Includes professional disclaimers
- ✅ Focus on actionable insights

## 📁 Project Structure

```
Dylan_Steman_Content/
├── dylan_content_agent.py      # Main AI agent
├── daily_scheduler.py          # Automated scheduling
├── requirements.txt            # Python dependencies
├── .env.example               # Configuration template
├── generated_content/         # Output directory
├── logs/                      # Generation logs
└── existing_content/          # Dylan's current content
```

## ⚙️ Configuration

### Schedule Settings
- **Daily Posts**: 9:00 AM
- **Content Review**: 8:30 AM
- **Weekly Articles**: Tuesdays
- **Weekend Prep**: Fridays 5:00 PM

### Content Parameters
- Short posts: 150-200 words
- Long articles: 800-1200 words
- Platform: LinkedIn (primary)
- Tone: Professional, data-driven
- Disclaimer: "Views are my own; not investment advice."

## 🎛 Usage Examples

### 1. Generate Daily Content
```python
from dylan_content_agent import DylanContentAgent

agent = DylanContentAgent()
content = agent.generate_daily_content('short_post')
agent.save_content(content)
```

### 2. Batch Generate Week's Content
```python
# Generates 7 days of mixed content
for i in range(7):
    content_type = 'long_article' if i % 3 == 0 else 'short_post'
    content = agent.generate_daily_content(content_type)
    agent.save_content(content, f"day_{i+1}_{content_type}.md")
```

### 3. Run Continuous Scheduler
```bash
python daily_scheduler.py
# Select option 1 for continuous operation
```

## 📈 Content Quality Features

- **Topic Rotation**: Avoids repeating recent topics
- **Market Data Integration**: Uses current CRE market trends
- **Style Consistency**: Maintains Dylan's professional voice
- **Engagement Optimization**: Always includes discussion questions
- **Source Attribution**: Cites data sources for credibility

## 🔧 Customization

### Adding New Topics
Edit `content_topics` list in `dylan_content_agent.py`:
```python
self.content_topics.append("Your new CRE topic")
```

### Modifying Content Style
Update system prompts in `load_content_templates()` method.

### Changing Schedule
Modify `schedule_config` in `daily_scheduler.py`.

## 📝 Output Examples

### Short Post Example
```
**Minneapolis multifamily sales surged 95% in the first half of 2025.**

That's not a typo. While Sun Belt markets grapple with oversupply headwinds, 
the Midwest is quietly becoming institutional capital's new destination...

What markets are you watching that others might be missing?

*Views are my own; not investment advice.*
```

### Long Article Example
```
# Multifamily Markets Surge 23% as Midwest Outpaces Sun Belt

**Executive Summary:**
• Large multifamily sales jumped 23% to $52.95B in H1 2025
• Midwest markets like Minneapolis (+95%) dramatically outperformed...
```

## 🚨 Important Notes

- **API Key Optional**: System works with fallback templates if no OpenAI key
- **Content Review**: Always review generated content before posting
- **Data Sources**: Update market data regularly for accuracy
- **Compliance**: Includes appropriate disclaimers for financial content

## 🔄 Workflow

1. **Morning Review** (8:30 AM): Check content queue
2. **Daily Generation** (9:00 AM): Create and save content
3. **Manual Review**: Review generated content
4. **Post to LinkedIn**: Copy content to LinkedIn
5. **Track Performance**: Monitor engagement
6. **Weekly Analysis**: Generate long-form article (Tuesdays)

## 🎯 Next Steps

1. **Set up API keys** in `.env` file
2. **Run initial content generation** to test
3. **Review and customize** content style if needed
4. **Start automated scheduler** for daily operation
5. **Monitor and iterate** based on engagement

## 📞 Support

For questions or customizations, refer to the code comments or modify the configuration files to match your specific needs.

---

*This AI agent is designed to maintain Dylan Steman's professional voice while scaling content production for social media growth.*
