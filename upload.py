import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    token_path = "token.json"

    # ✅ Check for existing token
    if os.path.exists(token_path):
        print("🔑 Loading existing token...")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # 🧼 If token missing or invalid, login again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("🔐 No valid token found. Starting login flow...")
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # 💾 Save new token
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())
            print("✅ Token saved for future use!")

    return build("youtube", "v3", credentials=creds)

def upload_video(title, description, tags):
    youtube = get_authenticated_service()

    # 📂 Find latest final video
    output_dir = "assets"
    video_path = None
    for fname in sorted(os.listdir(output_dir), reverse=True):
        if fname.startswith("final_video") and fname.endswith(".mp4"):
            video_path = os.path.join(output_dir, fname)
            break

    if not video_path:
        print("❌ No final video found in 'assets' folder.")
        return

    print(f"📤 Uploading video: {video_path}")

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "24"  # Entertainment
        },
        "status": {
            "privacyStatus": "public",               # 🔓 Set to public
            "selfDeclaredMadeForKids": False         # 🧒 Not made for kids = comments enabled
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media)

    response = None
    while response is None:
        print("📡 Uploading in chunks...")
        status, response = request.next_chunk()
        if status:
            print(f"📈 Upload progress: {int(status.progress() * 100)}%")

    print(f"✅ Upload complete! 🎉")
    print(f"📺 Video ID: {response['id']}")
    print(f"https://www.youtube.com/watch?v={response['id']}")
