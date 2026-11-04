# Kids Rhyme Channel - Automated Pipeline

## Quick Start

### 1. Install Dependencies
```bash
pip install moviepy pillow numpy edge-tts
# OR for premium TTS:
pip install elevenlabs openai TTS
```

### 2. Generate Audio (TTS)
```bash
# Free option (Microsoft Edge voices)
python generate/tts_generate.py --topic 1 --provider edge
python generate/tts_generate.py --topic 2 --provider edge
python generate/tts_generate.py --topic 7 --provider edge
python generate/tts_generate.py --topic 8 --provider edge

# Premium option (ElevenLabs - best quality)
python generate/tts_generate.py --topic 1 --provider elevenlabs --api-key YOUR_KEY

# Premium option (OpenAI)
python generate/tts_generate.py --topic 1 --provider openai --api-key YOUR_KEY
```

### 3. Generate Videos
```bash
# Without audio (silent videos with text)
python generate/video_template.py --topic 1
python generate/video_template.py --topic 2
python generate/video_template.py --topic 7
python generate/video_template.py --topic 8

# With audio (add --audio path/to/audio.mp3)
python generate/video_template.py --topic 1 --audio assets/audio/topic_01_alphabet_adventure.mp3
```

### 4. Generate All at Once
```bash
# Generate all audio
for t in 1 2 7 8; do python generate/tts_generate.py --topic $t --provider edge; done

# Generate all videos with audio
for t in 1 2 7 8; do
  python generate/video_template.py --topic $t --audio assets/audio/topic_${t:02d}_*.mp3
done
```

## Output Structure
```
kids-rhyme-channel/
├── assets/
│   └── audio/           # Generated TTS files
├── generate/
│   ├── video_template.py   # Video generation
│   └── tts_generate.py     # TTS generation
├── scripts/             # Rhyme scripts & metadata
│   ├── topic_01_alphabet_adventure.txt
│   ├── topic_02_counting_1to10.txt
│   ├── topic_07_body_parts_dance.txt
│   └── topic_08_opposites.txt
├── output/              # Generated MP4 videos
└── upload/
    └── youtube_upload.py   # YouTube API upload (see below)
```

## YouTube Upload Automation

Create `upload/youtube_upload.py`:
```python
# Requires: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
# Setup: Google Cloud Console → YouTube Data API v3 → OAuth credentials

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import os

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(file_path, title, description, tags, privacy="private"):
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=credentials)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27"  # Education
        },
        "status": {
            "privacyStatus": privacy,  # private, unlisted, public
            "selfDeclaredMadeForKids": True
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print(f"Uploaded: https://youtube.com/watch?v={response['id']}")
    return response['id']
```

## Instagram/Facebook (Meta) Upload
Use `instagram-scraper` or `facebook-sdk` - requires Meta Developer App with:
- Instagram Basic Display API
- Instagram Content Publishing API
- Page access tokens

## Scheduling (GitHub Actions)
Create `.github/workflows/upload.yml`:
```yaml
name: Daily Kids Rhyme Upload
on:
  schedule:
    - cron: '0 10 * * *'  # Daily 10 AM UTC
  workflow_dispatch:

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install -r requirements.txt
      - run: python generate/tts_generate.py --topic 1 --provider edge
      - run: python generate/video_template.py --topic 1 --audio assets/audio/topic_01_alphabet_adventure.mp3
      - run: python upload/youtube_upload.py output/topic_01_alphabet_adventure.mp4 "Title" "Desc" "tags"
        env:
          YOUTUBE_CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
```

## Platform-Specific Metadata

### YouTube Shorts (vertical, <60s)
- Title: "Alphabet Adventure! A-Z Animals Song for Kids 🦁🐘🐒"
- Hashtags: #shorts #kids #alphabet #animals #learning

### Instagram Reels (vertical, <90s)
- Caption with 3-5 hashtags, save CTA
- Cover image: first frame with title text

### Facebook Reels (vertical, <90s)
- Similar to Instagram, cross-post via Meta Business Suite

## Customization Tips

### Add Background Music
```python
# In video_template.py, add to build_video():
from moviepy.editor import AudioFileClip, CompositeAudioClip

music = AudioFileClip("assets/music/cheerful_loop.mp3").volumex(0.15)
if final.audio:
    final.audio = CompositeAudioClip([final.audio, music.set_duration(final.duration)])
else:
    final.audio = music.set_duration(final.duration)
```

### Add Character Animations
Replace solid backgrounds with animated GIFs/MP4s:
```python
bg = VideoFileClip("assets/backgrounds/classroom_loop.mp4").loop(duration=duration)
```

### Add Subtitles (burned in)
Already included via TextClip - customize font/color/position in `create_text_clip()`

## Requirements.txt
```
moviepy==1.0.3
pillow==10.0.0
numpy==1.24.0
edge-tts==6.1.9
# Premium:
# elevenlabs==0.2.27
# openai==1.12.0
# TTS==0.22.0
# google-api-python-client==2.108.0
# google-auth-oauthlib==1.1.0
```

## Next Steps
1. ✅ Scripts written (4 topics)
2. ✅ Video template code ready
3. ✅ TTS generation code ready
4. 🔲 Run TTS generation
5. 🔲 Run video generation
6. 🔲 Set up YouTube API credentials
7. 🔲 Test upload
8. 🔲 Schedule automation