#!/usr/bin/env python3
"""
Integrated AI Video Workflow
This script combines:
1. Video prompt generation (4 scene prompts)
2. Veo 3.1 video generation for each prompt
3. Automatic video merging with transitions

Author: AI Video Workflow System
"""

import time
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
import subprocess
import platform

# Import existing modules
from video_prompt_generator import VideoPromptGenerator, VideoScenePrompts

# Google AI and Cloud imports
from google import genai
from google.genai.types import GenerateVideosConfig, Image
from google.cloud import storage
from google.api_core.exceptions import NotFound

# Video processing imports
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from merge import merge_videos

class IntegratedVideoWorkflow:
    """
    Main workflow orchestrator that handles the complete video generation pipeline:
    Prompt Generation -> Video Generation -> Video Merging
    """
    
    def __init__(self, project_dir: str = None, enable_debugger: bool = True):
        """Initialize the integrated workflow."""
        # Setup directories
        self.project_dir = project_dir or r"E:\AsapStudio\Ai_Video_Workflow"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(self.project_dir, f"generated_videos_{self.timestamp}")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Debugger settings
        self.enable_debugger = enable_debugger
        
        # Video generation settings
        self.gcs_input_uri = "gs://abd756/shared image.jpg"  # Your existing image
        self.gcs_output_base = "gs://abd756/veo_output/"
        
        # Initialize components
        self.prompt_generator = None
        self.genai_client = None
        self.storage_client = None
        self.generated_video_paths = []
        
        print(f"🚀 Integrated Video Workflow initialized")
        print(f"📁 Output directory: {self.output_dir}")
        if self.enable_debugger:
            print(f"🔍 Interactive debugger ENABLED - will pause after each video for review")
        else:
            print(f"⚡ Auto-mode ENABLED - will generate all videos without pause")
    
    def initialize_clients(self):
        """Initialize Google GenAI and Storage clients."""
        try:
            print("🔧 Initializing Google GenAI and Storage clients...")
            
            # Initialize prompt generator
            self.prompt_generator = VideoPromptGenerator()
            
            # Initialize GenAI client
            self.genai_client = genai.Client(
                vertexai=True,
                project="gen-lang-client-0207694487",
                location="us-central1"
            )
            
            # Initialize Storage client
            self.storage_client = storage.Client()
            
            print("✅ All clients initialized successfully")
            return True
            
        except Exception as e:
            # Fail loudly so callers know initialization didn't succeed
            print(f"❌ Failed to initialize clients: {e}")
            raise
    
    def generate_video_prompts(self, user_input: str) -> VideoScenePrompts:
        """Generate 4 scene prompts using the existing VideoPromptGenerator."""
        try:
            print(f"\n🎬 Generating 4 video scene prompts...")
            print(f"📝 User input preview: {user_input[:100]}...")
            
            prompts = self.prompt_generator.generate_video_prompts(user_input)
            
            # Save prompts to output directory
            prompts_file = os.path.join(self.output_dir, "generated_prompts.json")
            with open(prompts_file, 'w', encoding='utf-8') as f:
                json.dump(prompts.model_dump(), f, indent=2, ensure_ascii=False)
            
            print("✅ Video prompts generated and saved")
            self.print_prompts_summary(prompts)
            
            return prompts
            
        except Exception as e:
            print(f"❌ Error generating prompts: {e}")
            raise
    
    def generate_single_video(self, prompt: str, scene_number: int) -> str:
        """Generate a single video using Veo 3.1 with the given prompt."""
        try:
            print(f"\n🎥 Generating video for Scene {scene_number}...")
            print(f"📝 Prompt preview: {prompt[:100]}...")
            
            # Create unique output URI for this video
            output_gcs_uri = f"{self.gcs_output_base}scene_{scene_number}_{self.timestamp}/"
            
            # Start video generation
            operation = self.genai_client.models.generate_videos(
                model="veo-3.1-fast-generate-001",
                prompt=prompt,
                config=GenerateVideosConfig(
                    aspect_ratio="16:9",
                    output_gcs_uri=output_gcs_uri,
                ),
            )
            
            print(f"⏳ Video generation started for Scene {scene_number}. Polling for completion...")
            
            # Poll for completion
            while not operation.done:
                time.sleep(20)
                operation = self.genai_client.operations.get(operation)
                print(f"⏳ Still generating Scene {scene_number}...")
            
            # Handle result
            if operation.response:
                gcs_video_uri = operation.result.generated_videos[0].video.uri
                print(f"✅ Scene {scene_number} generated at: {gcs_video_uri}")
                
                # Download video locally
                local_path = self.download_video_from_gcs(gcs_video_uri, scene_number)
                return local_path
            else:
                raise Exception(f"Video generation returned no response for Scene {scene_number}")
                
        except Exception as e:
            print(f"❌ Error generating video for Scene {scene_number}: {e}")
            raise
    
    def download_video_from_gcs(self, gcs_uri: str, scene_number: int) -> str:
        """Download generated video from Google Cloud Storage."""
        try:
            if not gcs_uri.startswith("gs://"):
                raise ValueError("Invalid GCS URI format")
            
            # Extract bucket and blob name
            parts = gcs_uri.replace("gs://", "").split("/", 1)
            bucket_name, blob_name = parts[0], parts[1]
            
            # Create local filename
            local_filename = f"scene_{scene_number}_{self.timestamp}.mp4"
            local_path = os.path.join(self.output_dir, local_filename)
            
            # Download from GCS
            print(f"📥 Downloading Scene {scene_number} to: {local_filename}")
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.download_to_filename(local_path)
            
            print(f"✅ Scene {scene_number} downloaded successfully")
            return local_path
            
        except Exception as e:
            print(f"❌ Error downloading Scene {scene_number}: {e}")
            raise
    
    def interactive_video_review(self, video_path: str, scene_number: int, prompt: str) -> bool:
        """Interactive review of generated video with options to continue or stop."""
        if not self.enable_debugger:
            return True  # Auto-continue if debugger disabled
            
        print(f"\n" + "="*80)
        print(f"🎬 VIDEO REVIEW - Scene {scene_number}")
        print(f"="*80)
        print(f"📹 Video generated: {os.path.basename(video_path)}")
        print(f"📁 Full path: {video_path}")
        print(f"📝 Prompt used: {prompt[:100]}...")
        
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            print(f"📊 File size: {file_size:.2f} MB")
            print(f"✅ Video file exists and ready for review")
        else:
            print(f"❌ Warning: Video file not found at expected location")
        
        print(f"\n🔍 REVIEW OPTIONS:")
        print(f"1. 📺 Open video for preview (recommended)")
        print(f"2. ✅ Continue to next video")
        print(f"3. ❌ Stop workflow (save costs)")
        print(f"4. 📋 View full prompt")
        print(f"5. 📊 Show workflow progress")
        
        while True:
            choice = input(f"\n🎯 Choose option (1-5): ").strip()
            
            if choice == "1":
                self.open_video_preview(video_path)
                continue
            elif choice == "2":
                print(f"✅ Continuing to next video...")
                return True
            elif choice == "3":
                confirm = input(f"⚠️ Stop workflow? You'll lose progress on remaining videos (y/n): ")
                if confirm.lower() in ['y', 'yes']:
                    print(f"🛑 Workflow stopped by user")
                    return False
                continue
            elif choice == "4":
                print(f"\n📋 FULL PROMPT:")
                print(f"-" * 60)
                print(f"{prompt}")
                print(f"-" * 60)
                continue
            elif choice == "5":
                self.show_workflow_progress(scene_number)
                continue
            else:
                print(f"❌ Invalid choice. Please enter 1-5.")
                continue
    
    def open_video_preview(self, video_path: str):
        """Open video file in default media player for preview."""
        try:
            if not os.path.exists(video_path):
                print(f"❌ Video file not found: {video_path}")
                return
            
            print(f"🎬 Opening video in default media player...")
            
            # Cross-platform video opening
            system = platform.system()
            if system == "Windows":
                os.startfile(video_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", video_path])
            else:  # Linux
                subprocess.run(["xdg-open", video_path])
            
            print(f"✅ Video should open in your default media player")
            print(f"💡 Tip: Check video quality, relevance to your business, and overall satisfaction")
            
        except Exception as e:
            print(f"❌ Error opening video: {e}")
            print(f"📁 Manual path: {video_path}")
    
    def show_workflow_progress(self, current_scene: int):
        """Show current workflow progress and cost estimation."""
        total_scenes = 4
        completed = current_scene
        remaining = total_scenes - current_scene
        
        print(f"\n📊 WORKFLOW PROGRESS:")
        print(f"-" * 40)
        print(f"✅ Completed: {completed}/{total_scenes} videos")
        print(f"⏳ Remaining: {remaining} videos")
        print(f"📈 Progress: {(completed/total_scenes)*100:.1f}%")
        
        # Cost estimation (approximate)
        cost_per_video = 0.50  # Approximate cost in USD
        spent = completed * cost_per_video
        remaining_cost = remaining * cost_per_video
        
        print(f"\n💰 ESTIMATED COSTS:")
        print(f"-" * 40)
        print(f"💸 Spent so far: ~${spent:.2f}")
        print(f"🔮 Remaining cost: ~${remaining_cost:.2f}")
        print(f"💵 Total estimated: ~${spent + remaining_cost:.2f}")
        print(f"⚠️ Note: Actual costs may vary based on video length and complexity")
    
    def generate_all_videos(self, prompts: VideoScenePrompts) -> List[str]:
        """Generate videos for all 4 prompts with interactive review."""
        video_paths = []
        
        scenes = [
            ("Scene 1", prompts.prompt_1),
            ("Scene 2", prompts.prompt_2),
            ("Scene 3", prompts.prompt_3),
            ("Scene 4", prompts.prompt_4)
        ]
        
        print(f"\n🎬 Starting generation of {len(scenes)} videos...")
        
        for i, (scene_name, prompt) in enumerate(scenes, 1):
            try:
                print(f"\n{'='*60}")
                print(f"🎯 Processing {scene_name} ({i}/{len(scenes)})")
                print(f"{'='*60}")
                
                video_path = self.generate_single_video(prompt, i)
                video_paths.append(video_path)
                
                print(f"✅ {scene_name} completed: {os.path.basename(video_path)}")
                
                # Interactive review if debugger enabled
                if self.enable_debugger:
                    should_continue = self.interactive_video_review(video_path, i, prompt)
                    if not should_continue:
                        print(f"\n🛑 Workflow stopped by user after Scene {i}")
                        print(f"💾 Generated videos saved in: {self.output_dir}")
                        return video_paths  # Return what we have so far
                else:
                    print(f"⚡ Auto-continuing to next video (debugger disabled)")
                
            except Exception as e:
                print(f"❌ Failed to generate {scene_name}: {e}")
                # Continue with other videos even if one fails
                continue
        
        self.generated_video_paths = video_paths
        print(f"\n🎉 Generated {len(video_paths)} out of {len(scenes)} videos successfully!")
        
        return video_paths
    
    def merge_videos(self, video_paths: List[str], transition_type: str = "crossfade", transition_duration: float = 0.3) -> str:
        """Merge all generated videos with transitions using merge.py utility."""
        try:
            if not video_paths:
                raise ValueError("No video files provided for merging.")
            print(f"\n🔄 Starting video merge process...")
            print(f"📹 Videos to merge: {len(video_paths)}")
            print(f"⏱️ Transition duration: {transition_duration}s")
            output_path = os.path.join(self.output_dir, f"merged_video_{self.timestamp}.mp4")
            merged_path = merge_videos(
                video_paths=video_paths,
                output_path=output_path,
                transition_type=transition_type,
                transition_duration=transition_duration
            )
            print(f"✅ Merged video saved: {merged_path}")
            return merged_path
        except Exception as e:
            print(f"❌ Error merging videos: {e}")
            raise
    
    def apply_crossfade_transition(self, clips, transition_duration):
        """Apply crossfade transition between clips (adapted from merge.py)."""
        if len(clips) < 2:
            return clips[0] if clips else None
        
        # Process clips with fade effects
        processed_clips = []
        
        for i, clip in enumerate(clips):
            current_clip = clip
            
            # Add fadeout to all clips except the last one
            if i < len(clips) - 1:
                current_clip = current_clip.fadeout(transition_duration)
            
            # Add fadein to all clips except the first one
            if i > 0:
                current_clip = current_clip.fadein(transition_duration)
            
            processed_clips.append(current_clip)
        
        # Create crossfade effect by overlapping clips
        if len(processed_clips) == 2:
            # For two clips, create a simple crossfade
            clip1 = processed_clips[0]
            clip2 = processed_clips[1].set_start(clip1.duration - transition_duration)
            
            final_clip = CompositeVideoClip([clip1, clip2])
        else:
            # For multiple clips, chain them with overlaps
            final_clip = processed_clips[0]
            
            for i in range(1, len(processed_clips)):
                next_clip = processed_clips[i].set_start(final_clip.duration - transition_duration)
                final_clip = CompositeVideoClip([final_clip, next_clip])
        
        return final_clip
    
    def run_complete_workflow(self, user_input: str) -> str:
        """Run the complete workflow from prompts to final merged video."""
        try:
            print("\n" + "="*80)
            print("🚀 STARTING COMPLETE AI VIDEO WORKFLOW")
            print("="*80)
            print(f"📅 Timestamp: {self.timestamp}")
            print(f"📁 Output Directory: {self.output_dir}")
            
            # Step 1: Initialize clients
            # Step 1: Initialize clients (will raise on failure)
            self.initialize_clients()
            
            # Step 2: Generate prompts
            prompts = self.generate_video_prompts(user_input)
            
            # Step 3: Generate videos for each prompt
            video_paths = self.generate_all_videos(prompts)
            
            if not video_paths:
                raise Exception("No videos were generated successfully")
            
            # Step 4: Merge all videos (if any were generated)
            if video_paths:
                final_video_path = self.merge_videos(video_paths)
            else:
                raise Exception("No videos were generated to merge")
            
            # Step 5: Create summary
            self.create_workflow_summary(user_input, prompts, video_paths, final_video_path)
            
            print("\n" + "="*80)
            print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
            print("="*80)
            print(f"📹 Final Video: {os.path.basename(final_video_path)}")
            print(f"📁 Full Path: {final_video_path}")
            print(f"📊 Generated {len(video_paths)} individual videos")
            print("="*80)
            
            return final_video_path
            
        except Exception as e:
            print(f"\n❌ WORKFLOW FAILED: {e}")
            raise
    
    def create_workflow_summary(self, user_input: str, prompts: VideoScenePrompts, 
                              video_paths: List[str], final_video_path: str):
        """Create a summary report of the workflow execution."""
        summary = {
            "workflow_info": {
                "timestamp": self.timestamp,
                "output_directory": self.output_dir,
                "user_input": user_input
            },
            "generated_prompts": prompts.model_dump(),
            "individual_videos": [
                {
                    "scene_number": i+1,
                    "filename": os.path.basename(path),
                    "full_path": path,
                    "exists": os.path.exists(path)
                }
                for i, path in enumerate(video_paths)
            ],
            "final_video": {
                "filename": os.path.basename(final_video_path),
                "full_path": final_video_path,
                "exists": os.path.exists(final_video_path)
            }
        }
        
        summary_file = os.path.join(self.output_dir, "workflow_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Workflow summary saved: {os.path.basename(summary_file)}")
    
    def print_prompts_summary(self, prompts: VideoScenePrompts):
        """Print a summary of generated prompts."""
        print("\n📋 Generated Prompts Summary:")
        print("-" * 50)
        
        scenes = [
            ("Scene 1", prompts.prompt_1),
            ("Scene 2", prompts.prompt_2),
            ("Scene 3", prompts.prompt_3),
            ("Scene 4", prompts.prompt_4)
        ]
        
        for scene_name, prompt in scenes:
            preview = prompt[:80] + "..." if len(prompt) > 80 else prompt
            print(f"🎯 {scene_name}: {preview}")


def main():
    """Main function for interactive workflow execution."""
    print("🎬 AI Video Generation Complete Workflow")
    print("=" * 60)
    print("This tool will:")
    print("1. Generate 4 video scene prompts")
    print("2. Create videos using Veo 3.1 for each prompt")
    print("3. Merge all videos with smooth transitions")
    print("\n" + "-" * 60)
    
    # Get user input
    user_input = input("\nEnter your complete message (company info + script + requirements):\n")
    
    if not user_input.strip():
        print("❌ No input provided. Using example...")
        user_input = """I run iCONNCT, a real estate technology platform that connects buyers, sellers, and agents instantly. 
        Our platform works like Uber for real estate - tap, talk, connect with trusted agents. 
        We offer instant video/voice calls, real-time scheduling, and seamless property tours. 
        I want to create video reels showing our modern technology, professional agents, property showcases, and satisfied customers."""
    
    try:
        # Ask about debugger preference
        print("\n🔧 Workflow Configuration:")
        print("The interactive debugger pauses after each video generation for review.")
        print("This helps save costs by letting you stop if videos aren't satisfactory.")
        
        debugger_choice = input("\nEnable interactive debugger? (y/n, default=y): ").strip().lower()
        enable_debugger = debugger_choice != 'n'  # Default to enabled
        
        if enable_debugger:
            print("✅ Interactive debugger enabled - you'll review each video before continuing")
        else:
            print("⚡ Auto-mode enabled - all videos will generate without pause")
            
        # Initialize and run workflow
        workflow = IntegratedVideoWorkflow(enable_debugger=enable_debugger)
        final_video = workflow.run_complete_workflow(user_input)
        
        print(f"\n🎉 SUCCESS! Your final video is ready:")
        print(f"📹 {final_video}")
        
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        print("Please check your Google API keys and GCS configuration.")


def run_quick_workflow(user_message: str, project_dir: str = None, enable_debugger: bool = True) -> str:
    """
    Quick function to run the complete workflow with a single function call.
    
    Args:
        user_message: Complete description (company info + script + requirements)
        project_dir: Optional custom project directory
        enable_debugger: Enable interactive review after each video (default: True)
    
    Returns:
        Path to the final merged video file
    """
    workflow = IntegratedVideoWorkflow(project_dir, enable_debugger)
    return workflow.run_complete_workflow(user_message)


if __name__ == "__main__":
    main()