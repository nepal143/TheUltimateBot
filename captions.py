import os
import json
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)

def generate_fake_word_timestamps(sentence, audio_path, output_json):
    """Generate dummy timestamps for each word."""
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    words = sentence.strip().split()
    word_duration = duration / len(words)
    word_data = []
    for i, word in enumerate(words):
        start = i * word_duration
        end = start + word_duration
        word_data.append({
            "word": word,
            "start": round(start, 3),
            "end": round(end, 3)
        })
    with open(output_json, "w") as f:
        json.dump({"words": word_data}, f, indent=2)
    audio.close()
    print(f"✅ Word timestamps saved: {output_json}")


def generate_kinetic_caption_line(
    line_number,
    sentence,
    gif_path,
    audio_path,
    word_timestamps_path,
    output_path,
    resolution=(1080, 1920)
):
    """Create a single line kinetic caption MP4."""
    print(f"🎬 Processing line {line_number}...")

    generate_fake_word_timestamps(sentence, audio_path, word_timestamps_path)

    bg = VideoFileClip(gif_path).resize(height=resolution[1])
    if bg.w < resolution[0]:
        bg = bg.resize(width=resolution[0])

    x_center = bg.w // 2
    crop_width = resolution[0]
    x1 = max(0, x_center - crop_width // 2)
    x2 = x1 + crop_width
    bg = bg.crop(x1=x1, x2=x2)

    audio = AudioFileClip(audio_path)

    with open(word_timestamps_path, "r") as f:
        word_data = json.load(f)["words"]

    captions = []
    for w in word_data:
        txt = (
            TextClip(
                w["word"],
                fontsize=90,
                color="yellow",
                stroke_color="black",
                stroke_width=6,
                font="BebasNeue-Regular",
                method="caption",
                size=(resolution[0] - 100, None)
            )
            .set_start(w["start"])
            .set_end(w["end"])
            .set_position(("center", "bottom"))
            .crossfadein(0.05)
            .crossfadeout(0.05)
        )
        captions.append(txt)

    final = CompositeVideoClip([bg] + captions).set_audio(audio).set_duration(audio.duration)
    final.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        preset="ultrafast",
        audio_codec="aac"
    )

    print(f"✅ Line {line_number} exported: {output_path}")
    final.close()
    bg.close()
    audio.close()


def batch_generate_captions(script_data):
    """Run kinetic captions for each line in script_data."""
    os.makedirs("assets/video/lines", exist_ok=True)
    os.makedirs("assets/captions", exist_ok=True)

    for i, item in enumerate(script_data, start=1):
        sentence = item["sentence"]
        gif_path = f"assets/video/clips/temp_{i}_0.mp4"  # <- adjust if needed
        audio_path = f"assets/audio/lines/line_{i}.mp3"
        word_ts_path = f"assets/captions/line_{i}_timestamps.json"
        output_path = f"assets/video/lines/line_{i}.mp4"

        if not os.path.exists(gif_path):
            print(f"⚠️ GIF/video missing for line {i}. Skipping.")
            continue
        if not os.path.exists(audio_path):
            print(f"⚠️ Audio missing for line {i}. Skipping.")
            continue

        generate_kinetic_caption_line(
            i, sentence, gif_path, audio_path, word_ts_path, output_path
        )
