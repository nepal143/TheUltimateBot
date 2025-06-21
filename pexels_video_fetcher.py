import os
import requests
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

HEADERS = {
    "Authorization": PEXELS_API_KEY
}

# 🔁 Get multiple related videos
def search_pexels_videos(query, count=4):
    url = f"https://api.pexels.com/videos/search?query={query}&per_page={count}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Pexels Error: {response.status_code} - {response.text}")
        return []

    videos = response.json().get("videos", [])
    return [video["video_files"][-1]["link"] for video in videos]

def download_video(url, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"✅ Downloaded: {filename}")
    return filename
