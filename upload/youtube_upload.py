#!/usr/bin/env python3
"""
YouTube Upload Script for Kids Rhyme Channel
Usage: python youtube_upload.py --help
"""

import argparse
import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "token.pickle"
CLIENT_SECRETS_FILE = "client_secrets.json"

# Metadata for each topic
METADATA = {
    1: {
        "title": "Alphabet Adventure! A-Z Animals Song for Kids 🦁🐘🐒",
        "description": """Learn the ABCs with 26 amazing animals! 🎵

A is for Alligator, B is for Bear... all the way to Z for Zebra!

Perfect for preschoolers and toddlers learning their letters. Sing along and discover new animals!

🔔 Subscribe for more educational songs!
👍 Like if you enjoyed!
💬 Comment your favorite animal!

#alphabet #animals #kidslearning #preschool #toddler #educational #abcsong #phonics""",
        "tags": ["alphabet song", "kids learning", "animals for kids", "preschool education", "ABC", "toddler songs", "educational videos", "phonics"],
        "privacy": "private"
    },
    2: {
        "title": "Counting 1 to 10 with Actions! 👏🦶🤸 Kids Exercise Song",
        "description": """Count 1 to 10 AND get the wiggles out! 🎵

One, one, clap your hands!
Two, two, touch your shoes!
... all the way to 10!

Perfect action song for circle time, brain breaks, or exercise time.

🔔 Subscribe for more!
👍 Like if you had fun!
💬 Comment your favorite number!

#counting #numbers #preschool #kindergarten #actionsong #braingym #movement #mathforkids""",
        "tags": ["counting song", "numbers for kids", "action songs", "brain breaks", "preschool math", "movement songs", "counting 1-10", "kindergarten"],
        "privacy": "private"
    },
    7: {
        "title": "Head Shoulders Knees & Toes - Body Parts Dance! 🕺💃",
        "description": """Classic body parts song with a DANCE PARTY twist! 🕺💃

Head, shoulders, knees, and toes...
Eyes and ears and mouth and nose...
Now let's DANCE! 💃

How fast can you go? Challenge your little one!

🔔 Subscribe for more!
👍 Like if you danced!
💬 Comment your speed!

#bodyparts #headshoulderskneestoes #kidsdance #preschool #toddler #movement #actionsong #circletime""",
        "tags": ["head shoulders knees toes", "body parts song", "kids dance", "action songs", "preschool movement", "toddler songs", "exercise for kids", "circle time songs"],
        "privacy": "private"
    },
    8: {
        "title": "Opposites Song for Kids! Big/Small, Fast/Slow, Up/Down 🐘🐭🎵",
        "description": """Learn 8 opposite pairs in one fun song! 🐘🐭

Big/Small, Fast/Slow, Up/Down, Hot/Cold
Happy/Sad, Loud/Quiet, Open/Close, Day/Night

Perfect for building vocabulary and understanding concepts!

🔔 Subscribe for more!
👍 Like if you learned!
💬 Comment your favorite opposite!

#opposites #vocabulary #preschool #kindergarten #earlylearning #toddler #concepts #bigsmall #fastslow""",
        "tags": ["opposites song", "big small", "fast slow", "up down", "hot cold", "happy sad", "loud quiet", "open close", "day night", "preschool vocabulary", "kindergarten concepts", "early learning"],
        "privacy": "private"
    },
}


def get_authenticated_service(client_secrets_path):
    """Get authenticated YouTube service."""
    creds = None

    # Load existing token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for next run
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('youtube', 'v3', credentials=creds)


def upload_video(youtube, video_path, title, description, tags, privacy="private"):
    """Upload a video to YouTube."""
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27"  # Education
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": True
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print(f"Uploading {video_path}...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  Progress: {int(status.progress() * 100)}%")

    video_id = response['id']
    print(f"✅ Uploaded! https://youtube.com/watch?v={video_id}")
    return video_id


def main():
    parser = argparse.ArgumentParser(description="Upload kids rhyme videos to YouTube")
    parser.add_argument("--client-secret", required=True, help="Path to client_secrets.json")
    parser.add_argument("--topic", type=int, choices=[1, 2, 7, 8], required=True, help="Topic number")
    parser.add_argument("--title", help="Custom title (overrides default)")
    parser.add_argument("--description", help="Custom description (overrides default)")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    args = parser.parse_args()

    # Find video file
    output_dir = Path("output")
    video_files = list(output_dir.glob(f"topic_{args.topic:02d}_*.mp4"))

    if not video_files:
        print(f"❌ No video found for topic {args.topic} in {output_dir}")
        print("Run video generation first!")
        return 1

    video_path = video_files[0]
    print(f"Found video: {video_path}")

    # Get metadata
    meta = METADATA[args.topic]
    title = args.title or meta["title"]
    description = args.description or meta["description"]
    tags = meta["tags"]
    privacy = args.privacy or meta["privacy"]

    # Authenticate and upload
    try:
        youtube = get_authenticated_service(args.client_secret)
        video_id = upload_video(youtube, str(video_path), title, description, tags, privacy)
        print(f"\n🎉 Done! Video ID: {video_id}")
        print(f"Watch: https://youtube.com/watch?v={video_id}")
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())