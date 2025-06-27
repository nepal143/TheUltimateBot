import os
import random

def fetch_background_music(mood="uplifting", filename="assets/music/background.mp3"):
    music_dir = "assets/music"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Get list of all MP3s in the folder
    all_mp3s = [f for f in os.listdir(music_dir) if f.lower().endswith(".mp3")]
    if not all_mp3s:
        print("❌ No music files found in 'assets/music'.")
        return None

    # Try to filter by mood in filename
    mood_filtered = [f for f in all_mp3s if mood.lower() in f.lower()]
    selected_file = random.choice(mood_filtered if mood_filtered else all_mp3s)

    # Copy to target path (background.mp3)
    source_path = os.path.join(music_dir, selected_file)
    try:
        with open(source_path, "rb") as src, open(filename, "wb") as dst:
            dst.write(src.read())
        print(f"✅ Selected background music: {selected_file}")
        return filename
    except Exception as e:
        print(f"❌ Failed to copy music file: {e}")
        return None
