from app.agents.fact_agent import CricketFactAgent
from app.agents.script_agent import ScriptAgent
from app.services.image_search import download_images_from_facts
import json
# from app.services.image_downloader import download_images_from_facts
if __name__ == "__main__":
    fact_agent = CricketFactAgent(
        credentials_path="salk-ai-app-83f08d5d8778.json",
        project="salk-ai-app",
        location="us-central1"
    )
    script_agent = ScriptAgent(
        credentials_path="salk-ai-app-83f08d5d8778.json",
        project="salk-ai-app",
        location="us-central1"
    )
    facts ="""
            ```json
            {
                "facts": [
                    {
                        "fact": "On June 26, 2000, Bangladesh was officially granted Test status by the International Cricket Council (ICC), becoming the 10th Test-playing nation.",
                        "image_query": "Bangladesh cricket team Celebration Test status 2000"
                    },
                    {
                        "fact": "Indian all-rounder Eknath Solkar, known for his exceptional close-in fielding, passed away on June 26, 2005, at the age of 57. He played 27 Tests and 7 One Day Internationals for India.",
                        "image_query": "Eknath Solkar fielding"
                    },
                    {
                        "fact": "Legendary English batsman Leonard 'Len' Hutton made his Test debut on June 26, 1937, against New Zealand at Lord's.",
                        "image_query": "Len Hutton batting 1937"
                    },
                    {
                        "fact": "South African wicketkeeper-batter Trisha Chetty, a prominent figure in women's cricket, was born on June 26, 1988.",
                        "image_query": "Trisha Chetty cricket"
                    }
                ]
            }
            ```
            """
    # facts = fact_agent.get_facts()
    print("\n--- Cricket Facts ---\n", facts)

    # Clean the response to remove extra formatting
    if isinstance(facts, str):
        try:
            # Remove triple backticks and any extra whitespace
            cleaned_facts = fact_agent.parse_facts_string(facts)
            facts = cleaned_facts  # Parse the cleaned JSON string
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            facts = {"facts": []}  # Fallback to an empty dictionary with an empty list


    # Extract the list of facts
    facts_list = facts.get("facts", [])  # Extract the list of dictionaries from the "facts" key

    # Process facts with images
    facts_with_images = download_images_from_facts(facts_list)
    print("\n--- Facts with Images ---\n", facts_with_images)
    