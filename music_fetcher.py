import os
import requests

def fetch_background_music(filename="assets/music/background.mp3"):
    os.makedirs("assets/music", exist_ok=True)

    fallback_music_urls = [
        "https://cdn.pixabay.com/audio/2022/10/19/audio_3514b2b31f.mp3",
        "https://cdn.pixabay.com/audio/2022/03/15/audio_c2c5a5c3d5.mp3",
        "https://cdn.pixabay.com/audio/2022/06/07/audio_5a3e50590b.mp3",
        "https://cdn.pixabay.com/audio/2021/08/09/audio_d91c57a9d7.mp3",
    ]

    try:
        selected_url = fallback_music_urls[0]
        response = requests.get(selected_url)
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Music downloaded to: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Music download failed: {e}")
        return None
