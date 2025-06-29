# stitch_lines.py
from moviepy.editor import VideoFileClip, concatenate_videoclips

def stitch_lines(num_lines, output_path="assets/final_video.mp4"):
    clips = []
    for i in range(1, num_lines + 1):
        clip_path = f"assets/video/lines/line_{i}.mp4"
        if not os.path.exists(clip_path):
            print(f"⚠️ Missing: {clip_path}")
            continue
        clip = VideoFileClip(clip_path)
        clips.append(clip)

    if not clips:
        print("🚫 No clips to stitch.")
        return

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=24)
    print(f"✅ Final stitched video: {output_path}")

if __name__ == "__main__":
    stitch_lines(num_lines=5)  # Or however many lines you have
