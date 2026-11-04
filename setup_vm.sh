#!/bin/bash
# Cloud VM Setup Script for Kids Rhyme Channel
# Run on a fresh Ubuntu 22.04/24.04 VM (2GB+ RAM recommended)
# Usage: curl -sSL https://raw.githubusercontent.com/yourrepo/main/setup_vm.sh | bash
# OR: chmod +x setup_vm.sh && ./setup_vm.sh

set -e

echo "🚀 Setting up Kids Rhyme Channel on Cloud VM..."

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    python3 python3-venv python3-pip \
    ffmpeg \
    fonts-dejavu-core \
    git \
    htop

# Clone repo (replace with your actual repo)
REPO_URL="https://github.com/YOUR_USERNAME/kids-rhyme-channel.git"
REPO_DIR="kids-rhyme-channel"

if [ ! -d "$REPO_DIR" ]; then
    git clone "$REPO_URL" "$REPO_DIR"
fi

cd "$REPO_DIR"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install moviepy pillow numpy edge-tts

# Generate TTS audio
echo "🎤 Generating TTS audio..."
for topic in 1 2 7 8; do
    python generate/tts_generate.py --topic $topic --provider edge
done

# Generate videos (one at a time to save memory)
echo "🎬 Generating videos..."
for topic in 1 2 7 8; do
    echo "  Topic $topic..."
    audio_file=$(ls assets/audio/topic_$(printf "%02d" $topic)_*.mp3 2>/dev/null | head -1)
    if [ -n "$audio_file" ]; then
        python generate/video_template.py --topic $topic --audio "$audio_file"
    else
        echo "  ⚠️ No audio found for topic $topic, generating without audio"
        python generate/video_template.py --topic $topic
    fi
done

# List results
echo "✅ Done! Generated files:"
ls -la output/
ls -la assets/audio/

echo ""
echo "🎉 All videos generated! Upload to YouTube:"
echo "  python upload/youtube_upload.py --client-secret client_secrets.json --topic 1"
echo ""
echo "📁 Videos are in: $(pwd)/output/"