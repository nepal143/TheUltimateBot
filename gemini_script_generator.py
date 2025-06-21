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
        f"Write a 45 to 60-second YouTube short script about the topic: '{topic}'.\n"
        "The tone should be energetic, casual, and conversational — like a passionate creator speaking directly to the viewer.\n"
        "Start with a strong hook, explain the topic in simple terms, and end with a memorable conclusion and call to action like 'Subscribe for more!'\n"
        "Keep the word count around 120 to 150 words — just enough to fit in a one-minute video.\n"
        "Avoid dry narration or robotic tone. Include a bit of personality or humor if it fits."
    )

    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",  # Try Claude or Mixtral for richer style
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
