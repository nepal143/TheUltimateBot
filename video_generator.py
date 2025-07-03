import os
import random
import gc
import json

from moviepy.config import change_settings

change_settings({
    "IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
})

from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
    CompositeVideoClip,
    TextClip
)
from moviepy.video.fx.all import resize, crop

from pixabay_utils import search_pixabay_videos, download_video

from word_timestamp_generator import generate_fake_word_timestamps


def generate_video(
    script_data,
    audio_dir="assets/audio/lines",
    music_path="assets/music/background.mp3"
):
    os.makedirs("assets/video/clips", exist_ok=True)
    MAX_DURATION = 60
    used_duration = 0
    final_clips = []

    for idx, item in enumerate(script_data):
        sentence = item["sentence"]
        keyword = item["keyword"]
        print(f"🔍 Sentence {idx + 1}: '{sentence.strip()}' ➞ Keyword: '{keyword}'")

        video_urls = search_pixabay_videos(keyword, count=5)
        if not video_urls:
            print(f"⚠️ No videos found for: {keyword}")
            continue

        audio_path = os.path.join(audio_dir, f"line_{idx + 1}.mp3")
        if not os.path.exists(audio_path):
            print(f"⚠️ No voiceover found for line {idx + 1}")
            continue

        output_json = f"assets/captions/line_{idx + 1}_timestamps.json"
        generate_fake_word_timestamps(sentence, audio_path, output_json)

        try:
            voice = AudioFileClip(audio_path)
            target_duration = voice.duration

            accumulated = 0
            clip_parts = []
            loop_index = 0

            while accumulated < target_duration:
                video_url = video_urls[loop_index % len(video_urls)]
                temp_path = f"assets/video/clips/temp_{idx + 1}_{loop_index}.mp4"
                download_video(video_url, temp_path)

                clip = VideoFileClip(temp_path).resize(height=1280)
                clip = crop(clip, width=720, height=1280, x_center=clip.w // 2, y_center=clip.h // 2)

                remaining = target_duration - accumulated
                if clip.duration <= remaining:
                    part = clip
                else:
                    part = clip.subclip(0, remaining)

                accumulated += part.duration
                clip_parts.append(part)

                loop_index += 1
                if loop_index > 20:
                    print(f"⚠️ Breaking loop for line {idx + 1} — too many clips.")
                    break

            stitched_clip = concatenate_videoclips(clip_parts, method="compose")

            # ✅ Load word timestamps
            with open(output_json, "r", encoding="utf-8") as f:
                word_data = json.load(f)["words"]

            # ✅ Create word-by-word TextClips — only once!
            word_clips = []
            for w in word_data:
                word_clip = (
                    TextClip(
                        txt=w["word"],
                        fontsize=80,
                        font='Impact',
                        color='yellow',
                        stroke_color='black',
                        stroke_width=6,
                        method='caption',
                        size=(700, None)
                    )
                    .set_start(w["start"])
                    .set_end(w["end"])
                    .set_position(("center", "bottom"))
                    .crossfadein(0.05)
                    .crossfadeout(0.05)
                )
                word_clips.append(word_clip)

            # ✅ Composite: base visuals + captions once only
            stitched_with_captions = CompositeVideoClip([stitched_clip] + word_clips)
            stitched_with_captions = stitched_with_captions.set_audio(voice)
            stitched_with_captions = stitched_with_captions.set_duration(voice.duration)

            final_clips.append(stitched_with_captions)
            used_duration += target_duration

        except Exception as e:
            print(f"❌ Error on line {idx + 1}: {e}")

        if used_duration >= MAX_DURATION:
            break

    if not final_clips:
        print("❌ No clips to render.")
        return

    # ✅ Stitch all lines together
    final_video = concatenate_videoclips(final_clips, method="compose")

    # ✅ Add background music (optional)
    if music_path and os.path.exists(music_path):
        try:
            music = AudioFileClip(music_path).volumex(0.03).subclip(0, final_video.duration)
            final_audio = CompositeAudioClip([final_video.audio, music])
            final_video = final_video.set_audio(final_audio)
        except Exception as e:
            print(f"⚠️ Music error: {e}")

    # ✅ Save with auto-increment
    base_output = "assets/final_video"
    ext = ".mp4"
    counter = 0
    final_output = f"{base_output}{ext}"
    while os.path.exists(final_output):
        counter += 1
        final_output = f"{base_output}_{counter}{ext}"

    final_video.write_videofile(final_output, fps=24)
    print(f"✅ Final video saved: {final_output}")

    final_video.close()
    gc.collect()

