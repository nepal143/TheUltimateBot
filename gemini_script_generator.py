import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_youtube_script(topic):
    prompt = (
        f"Write a highly engaging YouTube script about: '{topic}'. "
        "The script should be 60 to 90 seconds long, written in a casual and energetic tone. "
        "Start with a strong hook to grab attention, then explain the topic in simple, digestible parts. "
        "Wrap it up with a clever or satisfying conclusion, and a call to action like 'Subscribe for more fun facts!' "
        "Make it sound like a passionate creator speaking directly to the viewer — no dry narration!"
    )

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",  # You can change this
            messages=[
                {"role": "system", "content": "You are a helpful YouTube content writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        script = response.choices[0].message.content.strip()

        os.makedirs("assets/scripts", exist_ok=True)
        with open("assets/scripts/latest_script.txt", "w", encoding="utf-8") as f:
            f.write(script)

        return script

    except Exception as e:
        print("🚨 OpenRouter Error:", e)
        return None
