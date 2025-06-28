import os
import time
import random
from elevenlabs import generate, save, set_api_key, voices
from dotenv import load_dotenv

load_dotenv()

API_KEYS = os.getenv("ELEVENLABS_API_KEYS", "").split(",")
API_KEYS = [key.strip() for key in API_KEYS if key.strip()]

if not API_KEYS:
    raise Exception("❌ No ElevenLabs API keys found in .env under 'ELEVENLABS_API_KEYS'.")

PREFERRED_VOICES = ["Rachel", "Josh", "Clyde", "Adam", "George", "Callum", "Charlotte"]

def get_valid_voice(preferred_list=PREFERRED_VOICES):
    random.shuffle(API_KEYS)  # Shuffle for random rotation
    for key in API_KEYS:
        try:
            print(f"🔑 Trying key: {key[:6]}...")
            set_api_key(key)
            voice_list = voices()
            available_names = [v.name.lower() for v in voice_list]

            for preferred in preferred_list:
                if preferred.lower() in available_names:
                    print(f"✅ Using voice: {preferred} with key {key[:6]}...")
                    return preferred, key
        except Exception as e:
            print(f"⚠️ Voice fetch failed with key {key[:6]}...: {e}")
            time.sleep(random.uniform(10, 20))  # Random pause before trying next key
    raise Exception("❌ No valid voice found with any API key.")

def generate_voiceover(script_data, voice=None):
    os.makedirs("assets/audio/lines", exist_ok=True)
    preferred_list = [voice] + PREFERRED_VOICES if voice else PREFERRED_VOICES
    valid_voice, working_key = get_valid_voice(preferred_list)

    for idx, item in enumerate(script_data):
        sentence = item["sentence"]
        line_path = f"assets/audio/lines/line_{idx + 1}.mp3"
        print(f"\n📄 Processing line {idx + 1}: '{sentence}'")

        keys_to_try = [working_key] + [k for k in API_KEYS if k != working_key]
        random.shuffle(keys_to_try)  # Add randomness to rotation

        success = False
        for api_key in keys_to_try:
            try:
                set_api_key(api_key)
                print(f"🎤 Using key {api_key[:6]}...")

                audio = generate(text=sentence, voice=valid_voice, model="eleven_monolingual_v1")
                save(audio, line_path)

                print(f"✅ Line {idx + 1} saved to: {line_path}")
                success = True

                # Simulate human pace
                time.sleep(random.uniform(2, 5))
                break
            except Exception as e:
                print(f"❌ Key {api_key[:6]} failed: {e}")
                # Longer pause on failure to avoid pattern detection
                time.sleep(random.uniform(10, 25))

        if not success:
            print(f"🚫 Skipped line {idx + 1} — all keys failed.")

# Example usage
# generate_voiceover([{"sentence": "Hello world!"}, {"sentence": "This is another line."}])
