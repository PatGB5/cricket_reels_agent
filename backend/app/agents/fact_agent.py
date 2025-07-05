import os
import datetime
from google import genai
from google.genai import types
import json
import re

class CricketFactAgent:
    def __init__(self, credentials_path: str, project: str, location: str = "us-central1"):
        # Set service account credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # Initialize Gemini Client
        self.client = genai.Client(vertexai=True, project=project, location=location)

        self.model = "gemini-2.5-flash-preview-04-17"
        self.system_instruction = """You are a cricket historian. Use the web search tool to find interesting, historically significant cricket facts that happened specifically on a given date in previous years (not the current year). The date context is critical — only return facts that occurred on the exact date (e.g. May 27), with no date buffering allowed.

                                    Return exactly 4-5 facts in JSON format, structured exactly as described below, with no extra commentary or formatting outside the JSON block.

                                    Each fact must be historically relevant and should ideally include matches, player milestones, records, team wins ,notable debuts, or player birthdays with high cricketing significance. Ignore lesser-known or non-noteworthy events.
                                        Along with each fact, provide a short image search query relevant to the fact. This should be a concise, clear string suitable for searching on an image search engine like Google Images or SerpAPI.

                                        Examples of image search queries:
                                        - “Mahela Jayawardene batting”
                                        - “Kolkata Knight Riders IPL 2012 final”
                                        - “Shane Watson 117 vs SRH”
                                        - “Ravi Shastri 1985 World Championship”

                                        Strictly output only the JSON block below. No markdown, explanation, or source citations.

                                       example:
                                       {
                                            "facts": [
                                                        {
                                                            "fact": "Former Indian all-rounder, commentator, and coach Ravi Shastri was born on May 27, 1962.",
                                                            "image_query": "Ravi Shastri India cricket"
                                                        },
                                                        {
                                                            "fact": "Former Sri Lankan captain and stylish batsman Mahela Jayawardene was born on May 27, 1977."
                                                            "image_query": "Mahela Jayawardene batting Sri Lanka"
                                                        },
                                                        {
                                                            "fact": "On May 27, 2012, Kolkata Knight Riders won their maiden IPL title by chasing down 191 against Chennai Super Kings, with Manvinder Bisla scoring a match-winning 89."
                                                            "image_query": "KKR vs CSK IPL 2012 final Manvinder Bisla"
                                                        },
                                                        {
                                                            "fact": "On May 27, 2018, Chennai Super Kings claimed their third IPL title as Shane Watson smashed an unbeaten 117 to beat Sunrisers Hyderabad by eight wickets."
                                                            "image_query": "Shane Watson IPL 2018 final CSK vs SRH"
                                                        }
                                                    ]
                                        }"""

        self.generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=1,
            seed=0,
            max_output_tokens=65535,
            safety_settings=[
                types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
                types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF")
            ],
            tools=[types.Tool(google_search=types.GoogleSearch())],
            system_instruction=[types.Part.from_text(text=self.system_instruction)],
        )

    async def get_facts(self, date: datetime.date = None) -> str:
        """Fetch cricket facts from Gemini based on the current date"""
        if not date:
            date = datetime.date.today()

        query = f"Give me amazing cricket facts for {date.strftime('%B %d')}"
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=query)])
        ]

        print(f"[Gemini FactAgent] Fetching facts for: {date.strftime('%B %d')}")
        response_text = ""

        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=self.generate_content_config,
        ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
            response_text += chunk.text

        return response_text.strip()

    async def parse_facts_string(self, facts):
        if isinstance(facts, str):
            try:
                # Extract the JSON block from the string using regex
                match = re.search(r"\{[\s\S]*\}", facts)
                if match:
                    json_str = match.group(0)
                    return json.loads(json_str)
                else:
                    print("[Error] No JSON object found in the string.")
                    return {"facts": []}
            except json.JSONDecodeError as e:
                print("[Error] Failed to decode JSON:", e)
                return {"facts": []}
        elif isinstance(facts, dict):
            return facts
        else:
            print("[Error] Unsupported format for facts.")
            return {"facts": []}
