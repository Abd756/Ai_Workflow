# AI Video Workflow - Complete Pipeline

A complete AI-powered video generation workflow that combines prompt generation, Veo 3.1 video generation, and automatic video merging.

## 🚀 Features

- **Intelligent Prompt Generation**: Creates 4 unique scene prompts based on your business description
- **Veo 3.1 Video Generation**: Generates professional videos for each scene
- **Automatic Video Merging**: Combines all videos with smooth crossfade transitions
- **Professional Output**: Creates a complete, polished video ready for marketing

## 📋 Prerequisites

1. **Google Cloud Account** with Veo 3.1 access
2. **Google API Key** for Gemini
3. **Google Cloud Storage** bucket setup
4. **Python 3.8+** installed

## 🛠️ Installation

1. **Clone or download the workflow files**:
   ```
   video_prompt_generator.py
   integrated_video_workflow.py
   demo_workflow.py
   requirements.txt
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. **Configure Google Cloud**:
   - Set up Google Cloud authentication
   - Update bucket names in `integrated_video_workflow.py`:
     ```python
     self.gcs_input_uri = "gs://your-bucket/your-image.jpg"
     self.gcs_output_base = "gs://your-bucket/veo_output/"
     ```

## 🎬 Usage

### Method 1: Quick Start (Recommended)

```python
from integrated_video_workflow import run_quick_workflow

# Your business description
user_input = """
I run TechFlow Solutions, a software development company specializing in AI automation.
We help businesses streamline operations through intelligent automation and cloud solutions.

I want to create a professional video showcasing:
- Our modern office and team collaboration
- AI solutions in action
- Client testimonials
- Our technical expertise

The video should convey innovation and professional excellence.
"""

# Generate complete video workflow
final_video_path = run_quick_workflow(user_input)
print(f"Your video is ready: {final_video_path}")
```

### Method 2: Interactive Script

```bash
python demo_workflow.py
```

Choose from:
1. **Complete Demo** - Full workflow with sample company
2. **Step-by-Step** - See each stage of the process
3. **Custom Business** - Enter your own business information

### Method 3: Step-by-Step Control

```python
from integrated_video_workflow import IntegratedVideoWorkflow

# Initialize workflow
workflow = IntegratedVideoWorkflow()

# Step 1: Initialize clients
workflow.initialize_clients()

# Step 2: Generate prompts
prompts = workflow.generate_video_prompts(user_input)

# Step 3: Generate videos (this takes time!)
video_paths = workflow.generate_all_videos(prompts)

# Step 4: Merge videos
final_video = workflow.merge_videos(video_paths)
```

## 📁 Output Structure

Each workflow run creates a timestamped directory:
```
generated_videos_20241119_143022/
├── generated_prompts.json          # Generated scene prompts
├── scene_1_20241119_143022.mp4    # Individual scene videos
├── scene_2_20241119_143022.mp4
├── scene_3_20241119_143022.mp4
├── scene_4_20241119_143022.mp4
├── merged_final_video_20241119_143022.mp4  # Final merged video
└── workflow_summary.json          # Complete workflow report
```

## 🎯 Workflow Process

1. **Prompt Generation** (30 seconds)
   - Analyzes your business description
   - Creates 4 unique, contextually relevant scene prompts
   - Each scene showcases different aspects of your business

2. **Video Generation** (8-20 minutes total)
   - Generates 4 individual videos using Veo 3.1
   - Each video is 8 seconds long, professional quality
   - Downloads videos to local storage

3. **Video Merging** (1-2 minutes)
   - Combines all videos with smooth transitions
   - Applies crossfade effects between scenes
   - Outputs final polished video

## 📝 Input Guidelines

For best results, include:

- **Company Description**: What you do, your industry
- **Services/Products**: Key offerings you want to highlight  
- **Target Audience**: Who you're trying to reach
- **Video Goals**: What message you want to convey
- **Specific Scenes**: Any particular scenarios you want included

### Example Input:
```
I run Green Garden Cafe, a sustainable farm-to-table restaurant in downtown.
We source ingredients locally, offer organic dishes, and create a cozy atmosphere.

Services: Fresh breakfast/lunch, organic coffee, catering, private events
Target: Health-conscious families and professionals
Goals: Showcase freshness, sustainability, and welcoming atmosphere

Specific scenes I'd like:
- Chef preparing fresh ingredients
- Happy customers enjoying meals
- Cozy restaurant interior
- Local sourcing/sustainability focus
```

## ⚙️ Configuration Options

### Video Settings
```python
# In integrated_video_workflow.py

# Change video duration (default: 8 seconds per scene)
# This is set in the Veo 3.1 model - currently fixed at 8s

# Change aspect ratio
config=GenerateVideosConfig(
    aspect_ratio="16:9",  # Options: "16:9", "9:16", "1:1"
    output_gcs_uri=output_gcs_uri,
)

# Change transition duration
final_video = workflow.merge_videos(video_paths, transition_duration=0.5)  # Default: 0.3s
```

### Output Settings
```python
# Change project directory
workflow = IntegratedVideoWorkflow(project_dir="your/custom/path")

# Change GCS bucket
self.gcs_input_uri = "gs://your-bucket/your-image.jpg"
self.gcs_output_base = "gs://your-bucket/output/"
```

## 🔧 Troubleshooting

### Common Issues:

1. **"GOOGLE_API_KEY not found"**
   - Create `.env` file with your Gemini API key
   - Ensure the file is in the same directory as your scripts

2. **"Failed to initialize clients"**
   - Check Google Cloud authentication: `gcloud auth application-default login`
   - Verify project ID and region in the code

3. **"Image not found at GCS URI"**
   - Upload an image to your GCS bucket
   - Update `INPUT_GCS_URI` with correct path

4. **Video generation takes too long**
   - Veo 3.1 typically takes 2-5 minutes per video
   - Total workflow: 8-20 minutes for 4 videos
   - This is normal for high-quality AI video generation

5. **Merge fails**
   - Ensure moviepy is installed: `pip install moviepy`
   - Check that generated video files exist and aren't corrupted

## 📊 Performance Notes

- **Total Time**: 10-25 minutes for complete workflow
- **Video Quality**: Professional, 8 seconds per scene, 16:9 aspect ratio
- **File Sizes**: ~10-50MB per individual video, ~50-200MB final video
- **Cost**: Depends on Google Cloud usage (Veo 3.1 + storage + API calls)

## 🔄 Advanced Usage

### Batch Processing Multiple Companies:
```python
companies = [
    {"name": "TechCorp", "description": "Software development..."},
    {"name": "GreenCafe", "description": "Sustainable restaurant..."},
    # Add more...
]

for company in companies:
    try:
        video_path = run_quick_workflow(company["description"])
        print(f"✅ {company['name']}: {video_path}")
    except Exception as e:
        print(f"❌ {company['name']}: {e}")
```

### Custom Scene Types:
Modify the system prompt in `video_prompt_generator.py` to focus on specific scene types:
```python
system_prompt = f"""
Create 4 video scenes focusing specifically on:
1. Product demonstration
2. Customer testimonials  
3. Behind-the-scenes operations
4. Call-to-action/contact information
...
"""
```

## 📞 Support

For issues or questions:
1. Check this README for common solutions
2. Verify all prerequisites are met
3. Test with provided demo scripts first
4. Check Google Cloud logs for API errors

## 🎉 Success Tips

- **Be Specific**: More detailed business descriptions = better scene prompts
- **Test First**: Run demo scripts before using your own content
- **Monitor Progress**: The workflow provides detailed status updates
- **Check Output**: Review individual videos before merging if needed
- **Backup Important**: Save successful outputs as the process takes time

---

**Happy Video Creating! 🎬**