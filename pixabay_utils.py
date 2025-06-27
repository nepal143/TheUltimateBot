import os
import requests
from moviepy.editor import VideoFileClip
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

HEADERS = {
    "Accept": "application/json"
}

fallback_terms = ["anime fight", "anime fire", "anime punch", "cyberpunk", "anime explosion"]

def search_pixabay_videos(query, count=3):
    # Clean overly long queries
    clean_query = " ".join(query.split()[:6])
    if len(clean_query) > 50:
        clean_query = clean_query[:50]

    url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={clean_query}&limit={count}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Giphy Error: {response.status_code} - {response.text}")
        return []

    gifs = response.json().get("data", [])
    gif_urls = [g["images"]["original"]["url"] for g in gifs if "images" in g]
    
    # Fallback logic if no valid GIFs found
    if not gif_urls:
        print(f"⚠️ No results for query: '{query}'. Trying fallback...")
        fallback = fallback_terms[hash(query) % len(fallback_terms)]
        return search_pixabay_videos(fallback, count)

    return gif_urls

def download_video(gif_url, output_path):
    gif_temp_path = output_path.replace(".mp4", ".gif")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        gif_data = requests.get(gif_url).content
        with open(gif_temp_path, "wb") as f:
            f.write(gif_data)
        print(f"⬇️ Downloaded GIF: {gif_temp_path}")

        clip = VideoFileClip(gif_temp_path)
        clip.write_videofile(output_path, codec="libx264", audio=False)
        print(f"✅ Converted to MP4: {output_path}")
    except Exception as e:
        print(f"⚠️ Failed: {gif_url} ➞ {e}")
    finally:
        if os.path.exists(gif_temp_path):
            os.remove(gif_temp_path)
