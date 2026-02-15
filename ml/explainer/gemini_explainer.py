import google.generativeai as genai
import json
from dotenv import load_dotenv
import os

import os
from pathlib import Path

# Load .env.local from project root (one level up from ml folder)
env_path = Path(__file__).resolve().parent.parent.parent / '.env.local'
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_API_KEY = API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3-flash-preview")


def generate_celestial_explanation(raw_text, event_name):

    prompt = f"""
You are a space educator AI.

Convert the celestial event description into VERY SIMPLE language
understandable by kids and beginners.

Return ONLY valid JSON with this structure:

{{
"title": "",
"simple_explanation": "",
"difficulty": "",
"random_facts": ["", "", ""]
}}

Rules:
- Keep explanation short.
- Difficulty must be Easy, Moderate, or Hard.
- Provide 3 fun space facts related to the event.

Event Name: {event_name}
Description: {raw_text}
"""

    response = model.generate_content(prompt)

    # Gemini returns text → convert to JSON safely
    try:
        cleaned = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned)
    except:
        # fallback if AI formatting breaks
        return {
            "title": event_name,
            "simple_explanation": "A celestial event will be visible in the sky.",
            "difficulty": "Moderate",
            "random_facts": [
                "Space is completely silent.",
                "Light from stars takes years to reach Earth.",
                "Astronomy helps us understand our universe."
            ]
        }
