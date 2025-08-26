#!/usr/bin/env python3
"""
Dylan's Content Generator - Ultra-minimal Flask app
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Main page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dylan's Content Generator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; }
            .status { background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
            .feature { background: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #007bff; }
            button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
            button:hover { background: #0056b3; }
            .content-box { background: #fff; border: 1px solid #ddd; padding: 20px; margin: 20px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Dylan's AI Content Generator</h1>
            
            <div class="status">
                <h3>✅ System Status: Online</h3>
                <p>Content generator is successfully deployed and running!</p>
            </div>
            
            <div class="feature">
                <h4>📝 Content Generation</h4>
                <p>AI-powered content creation for commercial real estate professionals</p>
                <button onclick="generateContent()">Generate Sample Content</button>
            </div>
            
            <div class="feature">
                <h4>🏢 Market Focus</h4>
                <p>Midwest, Gateway, and Sun Belt markets with data-driven insights</p>
            </div>
            
            <div class="feature">
                <h4>📊 Professional Content</h4>
                <p>LinkedIn posts and articles matching Dylan's authentic voice</p>
            </div>
            
            <div id="content-output" class="content-box" style="display:none;">
                <h4>Generated Content:</h4>
                <div id="generated-text"></div>
            </div>
        </div>
        
        <script>
            function generateContent() {
                fetch('/api/generate', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('generated-text').innerHTML = '<pre>' + data.content + '</pre>';
                        document.getElementById('content-output').style.display = 'block';
                    })
                    .catch(error => {
                        document.getElementById('generated-text').innerHTML = 'Error generating content';
                        document.getElementById('content-output').style.display = 'block';
                    });
            }
        </script>
    </body>
    </html>
    """

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

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Dylan Content Generator'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
