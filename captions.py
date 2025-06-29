import os
import json
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)

def generate_kinetic_caption_line(
    line_number,
    gif_path,
    audio_path,
    word_timestamps_path,
    output_path,
    resolution=(1080, 1920)
):
    """
    For a single line:
    - Load GIF
    - Load line voiceover
    - Load word timestamps
    - Create word-by-word kinetic captions
    - Composite & export final line video
    """

    print(f"🎬 Processing line {line_number}...")

    # Load GIF background and resize for vertical video
    bg = VideoFileClip(gif_path).resize(height=resolution[1])
    if bg.w < resolution[0]:
        bg = bg.resize(width=resolution[0])

    # Center crop if needed
    x_center = bg.w // 2
    crop_width = resolution[0]
    x1 = max(0, x_center - crop_width // 2)
    x2 = x1 + crop_width
    bg = bg.crop(x1=x1, x2=x2)

    # Load audio
    audio = AudioFileClip(audio_path)

    # Load timestamps
    with open(word_timestamps_path, "r", encoding="utf-8") as f:
        word_data = json.load(f)["words"]

    # Generate TextClips for each word
    captions = []
    for w in word_data:
        word_clip = (
            TextClip(
                txt=w["word"],
                fontsize=90,
                font="BebasNeue-Regular",  # Use your bold, thick font
                color="yellow",            # Bright highlight color
                stroke_color="black",      # Outline color
                stroke_width=6,            # Thicker outline
                method="caption",
                size=(resolution[0] - 100, None),
            )
            .set_start(w["start"])
            .set_end(w["end"])
            .set_position(("center", "bottom"))
            .crossfadein(0.05)
            .crossfadeout(0.05)
        )
    captions.append(word_clip)


    # Combine GIF + captions + audio
    final = (
        CompositeVideoClip([bg] + captions)
        .set_audio(audio)
        .set_duration(audio.duration)
    )

    # Export
    final.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        preset="ultrafast",
        threads=4,
        audio_codec="aac"
    )

    print(f"✅ Line {line_number} exported: {output_path}")

    final.close()
    bg.close()
    audio.close()


def batch_generate_captions(script_data):
    """
    Loop through all lines in script_data.
    Assumes:
      - GIFs in assets/gifs/line_{i}.gif
      - Audio in assets/audio/lines/line_{i}.mp3
      - Timestamps in assets/captions/line_{i}_timestamps.json
    """
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

        generate_kinetic_caption_line(
            i, gif_path, audio_path, word_ts_path, output_path
        )


if __name__ == "__main__":
    # Dummy example usage
    fake_script = [{"sentence": "This is line one."}, {"sentence": "This is line two."}]
    batch_generate_captions(fake_script)
