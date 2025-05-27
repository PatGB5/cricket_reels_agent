import os
import datetime
from google import genai
from google.genai import types

class CricketFactAgent:
    def __init__(self, credentials_path: str, project: str, location: str = "us-central1"):
        # Set service account credentials
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # Initialize Gemini Client
        self.client = genai.Client(vertexai=True, project=project, location=location)

        self.model = "gemini-2.5-flash-preview-04-17"
        self.system_instruction = """You are a cricket historian. Use the web search tool to find interesting facts that happened on a given day in cricket history. Return 4-5 credible facts in json format having facts as a list. 
                                    Understand the significance of a match if you are going to add that if it is not relevent and has very little significance then don't add that.
                                    While searching the web try to have facts from reputable sources like ESPN, Cricbuzz,ICC Cricket, Cricket.com or Wikipedia or similar.Don't give the source of the fact in the response.
                                    With the fact provide link to download the image related to the fact if available, if not available then just give the fact(the image is important so try hard to find the image).
                                    The image can be scorecard, player image, stadium image or any other image relevant to the fact. If you don't find image of the exact fact then tru to find image of the player or the stadium or the match or the team.
                                    the facts should be strictly related to the date provided.(like if the date is 22nd May then the facts should be related to 22nd May only not even 1-2 days buffer) and also from previous years not the current year."""

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

    def get_facts(self, date: datetime.date = None) -> str:
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
