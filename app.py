from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Dylan's Content Generator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; }
        h1 { color: #2c3e50; text-align: center; }
        .status { background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
        button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Dylan's AI Content Generator</h1>
        <div class="status">
            <h3>✅ System Status: Online</h3>
            <p>Content generator is successfully deployed and running!</p>
        </div>
        <button onclick="generateContent()">Generate Sample Content</button>
        <div id="output" style="margin-top: 20px;"></div>
    </div>
    <script>
        function generateContent() {
            fetch('/generate')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('output').innerHTML = '<pre>' + data.content + '</pre>';
                });
        }
    </script>
</body>
</html>
    '''

@app.route('/generate')
def generate():
    return jsonify({
        'content': '''**Interest rates at 5.25% continue reshaping CRE investment strategies.**

Recent market data shows institutional capital increasingly focused on markets with proven fundamentals and construction discipline from previous cycles.

The underlying story: selective deployment is replacing broad-based acquisition strategies as every deal becomes location and story-specific.

For CRE professionals, this environment rewards deep market knowledge and surgical capital allocation over traditional approaches.

What markets are you watching that others might be overlooking?

*Views are my own; not investment advice.*'''
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)
