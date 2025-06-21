from moviepy.editor import *
from pexels_video_fetcher import search_pexels_videos, download_video
import os
import re
import random
import gc

# 🧠 Smart keyword extractor
def extract_keyword(sentence, topic):
    sentence = sentence.lower()
    topic = topic.lower()
    context = f"{sentence} {topic}"

    keywords = [
        "honey", "bees", "beekeeping", "jar", "natural", "sugar", "preservation",
        "ancient", "bacteria", "nectar", "pollen", "gold", "medicine"
    ]
    for word in keywords:
        if word in context:
            return word

    words = re.findall(r'\b[a-z]{4,}\b', context)
    return words[0] if words else "nature"

# 🧾 Split script into sentences
def clean_sentences(script):
    return re.split(r'(?<=[.!?]) +', script.strip())

# 🎬 Final video generator
def generate_video(script_text, audio_path="assets/audio/voiceover.mp3", output_path="assets/final_video.mp4"):
    os.makedirs("assets/video/clips", exist_ok=True)

    audio_clip = AudioFileClip(audio_path)
    sentences = clean_sentences(script_text)

    MAX_DURATION = 60  # in seconds
    MIN_DURATION = 45

    total_audio_duration = audio_clip.duration
    clip_limit = min(len(sentences), int(MAX_DURATION / 3))  # ~3 sec per sentence

    final_clips = []
    used_duration = 0

    for idx, sentence in enumerate(sentences[:clip_limit]):
        keyword = extract_keyword(sentence, script_text)
        print(f"🔍 Sentence {idx+1}: '{sentence.strip()}' ➜ Keyword: '{keyword}'")

        video_urls = search_pexels_videos(keyword, count=3)
        if not video_urls:
            continue

        selected_urls = random.sample(video_urls, min(2, len(video_urls)))
        subclips = []

        for vid_idx, url in enumerate(selected_urls):
            filename = f"assets/video/clips/clip_{idx+1}_{vid_idx+1}.mp4"
            download_video(url, filename)

            try:
                clip = VideoFileClip(filename)
                clip_duration = min(3, clip.duration)
                used_duration += clip_duration
                if used_duration > MAX_DURATION:
                    break

                subclip = clip.subclip(0, clip_duration).resize(height=480)
                subclips.append(subclip)
            except Exception as e:
                print(f"❌ Clip error: {e}")

        if subclips:
            sentence_clip = concatenate_videoclips(subclips, method="compose")
            final_clips.append(sentence_clip)

        if used_duration > MAX_DURATION:
            break

    if not final_clips:
        print("❌ No usable clips. Aborting video.")
        return

    final_video = concatenate_videoclips(final_clips, method="compose")

    # Trim voiceover to match video
    audio_trimmed = audio_clip.subclip(0, min(final_video.duration, MAX_DURATION))
    final_with_audio = final_video.set_audio(audio_trimmed)

    final_with_audio.write_videofile(output_path, fps=24)
    print(f"✅ Final video saved to: {output_path}")

    # Clean up
    final_with_audio.close()
    final_video.close()
    audio_clip.close()
    gc.collect()
