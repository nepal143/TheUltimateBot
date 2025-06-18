from gemini_script_generator import generate_youtube_script
from voiceover_generator import generate_voiceover  # 👈 import the voiceover logic

if __name__ == "__main__":
    topic = input("🎯 Enter your video topic: ")
    script = generate_youtube_script(topic)

    if script:
        print("\n📝 Your Gemini-Generated Script:\n")
        print(script)

        generate_voiceover(script)  # 👈 Call voiceover function
    else:
        print("❌ Script generation failed.")
