import whisper
from moviepy.editor import VideoFileClip
import os

async def get_fact_timestamps(video_path, facts):
    model = whisper.load_model("base")
    result =  model.transcribe(video_path)  # Assuming transcribe supports async
    transcript = result["text"].lower()

    updated_facts = []
    for fact in facts:
        snippet = fact["fact"][:12].lower()
        idx = transcript.find(snippet)
        if idx == -1:
            fact["start"] = 0  # fallback
        else:
            # approx position in audio
            duration = await get_video_duration(video_path)
            fact["start"] = (idx / len(transcript)) * duration
        updated_facts.append(fact)

    return updated_facts

async def get_video_duration(video_path):
    clip = VideoFileClip(video_path)
    duration = clip.duration
    clip.close()
    return duration
