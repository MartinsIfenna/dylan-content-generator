#!/usr/bin/env python3
"""
Social Media Posting Module for Dylan's Content Agent
Handles automated posting to LinkedIn, Twitter, and other platforms
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import requests
from dataclasses import dataclass

@dataclass
class PostResult:
    """Result of a social media post"""
    platform: str
    success: bool
    post_id: Optional[str] = None
    error_message: Optional[str] = None
    posted_at: Optional[datetime] = None

class SocialMediaPoster:
    """Handles posting content to various social media platforms"""
    
    def __init__(self):
        self.linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.twitter_credentials = {
            'api_key': os.getenv('TWITTER_API_KEY'),
            'api_secret': os.getenv('TWITTER_API_SECRET'),
            'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
            'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        }
        
        self.posting_log = []
        self.load_posting_history()
    
    def load_posting_history(self):
        """Load previous posting history"""
        log_file = Path(__file__).parent / "logs" / "posting_history.json"
        if log_file.exists():
            with open(log_file, 'r') as f:
                self.posting_log = json.load(f)
    
    def save_posting_history(self):
        """Save posting history to file"""
        log_dir = Path(__file__).parent / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / "posting_history.json"
        with open(log_file, 'w') as f:
            json.dump(self.posting_log, f, indent=2, default=str)
    
    def post_to_linkedin(self, content: str, title: str = "") -> PostResult:
        """Post content to LinkedIn"""
        if not self.linkedin_token:
            return PostResult(
                platform="linkedin",
                success=False,
                error_message="LinkedIn access token not configured"
            )
        
        try:
            # LinkedIn API v2 posting
            headers = {
                'Authorization': f'Bearer {self.linkedin_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            
            # Get user profile ID first
            profile_response = requests.get(
                'https://api.linkedin.com/v2/people/~',
                headers=headers
            )
            
            if profile_response.status_code != 200:
                return PostResult(
                    platform="linkedin",
                    success=False,
                    error_message=f"Failed to get LinkedIn profile: {profile_response.text}"
                )
            
            profile_id = profile_response.json()['id']
            
            # Create post
            post_data = {
                "author": f"urn:li:person:{profile_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 201:
                post_id = response.json().get('id')
                result = PostResult(
                    platform="linkedin",
                    success=True,
                    post_id=post_id,
                    posted_at=datetime.now()
                )
            else:
                result = PostResult(
                    platform="linkedin",
                    success=False,
                    error_message=f"LinkedIn API error: {response.text}"
                )
            
            self.log_post_attempt(result, content, title)
            return result
            
        except Exception as e:
            result = PostResult(
                platform="linkedin",
                success=False,
                error_message=f"Exception posting to LinkedIn: {str(e)}"
            )
            self.log_post_attempt(result, content, title)
            return result
    
    def post_to_twitter(self, content: str) -> PostResult:
        """Post content to Twitter/X"""
        try:
            import tweepy
            
            if not all(self.twitter_credentials.values()):
                return PostResult(
                    platform="twitter",
                    success=False,
                    error_message="Twitter credentials not fully configured"
                )
            
            # Initialize Twitter API
            auth = tweepy.OAuthHandler(
                self.twitter_credentials['api_key'],
                self.twitter_credentials['api_secret']
            )
            auth.set_access_token(
                self.twitter_credentials['access_token'],
                self.twitter_credentials['access_token_secret']
            )
            
            api = tweepy.API(auth)
            
            # Twitter has character limits, so truncate if needed
            max_length = 280
            if len(content) > max_length:
                content = content[:max_length-3] + "..."
            
            # Post tweet
            tweet = api.update_status(content)
            
            result = PostResult(
                platform="twitter",
                success=True,
                post_id=str(tweet.id),
                posted_at=datetime.now()
            )
            
            self.log_post_attempt(result, content)
            return result
            
        except Exception as e:
            result = PostResult(
                platform="twitter",
                success=False,
                error_message=f"Exception posting to Twitter: {str(e)}"
            )
            self.log_post_attempt(result, content)
            return result
    
    def create_twitter_thread(self, content: str, max_tweet_length: int = 250) -> List[PostResult]:
        """Create a Twitter thread from long-form content"""
        # Split content into tweet-sized chunks
        paragraphs = content.split('\n\n')
        tweets = []
        current_tweet = ""
        
        for paragraph in paragraphs:
            if len(current_tweet + paragraph) <= max_tweet_length:
                current_tweet += paragraph + "\n\n"
            else:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = paragraph + "\n\n"
        
        if current_tweet:
            tweets.append(current_tweet.strip())
        
        # Post thread
        results = []
        reply_to = None
        
        for i, tweet_content in enumerate(tweets):
            if i > 0:
                tweet_content = f"{i+1}/{len(tweets)} {tweet_content}"
            
            try:
                import tweepy
                
                auth = tweepy.OAuthHandler(
                    self.twitter_credentials['api_key'],
                    self.twitter_credentials['api_secret']
                )
                auth.set_access_token(
                    self.twitter_credentials['access_token'],
                    self.twitter_credentials['access_token_secret']
                )
                
                api = tweepy.API(auth)
                
                if reply_to:
                    tweet = api.update_status(tweet_content, in_reply_to_status_id=reply_to)
                else:
                    tweet = api.update_status(tweet_content)
                
                reply_to = tweet.id
                
                results.append(PostResult(
                    platform="twitter_thread",
                    success=True,
                    post_id=str(tweet.id),
                    posted_at=datetime.now()
                ))
                
                # Small delay between tweets
                time.sleep(2)
                
            except Exception as e:
                results.append(PostResult(
                    platform="twitter_thread",
                    success=False,
                    error_message=f"Thread tweet {i+1} failed: {str(e)}"
                ))
                break
        
        return results
    
    def post_content_file(self, filepath: str, platforms: List[str] = ['linkedin']) -> Dict[str, PostResult]:
        """Post content from a saved file to specified platforms"""
        try:
            with open(filepath, 'r') as f:
                file_content = f.read()
            
            # Extract title and content
            lines = file_content.split('\n')
            title = ""
            content = ""
            
            # Find title
            for line in lines:
                if line.startswith('# '):
                    title = line[2:].strip()
                    break
            
            # Extract main content (skip metadata)
            content_started = False
            content_lines = []
            
            for line in lines:
                if line.strip() == "---" and not content_started:
                    content_started = True
                    continue
                elif content_started:
                    content_lines.append(line)
            
            content = '\n'.join(content_lines).strip()
            
            # Post to each platform
            results = {}
            
            for platform in platforms:
                if platform == 'linkedin':
                    results[platform] = self.post_to_linkedin(content, title)
                elif platform == 'twitter':
                    # For long content, create a thread
                    if len(content) > 250:
                        thread_results = self.create_twitter_thread(content)
                        results[platform] = thread_results[0] if thread_results else PostResult(
                            platform="twitter", success=False, error_message="Thread creation failed"
                        )
                    else:
                        results[platform] = self.post_to_twitter(content)
                
                # Small delay between platforms
                time.sleep(1)
            
            return results
            
        except Exception as e:
            return {platform: PostResult(
                platform=platform,
                success=False,
                error_message=f"Error reading file {filepath}: {str(e)}"
            ) for platform in platforms}
    
    def log_post_attempt(self, result: PostResult, content: str, title: str = ""):
        """Log posting attempt for tracking"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': result.platform,
            'success': result.success,
            'post_id': result.post_id,
            'error_message': result.error_message,
            'title': title,
            'content_preview': content[:100] + "..." if len(content) > 100 else content,
            'content_length': len(content)
        }
        
        self.posting_log.append(log_entry)
        self.save_posting_history()
    
    def get_posting_stats(self, days: int = 30) -> Dict:
        """Get posting statistics for the last N days"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_posts = [
            post for post in self.posting_log
            if datetime.fromisoformat(post['timestamp']) > cutoff_date
        ]
        
        stats = {
            'total_posts': len(recent_posts),
            'successful_posts': len([p for p in recent_posts if p['success']]),
            'failed_posts': len([p for p in recent_posts if not p['success']]),
            'platforms': {},
            'success_rate': 0
        }
        
        if stats['total_posts'] > 0:
            stats['success_rate'] = stats['successful_posts'] / stats['total_posts'] * 100
        
        # Platform breakdown
        for post in recent_posts:
            platform = post['platform']
            if platform not in stats['platforms']:
                stats['platforms'][platform] = {'total': 0, 'successful': 0}
            
            stats['platforms'][platform]['total'] += 1
            if post['success']:
                stats['platforms'][platform]['successful'] += 1
        
        return stats

def main():
    """Main function for testing social media posting"""
    print("🚀 Dylan Social Media Poster")
    print("=" * 40)
    
    poster = SocialMediaPoster()
    
    # Check credentials
    linkedin_ready = "✅" if poster.linkedin_token else "❌"
    twitter_ready = "✅" if all(poster.twitter_credentials.values()) else "❌"
    
    print(f"LinkedIn: {linkedin_ready}")
    print(f"Twitter: {twitter_ready}")
    print()
    
    if not poster.linkedin_token and not all(poster.twitter_credentials.values()):
        print("⚠️  No social media credentials configured.")
        print("   Set up API keys in .env file to enable posting.")
        print("   For now, you can test with demo content.")
        print()
    
    while True:
        print("Social Media Posting Options:")
        print("1. Post demo content to LinkedIn")
        print("2. Post demo content to Twitter")
        print("3. Post content file")
        print("4. View posting statistics")
        print("5. Test credentials")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            demo_content = """**Midwest multifamily markets continue their remarkable surge.**

Recent data shows Minneapolis sales up 95% and Chicago up 88% year-over-year, while Sun Belt markets face oversupply headwinds.

The underlying story: markets that maintained construction discipline during 2021-2022 are now reaping the rewards.

What markets are you watching that others might be overlooking?

*Views are my own; not investment advice.*"""
            
            result = poster.post_to_linkedin(demo_content, "Midwest Market Update")
            
            if result.success:
                print(f"✅ Posted to LinkedIn successfully! Post ID: {result.post_id}")
            else:
                print(f"❌ LinkedIn posting failed: {result.error_message}")
        
        elif choice == '2':
            demo_content = """Midwest multifamily sales surge: Minneapolis +95%, Chicago +88%. 

While Sun Belt faces oversupply, Midwest markets that maintained construction discipline are now outperforming.

Geography matters more than ever in today's CRE landscape."""
            
            result = poster.post_to_twitter(demo_content)
            
            if result.success:
                print(f"✅ Posted to Twitter successfully! Tweet ID: {result.post_id}")
            else:
                print(f"❌ Twitter posting failed: {result.error_message}")
        
        elif choice == '3':
            filepath = input("Enter path to content file: ").strip()
            platforms = input("Enter platforms (linkedin,twitter): ").strip().split(',')
            platforms = [p.strip() for p in platforms if p.strip()]
            
            if not platforms:
                platforms = ['linkedin']
            
            results = poster.post_content_file(filepath, platforms)
            
            for platform, result in results.items():
                if result.success:
                    print(f"✅ {platform}: Posted successfully! ID: {result.post_id}")
                else:
                    print(f"❌ {platform}: Failed - {result.error_message}")
        
        elif choice == '4':
            stats = poster.get_posting_stats()
            print(f"\n📊 Posting Statistics (Last 30 Days)")
            print(f"Total Posts: {stats['total_posts']}")
            print(f"Successful: {stats['successful_posts']}")
            print(f"Failed: {stats['failed_posts']}")
            print(f"Success Rate: {stats['success_rate']:.1f}%")
            
            if stats['platforms']:
                print("\nPlatform Breakdown:")
                for platform, data in stats['platforms'].items():
                    rate = (data['successful'] / data['total'] * 100) if data['total'] > 0 else 0
                    print(f"  {platform}: {data['successful']}/{data['total']} ({rate:.1f}%)")
        
        elif choice == '5':
            print("\n🔍 Testing Credentials...")
            print(f"LinkedIn Token: {'✅ Configured' if poster.linkedin_token else '❌ Missing'}")
            
            twitter_configured = all(poster.twitter_credentials.values())
            print(f"Twitter Credentials: {'✅ Configured' if twitter_configured else '❌ Missing'}")
            
            if not poster.linkedin_token:
                print("   Set LINKEDIN_ACCESS_TOKEN in .env file")
            if not twitter_configured:
                print("   Set Twitter API credentials in .env file")
        
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")
        
        print()

if __name__ == "__main__":
    main()
