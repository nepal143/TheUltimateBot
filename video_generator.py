import os
import random
import gc
from moviepy.editor import (
    AudioFileClip,
    VideoFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)
from pixabay_utils import search_pixabay_videos, download_video  # ✅ Custom helper

def generate_video(
    script_data,
    audio_dir="assets/audio/lines",
    output_path="assets/final_video.mp4",
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

        try:
            voice = AudioFileClip(audio_path)
            target_duration = voice.duration  # 🟢 Match entire voice length

            accumulated = 0
            gif_clips = []

            loop_index = 0
            while accumulated < target_duration:
                gif_url = video_urls[loop_index % len(video_urls)]
                temp_path = f"assets/video/clips/temp_{idx + 1}_{loop_index}.mp4"
                download_video(gif_url, temp_path)

                try:
                    clip = VideoFileClip(temp_path).resize(height=480)
                    remaining = target_duration - accumulated

                    if clip.duration <= remaining:
                        gif_clips.append(clip)
                        accumulated += clip.duration
                    else:
                        gif_clips.append(clip.subclip(0, remaining))
                        accumulated += remaining
                except Exception as e:
                    print(f"⚠️ Skipping broken clip {temp_path}: {e}")

                loop_index += 1

                # Prevent infinite loop if all clips fail
                if loop_index > 20:
                    print("⚠️ Breaking to avoid infinite GIF loop")
                    break

            if not gif_clips:
                print(f"⚠️ Could not assemble clips for line {idx + 1}")
                continue

            stitched = concatenate_videoclips(gif_clips, method="compose")
            stitched = stitched.set_audio(voice)

            final_clips.append(stitched)
            used_duration += target_duration

        except Exception as e:
            print(f"❌ Error processing line {idx + 1}: {e}")

        if used_duration >= MAX_DURATION:
            break

    if not final_clips:
        print("❌ No clips to render.")
        return

    try:
        final_video = concatenate_videoclips(final_clips, method="compose")

        if music_path and os.path.exists(music_path):
            try:
                music = AudioFileClip(music_path).volumex(0.1).subclip(0, final_video.duration)
                final_audio = CompositeAudioClip([final_video.audio, music])
                final_video = final_video.set_audio(final_audio)
            except Exception as e:
                print(f"⚠️ Music error: {e}")

        final_video.write_videofile(output_path, fps=24)
        print(f"✅ Final video saved: {output_path}")

        final_video.close()
        gc.collect()

    except Exception as e:
        print(f"❌ Final video generation failed: {e}")
