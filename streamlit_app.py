import streamlit as st
import time
import json
from datetime import datetime
import os
from typing import Dict, Any

# Import your existing modules
try:
    from video_prompt_generator import VideoPromptGenerator, VideoScenePrompts
    from cost_tracker import APISpendingTracker
except ImportError:
    st.error("❌ Unable to import required modules. Please ensure all modules are available.")

# Page configuration
st.set_page_config(
    page_title="AI Video Workflow Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .prompt-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .scene-title {
        color: #667eea;
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 0.5rem;
    }
    
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2rem;
    }
    
    .stats-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-message {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'prompts_generated' not in st.session_state:
        st.session_state.prompts_generated = False
    if 'generated_prompts' not in st.session_state:
        st.session_state.generated_prompts = None
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'generation_timestamp' not in st.session_state:
        st.session_state.generation_timestamp = None

def display_loading_animation():
    """Display attractive loading animation."""
    loading_placeholder = st.empty()
    
    # Loading messages to cycle through
    loading_messages = [
        "🧠 Analyzing your business description...",
        "🎯 Understanding your target audience...",
        "🎨 Crafting creative scene concepts...", 
        "📝 Generating professional video prompts...",
        "✨ Adding cinematic details...",
        "🎬 Finalizing your video scenes..."
    ]
    
    progress_bar = st.progress(0)
    
    for i, message in enumerate(loading_messages):
        with loading_placeholder.container():
            st.markdown(f"""
            <div class="loading-container">
                <h3 style="color: #667eea;">{message}</h3>
                <div style="margin: 1rem 0;">
                    <div style="font-size: 2rem;">
                        {"🔄" if i % 2 == 0 else "⚡"}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        progress = (i + 1) / len(loading_messages)
        progress_bar.progress(progress)
        time.sleep(0.8)  # Simulate processing time
    
    loading_placeholder.empty()
    progress_bar.empty()

def display_prompts_attractively(prompts: VideoScenePrompts):
    """Display generated prompts in an attractive format."""
    
    st.markdown("""
    <div class="success-message">
        <h3>🎉 Video Prompts Generated Successfully!</h3>
        <p>Your AI-powered video scenes are ready. Each prompt is crafted specifically for your business and goals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Scene Overview", "📊 Prompt Details", "💾 Export Options"])
    
    with tab1:
        st.subheader("🎬 Your Video Scene Collection")
        
        scenes = [
            ("Scene 1: Opening Impact", prompts.prompt_1, "🌟"),
            ("Scene 2: Core Message", prompts.prompt_2, "🎯"), 
            ("Scene 3: Proof & Trust", prompts.prompt_3, "✅"),
            ("Scene 4: Call to Action", prompts.prompt_4, "🚀")
        ]
        
        cols = st.columns(2)
        
        for i, (title, prompt, emoji) in enumerate(scenes):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="prompt-card">
                    <div class="scene-title">{emoji} {title}</div>
                    <div style="color: #666; line-height: 1.6;">
                        {prompt[:200]}{"..." if len(prompt) > 200 else ""}
                    </div>
                    <div style="margin-top: 1rem; font-size: 0.9em; color: #888;">
                        Length: {len(prompt)} characters
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.subheader("📝 Complete Prompt Details")
        
        for i, (title, prompt, emoji) in enumerate(scenes, 1):
            with st.expander(f"{emoji} Scene {i}: View Full Prompt", expanded=False):
                st.markdown(f"**{title}**")
                st.text_area(
                    f"Full prompt for Scene {i}:",
                    value=prompt,
                    height=150,
                    key=f"prompt_{i}",
                    disabled=True
                )
                
                # Prompt statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Characters", len(prompt))
                with col2:
                    st.metric("Words", len(prompt.split()))
                with col3:
                    st.metric("Lines", prompt.count('\n') + 1)
    
    with tab3:
        st.subheader("💾 Export & Save Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📋 Copy Individual Prompts:**")
            for i, (title, prompt, emoji) in enumerate(scenes, 1):
                if st.button(f"📋 Copy Scene {i}", key=f"copy_{i}"):
                    st.code(prompt, language="text")
                    st.success(f"✅ Scene {i} prompt ready to copy!")
        
        with col2:
            st.markdown("**📄 Download Options:**")
            
            # Prepare data for download
            prompts_dict = {
                "generation_info": {
                    "timestamp": st.session_state.generation_timestamp,
                    "user_input": st.session_state.user_input[:100] + "..." if len(st.session_state.user_input) > 100 else st.session_state.user_input
                },
                "prompts": {
                    "scene_1": prompts.prompt_1,
                    "scene_2": prompts.prompt_2,
                    "scene_3": prompts.prompt_3,
                    "scene_4": prompts.prompt_4
                }
            }
            
            # JSON download
            json_data = json.dumps(prompts_dict, indent=2)
            st.download_button(
                label="📥 Download as JSON",
                data=json_data,
                file_name=f"video_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # Text download
            text_data = f"""AI Video Prompts Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

User Input: {st.session_state.user_input}

==========================================

SCENE 1: Opening Impact
{prompts.prompt_1}

==========================================

SCENE 2: Core Message  
{prompts.prompt_2}

==========================================

SCENE 3: Proof & Trust
{prompts.prompt_3}

==========================================

SCENE 4: Call to Action
{prompts.prompt_4}

==========================================

Generated by AI Video Workflow Studio
"""
            
            st.download_button(
                label="📄 Download as Text",
                data=text_data,
                file_name=f"video_prompts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

def display_cost_estimate(user_input: str):
    """Display real-time cost estimates."""
    if user_input and len(user_input.strip()) > 10:
        try:
            tracker = APISpendingTracker()
            estimate = tracker.estimate_complete_workflow_cost(user_input)
            
            st.sidebar.markdown("### 💰 Cost Estimate")
            
            # Prompt generation cost (very small)
            prompt_cost = estimate['breakdown']['prompt_generation']['total_cost']
            st.sidebar.markdown(f"""
            <div class="stats-card">
                <strong>📝 Prompt Generation:</strong><br>
                💸 ~${prompt_cost:.4f}<br>
                🔢 ~{estimate['breakdown']['prompt_generation']['input_tokens']:,} input tokens<br>
                🔢 ~{estimate['breakdown']['prompt_generation']['output_tokens']:,} output tokens
            </div>
            """, unsafe_allow_html=True)
            
            # Video generation cost (major cost)
            video_cost = estimate['breakdown']['video_generation']['total_cost']
            st.sidebar.markdown(f"""
            <div class="stats-card" style="border-left: 3px solid #ff6b6b;">
                <strong>🎥 Video Generation:</strong><br>
                💸 ~${video_cost:.2f} (4 videos)<br>
                📹 ~${video_cost/4:.2f} per video<br>
                ⚠️ <em>Major cost component</em>
            </div>
            """, unsafe_allow_html=True)
            
            # Total estimate
            total_cost = estimate['total_estimated_cost']
            st.sidebar.markdown(f"""
            <div class="stats-card" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white;">
                <strong>🎯 Total Workflow:</strong><br>
                💰 ~${total_cost:.2f}<br>
                📊 Videos: {(video_cost/total_cost)*100:.0f}% of cost
            </div>
            """, unsafe_allow_html=True)
            
            # Cost-saving tips
            st.sidebar.markdown("""  
            <div style="font-size: 0.85em; color: #666; margin-top: 1rem;">
                💡 <strong>Cost Tips:</strong><br>
                • Prompts are very cheap (~$0.01)<br>
                • Videos are expensive (~$0.75 each)<br>
                • Use debugger to review before generating all videos<br>
                • Stop after first video if quality is poor
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.sidebar.error(f"Cost estimation error: {e}")

def display_prompt_statistics():
    """Display statistics about generated prompts."""
    if st.session_state.generated_prompts:
        prompts = st.session_state.generated_prompts
        
        st.sidebar.markdown("### 📊 Prompt Statistics")
        
        total_chars = len(prompts.prompt_1) + len(prompts.prompt_2) + len(prompts.prompt_3) + len(prompts.prompt_4)
        total_words = len(prompts.prompt_1.split()) + len(prompts.prompt_2.split()) + len(prompts.prompt_3.split()) + len(prompts.prompt_4.split())
        
        st.sidebar.markdown(f"""
        <div class="stats-card">
            <strong>Total Content:</strong><br>
            📝 {total_chars:,} characters<br>
            📖 {total_words:,} words<br>
            🎬 4 video scenes
        </div>
        """, unsafe_allow_html=True)
        
        st.sidebar.markdown(f"""
        <div class="stats-card">
            <strong>Generation Info:</strong><br>
            🕒 {st.session_state.generation_timestamp}<br>
            ⚡ Ready for video generation
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main Streamlit application."""
    initialize_session_state()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 AI Video Workflow Studio</h1>
        <p>Transform your business description into professional video prompts using AI</p>
        <small>💡 Prompts: ~$0.01 • Videos: ~$3.00 • Total workflow: ~$3.01</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🛠️ Workflow Studio")
    st.sidebar.markdown("---")
    
    # Enhanced step indicator for workflow progress
    video1_generating = st.session_state.get('video1_generating', False)
    video1_ready = st.session_state.get('video1_ready', False)
    video1_started = video1_generating or video1_ready

    if not st.session_state.prompts_generated:
        st.sidebar.info("📝 Step 1: Generate Prompts")
        st.sidebar.markdown("⏳ Step 2: Video Generation")
        st.sidebar.markdown("⏳ Step 3: Video Merging")
    elif not video1_started:
        st.sidebar.success("✅ Step 1: Prompts Generated")
        st.sidebar.info("🔜 Step 2: Video Generation")
        st.sidebar.info("🔜 Step 3: Video Merging (Coming Soon)")
    elif video1_generating:
        st.sidebar.success("✅ Step 1: Prompts Generated")
        st.sidebar.warning("⏳ Step 2: Video Generation in Progress...")
        st.sidebar.info("🔜 Step 3: Video Merging (Coming Soon)")
    elif video1_ready:
        st.sidebar.success("✅ Step 1: Prompts Generated")
        st.sidebar.success("✅ Step 2: 1st Video Generated")
        st.sidebar.info("🔜 Step 3: Video Merging (Coming Soon)")
    
    st.sidebar.markdown("---")
    
    # Main content area
    if not st.session_state.prompts_generated:
        # Input section
        st.subheader("📝 Tell Us About Your Business")
        
        # Example templates
        with st.expander("💡 See Example Inputs", expanded=False):
            st.markdown("""
            **Restaurant Example:**
            ```
            I run Green Garden Cafe, a sustainable farm-to-table restaurant in downtown. 
            We source ingredients locally, offer organic dishes, and create a cozy atmosphere 
            for families and professionals. I want videos showcasing our fresh ingredient 
            preparation, happy customers, cozy atmosphere, and sustainability commitment.
            ```
            
            **Tech Company Example:**
            ```
            I run TechFlow Solutions, a software development company specializing in AI automation. 
            We help businesses streamline operations through intelligent automation and cloud solutions. 
            I want professional videos showing our modern office, team collaboration, AI solutions 
            in action, and client testimonials that convey innovation and expertise.
            ```
            
            **Real Estate Example:**
            ```
            I run iCONNCT, a real estate technology platform that works like Uber for real estate. 
            We offer instant agent connections, video calls, and seamless property tours. 
            I want videos demonstrating our technology, showing agents helping clients, 
            property showcases, and satisfied customers.
            ```
            """)
        
        # Input form
        st.markdown("### ✍️ Your Business Description")
        
        user_input = st.text_area(
            "Describe your business and video goals:",
            placeholder="""Enter details about:
• Your company name and industry
• Main services or products you offer  
• Target audience (families, professionals, etc.)
• Specific scenes you'd like in the video
• The message you want to convey
• Any unique selling points to highlight

The more specific you are, the better your video prompts will be!""",
            height=200,
            key="user_input_field"
        )
        
        # Input validation and hints
        if user_input:
            word_count = len(user_input.split())
            char_count = len(user_input)
            
            # Display real-time cost estimate in sidebar
            display_cost_estimate(user_input)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if word_count >= 50:
                    st.success(f"✅ {word_count} words - Great detail!")
                elif word_count >= 25:
                    st.warning(f"⚠️ {word_count} words - Add more details")
                else:
                    st.error(f"❌ {word_count} words - Need more information")
            
            with col2:
                st.info(f"📊 {char_count} characters")
            
            with col3:
                if "company" in user_input.lower() or "business" in user_input.lower():
                    st.success("✅ Business context detected")
                else:
                    st.warning("⚠️ Add business context")
        
        # Generate button
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🚀 Generate Video Prompts", 
                type="primary", 
                use_container_width=True,
                disabled=not user_input or len(user_input.split()) < 15
            ):
                if user_input and len(user_input.split()) >= 15:
                    # Store user input
                    st.session_state.user_input = user_input
                    
                    # Show loading animation
                    display_loading_animation()
                    
                    # Generate prompts
                    try:
                        with st.spinner("🤖 AI is analyzing your business and generating prompts..."):
                            generator = VideoPromptGenerator()
                            prompts = generator.generate_video_prompts(user_input)
                        
                        # Log cost tracking
                        try:
                            tracker = APISpendingTracker()
                            # Convert prompts to string for cost calculation
                            prompts_text = f"{prompts.prompt_1} {prompts.prompt_2} {prompts.prompt_3} {prompts.prompt_4}"
                            cost_info = tracker.estimate_prompt_generation_cost(user_input, prompts_text)
                            tracker.log_actual_usage("Gemini 2.0 Flash - Prompt Generation", cost_info['total_cost'], {
                                "input_tokens": cost_info['input_tokens'],
                                "output_tokens": cost_info['output_tokens'],
                                "user_input_length": len(user_input)
                            })
                        except Exception as cost_error:
                            st.warning(f"Cost tracking failed: {cost_error}")
                        
                        # Store results
                        st.session_state.generated_prompts = prompts
                        st.session_state.prompts_generated = True
                        st.session_state.generation_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # Success message and rerun to show results
                        st.success("🎉 Prompts generated successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error generating prompts: {str(e)}")
                        st.markdown("""
                        **Troubleshooting:**
                        - Check your GOOGLE_API_KEY in .env file
                        - Ensure you have internet connection
                        - Verify your Google API quota
                        """)
                else:
                    st.warning("⚠️ Please provide a more detailed business description (at least 15 words).")
    
    else:
        # Display generated prompts
        display_prompts_attractively(st.session_state.generated_prompts)

        # --- VIDEO GENERATION & MERGING SECTION ---
        st.markdown("---")
        # Initialize session state for all videos and merging
        for i in range(1, 5):
            if f'video{i}_path' not in st.session_state:
                st.session_state[f'video{i}_path'] = None
                st.session_state[f'video{i}_ready'] = False
                st.session_state[f'video{i}_generating'] = False
                st.session_state[f'video{i}_error'] = None
        if 'merged_video_path' not in st.session_state:
            st.session_state.merged_video_path = None
            st.session_state.merged_video_ready = False
            st.session_state.merged_video_generating = False
            st.session_state.merged_video_error = None

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Generate New Prompts", type="secondary"):
                # Reset session state
                st.session_state.prompts_generated = False
                st.session_state.generated_prompts = None
                st.session_state.user_input = ""
                for i in range(1, 5):
                    st.session_state[f'video{i}_path'] = None
                    st.session_state[f'video{i}_ready'] = False
                    st.session_state[f'video{i}_generating'] = False
                    st.session_state[f'video{i}_error'] = None
                st.session_state.merged_video_path = None
                st.session_state.merged_video_ready = False
                st.session_state.merged_video_generating = False
                st.session_state.merged_video_error = None
                st.rerun()

        with col2:
            # Video generation buttons and display for each scene
            prompts = st.session_state.generated_prompts
            video_labels = [
                (1, "🎥 Generate 1st Video", "✅ 1st video generated!", prompts.prompt_1),
                (2, "🎥 Generate 2nd Video", "✅ 2nd video generated!", prompts.prompt_2),
                (3, "🎥 Generate 3rd Video", "✅ 3rd video generated!", prompts.prompt_3),
                (4, "🎥 Generate 4th Video", "✅ 4th video generated!", prompts.prompt_4),
            ]
            # Show all generated videos so far, and after each, show the continue button for the next (if not yet generated)
            for idx, (num, gen_label, ready_label, prompt) in enumerate(video_labels, 1):
                if st.session_state[f'video{num}_ready'] and st.session_state[f'video{num}_path']:
                    st.success(ready_label)
                    st.video(st.session_state[f'video{num}_path'])
                    with open(st.session_state[f'video{num}_path'], "rb") as f:
                        st.download_button(f"📥 Download {num} Video", f, file_name=os.path.basename(st.session_state[f'video{num}_path']))
                    # Show continue button for next video (if not last video and next not yet generated)
                    if num < 4 and not st.session_state[f'video{num+1}_ready'] and not st.session_state[f'video{num+1}_generating']:
                        if st.button(f"➡️ Continue to Next Video", key=f'continue_{num+1}'):
                            st.session_state[f'video{num+1}_generating'] = True
                            st.rerun()
            # Show the next available generate button (if no video is being generated and not all are ready)
            for idx, (num, gen_label, ready_label, prompt) in enumerate(video_labels, 1):
                prev_ready = True if num == 1 else st.session_state.get(f'video{num-1}_ready', False)
                if not st.session_state[f'video{num}_ready'] and not st.session_state[f'video{num}_generating'] and prev_ready:
                    if st.button(gen_label, key=f'gen_btn_{num}'):
                        st.session_state[f'video{num}_generating'] = True
                        st.rerun()
                    break
                elif st.session_state[f'video{num}_generating']:
                    st.info(f"⏳ Generating video {num}... This may take a few minutes.")
                    break
            # After all 4 videos are ready, show merge option
            if all(st.session_state[f'video{i}_ready'] for i in range(1, 5)):
                st.markdown("---")
                if not st.session_state.merged_video_ready and not st.session_state.merged_video_generating:
                    if st.button("🔗 Merge All Videos", type="primary"):
                        st.session_state.merged_video_generating = True
                        st.rerun()
                elif st.session_state.merged_video_generating:
                    st.info("⏳ Merging videos... This may take a minute.")
                elif st.session_state.merged_video_ready and st.session_state.merged_video_path:
                    st.success("🎉 Merged video ready!")
                    st.video(st.session_state.merged_video_path)
                    with open(st.session_state.merged_video_path, "rb") as f:
                        st.download_button("📥 Download Merged Video", f, file_name=os.path.basename(st.session_state.merged_video_path))

        with col3:
            if st.button("📋 Edit Input", type="secondary"):
                st.session_state.prompts_generated = False
                st.rerun()

        # Handle video generation logic for each video
        from integrated_video_workflow import IntegratedVideoWorkflow
        workflow = None
        for num in range(1, 5):
            if st.session_state[f'video{num}_generating'] and not st.session_state[f'video{num}_ready']:
                try:
                    with st.spinner(f"Generating video for Scene {num}. This may take several minutes..."):
                        if workflow is None:
                            workflow = IntegratedVideoWorkflow(enable_debugger=False)
                            workflow.initialize_clients()
                        prompt = getattr(st.session_state.generated_prompts, f'prompt_{num}')
                        video_path = workflow.generate_single_video(prompt, num)
                        st.session_state[f'video{num}_path'] = video_path
                        st.session_state[f'video{num}_ready'] = True
                        st.session_state[f'video{num}_error'] = None
                except Exception as e:
                    st.session_state[f'video{num}_error'] = str(e)
                # Always reset generating flag, even on error
                st.session_state[f'video{num}_generating'] = False
                st.rerun()
                break
        # Handle merging logic
        if st.session_state.merged_video_generating and not st.session_state.merged_video_ready:
            try:
                with st.spinner("Merging all videos. This may take a minute..."):
                    if workflow is None:
                        workflow = IntegratedVideoWorkflow(enable_debugger=False)
                        workflow.initialize_clients()
                    video_paths = [st.session_state[f'video{i}_path'] for i in range(1, 5)]
                    merged_path = workflow.merge_videos(video_paths)
                    st.session_state.merged_video_path = merged_path
                    st.session_state.merged_video_ready = True
                    st.session_state.merged_video_generating = False
                    st.session_state.merged_video_error = None
                    st.rerun()
            except Exception as e:
                st.session_state.merged_video_error = str(e)
                st.session_state.merged_video_generating = False
                st.error(f"❌ Error merging videos: {e}")

        # Show errors if any
        for num in range(1, 5):
            if st.session_state[f'video{num}_error']:
                st.error(f"❌ Error: {st.session_state[f'video{num}_error']}")
        if st.session_state.merged_video_error:
            st.error(f"❌ Error: {st.session_state.merged_video_error}")
    
    # Display statistics in sidebar
    display_prompt_statistics()
    
    # Show spending summary
    try:
        tracker = APISpendingTracker()
        summary = tracker.get_spending_summary(7)  # Last 7 days
        
        if summary['num_entries'] > 0:
            st.sidebar.markdown("### 📈 Recent Spending (7 days)")
            st.sidebar.markdown(f"""
            <div class="stats-card">
                <strong>Total Spent:</strong> ${summary['total_cost']:.4f}<br>
                <strong>API Calls:</strong> {summary['num_entries']}<br>
                <small>Click to view details</small>
            </div>
            """, unsafe_allow_html=True)
            
            with st.sidebar.expander("💸 Spending Details", expanded=False):
                for service, data in summary['by_service'].items():
                    avg_cost = data['total_cost'] / data['count'] if data['count'] > 0 else 0
                    st.write(f"**{service}:**")
                    st.write(f"• {data['count']} calls")
                    st.write(f"• ${data['total_cost']:.4f} total")
                    st.write(f"• ${avg_cost:.4f} average")
    except Exception as e:
        pass  # Silently fail if cost tracking isn't working
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <small>🎬 AI Video Workflow Studio | Powered by Google Gemini & Veo 3.1</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()