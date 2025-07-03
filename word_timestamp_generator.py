import os
import json
from moviepy.editor import AudioFileClip

def generate_fake_word_timestamps(sentence, audio_path, output_json):
    words = sentence.strip().split()
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    word_duration = total_duration / len(words)

    word_data = []
    for i, word in enumerate(words):
        start = i * word_duration
        end = start + word_duration
        word_data.append({
            "word": word,
            "start": round(start, 3),
            "end": round(end, 3)
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump({"words": word_data}, f, indent=2)
    print(f"✅ Generated: {output_json}")

    audio.close()

def batch_generate_captions(script_data):
    os.makedirs("assets/video/lines", exist_ok=True)
    num_lines = len(script_data)

    for i in range(1, num_lines + 1):
        gif_path = f"assets/gifs/line_{i}.gif"
        audio_path = f"assets/audio/lines/line_{i}.mp3"
        word_ts_path = f"assets/captions/line_{i}_timestamps.json"
        output_path = f"assets/video/lines/line_{i}.mp4"

        if not os.path.exists(gif_path):
            print(f"⚠️ GIF missing for line {i}. Skipping.")
            continue
        if not os.path.exists(audio_path):
            print(f"⚠️ Audio missing for line {i}. Skipping.")
            continue
        if not os.path.exists(word_ts_path):
            print(f"⚠️ Timestamps missing for line {i}. Skipping.")
            continue

        from captions import generate_kinetic_caption_line

        generate_kinetic_caption_line(i, gif_path, audio_path, word_ts_path, output_path)
