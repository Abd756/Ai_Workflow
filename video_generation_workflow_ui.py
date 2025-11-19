import streamlit as st
from datetime import datetime
import os
from video_prompt_generator import VideoPromptGenerator, VideoScenePrompts
from integrated_video_workflow import IntegratedVideoWorkflow


# Helper: safe rerun to support multiple Streamlit versions
def safe_rerun():
    """Attempt to rerun the Streamlit script in a compatible way.

    Tries `experimental_rerun` first, then `rerun`. If neither exists, falls
    back to `st.stop()` which halts execution (user can refresh).
    """
    try:
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
            return
    except Exception:
        pass
    try:
        if hasattr(st, "rerun"):
            st.rerun()
            return
    except Exception:
        pass
    # Last resort: stop execution (safe fallback)
    try:
        st.stop()
    except Exception:
        # If even stop isn't available, raise a clear error so caller can handle it
        raise RuntimeError("Streamlit rerun/stop not available in this environment")

st.set_page_config(
    page_title="AI Video Generation Workflow",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .success-message {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .video-card {
        background: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        padding: 1rem;
        margin-bottom: 1.5rem;
        border-left: 5px solid #764ba2;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎬 AI Video Generation Workflow</h1>
    <p>Generate, review, and merge professional AI videos step by step</p>
    <small>💡 Powered by Gemini & Veo 3.1</small>
</div>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
def init_state():
    if 'workflow' not in st.session_state:
        st.session_state.workflow = None
    if 'prompts' not in st.session_state:
        st.session_state.prompts = None
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    if 'video_paths' not in st.session_state:
        st.session_state.video_paths = [None, None, None, None]
    if 'video_ready' not in st.session_state:
        st.session_state.video_ready = [False, False, False, False]
    if 'video_generating' not in st.session_state:
        st.session_state.video_generating = [False, False, False, False]
    if 'video_errors' not in st.session_state:
        st.session_state.video_errors = [None, None, None, None]
    if 'merged_video_path' not in st.session_state:
        st.session_state.merged_video_path = None
    if 'merged_video_ready' not in st.session_state:
        st.session_state.merged_video_ready = False
    if 'merged_video_generating' not in st.session_state:
        st.session_state.merged_video_generating = False
    if 'merged_video_error' not in st.session_state:
        st.session_state.merged_video_error = None
init_state()

# --- PROMPT GENERATION ---
st.subheader("📝 Enter Your Script/Business Description")
user_input = st.text_area(
    "Describe your business and video goals:",
    placeholder="Enter your company description, script, and any requirements...",
    height=200,
    value=st.session_state.user_input
)

if st.button("🚀 Generate Prompts", type="primary", use_container_width=True, disabled=not user_input or len(user_input.split()) < 15):
    with st.spinner("Generating video prompts..."):
        try:
            generator = VideoPromptGenerator()
            prompts = generator.generate_video_prompts(user_input)
            st.session_state.prompts = prompts
            st.session_state.user_input = user_input
            st.session_state.video_paths = [None, None, None, None]
            st.session_state.video_ready = [False, False, False, False]
            st.session_state.video_generating = [False, False, False, False]
            st.session_state.video_errors = [None, None, None, None]
            st.session_state.merged_video_path = None
            st.session_state.merged_video_ready = False
            st.session_state.merged_video_generating = False
            st.session_state.merged_video_error = None
            st.session_state.workflow = IntegratedVideoWorkflow(enable_debugger=False)
            st.success("Prompts generated! Proceed to video generation below.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

if st.session_state.prompts:
    prompts = st.session_state.prompts
    scenes = [
        ("Scene 1", prompts.prompt_1, "🌟"),
        ("Scene 2", prompts.prompt_2, "🎯"),
        ("Scene 3", prompts.prompt_3, "✅"),
        ("Scene 4", prompts.prompt_4, "🚀")
    ]
    st.markdown("""
    <div class="success-message">
        <h3>🎉 Prompts Ready!</h3>
        <p>Generate each video below. Review before proceeding to the next.</p>
    </div>
    """, unsafe_allow_html=True)
    for idx, (title, prompt, emoji) in enumerate(scenes):
        st.markdown(f"<div class='prompt-card'><div class='scene-title'>{emoji} {title}</div><div style='color:#666;line-height:1.6;'>{prompt[:200]}{'...' if len(prompt) > 200 else ''}</div></div>", unsafe_allow_html=True)
        # Video generation button and display
        if st.session_state.video_ready[idx]:
            st.markdown(f"<div class='video-card'><b>{emoji} {title} Video:</b>", unsafe_allow_html=True)
            st.video(st.session_state.video_paths[idx])
            st.markdown("</div>", unsafe_allow_html=True)
        elif st.session_state.video_generating[idx]:
            st.info(f"⏳ Generating {title} video... This may take a few minutes.")
        else:
            # Only enable if previous video is ready or this is the first
            prev_ready = True if idx == 0 else st.session_state.video_ready[idx-1]
            if prev_ready:
                if st.button(f"🎥 Generate {title} Video", key=f"gen_btn_{idx}"):
                    st.session_state.video_generating[idx] = True
                    safe_rerun()
            else:
                st.warning("Please generate the previous video first.")
        # Handle video generation logic
        if st.session_state.video_generating[idx] and not st.session_state.video_ready[idx]:
            try:
                with st.spinner(f"Generating video for {title}..."):
                    workflow = st.session_state.workflow
                    workflow.initialize_clients()
                    video_path = workflow.generate_single_video(prompt, idx+1)
                    st.session_state.video_paths[idx] = video_path
                    st.session_state.video_ready[idx] = True
                    st.session_state.video_generating[idx] = False
                    st.success(f"{title} video generated!")
                    safe_rerun()
            except Exception as e:
                st.session_state.video_errors[idx] = str(e)
                st.session_state.video_generating[idx] = False
                st.error(f"❌ Error generating {title} video: {e}")
    # After all videos are ready, show merge option
    if all(st.session_state.video_ready):
        st.markdown("---")
        st.markdown("<div class='success-message'><h3>🎬 All Videos Ready!</h3><p>Click below to merge all scenes into a final video.</p></div>", unsafe_allow_html=True)
        if st.session_state.merged_video_ready and st.session_state.merged_video_path:
            st.success("🎉 Merged video ready!")
            st.video(st.session_state.merged_video_path)
            st.markdown(f"<a href='{st.session_state.merged_video_path}' download>📥 Download Final Video</a>", unsafe_allow_html=True)
        elif st.session_state.merged_video_generating:
            st.info("⏳ Merging videos... This may take a minute.")
        else:
            if st.button("🔗 Merge All Videos", type="primary"):
                st.session_state.merged_video_generating = True
                safe_rerun()
        # Handle merging logic
        if st.session_state.merged_video_generating and not st.session_state.merged_video_ready:
            try:
                with st.spinner("Merging all videos. This may take a minute..."):
                    workflow = st.session_state.workflow
                    merged_path = workflow.merge_videos(st.session_state.video_paths)
                    st.session_state.merged_video_path = merged_path
                    st.session_state.merged_video_ready = True
                    st.session_state.merged_video_generating = False
                    st.success("Merged video created!")
                    safe_rerun()
            except Exception as e:
                st.session_state.merged_video_error = str(e)
                st.session_state.merged_video_generating = False
                st.error(f"❌ Error merging videos: {e}")
    # Show errors if any
    for idx, err in enumerate(st.session_state.video_errors):
        if err:
            st.error(f"❌ Error: {err}")
    if st.session_state.merged_video_error:
        st.error(f"❌ Error: {st.session_state.merged_video_error}")
