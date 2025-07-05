from agents import Agent, function_tool
from app.services.analytics_service import get_insights
from app.utils.model_provider import get_model

@function_tool
def fetch_insights():
    return get_insights()

llm = get_model(provider="google", model_name="gemini-pro")

analytics_agent = Agent(
    name="AnalyticsInsightAgent",
    instructions="You are a social media strategist. Use analytics to suggest the best posting time, caption style, and hashtag recommendations.",
    model=llm,
    tools=[fetch_insights]
)
