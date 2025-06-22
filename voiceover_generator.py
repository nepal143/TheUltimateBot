from elevenlabs import generate, save, set_api_key, voices
import os
from dotenv import load_dotenv

load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

# Preferred fallback order
PREFERRED_VOICES = ["Rachel", "Josh", "Clyde" , "Charlotte"]

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

def generate_voiceover(script_data, filename="assets/audio/voiceover.mp3", voice=None):
    os.makedirs("assets/audio", exist_ok=True)
    script_text = "\n".join(item["sentence"] for item in script_data)
    valid_voice = get_valid_voice([voice] + PREFERRED_VOICES if voice else PREFERRED_VOICES)

    try:
        print(f"🎤 Generating voiceover with voice: {valid_voice}")
        audio = generate(text=script_text, voice=valid_voice, model="eleven_monolingual_v1")
        save(audio, filename)
        print(f"✅ Voiceover saved to: {filename}")
    except Exception as e:
        print(f"❌ ElevenLabs Error: {e}")
