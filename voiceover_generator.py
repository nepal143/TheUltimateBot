from elevenlabs import generate, save, set_api_key, voices
import os
from dotenv import load_dotenv

load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

# Preferred fallback order
PREFERRED_VOICES = ["Rachel", "Josh", "Clyde", "Adam" , "George","Callum", "Charlotte"]

def get_valid_voice(preferred_list=PREFERRED_VOICES):
    try:
        voice_list = voices()
        print("🔊 Available voices from ElevenLabs:")
        for v in voice_list:
            print(f"- {v.name}")

        available_names = [v.name.lower() for v in voice_list]
        for preferred in preferred_list:
            if preferred.lower() in available_names:
                print(f"✅ Using voice: {preferred}")
                return preferred

        fallback = voice_list[0].name
        print(f"⚠️ None of {preferred_list} found. Using '{fallback}' instead.")
        return fallback

    except Exception as e:
        print("❌ Voice fetch failed:", e)
        return preferred_list[0]

def generate_voiceover(script_data, voice=None):
    os.makedirs("assets/audio/lines", exist_ok=True)
    valid_voice = get_valid_voice([voice] + PREFERRED_VOICES if voice else PREFERRED_VOICES)

    for idx, item in enumerate(script_data):
        sentence = item["sentence"]
        line_path = f"assets/audio/lines/line_{idx + 1}.mp3"
        try:
            print(f"🎤 Generating voiceover for line {idx + 1}: '{sentence}'")
            audio = generate(text=sentence, voice=valid_voice, model="eleven_monolingual_v1")
            save(audio, line_path)
            print(f"✅ Line {idx + 1} saved to: {line_path}")
        except Exception as e:
            print(f"❌ Error generating line {idx + 1}: {e}")
