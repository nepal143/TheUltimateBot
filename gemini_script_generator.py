import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_youtube_script(topic):
    prompt = (
        f"Write a YouTube Shorts script on the topic: '{topic}'.\n"
        "The script must be 60–90 seconds long and contain at least **15 to 25 lines**, one per sentence.\n"
        "Return a JSON object with two properties:\n"
        "1. 'script': an array of objects with:\n"
        "   - 'sentence': short, casual, engaging line in the script (under 25 words)\n"
        "   - 'keyword': a descriptive, specific visual search phrase for stock footage (no repeats, no vague terms)\n"
        "2. 'mood': a single word describing background music mood (e.g., 'epic', 'uplifting', 'mysterious', 'lofi')\n\n"
        "**Keyword Tips:**\n"
        "- Avoid generic terms like 'person', 'walking', 'city'\n"
        "- Use clear stock-footage-style descriptions like 'man walking with umbrella in storm' or 'drone shot over mountain valley at sunrise'\n"
        "- Each keyword should match the sentence and be visually distinct\n\n"
        "Example output:\n"
        "{\n"
        "  \"script\": [\n"
        "    {\"sentence\": \"The sun rises over ancient ruins...\", \"keyword\": \"sunrise over old stone ruins\"},\n"
        "    {\"sentence\": \"History lives in these stones.\", \"keyword\": \"close-up of carved ancient writing\"},\n"
        "    ... (at least 10 lines total)\n"
        "  ],\n"
        "  \"mood\": \"mysterious\"\n"
        "}\n\n"
        "Respond ONLY with the raw JSON object. No extra text or explanation."
    )

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a YouTube script generator with stock footage and music mood matching."},
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
