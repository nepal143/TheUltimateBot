import os
import json
from upload import upload_video, get_authenticated_service

def validate_or_reset_token(token_path="token.json"):
    if not os.path.exists(token_path):
        return

    try:
        with open(token_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content or not json.loads(content):  # Empty or bad JSON
                raise ValueError("Invalid or empty token.")
    except Exception as e:
        print(f"⚠️ Detected corrupted token.json: {e}")
        print("🧹 Deleting token.json for clean re-auth...")
        os.remove(token_path)

def run_upload():
    print("🚀 Starting upload process...")
    validate_or_reset_token()

    # 👇 Customize this:
    title = "My YouTube Short"
    description = "This is a test upload from my bot."
    tags = ["test", "automation", "bot"]

    upload_video(title, description, tags)

if __name__ == "__main__":
    run_upload()
