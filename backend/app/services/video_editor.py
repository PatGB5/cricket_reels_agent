from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
import os
import asyncio
from datetime import datetime

async def overlay_images_on_video(base_video_path, facts):
    loop = asyncio.get_event_loop()
    base = await loop.run_in_executor(None, VideoFileClip, base_video_path)
    overlays = []

    for fact in facts:
        if not fact["image_path"]:
            continue
        img_clip = (
            ImageClip(fact["image_path"])
            .set_start(fact["start"] + 2)
            .set_duration(4)
            .resize(height=300)
            .set_position(("center", "bottom"))
        )
        overlays.append(img_clip)

    final = CompositeVideoClip([base] + overlays)
    
    os.makedirs("data/final_videos", exist_ok=True)  # ✅ Ensure folder
    filename = f"edited_reel_{datetime.now().strftime('%Y-%m-%d')}.mp4"
    save_path = os.path.join("data", "final_videos", filename)

    await loop.run_in_executor(
        None,
        lambda: final.write_videofile(save_path, codec="libx264", audio_codec="aac")
    )

    return save_path
