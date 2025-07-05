import os
import openai
import json
import re
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_youtube_script(topic):
    prompt = (
        f"Generate a controversial YouTube Shorts script for the anime/game/series topic: '{topic}'.\n\n"
        "Script Format:\n"
        "- Write 10 to 15 lines (1 punchy sentence each, max 25 words)\n"
        "- Only use famous and well-known characters from the anime/game/series\n"
        "- Each line must be a bold take or hot opinion directly tied to the topic\n"
        "- Use phrases like: 'Hot take:', 'Let’s be real...', 'What if...', 'Imagine if...'\n"
        "- End with a line that invites comments (e.g., 'Agree or nah?', 'Drop your take.')\n"
        "- ✳️ Keep it simple and debate-worthy\n\n"
        "Return JSON in this format:\n"
        "{\n"
        "  \"script\": [\n"
        "    {\"sentence\": \"<your line>\", \"keyword\": \"<anime-specific term with max 3 words>\"},\n"
        "    ...\n"
        "  ],\n"
        "  \"mood\": \"<one-word music mood>\",\n"
        "  \"title\": \"<video title>\",\n"
        "  \"description\": \"<YouTube video description>\",\n"
        "  \"tags\": [\"<tag1>\", \"<tag2>\", ...]\n"
        "}\n\n"
        "⚠️ Keyword Rules:\n"
        "- Must be max 3 words\n"
        "- Use only official names/powers/forms/items from the anime/game\n"
        "- No vague, emotional, or generic terms\n"
        "- Every keyword must start with a reference to the anime or game\n"
        "✅ Examples: 'Gojo Six Eyes', 'Luffy Gear Fifth', 'Eren Founding Titan'\n"
        "Return raw JSON. No explanation."
    )

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "You generate spicy anime/gaming takes in JSON with official character-based keywords for Giphy search."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.95,
        )

        raw = response['choices'][0]['message']['content'].strip()
        print("🪵 RAW RESPONSE:\n", raw)

        # 🧼 Extract first full JSON block
        match = re.search(r"\{[\s\S]+\}", raw)
        if not match:
            print("⚠️ No valid JSON object found in response.")
            return None

        cleaned_json = match.group(0)

        # 🧽 Fix common formatting issues:
        cleaned_json = re.sub(r",\s*([}\]])", r"\1", cleaned_json)  # Remove trailing commas
        cleaned_json = cleaned_json.replace("“", "\"").replace("”", "\"")  # Curly quotes to straight
        cleaned_json = cleaned_json.replace("‘", "'").replace("’", "'")    # Curly apostrophes to straight

        os.makedirs("assets/scripts", exist_ok=True)
        with open("assets/scripts/latest_script.json", "w", encoding="utf-8") as f:
            f.write(cleaned_json)

        return json.loads(cleaned_json)

    except Exception as e:
        print("🚨 OpenRouter Error:", e)
        return None
