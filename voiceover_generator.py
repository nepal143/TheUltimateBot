from elevenlabs import generate, save, set_api_key, voices
import os
from dotenv import load_dotenv

load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

def get_valid_voice(preferred="Rachel"):
    try:
        voice_list = voices()
        for v in voice_list:
            if v.name.lower() == preferred.lower():
                return v.name
        print(f"⚠️ '{preferred}' not found. Using '{voice_list[0].name}' instead.")
        return voice_list[0].name
    except Exception as e:
        print("❌ Voice fetch failed:", e)
        return preferred

def generate_voiceover(script_data, filename="assets/audio/voiceover.mp3", voice="Rachel"):
    os.makedirs("assets/audio", exist_ok=True)
    script_text = "\n".join(item["sentence"] for item in script_data)
    valid_voice = get_valid_voice(voice)

    try:
        print(f"🎤 Generating voiceover with voice: {valid_voice}")
        audio = generate(text=script_text, voice=valid_voice, model="eleven_monolingual_v1")
        save(audio, filename)
        print(f"✅ Voiceover saved to: {filename}")
    except Exception as e:
        print(f"❌ ElevenLabs Error: {e}")
