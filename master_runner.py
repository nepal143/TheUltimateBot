import subprocess
import sys
import os
import random

def get_python_from_venv():
    """Try to get the Python executable from the local venv."""
    venv_path = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")  # Windows
    if not os.path.exists(venv_path):
        print("⚠️ venv Python not found. Falling back to system Python.")
        return sys.executable
    return venv_path

def run_batch_from_file(file_path="topics.txt", limit=6):
    # Read all topics
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            topics = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return

    if not topics:
        print("⚠️ No topics found in the file.")
        return

    # Shuffle and limit topics
    random.shuffle(topics)
    topics = topics[:limit]

    python_executable = get_python_from_venv()

    # Loop through selected topics
    for i, topic in enumerate(topics, 1):
        print(f"\n🚀 [{i}/{len(topics)}] Generating video for: {topic}")
        try:
            subprocess.run(
                [python_executable, "main.py"],
                input=f"{topic}\n",
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating for '{topic}': {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    run_batch_from_file("topics.txt", limit=6)
