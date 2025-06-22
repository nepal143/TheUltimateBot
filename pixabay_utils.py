import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY")

HEADERS = {
    "Accept": "application/json"
}

def search_pixabay_videos(query, count=4):
    url = (
        f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}"
        f"&q={query}&per_page={count}"
    )
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Pixabay Error: {response.status_code} - {response.text}")
        return []

    videos = response.json().get("hits", [])
    video_links = []

    for v in videos:
        # Select the highest quality available (e.g., "large" resolution)
        if "videos" in v and "large" in v["videos"]:
            video_links.append(v["videos"]["large"]["url"])
        elif "videos" in v and "medium" in v["videos"]:
            video_links.append(v["videos"]["medium"]["url"])
    
    return video_links

def download_video(url, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    response = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in response.iter_content(8192):
            f.write(chunk)
    print(f"✅ Downloaded: {filename}")
    return filename

# Example usage
if __name__ == "__main__":
    query = "cyberpunk city"  # or "cat", "magic", etc.
    videos = search_pixabay_videos(query, count=3)

    for idx, link in enumerate(videos):
        download_video(link, f"assets/video/pixabay_{idx+1}.mp4")
