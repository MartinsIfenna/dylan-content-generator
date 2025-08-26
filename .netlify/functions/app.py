#!/usr/bin/env python3
"""
Dylan's AI Content Generator - Netlify Functions Version
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import random
import serverless_wsgi

app = Flask(__name__)
app.secret_key = 'dylan_content_secret_key_2025'

# Content topics for rotation
CONTENT_TOPICS = [
    "Interest rate impact on CRE",
    "Midwest multifamily market surge", 
    "Gateway market renaissance",
    "Sun Belt oversupply challenges",
    "Capital flows and liquidity trends",
    "Development pipeline analysis",
    "Regional market spotlights",
    "Investment strategy shifts",
    "Brokerage market dynamics",
    "Debt markets evolution"
]

# Sample market data
MARKET_DATA = {
    'current_rates': {
        'fed_funds': {'value': '5.25%', 'date': 'Dec 2024'},
        'mortgage_30yr': {'value': '7.1%', 'date': 'Dec 2024'}
    },
    'regional_markets': {
        'midwest': {'chicago': {'vacancy_rate': '4.8%', 'median_rent': '$2,100'}},
        'gateway': {'boston': {'vacancy_rate': '3.2%', 'median_rent': '$3,200'}},
        'sunbelt': {'austin': {'vacancy_rate': '6.1%', 'median_rent': '$1,850'}}
    }
}

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template_string(DASHBOARD_TEMPLATE, 
                                api_status="Online",
                                recent_content=get_recent_content(),
                                queue_status={'total': 3, 'pending': 2, 'posted': 1})

@app.route('/generate', methods=['GET', 'POST'])
def generate_content():
    """Content generation page"""
    if request.method == 'POST':
        content_type = request.form.get('content_type', 'short_post')
        custom_topic = request.form.get('custom_topic', '').strip()
        
        topic = custom_topic if custom_topic else random.choice(CONTENT_TOPICS)
        content = generate_sample_content(topic, content_type)
        
        return render_template_string(CONTENT_PREVIEW_TEMPLATE, 
                                    content=content, 
                                    topic=topic,
                                    content_type=content_type)
    
    return render_template_string(GENERATE_TEMPLATE, topics=CONTENT_TOPICS)

@app.route('/api/generate', methods=['POST', 'GET'])
def api_generate():
    """API endpoint for content generation"""
    if request.method == 'GET':
        topic = random.choice(CONTENT_TOPICS)
        content_type = 'short_post'
    else:
        data = request.get_json() or {}
        topic = data.get('topic', random.choice(CONTENT_TOPICS))
        content_type = data.get('content_type', 'short_post')
    
    content = generate_sample_content(topic, content_type)
    
    return jsonify({
        'status': 'success',
        'content': content,
        'topic': topic,
        'type': content_type,
        'timestamp': datetime.now().isoformat()
    })

def generate_sample_content(topic, content_type='short_post'):
    """Generate sample content based on topic and type"""
    if content_type == 'long_article':
        return f"""# Market Analysis: {topic}

## Executive Summary
- Current market dynamics showing significant shifts in investor behavior
- Institutional capital increasingly selective in deployment strategies
- Regional performance variations creating new opportunities

## Current Market Environment
Interest rates at {MARKET_DATA['current_rates']['fed_funds']['value']} continue to reshape investment strategies across commercial real estate sectors. Recent data from the Federal Reserve shows sustained pressure on acquisition financing, with 30-year mortgage rates at {MARKET_DATA['current_rates']['mortgage_30yr']['value']}.

## Regional Analysis
**Midwest Markets**: Chicago vacancy rates at {MARKET_DATA['regional_markets']['midwest']['chicago']['vacancy_rate']}, demonstrating construction discipline from previous cycles.

**Gateway Markets**: Boston maintaining tight fundamentals with {MARKET_DATA['regional_markets']['gateway']['boston']['vacancy_rate']} vacancy, attracting institutional capital.

**Sun Belt Markets**: Austin experiencing supply pressures with {MARKET_DATA['regional_markets']['sunbelt']['austin']['vacancy_rate']} vacancy as development pipeline creates near-term headwinds.

## Investment Implications
For CRE professionals, this environment rewards:
- Deep market knowledge and local expertise
- Surgical capital allocation over broad-based strategies
- Focus on markets with proven demand fundamentals
- Strategic positioning for the next cycle

## Forward-Looking Perspective
Market participants should monitor:
- Federal Reserve policy signals
- Regional employment trends
- Construction pipeline timing
- Capital market liquidity

What are your thoughts on these market dynamics?

*Views are my own; not investment advice.*

**Sources**: Federal Reserve Economic Data (FRED), U.S. Census Bureau, Industry Research"""
    
    else:  # short_post
        insights = get_topic_insights(topic)
        return f"""**{topic} continues reshaping the multifamily landscape.**

{insights}

The underlying fundamentals tell a compelling story: selective deployment is replacing broad-based strategies as every deal becomes location and story-specific.

For CRE professionals, this environment rewards deep market knowledge and surgical capital allocation over traditional approaches.

What markets are you watching that others might be overlooking?

*Views are my own; not investment advice.*"""

def get_topic_insights(topic):
    """Get relevant insights for a topic"""
    insights_map = {
        "Interest rate impact on CRE": f"Recent market data shows institutional capital increasingly focused on markets with proven fundamentals. Current Fed funds rate at {MARKET_DATA['current_rates']['fed_funds']['value']} driving strategic repositioning.",
        "Midwest multifamily market surge": f"Midwest markets showing resilience with Chicago vacancy at {MARKET_DATA['regional_markets']['midwest']['chicago']['vacancy_rate']}, construction discipline creating supply-demand balance.",
        "Gateway market renaissance": f"Gateway markets remain tight with Boston vacancy at {MARKET_DATA['regional_markets']['gateway']['boston']['vacancy_rate']}, institutional capital gravitating toward established markets.",
        "Sun Belt oversupply challenges": f"Sun Belt facing supply pressures with Austin vacancy at {MARKET_DATA['regional_markets']['sunbelt']['austin']['vacancy_rate']}, development pipeline creating headwinds."
    }
    return insights_map.get(topic, "Market dynamics reflect ongoing regional performance variations and interest rate impacts.")

def get_recent_content():
    """Get recent generated content"""
    return [
        {'title': 'Interest Rate Impact Analysis', 'type': 'Short Post', 'created': '2 hours ago'},
        {'title': 'Midwest Market Surge', 'type': 'Long Article', 'created': '1 day ago'},
        {'title': 'Gateway Renaissance', 'type': 'Short Post', 'created': '2 days ago'}
    ]

# HTML Templates
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Dylan's Content Generator - Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; background: #f8f9fa; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .nav { display: flex; gap: 2rem; margin-top: 1rem; }
        .nav a { color: #ecf0f1; text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; }
        .nav a:hover { background: #34495e; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
        .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .status-online { color: #27ae60; }
        .btn { background: #3498db; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2980b9; }
        .stats { display: flex; justify-content: space-between; margin-top: 1rem; }
        .stat { text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; color: #2c3e50; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Dylan's AI Content Generator</h1>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/generate">Generate</a>
            <a href="/api/generate">API Demo</a>
        </div>
    </div>
    
    <div class="container">
        <div class="grid">
            <div class="card">
                <h3>System Status</h3>
                <p class="status-online">✅ {{ api_status }}</p>
                <p>Content generator is online and ready to create professional CRE content.</p>
                <a href="/generate" class="btn">Generate Content</a>
            </div>
            
            <div class="card">
                <h3>Content Statistics</h3>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">{{ queue_status.total }}</div>
                        <div>Total</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{{ queue_status.pending }}</div>
                        <div>Pending</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{{ queue_status.posted }}</div>
                        <div>Posted</div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>Recent Content</h3>
                {% for item in recent_content %}
                <div style="border-bottom: 1px solid #eee; padding: 0.5rem 0;">
                    <strong>{{ item.title }}</strong><br>
                    <small>{{ item.type }} • {{ item.created }}</small>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
'''

GENERATE_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Generate Content - Dylan's Content Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; background: #f8f9fa; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .nav { display: flex; gap: 2rem; margin-top: 1rem; }
        .nav a { color: #ecf0f1; text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; }
        .nav a:hover { background: #34495e; }
        .container { max-width: 800px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .form-group { margin-bottom: 1.5rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
        select, input, textarea { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; }
        .btn { background: #27ae60; color: white; padding: 0.75rem 2rem; border: none; border-radius: 4px; cursor: pointer; font-size: 1rem; }
        .btn:hover { background: #229954; }
        .topic-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem; }
        .topic-btn { background: #ecf0f1; border: 1px solid #bdc3c7; padding: 0.5rem; border-radius: 4px; cursor: pointer; text-align: center; }
        .topic-btn:hover { background: #d5dbdb; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Dylan's AI Content Generator</h1>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/generate">Generate</a>
            <a href="/api/generate">API Demo</a>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>Generate New Content</h2>
            
            <form method="POST">
                <div class="form-group">
                    <label for="content_type">Content Type</label>
                    <select name="content_type" id="content_type">
                        <option value="short_post">Short LinkedIn Post (150-200 words)</option>
                        <option value="long_article">Long-form Article (800-1200 words)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="custom_topic">Custom Topic (optional)</label>
                    <input type="text" name="custom_topic" id="custom_topic" placeholder="Enter a specific topic or leave blank for random selection">
                </div>
                
                <div class="form-group">
                    <label>Suggested Topics</label>
                    <div class="topic-grid">
                        {% for topic in topics %}
                        <div class="topic-btn" onclick="document.getElementById('custom_topic').value='{{ topic }}'">
                            {{ topic }}
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <button type="submit" class="btn">Generate Content</button>
            </form>
        </div>
    </div>
</body>
</html>
'''

CONTENT_PREVIEW_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Content Preview - Dylan's Content Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; background: #f8f9fa; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .nav { display: flex; gap: 2rem; margin-top: 1rem; }
        .nav a { color: #ecf0f1; text-decoration: none; padding: 0.5rem 1rem; border-radius: 4px; }
        .nav a:hover { background: #34495e; }
        .container { max-width: 800px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .content-preview { background: #f8f9fa; padding: 2rem; border-radius: 8px; border-left: 4px solid #3498db; white-space: pre-wrap; line-height: 1.6; }
        .btn { background: #3498db; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; margin-right: 1rem; }
        .btn:hover { background: #2980b9; }
        .btn-success { background: #27ae60; }
        .btn-success:hover { background: #229954; }
        .meta { color: #7f8c8d; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Dylan's AI Content Generator</h1>
        <div class="nav">
            <a href="/">Dashboard</a>
            <a href="/generate">Generate</a>
            <a href="/api/generate">API Demo</a>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>Content Preview</h2>
            <div class="meta">
                <strong>Topic:</strong> {{ topic }}<br>
                <strong>Type:</strong> {{ content_type.replace('_', ' ').title() }}<br>
                <strong>Generated:</strong> Just now
            </div>
            
            <div class="content-preview">{{ content }}</div>
            
            <div style="margin-top: 2rem;">
                <a href="/generate" class="btn">Generate Another</a>
                <a href="/" class="btn btn-success">Back to Dashboard</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

def render_template_string(template, **context):
    """Simple template rendering"""
    for key, value in context.items():
        if isinstance(value, list):
            # Handle list rendering
            list_html = ""
            for item in value:
                if isinstance(item, dict):
                    list_html += f"<div>{item}</div>"
            template = template.replace(f"{{{{ {key} }}}}", list_html)
        else:
            template = template.replace(f"{{{{ {key} }}}}", str(value))
    
    # Handle loops
    import re
    for_pattern = r'{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%}(.*?){%\s*endfor\s*%}'
    
    def replace_for_loop(match):
        item_var, list_var, loop_content = match.groups()
        if list_var in context and isinstance(context[list_var], list):
            result = ""
            for item in context[list_var]:
                item_content = loop_content
                if isinstance(item, dict):
                    for k, v in item.items():
                        item_content = item_content.replace(f"{{{{ {item_var}.{k} }}}}", str(v))
                result += item_content
            return result
        return ""
    
    template = re.sub(for_pattern, replace_for_loop, template, flags=re.DOTALL)
    
    # Handle conditionals
    if_pattern = r'{%\s*if\s+.*?%}(.*?){%\s*else\s*%}(.*?){%\s*endif\s*%}'
    template = re.sub(if_pattern, r'\2', template, flags=re.DOTALL)
    
    if_pattern = r'{%\s*if\s+.*?%}(.*?){%\s*endif\s*%}'
    template = re.sub(if_pattern, r'\1', template, flags=re.DOTALL)
    
    return template

def handler(event, context):
    """Netlify Functions handler"""
    return serverless_wsgi.handle_request(app, event, context)
