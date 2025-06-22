import os
import random
import gc
from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)
from pixabay_utils import search_pixabay_videos, download_video  # ✅ Updated import


def generate_video(
    script_data,
    audio_path="assets/audio/voiceover.mp3",
    output_path="assets/final_video.mp4",
    music_path="assets/music/background.mp3"
):
    os.makedirs("assets/video/clips", exist_ok=True)

    try:
        audio_clip = AudioFileClip(audio_path)
    except Exception as e:
        print(f"❌ Failed to load audio: {e}")
        return

    MAX_DURATION = 60
    clip_limit = min(len(script_data), int(MAX_DURATION / 3))
    final_clips = []
    used_duration = 0

    for idx, item in enumerate(script_data[:clip_limit]):
        sentence = item["sentence"]
        keyword = item["keyword"]
        print(f"🔍 Sentence {idx + 1}: '{sentence.strip()}' ➞ Keyword: '{keyword}'")

        video_urls = search_pixabay_videos(keyword, count=3)  # ✅ Updated function
        if not video_urls:
            continue

        selected_urls = random.sample(video_urls, min(2, len(video_urls)))
        subclips = []

        for vid_idx, url in enumerate(selected_urls):
            filename = f"assets/video/clips/clip_{idx + 1}_{vid_idx + 1}.mp4"
            download_video(url, filename)
            try:
                clip = VideoFileClip(filename)
                clip_duration = min(3, clip.duration)
                if used_duration + clip_duration > MAX_DURATION:
                    break
                subclip = clip.subclip(0, clip_duration).resize(height=480)
                subclips.append(subclip)
                used_duration += clip_duration
            except Exception as e:
                print(f"❌ Clip error: {e}")

        if subclips:
            sentence_clip = concatenate_videoclips(subclips, method="compose")
            final_clips.append(sentence_clip)

        if used_duration > MAX_DURATION:
            break

    if not final_clips:
        print("❌ No clips found. Aborting.")
        return

    final_video = concatenate_videoclips(final_clips, method="compose")
    safe_duration = min(final_video.duration, audio_clip.duration, MAX_DURATION)

    try:
        print(f"🎵 Using music file: {music_path}")  # Debug log
        music = AudioFileClip(music_path).volumex(0.1).subclip(0, safe_duration)
        voice = audio_clip.subclip(0, safe_duration)
        final_audio = CompositeAudioClip([music, voice])
        final_with_audio = final_video.set_audio(final_audio)
    except Exception as e:
        print(f"⚠️ Music error: {e}")
        final_with_audio = final_video.set_audio(audio_clip.subclip(0, safe_duration))

    final_with_audio.write_videofile(output_path, fps=24)
    print(f"✅ Final video saved: {output_path}")

    final_with_audio.close()
    final_video.close()
    audio_clip.close()
    gc.collect()
