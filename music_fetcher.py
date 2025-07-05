import os
import random
from moviepy.editor import AudioFileClip

def fetch_background_music(mood="uplifting"):
    music_dir = "assets/music"

    if not os.path.exists(music_dir):
        print("❌ Music folder not found.")
        return None

    all_mp3s = [f for f in os.listdir(music_dir) if f.lower().endswith(".mp3")]
    if not all_mp3s:
        print("❌ No music files found in 'assets/music'.")
        return None

    # First try filtering by mood
    mood_filtered = [f for f in all_mp3s if mood.lower() in f.lower()]
    candidates = mood_filtered if mood_filtered else all_mp3s

    random.shuffle(candidates)  # 🎲 Shuffle to ensure randomness

    # Try to validate and return the first playable one
    for file in candidates:
        full_path = os.path.join(music_dir, file)
        try:
            test = AudioFileClip(full_path)
            test.close()
            print(f"✅ Randomly selected background music: {file}")
            return full_path
        except Exception as e:
            print(f"⚠️ Skipping unreadable MP3 '{file}': {e}")

    print("❌ No playable music files found.")
    return None
