import os
import requests
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import resize, crop
from dotenv import load_dotenv
import time

load_dotenv()
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

HEADERS = {
    "Accept": "application/json"
}

fallback_terms = ["anime fight", "anime fire", "anime punch", "cyberpunk", "anime explosion"]

def search_pixabay_videos(query, count=3):
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

    if not gif_urls:
        print(f"⚠️ No results for query: '{query}'. Trying fallback...")
        fallback = fallback_terms[hash(query) % len(fallback_terms)]
        return search_pixabay_videos(fallback, count)

    return gif_urls


def download_video(gif_url, output_path, max_attempts=5):
    """
    Tries downloading and converting the GIF to MP4. Retries up to 5 times if it fails.
    Returns True if successful, False otherwise.
    """
    gif_temp_path = output_path.replace(".mp4", ".gif")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    for attempt in range(1, max_attempts + 1):
        try:
            gif_data = requests.get(gif_url, timeout=10).content
            with open(gif_temp_path, "wb") as f:
                f.write(gif_data)
            print(f"⬇️ Downloaded GIF (Attempt {attempt}): {gif_temp_path}")

            clip = VideoFileClip(gif_temp_path).resize(height=1280)
            clip = crop(clip, width=720, height=1280, x_center=clip.w // 2, y_center=clip.h // 2)
            clip.write_videofile(output_path, codec="libx264", audio=False, verbose=False, logger=None)

            print(f"✅ Converted to MP4: {output_path}")
            clip.close()
            os.remove(gif_temp_path)
            return True

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed for {gif_url}: {e}")
            time.sleep(1.5)  # brief pause before retry

    print(f"❌ All attempts failed for {gif_url}")
    if os.path.exists(gif_temp_path):
        os.remove(gif_temp_path)

    return False
