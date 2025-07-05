from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, Form, Request  # Add Request
from fastapi.responses import FileResponse, JSONResponse  # Add JSONResponse
from app.services.script_generator import generate_script_and_images
from app.services.transcriber import get_fact_timestamps
from app.services.video_editor import overlay_images_on_video
from app.services.video_generator import create_heygen_video
from datetime import datetime
import os
import shutil
import json
from fastapi.staticfiles import StaticFiles

# Ensure directory exists
os.makedirs("data/base_videos", exist_ok=True)
os.makedirs("data/final_videos", exist_ok=True)

# Mount static directory
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. You can set specific origins like ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_script/")
async def generate_script(extra_prompt: str = Form("")):
    script, path = await generate_script_and_images(extra_prompt)
    return {"status": "success", "script_path": path, "script": script}

@app.post("/edit_video/")
async def edit_video(request: Request):
    # Load today's script file
    today_str = datetime.now().strftime("%Y%m%d")
    script_path = f"data/scripts/{today_str}_script.json"

    if not os.path.exists(script_path):
        return {"status": "error", "message": f"Script not found: {script_path}"}

    with open(script_path, "r") as f:
        script_data = json.load(f)

    facts = script_data.get("facts", [])
    if not facts:
        return {"status": "error", "message": "No facts found in script"}

    # Find the latest base video
    base_dir = "data/base_videos"
    latest_video = max(
        (os.path.join(base_dir, f) for f in os.listdir(base_dir) if os.path.isfile(os.path.join(base_dir, f))),
        key=os.path.getctime,
        default=None
    )

    if not latest_video:
        return {"status": "error", "message": "No base video found"}

    # Timestamp & overlay
    updated_facts = await get_fact_timestamps(latest_video, facts)
    final_path = await overlay_images_on_video(latest_video, updated_facts)

    # Generate public URL
    public_url = f"{request.base_url}final/{os.path.basename(final_path)}"
    return {
        "status": "edited",
        "final_url": public_url
    }
    
@app.post("/create_video/")
async def create_video(request: Request, script: str = Form(...)):
    try:
        print("📤 Received script:", script)

        # Download video and get absolute save path
        video_path = await create_heygen_video(script)

        # Generate preview URL for frontend
        filename = os.path.basename(video_path)
        preview_url = f"{request.base_url}videos/{filename}"

        print("✅ Video created successfully:", preview_url)
        return {"status": "created", "download_url": preview_url}
    except Exception as e:
        print("❌ Error creating video:", str(e))
        return {"status": "error", "message": str(e)}
    
    
app.mount("/videos", StaticFiles(directory="data/base_videos"), name="videos")
app.mount("/final", StaticFiles(directory="data/final_videos"), name="final")