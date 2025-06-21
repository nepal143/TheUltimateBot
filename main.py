from gemini_script_generator import generate_youtube_script
from voiceover_generator import generate_voiceover
from video_generator import generate_video

if __name__ == "__main__":
    topic = input("🎯 Enter your video topic: ")
    script = generate_youtube_script(topic)

    if script:
        print("\n📝 Your Gemini-Generated Script:\n")
        print(script)

        generate_voiceover(script)
        generate_video(script)
    else:
        print("❌ Script generation failed.")
