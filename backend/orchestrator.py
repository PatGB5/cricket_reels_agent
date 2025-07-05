from app.services.transcriber import get_fact_timestamps
from app.services.matcher import match_facts_to_segments
from app.services.video_editor import overlay_images_on_video
import json
video_path = "base_videos/may27_fact_video.mp4"
output_path = "final_videos/may27_fact_enhanced.mp4"

facts ="""
            {
                "facts": [
                    {
                    "fact": "Former Indian all-rounder, commentator, and coach Ravi Shastri was born on May 27, 1962.",
                    "image_path": "/home/parthtokekar/Desktop/project/cricket_reels_agent/downloaded_images/ravi.jpeg"
                    },
                    {
                    "fact": "Former Sri Lankan captain and stylish batsman Mahela Jayawardene was born on May 27, 1977."
                     
                    },
                    {
                    "fact": "On May 27, 2012, Kolkata Knight Riders won their maiden IPL title by chasing down 191 against Chennai Super Kings, with Manvinder Bisla scoring a match-winning 89."
                     
                    },
                    {
                    "fact": "On May 27, 2018, Chennai Super Kings claimed their third IPL title as Shane Watson smashed an unbeaten 117 to beat Sunrisers Hyderabad by eight wickets."
                     
                    }
                ]
            }
            """ # Load your facts with image_path from enriched JSON
facts_dict = json.loads(facts)
facts = facts_dict["facts"]

print("Transcribing video...")
segments = get_fact_timestamps(video_path)
# print("Transcription complete. Segments found:", len(segments))
print("Segments:", segments)
print("Matching facts with timestamps...")
matched_facts = match_facts_to_segments(facts, segments)

print("Overlaying images...")
overlay_images_on_video(video_path, matched_facts, output_path)

print("✅ Final video saved at:", output_path)
