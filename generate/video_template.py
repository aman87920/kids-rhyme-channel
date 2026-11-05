#!/usr/bin/env python3
"""
Video Generator for Kids Rhyme Channel
Uses MoviePy 2.x to create animated videos from scripts.

Requirements:
    pip install moviepy pillow numpy

Usage:
    python video_template.py --topic 1
    python video_template.py --topic 2
    python video_template.py --topic 7
    python video_template.py --topic 8
    python video_template.py --all
"""

import argparse
import os
from pathlib import Path
from moviepy import (
    VideoFileClip, ImageClip, TextClip, CompositeVideoClip,
    ColorClip, AudioFileClip, concatenate_videoclips
)
from moviepy.audio.AudioClip import concatenate_audioclips
from moviepy.video.fx import Resize
import numpy as np

# Configuration
OUTPUT_DIR = Path("output")
ASSETS_DIR = Path("assets")
SCRIPTS_DIR = Path("scripts")
FPS = 30
WIDTH, HEIGHT = 1080, 1920  # Vertical for Shorts/Reels
BG_COLOR = (255, 248, 230)  # Warm cream
TEXT_COLOR = (60, 40, 20)   # Dark brown
ACCENT_COLOR = (255, 140, 60)  # Orange

# Topic configurations
TOPICS = {
    1: {
        "name": "alphabet_adventure",
        "title": "Alphabet Adventure!",
        "lines": [
            ("A is for Alligator, snapping his jaws", 3),
            ("B is for Bear, climbing up paws", 3),
            ("C is for Cat, curled up so tight", 3),
            ("D is for Dog, barking all night", 3),
            ("E is for Elephant, trunk swinging wide", 3),
            ("F is for Fox, with a bushy tail to hide", 3),
            ("G is for Giraffe, reaching up high", 3),
            ("H is for Hippo, splashing nearby", 3),
            ("I is for Iguana, basking in sun", 3),
            ("J is for Jaguar, having such fun", 3),
            ("K is for Kangaroo, hopping around", 3),
            ("L is for Lion, the king of the ground", 3),
            ("M is for Monkey, swinging on vine", 3),
            ("N is for Nightingale, singing so fine", 3),
            ("O is for Owl, hooting at moon", 3),
            ("P is for Penguin, waddling in tune", 3),
            ("Q is for Quail, running so fast", 3),
            ("R is for Rabbit, hopping at last", 3),
            ("S is for Snake, sliding along", 3),
            ("T is for Tiger, brave and so strong", 3),
            ("U is for Unicorn, magical and bright", 3),
            ("V is for Vulture, soaring in flight", 3),
            ("W is for Whale, swimming so deep", 3),
            ("X is for X-ray fish, secrets to keep", 3),
            ("Y is for Yak, with shaggy long hair", 3),
            ("Z is for Zebra, stripes everywhere!", 3),
            ("Now you know your A to Z", 3),
            ("Animals are friends, you and me!", 3),
            ("Sing it again, sing it with glee", 3),
            ("Learning letters is easy as can be!", 4),
        ],
        "duration_per_line": 3,
    },
    2: {
        "name": "counting_1to10",
        "title": "Counting 1 to 10!",
        "lines": [
            ("One, one, clap your hands!", 3),
            ("Two, two, touch your shoes!", 3),
            ("Three, three, touch your knee!", 3),
            ("Four, four, touch the floor!", 3),
            ("Five, five, give a high-five!", 3),
            ("Six, six, do some kicks!", 3),
            ("Seven, seven, point to heaven!", 3),
            ("Eight, eight, skate like great!", 3),
            ("Nine, nine, draw a line!", 3),
            ("Ten, ten, do it again!", 3),
            ("One, two, three, four, five", 3),
            ("Six, seven, eight, nine, ten", 3),
            ("Count with me, count with you", 3),
            ("Numbers are fun to do!", 3),
            ("Let's count backwards, don't be slow", 3),
            ("Ten, nine, eight, seven, six", 3),
            ("Five, four, three, two, one", 3),
            ("Blast off! We're done!", 4),
        ],
        "duration_per_line": 3,
    },
    7: {
        "name": "body_parts_dance",
        "title": "Body Parts Dance!",
        "lines": [
            ("Head, shoulders, knees, and toes", 2),
            ("Knees and toes!", 2),
            ("Head, shoulders, knees, and toes", 2),
            ("Knees and toes!", 2),
            ("Eyes and ears and mouth and nose", 3),
            ("Head, shoulders, knees, and toes", 2),
            ("Knees and toes!", 2),
            ("Now let's dance, move your body!", 3),
            ("Touch your head, touch your shoulders", 3),
            ("Touch your knees, touch your toes", 3),
            ("Spin around, touch the ground", 3),
            ("Jump up high, reach the sky!", 3),
            ("Head, shoulders, knees, and toes", 2),
            ("Knees and toes!", 2),
            ("Head, shoulders, knees, and toes", 2),
            ("Knees and toes!", 2),
            ("Eyes and ears and mouth and nose", 3),
            ("Head, shoulders, knees, and toes", 2),
            ("Knees and toes!", 2),
            ("Faster now! Ready, set, go!", 2),
            ("Head, shoulders, knees, and toes!", 1.5),
            ("Super fast!", 1.5),
            ("Head, shoulders, knees, and toes!", 1.5),
            ("You did it! Great job!", 3),
        ],
        "duration_per_line": 2,
    },
    8: {
        "name": "opposites",
        "title": "Opposites Song!",
        "lines": [
            ("Big elephant, small little mouse", 3),
            ("Big and small, in this house!", 3),
            ("Fast cheetah, slow snail crawls", 3),
            ("Fast and slow, up the walls!", 3),
            ("Up goes the balloon in the sky", 3),
            ("Down comes the rain, falling by", 3),
            ("Hot soup warming in the bowl", 3),
            ("Cold ice cream, sweet and cold!", 3),
            ("Happy face with a great big smile", 3),
            ("Sad face crying for a while", 3),
            ("Loud drum beating boom boom boom", 3),
            ("Quiet whisper in the room", 3),
            ("Open the door, come on in", 3),
            ("Close the door, let's begin", 3),
            ("Daytime bright with sunny light", 3),
            ("Nighttime dark with stars so bright!", 3),
            ("Opposites everywhere, look and see", 3),
            ("How many pairs can you find with me?", 3),
            ("Big, Small. Fast, Slow. Up, Down.", 3),
            ("Hot, Cold. Happy, Sad. Loud, Quiet.", 3),
            ("Open, Close. Day, Night.", 3),
            ("Opposites are right!", 3),
        ],
        "duration_per_line": 3,
    },
}


def create_text_clip(text, duration, fontsize=80, color=TEXT_COLOR, position=("center", "center")):
    """Create a text clip with consistent styling."""
    clip = TextClip(
        text=text,
        font_size=fontsize,
        color=color,
        font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        stroke_color="white",
        stroke_width=3,
        method="label",
        text_align="center"
    ).with_duration(duration).with_position(position)
    return clip


def create_background_clip(duration, color=BG_COLOR):
    """Create a solid color background."""
    return ColorClip(size=(WIDTH, HEIGHT), color=color, duration=duration)


def create_title_card(title, duration=3):
    """Create an animated title card."""
    bg = create_background_clip(duration, ACCENT_COLOR)
    title_clip = TextClip(
        text=title,
        font_size=100,
        color="white",
        font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        stroke_color=TEXT_COLOR,
        stroke_width=4,
        method="caption",
        size=(WIDTH - 100, None),
        text_align="center"
    ).with_duration(duration).with_position(("center", HEIGHT // 3))

    # Add decorative elements
    emoji_clip = TextClip(
        text="🎵 🌟 🎵",
        font_size=80,
        color="white",
        font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        method="caption",
        size=(WIDTH, None),
        text_align="center"
    ).with_duration(duration).with_position(("center", HEIGHT // 2))

    return CompositeVideoClip([bg, title_clip, emoji_clip])


def create_end_card(duration=4):
    """Create end card with subscribe message."""
    bg = create_background_clip(duration, ACCENT_COLOR)

    subscribe = TextClip(
        text="Subscribe for More! 🔔",
        font_size=90,
        color="white",
        font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        stroke_color=TEXT_COLOR,
        stroke_width=3,
        method="caption",
        size=(WIDTH - 100, None),
        text_align="center"
    ).with_duration(duration).with_position(("center", HEIGHT // 2 - 50))

    channel = TextClip(
        text="Kids Rhyme Channel",
        font_size=60,
        color="white",
        font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        method="caption",
        size=(WIDTH, None),
        text_align="center"
    ).with_duration(duration).with_position(("center", HEIGHT // 2 + 80))

    return CompositeVideoClip([bg, subscribe, channel])


def build_video(topic_num, add_audio=False, audio_path=None):
    """Build a complete video for the given topic."""
    topic = TOPICS[topic_num]
    clips = []

    # Title card
    clips.append(create_title_card(topic["title"], 3))

    # Content lines
    for text, duration in topic["lines"]:
        bg = create_background_clip(duration)
        text_clip = create_text_clip(text, duration, fontsize=75)

        # Add line number / visual indicator for counting
        if topic_num == 2 and text.strip().startswith(("One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten")):
            num = text.split(",")[0]
            num_clip = TextClip(
                text=num,
                font_size=200,
                color=ACCENT_COLOR,
                font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                stroke_color="white",
                stroke_width=5,
                method="caption",
                size=(WIDTH - 100, None),
                text_align="center"
            ).with_duration(duration).with_position(("center", HEIGHT // 4))
            clips.append(CompositeVideoClip([bg, text_clip, num_clip]))
        else:
            clips.append(CompositeVideoClip([bg, text_clip]))

    # End card
    clips.append(create_end_card(4))

    # Concatenate all clips
    final = concatenate_videoclips(clips, method="compose")

    # Add audio if provided
    if add_audio and audio_path and os.path.exists(audio_path):
        audio = AudioFileClip(audio_path)
        # Loop or trim audio to match video duration
        if audio.duration < final.duration:
            # Repeat audio to match video duration
            repeats = int(final.duration / audio.duration) + 1
            audio = concatenate_audioclips([audio] * repeats).subclipped(0, final.duration)
        else:
            audio = audio.subclipped(0, final.duration)
        final = final.with_audio(audio)

    return final


def main():
    parser = argparse.ArgumentParser(description="Generate kids rhyme videos")
    parser.add_argument("--topic", type=int, choices=[1, 2, 7, 8], help="Topic number to generate")
    parser.add_argument("--all", action="store_true", help="Generate all topics")
    parser.add_argument("--audio", type=str, help="Path to audio file (TTS output)")
    parser.add_argument("--output-dir", type=str, default="output", help="Output directory")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    topics_to_generate = [1, 2, 7, 8] if args.all else ([args.topic] if args.topic else [1])

    for topic_num in topics_to_generate:
        print(f"Generating video for topic {topic_num}: {TOPICS[topic_num]['name']}...")
        video = build_video(topic_num, add_audio=bool(args.audio), audio_path=args.audio)

        output_path = OUTPUT_DIR / f"topic_{topic_num:02d}_{TOPICS[topic_num]['name']}.mp4"
        print(f"Rendering to {output_path}...")
        video.write_videofile(
            str(output_path),
            fps=FPS,
            codec="libx264",
            audio_codec="aac" if args.audio else None,
            threads=4,
            preset="medium"
        )
        print(f"✅ Done: {output_path}")

    print("\nAll videos generated!")


if __name__ == "__main__":
    main()