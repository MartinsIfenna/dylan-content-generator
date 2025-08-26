#!/usr/bin/env python3
"""
Automated Content Pipeline for Dylan Steman
Complete end-to-end content generation and posting system
"""

import os
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
from dylan_content_agent import DylanContentAgent
from social_media_poster import SocialMediaPoster
import json

class AutomatedContentPipeline:
    """Complete automated content pipeline"""
    
    def __init__(self):
        self.content_agent = DylanContentAgent()
        self.social_poster = SocialMediaPoster()
        self.pipeline_config = self.load_pipeline_config()
        
    def load_pipeline_config(self):
        """Load pipeline configuration"""
        return {
            'auto_post': False,  # Set to True to enable automatic posting
            'review_required': True,  # Require manual review before posting
            'platforms': ['linkedin'],  # Default platforms
            'daily_schedule': {
                'content_generation': '08:00',
                'content_review': '08:30',
                'posting_time': '09:00'
            },
            'weekly_schedule': {
                'long_article_day': 'tuesday',
                'weekend_prep': 'friday'
            }
        }
    
    def generate_and_queue_content(self, content_type: str = 'auto') -> str:
        """Generate content and queue for posting"""
        try:
            # Determine content type
            if content_type == 'auto':
                today = datetime.now().strftime('%A').lower()
                if today == self.pipeline_config['weekly_schedule']['long_article_day']:
                    content_type = 'long_article'
                else:
                    content_type = 'short_post'
            
            print(f"🤖 Generating {content_type} for {datetime.now().strftime('%Y-%m-%d')}")
            
            # Generate content
            content = self.content_agent.generate_daily_content(content_type)
            
            # Save to queue directory
            queue_dir = Path(__file__).parent / "content_queue"
            queue_dir.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{content_type}_queue.md"
            filepath = queue_dir / filename
            
            # Save content with posting metadata
            with open(filepath, 'w') as f:
                f.write(f"# {content.title}\n\n")
                f.write(f"**Type:** {content.content_type}\n")
                f.write(f"**Created:** {content.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Topics:** {', '.join(content.topics)}\n")
                f.write(f"**Status:** queued\n")
                f.write(f"**Platforms:** {', '.join(self.pipeline_config['platforms'])}\n")
                f.write(f"**Auto-post:** {self.pipeline_config['auto_post']}\n\n")
                f.write("---\n\n")
                f.write(content.content)
            
            print(f"✅ Content queued: {filepath}")
            
            # Log generation
            self.log_pipeline_event('content_generated', {
                'filepath': str(filepath),
                'content_type': content_type,
                'title': content.title
            })
            
            return str(filepath)
            
        except Exception as e:
            error_msg = f"Error generating content: {str(e)}"
            print(f"❌ {error_msg}")
            self.log_pipeline_event('generation_error', {'error': error_msg})
            return ""
    
    def review_queued_content(self) -> list:
        """Review content in the queue"""
        queue_dir = Path(__file__).parent / "content_queue"
        
        if not queue_dir.exists():
            print("📂 No content queue found")
            return []
        
        queued_files = list(queue_dir.glob("*_queue.md"))
        
        if not queued_files:
            print("📭 No content in queue")
            return []
        
        print(f"📋 Found {len(queued_files)} items in content queue:")
        
        for i, file in enumerate(queued_files, 1):
            # Read metadata
            with open(file, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            title = ""
            created = ""
            status = ""
            
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                elif line.startswith('**Created:**'):
                    created = line.split('**Created:**')[1].strip()
                elif line.startswith('**Status:**'):
                    status = line.split('**Status:**')[1].strip()
            
            print(f"   {i}. {title}")
            print(f"      Created: {created} | Status: {status}")
            print(f"      File: {file.name}")
        
        return queued_files
    
    def post_queued_content(self, filepath: str, platforms: list = None) -> dict:
        """Post content from queue to social media"""
        if platforms is None:
            platforms = self.pipeline_config['platforms']
        
        try:
            print(f"📤 Posting content: {Path(filepath).name}")
            
            # Post to platforms
            results = self.social_poster.post_content_file(filepath, platforms)
            
            # Update file status
            self.update_content_status(filepath, 'posted', results)
            
            # Log posting
            self.log_pipeline_event('content_posted', {
                'filepath': filepath,
                'platforms': platforms,
                'results': {p: r.success for p, r in results.items()}
            })
            
            return results
            
        except Exception as e:
            error_msg = f"Error posting content: {str(e)}"
            print(f"❌ {error_msg}")
            self.log_pipeline_event('posting_error', {
                'filepath': filepath,
                'error': error_msg
            })
            return {}
    
    def update_content_status(self, filepath: str, status: str, results: dict = None):
        """Update the status of content in queue"""
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Update status line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('**Status:**'):
                    lines[i] = f"**Status:** {status}"
                    if results:
                        lines.insert(i+1, f"**Posted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        for platform, result in results.items():
                            status_emoji = "✅" if result.success else "❌"
                            lines.insert(i+2, f"**{platform.title()}:** {status_emoji} {result.post_id or result.error_message}")
                    break
            
            with open(filepath, 'w') as f:
                f.write('\n'.join(lines))
                
        except Exception as e:
            print(f"⚠️  Error updating status: {e}")
    
    def automated_daily_workflow(self):
        """Run the complete automated daily workflow"""
        print(f"🚀 Running automated daily workflow - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Step 1: Generate content
            filepath = self.generate_and_queue_content()
            
            if not filepath:
                print("❌ Content generation failed, stopping workflow")
                return
            
            # Step 2: Auto-post if enabled, otherwise queue for review
            if self.pipeline_config['auto_post'] and not self.pipeline_config['review_required']:
                print("📤 Auto-posting enabled, posting immediately...")
                results = self.post_queued_content(filepath)
                
                success_count = sum(1 for r in results.values() if r.success)
                total_count = len(results)
                
                print(f"📊 Posted to {success_count}/{total_count} platforms successfully")
                
            else:
                print("📋 Content queued for manual review and posting")
                print(f"   Review content: {filepath}")
                print(f"   Use 'python automated_content_pipeline.py' to review and post")
            
            self.log_pipeline_event('daily_workflow_complete', {
                'filepath': filepath,
                'auto_posted': self.pipeline_config['auto_post']
            })
            
        except Exception as e:
            error_msg = f"Daily workflow error: {str(e)}"
            print(f"❌ {error_msg}")
            self.log_pipeline_event('workflow_error', {'error': error_msg})
    
    def log_pipeline_event(self, event_type: str, data: dict):
        """Log pipeline events for monitoring"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        
        log_file = log_dir / f"pipeline_log_{datetime.now().strftime('%Y%m')}.json"
        
        # Append to monthly log
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)
    
    def setup_automated_schedule(self):
        """Setup automated scheduling"""
        print("⏰ Setting up automated content pipeline...")
        
        # Daily content generation
        schedule.every().day.at(self.pipeline_config['daily_schedule']['content_generation']).do(
            self.automated_daily_workflow
        )
        
        print("✅ Automated schedule configured:")
        print(f"   📝 Daily workflow: {self.pipeline_config['daily_schedule']['content_generation']}")
        print(f"   🤖 Auto-post: {'Enabled' if self.pipeline_config['auto_post'] else 'Disabled'}")
        print(f"   👀 Review required: {'Yes' if self.pipeline_config['review_required'] else 'No'}")
    
    def run_scheduler(self):
        """Run the automated scheduler"""
        print("🚀 Dylan Automated Content Pipeline")
        print("=" * 50)
        
        self.setup_automated_schedule()
        
        print("\n⏳ Scheduler running... Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n👋 Pipeline scheduler stopped")

def main():
    """Main interactive interface"""
    pipeline = AutomatedContentPipeline()
    
    print("🚀 Dylan Automated Content Pipeline")
    print("=" * 50)
    
    while True:
        print("\nPipeline Options:")
        print("1. Generate content now")
        print("2. Review queued content")
        print("3. Post queued content")
        print("4. Run daily workflow")
        print("5. Start automated scheduler")
        print("6. Configure pipeline")
        print("7. View pipeline logs")
        print("8. Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            content_type = input("Content type (short_post/long_article/auto): ").strip() or 'auto'
            filepath = pipeline.generate_and_queue_content(content_type)
            if filepath:
                print(f"✅ Content generated and queued: {Path(filepath).name}")
        
        elif choice == '2':
            queued_files = pipeline.review_queued_content()
            
        elif choice == '3':
            queued_files = pipeline.review_queued_content()
            if queued_files:
                try:
                    file_num = int(input(f"\nSelect file to post (1-{len(queued_files)}): "))
                    if 1 <= file_num <= len(queued_files):
                        filepath = str(queued_files[file_num - 1])
                        platforms = input("Platforms (linkedin,twitter) [default: linkedin]: ").strip()
                        platforms = platforms.split(',') if platforms else ['linkedin']
                        platforms = [p.strip() for p in platforms]
                        
                        results = pipeline.post_queued_content(filepath, platforms)
                        
                        for platform, result in results.items():
                            if result.success:
                                print(f"✅ {platform}: Posted successfully!")
                            else:
                                print(f"❌ {platform}: {result.error_message}")
                    else:
                        print("❌ Invalid file number")
                except ValueError:
                    print("❌ Invalid input")
        
        elif choice == '4':
            pipeline.automated_daily_workflow()
        
        elif choice == '5':
            pipeline.run_scheduler()
        
        elif choice == '6':
            print("\n⚙️  Current Configuration:")
            print(f"   Auto-post: {pipeline.pipeline_config['auto_post']}")
            print(f"   Review required: {pipeline.pipeline_config['review_required']}")
            print(f"   Platforms: {', '.join(pipeline.pipeline_config['platforms'])}")
            print(f"   Daily generation: {pipeline.pipeline_config['daily_schedule']['content_generation']}")
            
            print("\nConfiguration changes require editing automated_content_pipeline.py")
        
        elif choice == '7':
            log_dir = Path(__file__).parent / "logs"
            if log_dir.exists():
                log_files = list(log_dir.glob("pipeline_log_*.json"))
                if log_files:
                    latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
                    print(f"\n📋 Latest pipeline log: {latest_log.name}")
                    
                    with open(latest_log, 'r') as f:
                        logs = json.load(f)
                    
                    print(f"   Total events: {len(logs)}")
                    
                    # Show recent events
                    recent_logs = logs[-5:] if len(logs) > 5 else logs
                    print("\n   Recent events:")
                    for log in recent_logs:
                        timestamp = log['timestamp'][:19].replace('T', ' ')
                        print(f"     {timestamp} - {log['event_type']}")
                else:
                    print("📭 No pipeline logs found")
            else:
                print("📂 No logs directory found")
        
        elif choice == '8':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()
