from gemini_script_generator import generate_youtube_script
from voiceover_generator import generate_voiceover
from video_generator import generate_video
from music_fetcher import fetch_background_music

if __name__ == "__main__":
    topic = input("🎯 Enter your video topic: ")
    result = generate_youtube_script(topic)

    if result:
        script_data = result["script"]
        mood = result.get("mood", "uplifting")

        print("\n📝 Your Gemini-Generated Script:\n")
        for idx, item in enumerate(script_data):
            print(f"{idx + 1}. {item['sentence']} [Keyword: {item['keyword']}]")
        print(f"\n🎶 Suggested Music Mood: {mood}")

        generate_voiceover(script_data)
        music_path = fetch_background_music(mood) or "assets/music/default.mp3"
        generate_video(script_data, music_path=music_path)
    else:
        print("❌ Script generation failed.")

