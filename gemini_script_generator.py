import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

def generate_youtube_script(topic):
    prompt = (
        f"Generate a controversial YouTube Shorts script for the anime/game/series topic: '{topic}'.\n\n"
        "Script Format:\n"
        "- Write 15 to 25 lines (1 punchy sentence each, max 25 words)\n"
        "- Only use the famous and well-known characters from the anime/game/series\n"
        "- Each line must be a bold take, hot opinion, or debate-worthy questio and each line must have relation with the topic \n"
        "- Use phrasing like: 'Hot take:', 'Let’s be real...', 'What if...', 'Imagine if...'\n"
        "- Focus on characters, power scaling, alternate outcomes, betrayals, abilities, etc.\n"
        "- End with a line that invites comment (e.g., 'Agree or nah?', 'Drop your take.')\n"
        "- ✳️ Keep it **simple and easy to understand** — avoid overcomplicating things or using hard-to-follow logic\n\n"
        "Return this format:\n"
        "{\n"
        "  \"script\": [\n"
        "    {\"sentence\": \"<your line>\", \"keyword\": \"<anime-specific term with 2–4 words>\"},\n"
        "    ...\n"
        "  ],\n"
        "  \"mood\": \"<one-word music mood like 'epic', 'lofi', 'tense'>\"\n"
        "}\n\n"
        "⚠️ Keyword Rules:\n"
        "- Keywords will be used to search **Giphy** for anime GIFs\n"
        "- Must contain ONLY terms/names from the same anime/game try using mostly names only every single keyword muset have first word reference with the series or anime  \n"
        "- Don't use the character's name which are not famous instead use the character's name which are famous and well known in the anime or series and also you can just search on the name of the name of the series/anime/game\n"
        "- Use official names of characters, powers, forms, items — like 'Gojo Six Eyes', 'Luffy Gear Fifth'\n"
        "- No vague emotions, story descriptions, or general terms\n"
        "- Keep each keyword 2 to 4 words max\n"
        "- Each keyword must be unique\n"
        "- Avoid using generic terms like 'anime', 'fight', 'power' — focus on specific characters or abilities\n"
        "✅ Valid examples: 'Gojo Six Eyes', 'Eren Founding Titan', 'Luffy Gear Fifth', 'Jin-Woo Shadow Monarch'\n\n"
        "Respond ONLY with the raw JSON object. No explanations or markdown formatting."
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

        os.makedirs("assets/scripts", exist_ok=True)
        with open("assets/scripts/latest_script.json", "w", encoding="utf-8") as f:
            f.write(raw)

        return json.loads(raw)

    except Exception as e:
        print("🚨 OpenRouter Error:", e)
        return None
