import time
import os
from datetime import datetime
from google import genai
from google.genai.types import GenerateVideosConfig, Image
from google.cloud import storage
from google.api_core.exceptions import NotFound

# ========== CONFIG ==========
PROJECT_DIR = r"E:\AsapStudio\AiVideoProject"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOCAL_DOWNLOAD_PATH = os.path.join(PROJECT_DIR, f"veo_output_{TIMESTAMP}.mp4")

INPUT_GCS_URI = "gs://abd756/shared image.jpg"
OUTPUT_GCS_URI = "gs://abd756/veo_output/"

# Updated prompt for walking lecture about life
PROMPT = "Cutting-Edge AI Solutions Showcase**\n\n*   **Setting/Environment:** A modern, minimalist office space with large glass windows overlooking a vibrant cityscape at dusk. The office features sleek workstations with multiple monitors displaying complex data visualizations and AI-generated graphics.\n*   **Presenter/Character Details:** A confident and approachable woman in her late 30s, dressed in smart casual attire (e.g., a tailored blazer over a blouse and dark trousers). She is the lead AI Solutions Architect at AssapStudios. She maintains direct eye contact with the camera, with a warm and reassuring smile.\n*   **Lighting Setup and Visual Style:** Soft, diffused lighting with a warm color temperature to create a welcoming and innovative atmosphere. The AI visualizations on the monitors should emit a subtle glow, adding depth to the scene. The visual style should be clean and modern, emphasizing the technological sophistication of AssapStudios.\n*   **Camera Movements and Angles:** Medium shot, focusing on the presenter and the AI visualizations in the background. A slow, steady cinematic push-in movement toward the presenter as she speaks.\n*   **Script/Message Integration:** The presenter gestures towards a monitor displaying a complex AI algorithm and says: \"At AssapStudios, we're revolutionizing businesses with cutting-edge AI solutions, tailored to your specific needs.\"\n*   **Duration:** 8 seconds\n*   **Aesthetic Notes:** Photorealistic with natural micro-movements (gentle hand gestures, slight head tilts). Professional, modern, visually appealing aesthetic. Steady camera with light cinematic push-in movement. Continuous, natural shots without fast motion. No background music or fade-ins.\n\n**"
# ...existing code...



# ============================


def debug(msg: str, success: bool = True):
    """Unified debug message format."""
    prefix = "✅" if success else "❌"
    print(f"{prefix} [DEBUG] {msg}")


def extract_bucket_blob(gcs_uri):
    """Extract bucket and blob name from gs:// URI."""
    parts = gcs_uri.replace("gs://", "").split("/", 1)
    return parts[0], parts[1]


def main():
    print("\n🚀 Starting Veo 3.1 video generation script...\n")

    # --- STEP 1: Initialize Clients ---
    try:
        debug("Initializing Google GenAI and Storage clients...")
        client = genai.Client(
    vertexai=True,
    project="gen-lang-client-0207694487",
    location="us-central1"  # recommended region for Veo models
)
        storage_client = storage.Client()
        debug("Clients initialized successfully.")
    except Exception as e:
        debug(f"Failed to initialize clients: {e}", success=False)
        return

    # --- STEP 2: Validate input image existence ---
    try:
        bucket_name, blob_name = extract_bucket_blob(INPUT_GCS_URI)
        bucket = storage_client.bucket(bucket_name)
        if not bucket.blob(blob_name).exists():
            raise NotFound(f"Image not found at {INPUT_GCS_URI}")
        debug(f"Confirmed input image exists at {INPUT_GCS_URI}")
    except Exception as e:
        debug(f"Error verifying input image: {e}", success=False)
        return

    # --- STEP 3: Start video generation ---
    try:
        debug("Submitting video generation request to Veo 3.1...")

        operation = client.models.generate_videos(
            model="veo-3.1-generate-preview",
            prompt=PROMPT,
            # image=Image(
            #     gcs_uri=INPUT_GCS_URI,
            #     mime_type="image/jpg",
            # ),
            config=GenerateVideosConfig(
                aspect_ratio="16:9",
                output_gcs_uri=OUTPUT_GCS_URI,                                                                                                                                                                                                                  
            ),
        )

        debug("Video generation started successfully.")
    except Exception as e:
        debug(f"Failed to start video generation: {e}", success=False)
        return

    # --- STEP 4: Poll for completion ---
    try:
        debug("Polling for video generation completion (this may take 2–5 minutes)...")
        while not operation.done:
            time.sleep(20)
            operation = client.operations.get(operation)
            print(operation)

        debug("Video generation operation completed.")
    except Exception as e:
        debug(f"Error while polling operation: {e}", success=False)
        return

    # --- STEP 5: Handle result ---
    try:
        if operation.response:
            gcs_video_uri = operation.result.generated_videos[0].video.uri
            debug(f"Video generated successfully at: {gcs_video_uri}")

            # --- STEP 6: Download video locally ---
            if gcs_video_uri.startswith("gs://"):
                bucket_name, blob_name = extract_bucket_blob(gcs_video_uri)
                bucket = storage_client.bucket(bucket_name)
                blob = bucket.blob(blob_name)

                debug(f"Downloading video to local path: {LOCAL_DOWNLOAD_PATH}")
                blob.download_to_filename(LOCAL_DOWNLOAD_PATH)

                debug(f"Download complete. Saved at:\n{LOCAL_DOWNLOAD_PATH}")
            else:
                debug("Invalid GCS URI format.", success=False)
        else:
            debug("Video generation returned no response.", success=False)
    except Exception as e:
        debug(f"Error handling result: {e}", success=False)


if __name__ == "__main__":
    main()
