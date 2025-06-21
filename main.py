from gemini_script_generator import generate_youtube_script
from voiceover_generator import generate_voiceover
from video_generator import generate_video
from music_fetcher import fetch_background_music

if __name__ == "__main__":
    topic = input("🎯 Enter your video topic: ")
    script = generate_youtube_script(topic)

    if script:
        print("\n📝 Your Gemini-Generated Script:\n")
        print(script)

        generate_voiceover(script)
        music_path = fetch_background_music("uplifting") or "assets/music/default.mp3"
        generate_video(script, music_path=music_path)
    else:
        print("❌ Script generation failed.")
