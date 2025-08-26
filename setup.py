#!/usr/bin/env python3
"""
Setup Script for Dylan's AI Content Agent
One-time setup and configuration
"""

import os
import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    else:
        print(f"✅ Python version: {sys.version.split()[0]}")
        return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "generated_content",
        "content_queue", 
        "logs",
        "demo_output"
    ]
    
    print("📁 Creating directories...")
    
    for directory in directories:
        dir_path = Path(directory)
        dir_path.mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def setup_environment_file():
    """Setup .env file from template"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("🔧 Setting up environment file...")
        
        # Copy example to .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ .env file created from template")
        print("   📝 Edit .env file to add your API keys")
        return True
    elif env_file.exists():
        print("✅ .env file already exists")
        return True
    else:
        print("⚠️  No .env.example file found")
        return False

def test_system():
    """Test the system components"""
    print("🧪 Testing system components...")
    
    try:
        # Test content agent
        from dylan_content_agent import DylanContentAgent
        agent = DylanContentAgent()
        print("   ✅ Content agent initialized")
        
        # Test social poster
        from social_media_poster import SocialMediaPoster
        poster = SocialMediaPoster()
        print("   ✅ Social media poster initialized")
        
        # Test pipeline
        from automated_content_pipeline import AutomatedContentPipeline
        pipeline = AutomatedContentPipeline()
        print("   ✅ Automated pipeline initialized")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ System test error: {e}")
        return False

def show_next_steps():
    """Show user what to do next"""
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Next Steps:")
    print()
    print("1. 🔑 Configure API Keys (Optional but recommended)")
    print("   Edit .env file and add your OpenAI API key:")
    print("   OPENAI_API_KEY=your_key_here")
    print()
    print("2. 🚀 Test the System")
    print("   python3 demo.py")
    print()
    print("3. 📝 Generate Content Manually") 
    print("   python3 dylan_content_agent.py")
    print()
    print("4. 🤖 Run Automated Pipeline")
    print("   python3 automated_content_pipeline.py")
    print()
    print("5. ⏰ Start Automated Scheduler")
    print("   python3 daily_scheduler.py")
    print()
    print("📚 Documentation:")
    print("   Read README.md for detailed usage instructions")
    print()
    print("🔧 Configuration:")
    print("   • Content style: Edit dylan_content_agent.py")
    print("   • Posting schedule: Edit daily_scheduler.py")
    print("   • Pipeline settings: Edit automated_content_pipeline.py")

def main():
    """Main setup function"""
    print("🚀 Dylan AI Content Agent Setup")
    print("=" * 50)
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    print()
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    print()
    
    # Create directories
    if not create_directories():
        return False
    
    print()
    
    # Setup environment
    if not setup_environment_file():
        return False
    
    print()
    
    # Test system
    if not test_system():
        print("⚠️  System test failed, but setup may still work")
    
    print()
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Setup completed successfully!")
    else:
        print("\n❌ Setup encountered errors. Please check the output above.")
        sys.exit(1)
