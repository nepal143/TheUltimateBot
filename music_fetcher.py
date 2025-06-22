import os
import requests

MUSIC_URLS_BY_MOOD = {
    "uplifting": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "chill": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "epic": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "lofi": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "mysterious": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
}

def fetch_background_music(mood="uplifting", filename="assets/music/background.mp3"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if not filename.lower().endswith(".mp3"):
        filename += ".mp3"

    url = MUSIC_URLS_BY_MOOD.get(mood.lower())
    if not url:
        print(f"⚠️ Unknown mood '{mood}', falling back to 'uplifting'.")
        url = MUSIC_URLS_BY_MOOD["uplifting"]

    try:
        print(f"🎵 Downloading '{mood}' music from: {url}")
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        if os.path.getsize(filename) < 100000:
            print(f"⚠️ Music file may be incomplete. Size too small.")
            return None

        print(f"✅ Music downloaded to: {filename}")
        return filename

    except Exception as e:
        print(f"❌ Music download failed: {e}")
        return None
