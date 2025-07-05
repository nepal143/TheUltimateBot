import os
import requests
import time
import numpy as np
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips
from moviepy.video.fx.all import resize, crop

load_dotenv()
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

HEADERS = {
    "Accept": "application/json"
}

fallback_terms = ["anime fight", "anime fire", "anime punch", "cyberpunk", "anime explosion"]


def search_giphy_videos(query, count=3):
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
        return search_giphy_videos(fallback, count)

    return gif_urls


def download_video(gif_url, output_path, max_attempts=5):
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

            if clip.duration <= 0 or clip.size[0] == 0 or clip.size[1] == 0:
                raise ValueError("❌ Invalid video: zero duration or size")

            clip.write_videofile(output_path, codec="libx264", audio=False, verbose=False, logger=None)

            print(f"✅ Converted to MP4: {output_path}")
            clip.close()
            os.remove(gif_temp_path)
            return True

        except Exception as e:
            print(f"⚠️ Attempt {attempt} failed for {gif_url}: {e}")
            time.sleep(1.5)

    print(f"❌ All attempts failed for {gif_url}")
    if os.path.exists(gif_temp_path):
        os.remove(gif_temp_path)

    return False


def create_text_clip(text, output_path, duration=2, font_size=60, color="white", bg_color="black", size=(720, 150)):
    """Replaces TextClip: generates text overlay with PIL and MoviePy ImageClip (no ImageMagick)"""
    img = Image.new("RGB", size, bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    w, h = draw.textsize(text, font=font)
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, font=font, fill=color)

    np_img = np.array(img)
    clip = ImageClip(np_img).set_duration(duration)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    clip.write_videofile(output_path, fps=24, codec="libx264", audio=False, verbose=False, logger=None)
    clip.close()
    print(f"📝 Created text clip: {output_path}")


# Example usage
if __name__ == "__main__":
    topic = input("🎯 Enter your video topic: ").strip()
    urls = search_giphy_videos(topic)

    for i, gif_url in enumerate(urls):
        out_mp4 = f"assets/video/clips/temp_{i}.mp4"
        download_video(gif_url, out_mp4)

    # Optional: create intro caption
    create_text_clip(f"🔥 {topic.upper()}!", "assets/video/clips/title_intro.mp4")
