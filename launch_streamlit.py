#!/usr/bin/env python3
"""
Streamlit App Launcher for AI Video Workflow
Run this script to start the web interface
"""

import os
import subprocess
import sys

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import video_prompt_generator
        print("✅ All dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Launch the Streamlit application."""
    print("🎬 AI Video Workflow Studio - Streamlit Launcher")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ streamlit_app.py not found in current directory")
        print("Please run this script from the AI_Video_Workflow directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found")
        print("Please create a .env file with your GOOGLE_API_KEY")
        print("Example:")
        print("GOOGLE_API_KEY=your_api_key_here")
        print()
    
    print("🚀 Starting Streamlit application...")
    print("📱 The app will open in your default web browser")
    print("🔗 Default URL: http://localhost:8501")
    print()
    print("💡 Tips:")
    print("   - Press Ctrl+C to stop the server")
    print("   - Refresh browser if you make code changes")
    print("   - Use --reload flag for auto-refresh during development")
    print()
    print("=" * 55)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--theme.base", "light",
            "--theme.primaryColor", "#667eea",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f5f7fa"
        ])
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
    except Exception as e:
        print(f"❌ Error launching Streamlit: {e}")

if __name__ == "__main__":
    main()