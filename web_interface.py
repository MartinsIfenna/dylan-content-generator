#!/usr/bin/env python3
"""
Web Interface for Dylan's AI Content Agent
Easy-to-use dashboard for content generation and management
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
from dylan_content_agent import DylanContentAgent
from social_media_poster import SocialMediaPoster
from automated_content_pipeline import AutomatedContentPipeline
import threading
import schedule
import time

app = Flask(__name__)
app.secret_key = 'dylan_content_secret_key_2025'

# Initialize components
content_agent = DylanContentAgent()
social_poster = SocialMediaPoster()
pipeline = AutomatedContentPipeline()

# Global scheduler thread
scheduler_thread = None
scheduler_running = False

@app.route('/')
def dashboard():
    """Main dashboard"""
    # Get system status
    api_status = "Connected" if content_agent.openai_client else "Template Mode"
    linkedin_status = "Connected" if social_poster.linkedin_token else "Not Connected"
    twitter_status = "Connected" if all(social_poster.twitter_credentials.values()) else "Not Connected"
    
    # Get recent content
    recent_content = get_recent_content(5)
    
    # Get posting stats
    posting_stats = social_poster.get_posting_stats(30)
    
    # Get queue status
    queue_status = get_queue_status()
    
    return render_template('dashboard.html',
                         api_status=api_status,
                         linkedin_status=linkedin_status,
                         twitter_status=twitter_status,
                         recent_content=recent_content,
                         posting_stats=posting_stats,
                         queue_status=queue_status,
                         scheduler_running=scheduler_running)

@app.route('/generate', methods=['GET', 'POST'])
def generate_content():
    """Content generation page"""
    if request.method == 'POST':
        content_type = request.form.get('content_type', 'short_post')
        custom_topic = request.form.get('custom_topic', '').strip()
        
        try:
            if custom_topic:
                # Add custom topic temporarily
                content_agent.content_topics.append(custom_topic)
            
            content = content_agent.generate_daily_content(content_type)
            
            # Save to queue
            filepath = pipeline.generate_and_queue_content(content_type)
            
            flash(f'✅ {content_type.replace("_", " ").title()} generated successfully!', 'success')
            
            return render_template('content_preview.html', 
                                 content=content, 
                                 filepath=filepath)
            
        except Exception as e:
            flash(f'❌ Error generating content: {str(e)}', 'error')
    
    return render_template('generate.html', 
                         topics=content_agent.content_topics)

@app.route('/queue')
def content_queue():
    """Content queue management"""
    queue_dir = Path(__file__).parent / "content_queue"
    queued_items = []
    
    if queue_dir.exists():
        for file in queue_dir.glob("*_queue.md"):
            with open(file, 'r') as f:
                content = f.read()
            
            # Parse metadata
            item = parse_content_metadata(content, file)
            queued_items.append(item)
    
    # Sort by creation date (newest first)
    queued_items.sort(key=lambda x: x['created'], reverse=True)
    
    return render_template('queue.html', queued_items=queued_items)

@app.route('/post/<filename>')
def post_content(filename):
    """Post content to social media"""
    queue_dir = Path(__file__).parent / "content_queue"
    filepath = queue_dir / filename
    
    if not filepath.exists():
        flash('❌ Content file not found', 'error')
        return redirect(url_for('content_queue'))
    
    platforms = request.args.getlist('platform') or ['linkedin']
    
    try:
        results = pipeline.post_queued_content(str(filepath), platforms)
        
        success_count = sum(1 for r in results.values() if r.success)
        total_count = len(results)
        
        if success_count == total_count:
            flash(f'✅ Posted to all {total_count} platforms successfully!', 'success')
        elif success_count > 0:
            flash(f'⚠️ Posted to {success_count}/{total_count} platforms', 'warning')
        else:
            flash('❌ Failed to post to any platforms', 'error')
        
        # Show detailed results
        for platform, result in results.items():
            if result.success:
                flash(f'✅ {platform.title()}: Posted successfully', 'success')
            else:
                flash(f'❌ {platform.title()}: {result.error_message}', 'error')
    
    except Exception as e:
        flash(f'❌ Error posting content: {str(e)}', 'error')
    
    return redirect(url_for('content_queue'))

@app.route('/preview/<filename>')
def preview_content(filename):
    """Preview a specific content file"""
    try:
        # Try content_queue first, then generated_content
        queue_path = os.path.join('content_queue', filename)
        generated_path = os.path.join('generated_content', filename)
        
        filepath = None
        if os.path.exists(queue_path):
            filepath = queue_path
        elif os.path.exists(generated_path):
            filepath = generated_path
        
        if not filepath:
            flash('Content file not found', 'error')
            return redirect(url_for('dashboard'))
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse content metadata
        lines = content.split('\n')
        title = lines[0].replace('#', '').strip() if lines else 'Untitled'
        
        item = {
            'title': title,
            'preview': content,
            'type': 'long_article' if 'Market Analysis' in title else 'short_post',
            'word_count': len(content.split()),
            'topics': 'CRE Analysis',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'status': 'queued' if 'content_queue' in filepath else 'generated'
        }
        
        return render_template('content_preview.html', item=item, filename=filename)
    except Exception as e:
        flash(f'Error loading content: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/analytics')
def analytics():
    """Analytics and reporting"""
    # Get posting statistics
    stats_7d = social_poster.get_posting_stats(7)
    stats_30d = social_poster.get_posting_stats(30)
    
    # Get content generation stats
    content_stats = get_content_generation_stats()
    
    # Get recent activity
    recent_activity = get_recent_activity(20)
    
    return render_template('analytics.html',
                         stats_7d=stats_7d,
                         stats_30d=stats_30d,
                         content_stats=content_stats,
                         recent_activity=recent_activity)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """Settings and configuration"""
    if request.method == 'POST':
        # Handle settings updates
        action = request.form.get('action')
        
        if action == 'update_schedule':
            # Update scheduling settings
            flash('⚠️ Schedule settings updated (requires restart)', 'warning')
        elif action == 'test_apis':
            # Test API connections
            results = test_api_connections()
            for result in results:
                flash(result, 'info')
    
    # Get current configuration
    config = {
        'openai_configured': bool(content_agent.openai_client),
        'linkedin_configured': bool(social_poster.linkedin_token),
        'twitter_configured': all(social_poster.twitter_credentials.values()),
        'scheduler_running': scheduler_running,
        'auto_post_enabled': pipeline.pipeline_config['auto_post'],
        'review_required': pipeline.pipeline_config['review_required']
    }
    
    return render_template('settings.html', config=config)

@app.route('/api/start_scheduler', methods=['POST'])
def start_scheduler():
    """Start the automated scheduler"""
    global scheduler_thread, scheduler_running
    
    if not scheduler_running:
        scheduler_running = True
        scheduler_thread = threading.Thread(target=run_scheduler_background)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        return jsonify({'status': 'started', 'message': 'Scheduler started successfully'})
    else:
        return jsonify({'status': 'already_running', 'message': 'Scheduler is already running'})

@app.route('/api/stop_scheduler', methods=['POST'])
def stop_scheduler():
    """Stop the automated scheduler"""
    global scheduler_running
    
    scheduler_running = False
    schedule.clear()
    return jsonify({'status': 'stopped', 'message': 'Scheduler stopped'})

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors"""
    return '', 204

@app.route('/api/generate_now', methods=['POST'])
def api_generate_now():
    """API endpoint to generate content immediately"""
    try:
        content_type = request.json.get('content_type', 'short_post')
        filepath = pipeline.generate_and_queue_content(content_type)
        
        return jsonify({
            'status': 'success',
            'message': f'{content_type.replace("_", " ").title()} generated successfully',
            'filepath': filepath
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def run_scheduler_background():
    """Run scheduler in background thread"""
    pipeline.setup_automated_schedule()
    
    while scheduler_running:
        schedule.run_pending()
        time.sleep(60)

def get_recent_content(limit=10):
    """Get recent generated content"""
    content_dir = Path(__file__).parent / "generated_content"
    queue_dir = Path(__file__).parent / "content_queue"
    
    files = []
    
    # Get from both directories
    for directory in [content_dir, queue_dir]:
        if directory.exists():
            files.extend(directory.glob("*.md"))
    
    # Sort by modification time
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    recent = []
    for file in files[:limit]:
        try:
            with open(file, 'r') as f:
                content = f.read()
            
            item = parse_content_metadata(content, file)
            recent.append(item)
        except:
            continue
    
    return recent

def get_queue_status():
    """Get content queue status"""
    queue_dir = Path(__file__).parent / "content_queue"
    
    if not queue_dir.exists():
        return {'total': 0, 'pending': 0, 'posted': 0}
    
    files = list(queue_dir.glob("*_queue.md"))
    
    pending = 0
    posted = 0
    
    for file in files:
        try:
            with open(file, 'r') as f:
                content = f.read()
            
            if '**Status:** queued' in content:
                pending += 1
            elif '**Status:** posted' in content:
                posted += 1
        except:
            continue
    
    return {
        'total': len(files),
        'pending': pending,
        'posted': posted
    }

def parse_content_metadata(content, filepath):
    """Parse content metadata from file"""
    lines = content.split('\n')
    
    item = {
        'filename': filepath.name,
        'filepath': str(filepath),
        'title': '',
        'type': '',
        'created': '',
        'status': 'queued',
        'topics': '',
        'preview': '',
        'word_count': 0
    }
    
    # Extract title from first line or filename
    if lines and lines[0].startswith('#'):
        item['title'] = lines[0].replace('#', '').strip()
    else:
        # Extract from filename
        name_parts = filepath.stem.replace('_', ' ').split()
        if 'long' in name_parts:
            item['title'] = ' '.join(name_parts[2:]).title()  # Skip 'day_X_long'
            item['type'] = 'Long Article'
        elif 'short' in name_parts:
            item['title'] = ' '.join(name_parts[2:]).title()  # Skip 'day_X_short'
            item['type'] = 'Short Post'
        else:
            item['title'] = filepath.stem.replace('_', ' ').title()
    
    # Determine type from content or filename
    if not item['type']:
        if 'Market Analysis' in content or 'long' in filepath.name:
            item['type'] = 'Long Article'
        else:
            item['type'] = 'Short Post'
    
    # Set creation time from file stats
    try:
        item['created'] = datetime.fromtimestamp(filepath.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
    except:
        item['created'] = 'Recently'
    
    # Parse structured metadata if present
    for line in lines:
        if line.startswith('**Type:**'):
            item['type'] = line.split('**Type:**')[1].strip()
        elif line.startswith('**Created:**'):
            item['created'] = line.split('**Created:**')[1].strip()
        elif line.startswith('**Status:**'):
            item['status'] = line.split('**Status:**')[1].strip()
        elif line.startswith('**Topics:**'):
            item['topics'] = line.split('**Topics:**')[1].strip()
    
    # Get content preview - clean and format for display
    content_started = False
    content_lines = []
    
    for line in lines:
        if line.strip() == "---" and not content_started:
            content_started = True
            continue
        elif content_started:
            # Skip empty lines at start
            if not content_lines and not line.strip():
                continue
            # Clean markdown formatting for preview
            clean_line = line.replace('**', '').replace('*', '').replace('#', '').strip()
            if clean_line:
                content_lines.append(clean_line)
    
    full_content = ' '.join(content_lines).strip()
    
    # Create a clean preview (first 150 chars for dashboard)
    if len(full_content) > 150:
        preview_text = full_content[:150].rsplit(' ', 1)[0] + "..."
    else:
        preview_text = full_content
    
    item['preview'] = preview_text
    item['full_content'] = '\n'.join(content_lines).strip()  # Keep full content for preview page
    item['word_count'] = len(full_content.split())
    
    return item

def get_content_generation_stats():
    """Get content generation statistics"""
    # This would analyze logs for generation stats
    return {
        'total_generated': 0,
        'this_week': 0,
        'success_rate': 100
    }

def get_recent_activity(limit=20):
    """Get recent system activity"""
    # This would parse logs for recent activity
    return []

def test_api_connections():
    """Test API connections"""
    results = []
    
    if content_agent.openai_client:
        results.append("✅ OpenAI API: Connected")
    else:
        results.append("⚠️ OpenAI API: Not configured (using template mode)")
    
    if social_poster.linkedin_token:
        results.append("✅ LinkedIn API: Connected")
    else:
        results.append("❌ LinkedIn API: Not configured")
    
    if all(social_poster.twitter_credentials.values()):
        results.append("✅ Twitter API: Connected")
    else:
        results.append("❌ Twitter API: Not configured")
    
    return results

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path(__file__).parent / "templates"
    templates_dir.mkdir(exist_ok=True)
    
    print("🚀 Starting Dylan's Content Management Dashboard")
    print("=" * 50)
    print("📱 Access the web interface at: http://localhost:5002")
    print("🔧 Configure API keys in the Settings page")
    print("📝 Generate and manage content through the web interface")
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5002)
