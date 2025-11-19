import os
import sys
import argparse
from datetime import datetime
import glob

# Import merge helper from the repo
try:
    from merge import merge_videos
except Exception as e:
    print("Failed to import merge_videos from merge.py:", e)
    sys.exit(2)


def find_scene_files(output_dir: str):
    pattern = os.path.join(output_dir, "scene_*.mp4")
    files = glob.glob(pattern)
    if not files:
        return []
    # Sort by scene number extracted from filename
    def scene_key(path):
        # filename like scene_1_20251119_213401.mp4 or scene_1_20251119_213401.mp4
        name = os.path.basename(path)
        parts = name.split("_")
        try:
            # second element should be scene number
            return int(parts[1])
        except Exception:
            return name
    files_sorted = sorted(files, key=scene_key)
    return files_sorted


def main():
    parser = argparse.ArgumentParser(description="Merge existing scene_*.mp4 files in an output directory")
    parser.add_argument("--output_dir", required=True, help="Path to the generated videos folder (example: generated_videos_20251119_213401)")
    parser.add_argument("--transition", default="crossfade", choices=["crossfade","fade_black","simple"], help="Transition type")
    parser.add_argument("--duration", type=float, default=0.3, help="Transition duration in seconds")

    args = parser.parse_args()
    out_dir = os.path.abspath(args.output_dir)
    if not os.path.isdir(out_dir):
        print(f"Output directory not found: {out_dir}")
        sys.exit(1)

    print(f"Looking for scene files in: {out_dir}")
    scene_files = find_scene_files(out_dir)
    if not scene_files:
        print("No scene_*.mp4 files found. Aborting.")
        sys.exit(1)

    print("Found scene files:")
    for p in scene_files:
        print(" -", p)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(out_dir, f"merged_resume_{ts}.mp4")

    try:
        print("Merging videos...")
        merged = merge_videos(video_paths=scene_files, output_path=output_path, transition_type=args.transition, transition_duration=args.duration)
        print(f"✅ Merged video created: {merged}")
    except Exception as e:
        print("❌ Error while merging:", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
