import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("PocketSmart AI 💰")
category = st.selectbox("Category", ["Home Decor", "Event Planning", "Jewelry"])
budget = st.number_input("Your budget (₹)", min_value=0, step=500)
notes = st.text_area("Any preferences?")

if st.button("Get Recommendations"):
    prompt = (
        f"I have a budget of ₹{budget} for {category}. "
        f"Preferences: {notes}. Suggest a budget breakdown and "
        f"5 product or idea recommendations with approximate prices."
    )
    models = ["gemini-flash-latest", "gemini-3.1-flash-lite"]
    response = None
    with st.spinner("Thinking..."):
        for model_name in models:
            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model=model_name, contents=prompt
                    )
                    break
                except Exception:
                    time.sleep(3)
            if response:
                break
    if response:
        st.write(response.text)
    else:
        st.error("Google's server is busy right now. Please try again in a minute.")