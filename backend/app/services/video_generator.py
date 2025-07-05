import os
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.heygen.com/v2"
API_KEY = os.getenv("HEYGEN_API_KEY")

HEADERS = {
    "x-api-key": API_KEY,
    "content-type": "application/json",
    "accept": "application/json"
}

async def create_heygen_video(script_text):
    # Step 1: Create the video job
    payload = {
        "caption": False,
        "video_inputs": [
            {
                "character": {
                    "type": "avatar",
                    "avatar_id": "Brent_sitting_office_front",
                    "avatar_style": "normal"
                },
                "voice": {
                    "type": "text",
                    "input_text": script_text,
                    "voice_id": "22e53b7815a9477b82245ff9ed6bf2c6",
                    "speed": 1.0
                }
            }
        ],
        "dimension": {
            "width": 720,
            "height": 1280
        }
    }

    response = requests.post(f"{BASE_URL}/video/generate", json=payload, headers=HEADERS)
    response.raise_for_status()
    video_id = response.json()["data"]["video_id"]

    # Step 2: Poll for completion
    print("⏳ Generating video on HeyGen...")
    while True:
        status = requests.get(
            "https://api.heygen.com/v1/video_status.get",
            params={"video_id": video_id},
            headers=HEADERS
        )
        status.raise_for_status()
        data = status.json()["data"]
        if data["status"] == "completed":
            video_url = data["video_url"]
            print("✅ Video generation complete.")
            break
        elif data["status"] == "failed":
            raise RuntimeError(f"HeyGen video generation failed: {data.get('error')}")
        time.sleep(3)

    # Step 3: Download the video
    filename = f"heygen_reel_{datetime.now().strftime('%Y-%m-%d')}.mp4"
    save_dir = "data/base_videos"
    os.makedirs(save_dir, exist_ok=True)  # ✅ Ensure dir exists
    save_path = os.path.join(save_dir, filename)

    await download_video(video_url, save_path)
    return save_path


async def download_video(video_url, save_path):
    print("⬇️ Downloading video...")
    response = requests.get(video_url, stream=True)
    response.raise_for_status()

    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"📁 Video saved to {save_path}")
