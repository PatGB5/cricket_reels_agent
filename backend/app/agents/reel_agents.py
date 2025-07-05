# app/agents/reel_agent.py

from openai import AssistantEventHandler, AsyncAssistantThreadRunner
from openai import OpenAI
from app.services import (
    fetch_cricket_facts,
    generate_script,
    generate_video,
    send_approval_email,
    post_reel,
)

client = OpenAI()

# Define tool schemas for OpenAI functions

tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_cricket_facts",
            "description": "Fetches cricket facts for a specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD"}
                },
                "required": ["date"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_script",
            "description": "Creates a script based on cricket facts",
            "parameters": {
                "type": "object",
                "properties": {
                    "facts": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["facts"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_video",
            "description": "Creates a video using a script",
            "parameters": {
                "type": "object",
                "properties": {
                    "script": {"type": "string"}
                },
                "required": ["script"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_approval_email",
            "description": "Send an email for approval of the reel",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_url": {"type": "string"}
                },
                "required": ["video_url"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "post_reel",
            "description": "Post the approved video to Instagram",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_url": {"type": "string"}
                },
                "required": ["video_url"]
            },
        },
    },
]

# Create the assistant
assistant = client.beta.assistants.create(
    name="CricketReelAgent",
    instructions="You are a digital assistant that creates daily cricket history reels for Instagram. Follow the workflow to fetch facts, generate a script, create a video, send it for approval, and post it if approved.",
    tools=tools,
    model="gpt-4"
)

# Optional runner setup for thread execution
runner = AsyncAssistantThreadRunner(client=client)

__all__ = ["assistant", "runner"]
