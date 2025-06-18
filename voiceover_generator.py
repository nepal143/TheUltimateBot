import pyttsx3
import os
import re

def clean_script(text):
    # Remove lines starting with # (comments)
    cleaned = "\n".join(line for line in text.splitlines() if not line.strip().startswith("#"))

    # Remove content inside parentheses () and brackets []
    cleaned = re.sub(r"\(.*?\)", "", cleaned)
    cleaned = re.sub(r"\[.*?\]", "", cleaned)

    # Replace multiple spaces/newlines with clean formatting
    cleaned = re.sub(r"\n{2,}", "\n", cleaned)
    cleaned = re.sub(r" {2,}", " ", cleaned)
    return cleaned.strip()

def generate_voiceover(script_text, filename="assets/audio/voiceover.mp3"):
    os.makedirs("assets/audio", exist_ok=True)
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 1.0)

    cleaned_script = clean_script(script_text)

    print("🎤 Generating voiceover...")
    engine.save_to_file(cleaned_script, filename)
    engine.runAndWait()
    print(f"✅ Voiceover saved to: {filename}")
