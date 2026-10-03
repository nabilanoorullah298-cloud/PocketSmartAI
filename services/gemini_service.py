import time

from google import genai

import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

TOPICS = {
    "home": "home interior decoration and furnishing",
    "party": "party planning (decor, food, venue, entertainment)",
    "jewelry": "jewelry shopping",
}


def build_prompt(kind, budget, details, preferences):
    return f"""You are PocketSmart AI, a friendly budget and recommendation assistant for Indian users.
Topic: {TOPICS[kind]}
Total budget: ₹{budget}
Requirements: {details}
Preferences: {preferences or "None"}

Reply in this format:
## Budget breakdown
A table with columns: Item, Estimated cost (₹), % of budget.
## Recommendations
For each requirement suggest 2-3 options with style, approximate price in ₹ and a short reason.
## Money-saving tips
Three short tips.
Keep the total within the budget. Prices are only estimates."""


def get_recommendations(kind, budget, details, preferences):
    prompt = build_prompt(kind, budget, details, preferences)
    for model_name in config.GEMINI_MODELS:
        for _ in range(3):
            try:
                return client.models.generate_content(
                    model=model_name, contents=prompt
                ).text
            except Exception:
                time.sleep(3)
    return None
