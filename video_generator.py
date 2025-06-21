from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap
import re

def clean_sentences(script):
    # Break on periods, exclamations, and questions
    sentences = re.split(r'(?<=[.!?]) +', script.strip())
    return [s for s in sentences if s.strip()]

def generate_text_image(text, output_path, width=1280, height=720):
    image = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw = ImageDraw.Draw(image)

    font_path = "C:/Windows/Fonts/arial.ttf"  # Adjust if needed
    try:
        font = ImageFont.truetype(font_path, 48)
    except:
        font = ImageFont.load_default()

    lines = textwrap.wrap(text, width=40)
    y = height // 2 - len(lines) * 30

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((width - w) // 2, y), line, font=font, fill=(255, 255, 255))
        y += h + 10

    image.save(output_path)
    return output_path

def generate_video(script_text, audio_path="assets/audio/voiceover.mp3", output_path="assets/final_video.mp4"):
    os.makedirs("assets/video", exist_ok=True)

    # 🧠 Step 1: Break script into sentences
    sentences = clean_sentences(script_text)
    num_sentences = len(sentences)

    # 🔊 Load voiceover and calculate per-slide duration
    audio_clip = AudioFileClip(audio_path)
    total_duration = audio_clip.duration
    duration_per_slide = total_duration / num_sentences

    print(f"🎬 Creating {num_sentences} slides, each {duration_per_slide:.2f}s long...")

    # 🖼️ Step 2: Generate image clips
    image_clips = []
    for i, sentence in enumerate(sentences):
        image_path = f"assets/video/slide_{i+1}.png"
        generate_text_image(sentence, image_path)

        img_clip = ImageClip(image_path).set_duration(duration_per_slide)
        image_clips.append(img_clip)

    # 🎞️ Step 3: Concatenate and sync with audio
    video = concatenate_videoclips(image_clips, method="compose")
    final_video = video.set_audio(audio_clip)

    final_video.write_videofile(output_path, fps=24)
    print(f"✅ Multi-slide video saved at: {output_path}")
