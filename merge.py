
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip

def apply_crossfade_transition(clips, transition_duration):
    """Apply crossfade transition between clips"""
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

def apply_fade_to_black_transition(clips, transition_duration):
    """Apply fade to black transition between clips"""
    if len(clips) < 2:
        return clips[0] if clips else None
    
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
    
    # Concatenate clips (fade to black will happen naturally due to fadeout/fadein)
    return concatenate_videoclips(processed_clips, method="compose")

def apply_simple_transition(clips, transition_duration):
    """Apply simple fade transitions"""
    if len(clips) < 2:
        return clips[0] if clips else None
    
    processed_clips = []
    
    for i, clip in enumerate(clips):
        current_clip = clip
        
        # Add slight fade effects for smoother transitions
        if i > 0:  # Add fadein to all clips except first
            current_clip = current_clip.fadein(transition_duration / 2)
        if i < len(clips) - 1:  # Add fadeout to all clips except last
            current_clip = current_clip.fadeout(transition_duration / 2)
        
        processed_clips.append(current_clip)
    
    return concatenate_videoclips(processed_clips, method="compose")


# --- MAIN MERGE FUNCTION FOR WORKFLOW USAGE ---
def merge_videos(
    video_paths,
    output_path,
    transition_type="crossfade",
    transition_duration=0.3
):
    """
    Merge a list of video files with transitions and save to output_path.
    Args:
        video_paths: List of video file paths to merge (in order)
        output_path: Output file path for merged video
        transition_type: 'crossfade', 'fade_black', or 'simple'
        transition_duration: Duration of transition in seconds
    Returns:
        output_path if successful
    """
    if not video_paths:
        raise ValueError("No video files provided for merging.")
    for path in video_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Video file not found: {path}")
    video_clips = [VideoFileClip(path) for path in video_paths]
    if transition_type == "crossfade":
        final_clip = apply_crossfade_transition(video_clips, transition_duration)
    elif transition_type == "fade_black":
        final_clip = apply_fade_to_black_transition(video_clips, transition_duration)
    else:
        final_clip = apply_simple_transition(video_clips, transition_duration)
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
    for clip in video_clips:
        clip.close()
    final_clip.close()
    return output_path