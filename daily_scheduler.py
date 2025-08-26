#!/usr/bin/env python3
"""
Daily Content Scheduler for Dylan Steman
Automated daily content generation and posting
"""

import schedule
import time
import os
from datetime import datetime
from dylan_content_agent import DylanContentAgent
from pathlib import Path
import json

class ContentScheduler:
    """Handles automated daily content generation and scheduling"""
    
    def __init__(self):
        self.agent = DylanContentAgent()
        self.schedule_config = self.load_schedule_config()
        
    def load_schedule_config(self):
        """Load scheduling configuration"""
        return {
            'daily_post_time': '09:00',  # 9 AM daily
            'weekly_article_day': 'tuesday',  # Tuesday for long-form
            'weekend_prep_day': 'friday',  # Friday prep for weekend
            'content_review_time': '08:30',  # 30 min before posting
        }
    
    def generate_and_save_daily_content(self):
        """Generate and save daily content"""
        try:
            print(f"🤖 Generating daily content - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Determine content type based on day
            today = datetime.now().strftime('%A').lower()
            
            if today == self.schedule_config['weekly_article_day']:
                content_type = 'long_article'
                print("📄 Generating weekly long-form article")
            else:
                content_type = 'short_post'
                print("📝 Generating daily short post")
            
            # Generate content
            content = self.agent.generate_daily_content(content_type)
            
            # Save with timestamp
            timestamp = datetime.now().strftime("%Y%m%d")
            filename = f"{timestamp}_{content_type}_dylan.md"
            
            filepath = self.agent.save_content(content, filename)
            
            # Log generation
            self.log_generation(content, filepath)
            
            print(f"✅ Content generated and saved: {filepath}")
            
        except Exception as e:
            print(f"❌ Error generating daily content: {e}")
            self.log_error(str(e))
    
    def prepare_weekend_content(self):
        """Prepare content for weekend posting"""
        print("📅 Preparing weekend content batch...")
        
        try:
            # Generate Saturday content
            saturday_content = self.agent.generate_daily_content('short_post')
            sat_filename = f"{datetime.now().strftime('%Y%m%d')}_saturday_dylan.md"
            self.agent.save_content(saturday_content, sat_filename)
            
            # Generate Sunday content  
            sunday_content = self.agent.generate_daily_content('short_post')
            sun_filename = f"{datetime.now().strftime('%Y%m%d')}_sunday_dylan.md"
            self.agent.save_content(sunday_content, sun_filename)
            
            print("✅ Weekend content prepared")
            
        except Exception as e:
            print(f"❌ Error preparing weekend content: {e}")
    
    def review_content_queue(self):
        """Review upcoming content for quality"""
        print("🔍 Reviewing content queue...")
        
        content_dir = Path(__file__).parent / "generated_content"
        if content_dir.exists():
            today_files = [f for f in content_dir.glob("*.md") 
                          if datetime.now().strftime("%Y%m%d") in f.name]
            
            print(f"📋 Found {len(today_files)} content pieces for today")
            for file in today_files:
                print(f"   - {file.name}")
        else:
            print("📂 No content directory found")
    
    def log_generation(self, content, filepath):
        """Log content generation for tracking"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'content_type': content.content_type,
            'title': content.title,
            'topics': content.topics,
            'filepath': str(filepath),
            'word_count': len(content.content.split())
        }
        
        log_file = log_dir / f"content_log_{datetime.now().strftime('%Y%m')}.json"
        
        # Append to monthly log
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def log_error(self, error_msg):
        """Log errors for debugging"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        error_log = log_dir / "errors.log"
        
        with open(error_log, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - ERROR: {error_msg}\n")
    
    def setup_schedule(self):
        """Setup the automated schedule"""
        print("⏰ Setting up content generation schedule...")
        
        # Daily content generation
        schedule.every().day.at(self.schedule_config['daily_post_time']).do(
            self.generate_and_save_daily_content
        )
        
        # Content review before posting
        schedule.every().day.at(self.schedule_config['content_review_time']).do(
            self.review_content_queue
        )
        
        # Weekend content preparation
        schedule.every().friday.at("17:00").do(
            self.prepare_weekend_content
        )
        
        print("✅ Schedule configured:")
        print(f"   📝 Daily content: {self.schedule_config['daily_post_time']}")
        print(f"   🔍 Content review: {self.schedule_config['content_review_time']}")
        print(f"   📅 Weekend prep: Friday 17:00")
        
    def run_scheduler(self):
        """Run the scheduler continuously"""
        print("🚀 Dylan Content Scheduler Started")
        print("=" * 50)
        
        self.setup_schedule()
        
        print("\n⏳ Waiting for scheduled tasks...")
        print("   Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\n👋 Scheduler stopped by user")
        except Exception as e:
            print(f"\n❌ Scheduler error: {e}")
            self.log_error(f"Scheduler error: {e}")

def main():
    """Main function"""
    scheduler = ContentScheduler()
    
    print("Dylan Content Scheduler")
    print("=" * 30)
    print("1. Run scheduler (continuous)")
    print("2. Generate content now")
    print("3. Prepare weekend content")
    print("4. Review content queue")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == '1':
        scheduler.run_scheduler()
    elif choice == '2':
        scheduler.generate_and_save_daily_content()
    elif choice == '3':
        scheduler.prepare_weekend_content()
    elif choice == '4':
        scheduler.review_content_queue()
    elif choice == '5':
        print("👋 Goodbye!")
    else:
        print("❌ Invalid option")

if __name__ == "__main__":
    main()
