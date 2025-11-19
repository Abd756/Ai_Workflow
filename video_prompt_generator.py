#!/usr/bin/env python3
"""
Video Prompt Generator for AI Video Creation
This script generates 4 different scene prompts based on user input and company information.
Uses Pydantic for structured outputs.
"""

import os
import json
from typing import Dict, List, Any
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, Field

class VideoScenePrompts(BaseModel):
    """Structured output for 4 video scene prompts."""
    prompt_1: str = Field(description="First video scene prompt - AI will determine the best scene type")
    prompt_2: str = Field(description="Second video scene prompt - AI will determine the best scene type")
    prompt_3: str = Field(description="Third video scene prompt - AI will determine the best scene type")
    prompt_4: str = Field(description="Fourth video scene prompt - AI will determine the best scene type")

class VideoPromptGenerator:
    """Generates professional video scene prompts for AI video creation."""
    
    def __init__(self):
        """Initialize the generator with Gemini API."""
        load_dotenv()
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables!")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_video_prompts(self, user_input: str) -> VideoScenePrompts:
        """
        Generate 4 different scene prompts using structured output.
        
        Args:
            user_input: Complete message/script including company information and requirements
            
        Returns:
            VideoScenePrompts object with 4 structured prompts
        """
        
        system_prompt = f"""
    You are an expert video production assistant specializing in creating detailed, professional video scene prompts for AI video generation.

    USER INPUT/COMPANY DESCRIPTION:
    {user_input}

    Your Task: Analyze the user's company/business information and script, then intelligently create 4 DIFFERENT but INTERCONNECTED video scene prompts that together form a single, cohesive video narrative for this specific business, niche, or creative context.

    Instructions:
    1. Read and understand the company type, industry, niche, and user's script/message.
    2. Use your expertise to determine what 4 different scenes would be most effective and logical for this specific case.
    3. For each scene, provide a 1-2 sentence summary of the previous scene(s) and the overall video goal, so that each prompt is self-contained and contextually aware even if processed independently.
    4. Do NOT use scene numbers or refer to "scene 2" or "scene 3". Instead, use natural language transitions and narrative summaries (e.g., "Previously, a frustrated homebuyer struggled to find the right agent. Now, show how the app provides a solution...").
    5. The scenes should be interconnected, with transitions or references that link them together (e.g., the ending of one scene leads naturally into the next, or a visual/narrative thread continues across scenes).
    6. Do NOT use a fixed template for the scenes—let the content, order, and focus of each scene be determined by the user's input and the needs of the business or creative project.
    7. Maintain a consistent visual and narrative style across all prompts.
    8. Make scenes industry-appropriate, contextually relevant, and tailored to the specific business or creative context.

    For each prompt, provide:
    - A brief summary of the previous scene(s) and the overall video narrative so far (1-2 sentences, in natural language).
    - Detailed setting/environment description
    - Professional presenter/character details (appearance, clothing, demeanor)
    - Specific lighting setup and visual style
    - Camera movements and angles
    - Natural integration of the user's script/message
    - Duration: 8 seconds per scene
    - Photorealistic with natural micro-movements (gentle hand gestures, slight head tilts)
    - Professional, modern, visually appealing aesthetic
    - Steady camera with light cinematic push-in movement
    - Continuous, natural shots without fast motion
    - No background music or fade-ins

    Label each prompt as:
    PROMPT 1: [Your chosen scene type]
    PROMPT 2: [Your chosen scene type]
    PROMPT 3: [Your chosen scene type]
    PROMPT 4: [Your chosen scene type]

    Be creative and ensure the scenes are interconnected, forming a single, unified video experience for the business or creative context described in the user input. Each prompt must be self-contained and provide enough context for a stateless model to generate a coherent scene.
    """
        
        try:
            response = self.model.generate_content(system_prompt)
            
            # Parse the response into structured format
            # For now, we'll assume the model returns plain text that we need to structure
            response_text = response.text.strip()
            
            # Split the response into 4 parts (assuming the model follows the structure)
            sections = response_text.split("PROMPT")
            
            if len(sections) >= 5:  # Should have intro + 4 prompts
                return VideoScenePrompts(
                    prompt_1=sections[1].split("PROMPT 2")[0].strip().replace("1:", "").strip(),
                    prompt_2=sections[2].split("PROMPT 3")[0].strip().replace("2:", "").strip(),
                    prompt_3=sections[3].split("PROMPT 4")[0].strip().replace("3:", "").strip(),
                    prompt_4=sections[4].strip().replace("4:", "").strip()
                )
            else:
                # If parsing fails, return the full response split roughly
                parts = response_text.split('\n\n')
                return VideoScenePrompts(
                    prompt_1=parts[0] if len(parts) > 0 else "Scene 1 prompt not generated",
                    prompt_2=parts[1] if len(parts) > 1 else "Scene 2 prompt not generated", 
                    prompt_3=parts[2] if len(parts) > 2 else "Scene 3 prompt not generated",
                    prompt_4=parts[3] if len(parts) > 3 else "Scene 4 prompt not generated"
                )
                
        except Exception as e:
            print(f"❌ Error generating prompts: {str(e)}")
            return VideoScenePrompts(
                prompt_1="Error generating prompt 1",
                prompt_2="Error generating prompt 2", 
                prompt_3="Error generating prompt 3",
                prompt_4="Error generating prompt 4"
            )
    

    def save_prompts_to_file(self, prompts: VideoScenePrompts, filename: str = "video_prompts.json"):
        """Save generated prompts to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(prompts.model_dump(), f, indent=2, ensure_ascii=False)
            print(f"✅ Prompts saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving prompts: {str(e)}")
    
    def print_prompts(self, prompts: VideoScenePrompts):
        """Print generated prompts in a formatted way."""
        print("\n" + "="*80)
        print("🎬 GENERATED VIDEO SCENE PROMPTS")
        print("="*80)
        
        scenes = [
            ("Scene 1", prompts.prompt_1),
            ("Scene 2", prompts.prompt_2), 
            ("Scene 3", prompts.prompt_3),
            ("Scene 4", prompts.prompt_4)
        ]
        
        for i, (scene_name, prompt) in enumerate(scenes, 1):
            print(f"\n🎯 SCENE {i}: {scene_name}")
            print("-" * 60)
            print(f"{prompt}")
            print("\n" + "-" * 60)

def main():
    """Main function with interactive input for video prompt generation."""
    
    print("🎬 AI Video Prompt Generator")
    print("="*50)
    print("This tool will generate 4 different scene prompts for your video based on your input.")
    print("\nPlease provide:")
    print("- Your company/business description")
    print("- The script/message you want in the video")
    print("- Any specific requirements or focus areas")
    print("\n" + "-"*50)
    
    # Get user input
    user_input = input("\nEnter your complete message (company info + script + requirements):\n")
    
    if not user_input.strip():
        print("❌ No input provided. Using example...")
        user_input = """I run iCONNCT, a real estate technology platform that connects buyers, sellers, and agents instantly. 
        Our platform works like Uber for real estate - tap, talk, connect with trusted agents. 
        We offer instant video/voice calls, real-time scheduling, and seamless property tours. 
        I want to create video reels showing our modern technology, professional agents, property showcases, and satisfied customers."""
    
    try:
        generator = VideoPromptGenerator()
        print(f"\n🚀 Generating 4 video scene prompts...")
        print(f"Input preview: {user_input[:100]}...")
        
        prompts = generator.generate_video_prompts(user_input)
        generator.print_prompts(prompts)
        generator.save_prompts_to_file(prompts)
        
        print(f"\n✅ Successfully generated 4 structured video scene prompts!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please check your GOOGLE_API_KEY in .env file")

def generate_custom_prompts(user_message: str) -> VideoScenePrompts:
    """
    Simple function to generate video prompts with custom user message.
    
    Args:
        user_message: Your complete description (company info + script + requirements)
    
    Returns:
        VideoScenePrompts object with 4 structured prompts
    """
    generator = VideoPromptGenerator()
    
    print(f"🚀 Generating video prompts...")
    print(f"User Message: {user_message[:100]}...")
    
    prompts = generator.generate_video_prompts(user_message)
    generator.print_prompts(prompts)
    generator.save_prompts_to_file(prompts)
    
    return prompts

if __name__ == "__main__":
    main()