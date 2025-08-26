#!/usr/bin/env python3
"""
Simple Flask app for Dylan's Content Generator
Minimal deployment-ready version
"""

from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dylan_content_secret_key_2025'

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html',
                         api_status="Template Mode",
                         linkedin_status="Not Connected", 
                         twitter_status="Not Connected",
                         recent_content=[],
                         posting_stats={'total': 0, 'this_week': 0},
                         queue_status={'total': 0, 'pending': 0, 'posted': 0},
                         scheduler_running=False)

@app.route('/generate')
def generate():
    """Content generation page"""
    return render_template('generate.html', topics=[
        "Interest rate impact on CRE",
        "Midwest multifamily market surge", 
        "Gateway market renaissance",
        "Sun Belt oversupply challenges"
    ])

@app.route('/queue')
def queue():
    """Content queue page"""
    return render_template('queue.html', queued_items=[])

@app.route('/analytics')
def analytics():
    """Analytics page"""
    return render_template('analytics.html',
                         stats_7d={'total': 0},
                         stats_30d={'total': 0},
                         content_stats={'total_generated': 0},
                         recent_activity=[])

@app.route('/settings')
def settings():
    """Settings page"""
    return render_template('settings.html', config={
        'openai_configured': False,
        'linkedin_configured': False,
        'twitter_configured': False,
        'scheduler_running': False
    })

@app.route('/api/generate', methods=['POST'])
def api_generate():
    """Generate sample content"""
    sample_content = """**Interest rates at 5.25% continue reshaping CRE investment strategies.**

Recent market data shows institutional capital increasingly focused on markets with proven fundamentals and construction discipline from previous cycles.

The underlying story: selective deployment is replacing broad-based acquisition strategies as every deal becomes location and story-specific.

For CRE professionals, this environment rewards deep market knowledge and surgical capital allocation over traditional approaches.

What markets are you watching that others might be overlooking?

*Views are my own; not investment advice.*"""
    
    return jsonify({
        'status': 'success',
        'content': sample_content,
        'message': 'Sample content generated successfully'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
