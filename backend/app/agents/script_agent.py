import os
from typing import List
from google import genai
from google.genai import types

class ScriptAgent:
    def __init__(self, project: str, location: str, credentials_path: str = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = genai.Client(vertexai=True, project=project, location=location)
        self.model = "gemini-2.5-flash-preview-05-20"

        self.generate_content_config = types.GenerateContentConfig(
            temperature=0.9,
            top_p=0.95,
            max_output_tokens=65535,
            seed=42,
            system_instruction="""
            You are a content creator who writes short, punchy Instagram reel scripts. You will be given cricket facts and should write a script that:
                MAKE SURE SCRIPT IS NOT MORE THAN 1000 CHARACTERS
            1. Understands which facts are interesting and relevant and then make script for only thoose facts (atleast 3-4 facts), the fact scrutiny is done by understanding the impact of the player/game or the event ,Don't have facts about normal matches having little insight.
                Rather than having many facts try to capitalize on the most interesting ones. Talk more about them like thier significance and what impact they have had. 
                -Like the fact is about a player then talk about the player's background, his career, and his impact on the game , his important contibutions/innings.
                -If the fact is about a game then talk about the significance of the game, the players involved, and the impact it had on the teams or players
                - if it is about a statdium then talk about the stadium, its history, and its significance in the game, important/siginificant matches/events that took place there.
                - if it is about a record then talk about the record, the player who set it, and its significance in the game.
                - try to have birthdays of players but keep them to max 2(if needed only understanding the impact of that player) and mention them as facts only.
            2. Uses an engaging, human tone.
            3. Starts with a hook to grab attention.
            4. Uses a conversational tone, as if speaking directly to the audience.
            5. Connects the facts with smooth transitions.
            7. If there are any scorecards available, include them in the script.
            6. Ends with a call to action like 'Which one do you remember? OR Which one is your favorite?'
            Length should fit in 45-60 seconds of speech.
            8. The script should only contain the script text which is what the character would say.
            Do not include hashtags or emojis in the script.
            MAKE SURE SCRIPT IS NOT MORE THAN 1000 CHARACTERS
            """
        )

    async def generate_script(self, facts: List[str]) -> str:
        query = f"Create an engaging 1-minute Instagram reel script using these facts:\n{facts}"
        
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=query)])
        ]

        # Updated configuration
        config = self.generate_content_config

        # Fetch the response directly
        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        # Return the response text
        return response.text.strip()
