import os
import random
from moviepy.editor import AudioFileClip

def fetch_background_music(mood="uplifting", filename="assets/music/background.mp3"):
    music_dir = "assets/music"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Get list of all MP3s in the folder
    all_mp3s = [f for f in os.listdir(music_dir) if f.lower().endswith(".mp3")]
    if not all_mp3s:
        print("❌ No music files found in 'assets/music'.")
        return None

    # Filter by mood if possible
    mood_filtered = [f for f in all_mp3s if mood.lower() in f.lower()]
    candidates = mood_filtered if mood_filtered else all_mp3s
    random.shuffle(candidates)

    # Try loading each candidate until one works
    for file in candidates:
        full_path = os.path.join(music_dir, file)
        try:
            test = AudioFileClip(full_path)
            test.close()

            with open(full_path, "rb") as src, open(filename, "wb") as dst:
                dst.write(src.read())
            print(f"✅ Selected background music: {file}")
            return filename
        except Exception as e:
            print(f"⚠️ Skipping invalid MP3 '{file}': {e}")

    print("❌ All music files are unreadable or corrupt.")
    return None
