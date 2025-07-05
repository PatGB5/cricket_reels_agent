from datetime import datetime
from app.services.image_search import download_images_from_facts
from app.agents.fact_agent import CricketFactAgent  # Assuming this is your existing function to get facts
from app.agents.script_agent import ScriptAgent  # Assuming this is your existing function to generate scripts
import json
import os

async def generate_script_and_images(extra_prompt: str = ""):
    # Step 1: Use your existing fact generation function here
    today = datetime.today().strftime("%B %d")
    full_prompt = f"Generate cricket facts for {today}. {extra_prompt}"
    call_fact_agent = CricketFactAgent(
        credentials_path="/home/parthtokekar/Desktop/project/cricket_reels_agent/backend/salk-ai-app-83f08d5d8778.json",
        project="salk-ai-app",
        location="us-central1"
    )
    write_script_from_facts = ScriptAgent(
        credentials_path="/home/parthtokekar/Desktop/project/cricket_reels_agent/backend/salk-ai-app-83f08d5d8778.json",
        project="salk-ai-app",
        location="us-central1"
    )
    # Let's assume facts_with_queries is a list of dicts: {fact, image_query}
    facts_with_queries = await call_fact_agent.get_facts()  # Use your agent here
    facts_with_queries = await call_fact_agent.parse_facts_string(facts_with_queries)
    facts_list = facts_with_queries.get("facts", [])
    
    # Step 2: Download images using existing function
    facts_with_images = await download_images_from_facts(facts_list)
    script_text = await write_script_from_facts.generate_script(facts_with_images)
    
    script_data = {
        "facts": facts_with_images,
        "script": script_text
    }
    # Step 3: Save to file
    os.makedirs("data/scripts", exist_ok=True)
    script_path = f"data/scripts/{datetime.today().strftime('%Y%m%d')}_script.json"
    with open(script_path, "w") as f:
        f.write(json.dumps(script_data, indent=2))

    return script_text, script_path
