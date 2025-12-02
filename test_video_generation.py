#!/usr/bin/env python3
"""
Test Video Generation Script
Simple test to verify Veo 3.1 video generation is working
"""

import os
import time
import argparse
from datetime import datetime
from video_prompt_generator import VideoPromptGenerator

# Test with a simple business input
test_input = """
I run TechFlow Solutions, a software development company specializing in AI automation.
We help businesses streamline operations through intelligent automation and cloud solutions.
I want professional videos showing our modern office, team collaboration, and AI solutions in action.
"""

def test_prompt_generation():
    """Test if prompt generation is working."""
    print("🧠 Testing Prompt Generation...")
    print("=" * 50)
    
    try:
        generator = VideoPromptGenerator()
        prompts = generator.generate_video_prompts(test_input)
        
        print("✅ Prompt generation successful!")
        print(f"📝 Generated {len([prompts.prompt_1, prompts.prompt_2, prompts.prompt_3, prompts.prompt_4])} prompts")
        
        # Show first prompt preview
        print(f"\n🎬 First Prompt Preview:")
        print("-" * 30)
        print(f"{prompts.prompt_1[:200]}...")
        print("-" * 30)
        
        return prompts
        
    except Exception as e:
        print(f"❌ Prompt generation failed: {e}")
        return None

def test_video_generation_setup():
    """Test if video generation clients can be initialized."""
    print("\n🔧 Testing Video Generation Setup...")
    print("=" * 50)
    
    try:
        from google import genai
        from google.cloud import storage
        
        # Test GenAI client
        print("🤖 Initializing GenAI client...")
        # Use GENAI_PROJECT env var if set, otherwise fall back to default
        project_id = os.environ.get('GENAI_PROJECT', 'gen-lang-client-0207694487')
        client = genai.Client(
            vertexai=True,
            project=project_id,
            location="us-central1"
        )
        print("✅ GenAI client initialized successfully")
        
        # Test Storage client  
        print("☁️ Initializing Storage client...")
        storage_client = storage.Client()
        print("✅ Storage client initialized successfully")
        
        # Test GCS bucket access
        print("📁 Testing GCS bucket access...")
        bucket_name = "abd756"  # Your bucket name
        bucket = storage_client.bucket(bucket_name)
        
        # Check if bucket exists and is accessible
        if bucket.exists():
            print(f"✅ GCS bucket '{bucket_name}' is accessible")
        else:
            print(f"❌ GCS bucket '{bucket_name}' not found or not accessible")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Video generation setup failed: {e}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Check if Google Cloud SDK is installed and authenticated")
        print("2. Run: gcloud auth application-default login")
        print("3. Verify your project ID and bucket name")
        print("4. Ensure you have Veo 3.1 API access")
        return False

def test_single_video_generation(prompt: str):
    """Test generating a single video."""
    print("\n🎥 Testing Single Video Generation...")
    print("=" * 50)
    print("⚠️ This will use real API credits (~$0.75)")
    
    # Respect AUTO_APPROVE env var or CLI flag
    auto_approve = os.environ.get('AUTO_APPROVE', '0') == '1' or getattr(test_single_video_generation, 'auto_yes', False)
    if not auto_approve:
        proceed = input("Do you want to proceed with video generation? (y/n): ").strip().lower()
        if proceed != 'y':
            print("❌ Video generation test skipped by user")
            return None
    
    try:
        from integrated_video_workflow import IntegratedVideoWorkflow
        
        # Initialize workflow without debugger for testing
        # Allow forcing project via GENAI_PROJECT env var or CLI arg
        project_override = getattr(test_single_video_generation, 'project_id', None)
        workflow = IntegratedVideoWorkflow(enable_debugger=False, project_id=project_override)
        
        print("🚀 Initializing video generation clients...")
        if not workflow.initialize_clients():
            print("❌ Failed to initialize clients")
            return None
        
        print("📝 Test prompt preview:")
        print(f"{prompt[:150]}...")
        
        print("\n⏳ Generating video... This will take 2-5 minutes...")
        print("💰 Cost: ~$0.75")
        
        start_time = time.time()
        
        # Generate single video
        video_path = workflow.generate_single_video(prompt, 1)
        
        end_time = time.time()
        generation_time = (end_time - start_time) / 60  # minutes
        
        if video_path and os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            
            print(f"\n🎉 SUCCESS! Video generated in {generation_time:.1f} minutes")
            print(f"📹 File: {os.path.basename(video_path)}")
            print(f"📊 Size: {file_size:.1f} MB")
            print(f"📁 Location: {video_path}")
            
            return video_path
        else:
            print(f"❌ Video generation failed - file not found")
            return None
            
    except Exception as e:
        print(f"❌ Video generation error: {e}")
        return None

def main():
    """Main test function."""
    print("🧪 Video Generation Test Suite")
    print("=" * 60)
    print("This script will test the video generation pipeline step by step.\n")
    
    # Step 1: Test prompt generation
    prompts = test_prompt_generation()
    if not prompts:
        print("❌ Cannot proceed without working prompt generation")
        return
    
    # Step 2: Test video generation setup
    if not test_video_generation_setup():
        print("❌ Video generation setup failed. Please fix the issues above.")
        return
    
    # Step 3: Optional video generation test
    print("\n" + "=" * 60)
    print("🎯 READY FOR VIDEO GENERATION TEST")
    print("=" * 60)
    print("All setup checks passed! You can now test actual video generation.")
    print("⚠️ Warning: This will use real API credits (~$0.75 per video)")
    
    test_video = input("\nWould you like to test video generation with the first prompt? (y/n): ").strip().lower()
    
    if test_video == 'y':
        video_path = test_single_video_generation(prompts.prompt_1)
        
        if video_path:
            print(f"\n🎬 Video Generation Test SUCCESSFUL!")
            print(f"📹 Your test video is ready at: {video_path}")
            
            # Ask if they want to open the video
            open_video = input("Would you like to open the video now? (y/n): ").strip().lower()
            if open_video == 'y':
                try:
                    if os.name == 'nt':  # Windows
                        os.startfile(video_path)
                    elif os.name == 'posix':  # macOS/Linux
                        import subprocess
                        subprocess.run(['open' if 'darwin' in os.sys.platform else 'xdg-open', video_path])
                    print("🎥 Video should open in your default media player")
                except Exception as e:
                    print(f"❌ Could not open video: {e}")
                    print(f"📁 Manual path: {video_path}")
        else:
            print(f"\n❌ Video Generation Test FAILED")
    else:
        print("\n✅ Setup verification complete. Video generation is ready when you are!")

if __name__ == "__main__":
    main()