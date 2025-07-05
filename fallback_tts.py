import pyttsx3
import os

def fallback_generate_voiceover(script_data, output_dir="assets/audio/lines"):
    os.makedirs(output_dir, exist_ok=True)
    engine = pyttsx3.init()

    # Set properties for better voice quality (optional tuning)
    engine.setProperty('rate', 180)  # Speed (words per minute)
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

    print("\n🔄 ElevenLabs failed or skipped. Using fallback TTS (pyttsx3)...")

    for idx, item in enumerate(script_data):
        sentence = item["sentence"]
        line_path = os.path.join(output_dir, f"line_{idx + 1}.mp3")
        print(f"🗣️ Fallback TTS: Generating line {idx + 1}: '{sentence}'")

        engine.save_to_file(sentence, line_path)
        engine.runAndWait()

        print(f"✅ Fallback line {idx + 1} saved to: {line_path}")

    engine.stop()
