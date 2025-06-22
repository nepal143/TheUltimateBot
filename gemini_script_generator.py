import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_youtube_script(topic):
    prompt = (
        f"Write a 45–60 second YouTube Shorts script on the topic: '{topic}'.\n"
        "Return a JSON object with 2 properties:\n"
        "- script: an array of objects with:\n"
        "   - sentence: short line in the script (under 25 words)\n"
        "   - keyword: descriptive visual search keyword (no duplicates, specific)\n"
        "- mood: one descriptive music mood (e.g., 'epic', 'chill', 'uplifting', 'lofi') to match the video tone.\n\n"
        "Example:\n"
        "{\n"
        "  \"script\": [\n"
        "    {\"sentence\": \"The sun rises over ancient ruins...\", \"keyword\": \"sunrise over old stone ruins\"},\n"
        "    {\"sentence\": \"History lives in these stones.\", \"keyword\": \"close-up of carved ancient writing\"}\n"
        "  ],\n"
        "  \"mood\": \"mysterious\"\n"
        "}\n\n"
        "Respond ONLY with this JSON object."
    )

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a YouTube script generator with stock footage and music matching."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        raw = response['choices'][0]['message']['content'].strip()

        os.makedirs("assets/scripts", exist_ok=True)
        with open("assets/scripts/latest_script.json", "w", encoding="utf-8") as f:
            f.write(raw)

        return json.loads(raw)

    except Exception as e:
        print("🚨 OpenRouter Error:", e)
        return None
