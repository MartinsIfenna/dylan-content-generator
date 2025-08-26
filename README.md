# Dylan Steman AI Content Agent 🚀

🚀 **AI-powered content generation system for commercial real estate professionals**

An intelligent content creation platform that generates professional, data-driven LinkedIn posts and articles focused on CRE markets, multifamily trends, and investment insights.

## ✨ Features

- **🤖 AI Content Generation**: Professional CRE content matching Dylan's voice
- **📊 Real Market Data**: Integration with Federal Reserve, Census Bureau APIs  
- **🕒 Automated Scheduling**: Daily posts, weekly long-form articles
- **📱 Web Dashboard**: Easy-to-use interface for content management
- **🔄 Social Media Integration**: Direct posting to LinkedIn and Twitter
- **📈 Analytics**: Track content performance and engagement
- **⚡ Template Fallbacks**: Works without API keys for testing

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/dylan-content-generator.git
cd dylan-content-generator
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys (optional for demo)
```

### 3. Run the Application
```bash
python web_interface.py
```
Access the dashboard at: **http://localhost:5001**

### 4. Generate Content
```bash
python demo.py  # Generate sample content
```

## 🔧 Configuration

### Environment Variables
```env
# AI Generation (Optional - has fallback templates)
OPENAI_API_KEY=your_openai_api_key

# Social Media (Optional)
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
```

## 📝 Content Types

| Type | Length | Frequency | Focus |
|------|--------|-----------|-------|
| **Short Posts** | 150-200 words | Daily | Market insights, data points |
| **Long Articles** | 800-1200 words | Weekly | Comprehensive analysis |

## 🏢 Market Coverage

- **Midwest**: Chicago, Minneapolis, Milwaukee
- **Gateway**: Boston, NYC, San Francisco  
- **Sun Belt**: Austin, Phoenix, Miami
- **Topics**: Interest rates, capital flows, development, vacancy trends

## 🏗️ Architecture

```
├── dylan_content_agent.py          # Core AI content generation
├── web_interface.py                # Flask web dashboard  
├── automated_content_pipeline.py   # Automation & scheduling
├── social_media_poster.py          # Social platform integration
├── enhanced_market_data_provider.py # Real market data APIs
├── templates/                      # Web interface templates
├── content_queue/                  # Generated content storage
└── static/                         # Web assets
```

## 📊 Data Sources

- **Federal Reserve Economic Data (FRED)**
- **U.S. Census Bureau**
- **Bureau of Labor Statistics** 
- **Industry Market Reports**

## 🚀 Deployment Options

### Heroku
```bash
git push heroku main
```

### Railway
```bash
railway login
railway deploy
```

### Render
Connect your GitHub repo for automatic deployments.

## 📱 Web Interface

The dashboard provides:
- **Content Generation**: Create posts with custom topics
- **Queue Management**: Review content before posting
- **Analytics**: Track performance metrics
- **Settings**: Configure APIs and automation
- **Scheduler**: Automated daily/weekly posting

## 🔒 Security

- Environment variables for API keys
- No hardcoded credentials
- Professional disclaimers included
- Source attribution for all data

## 📄 License

Proprietary and confidential.

## 📁 Project Structure

```
Dylan_Content_Generator/
├── dylan_content_agent.py      # Main AI agent
├── web_interface.py            # Flask web dashboard
├── automated_content_pipeline.py # Automation & scheduling
├── social_media_poster.py      # Social platform integration
├── enhanced_market_data_provider.py # Real market data APIs
├── templates/                  # Web interface templates
├── content_queue/              # Generated content storage
├── static/                     # Web assets
├── requirements.txt            # Python dependencies
├── .env.example               # Configuration template
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
