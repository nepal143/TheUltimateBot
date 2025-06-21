import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_youtube_script(topic):
    prompt = (
        f"Write a 45–60 second YouTube short script on the topic: '{topic}'.\n"
        "Respond in strict JSON format with an array of objects. Each object must have:\n"
        "- sentence: a line of the script (keep it natural and short)\n"
        "- keyword: one relevant visual keyword (noun/concept) from that sentence to help search for related stock video\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You are a helpful YouTube content writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        raw = response['choices'][0]['message']['content'].strip()

        os.makedirs("assets/scripts", exist_ok=True)
        with open("assets/scripts/latest_script.json", "w", encoding="utf-8") as f:
            f.write(raw)

        return json.loads(raw)

    except Exception as e:
        print("🚨 OpenRouter Error:", e)
        return None
