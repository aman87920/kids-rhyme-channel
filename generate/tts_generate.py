#!/usr/bin/env python3
"""
TTS Generation Script for Kids Rhyme Channel
Supports multiple TTS providers: ElevenLabs, OpenAI, Coqui (local), Edge TTS (free), Google Cloud TTS
"""

import os
import argparse
from pathlib import Path

# ============================================================
# PROVIDER 1: ElevenLabs (Best quality, paid)
# ============================================================
def generate_elevenlabs(text, output_path, voice_id="21m00Tcm4TlvDq8ikWAM", api_key=None):
    """
    Voice IDs for kids content:
    - Rachel (21m00Tcm4TlvDq8ikWAM) - Warm, friendly female
    - Domi (AZnzlk1XvdvUeBnXmlld) - Energetic female
    - Bella (EXAVITQu4vr4xnSDxMaL) - Soft female
    - Antoni (ErXwobaYiN019PkySvjV) - Warm male
    """
    try:
        from elevenlabs import generate, save, set_api_key
        if api_key:
            set_api_key(api_key)
        audio = generate(text=text, voice=voice_id, model="eleven_multilingual_v2")
        save(audio, output_path)
        return True
    except ImportError:
        print("Install: pip install elevenlabs")
        return False
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        return False


# ============================================================
# PROVIDER 2: OpenAI TTS (Good quality, paid)
# ============================================================
def generate_openai(text, output_path, voice="nova", api_key=None):
    """
    Voices: alloy, echo, fable, onyx, nova, shimmer
    Best for kids: nova (warm female), shimmer (gentle female)
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text,
            speed=1.0
        )
        response.stream_to_file(output_path)
        return True
    except ImportError:
        print("Install: pip install openai")
        return False
    except Exception as e:
        print(f"OpenAI TTS error: {e}")
        return False


# ============================================================
# PROVIDER 3: Edge TTS (FREE, Microsoft voices)
# ============================================================
async def generate_edge_tts(text, output_path, voice="en-US-JennyNeural"):
    """
    Free Microsoft Edge voices. Best for kids:
    - en-US-JennyNeural - Friendly female (default)
    - en-US-GuyNeural - Friendly male
    - en-US-AriaNeural - Warm female
    - en-GB-SoniaNeural - British female
    - en-AU-NatashaNeural - Australian female
    """
    try:
        import edge_tts
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return True
    except ImportError:
        print("Install: pip install edge-tts")
        return False
    except Exception as e:
        print(f"Edge TTS error: {e}")
        return False


# ============================================================
# PROVIDER 4: Coqui TTS (Local, free, open source)
# ============================================================
def generate_coqui(text, output_path, model_name="tts_models/en/ljspeech/tacotron2-DDC"):
    """
    Runs locally, no API key needed. Models:
    - tts_models/en/ljspeech/tacotron2-DDC (fast, decent)
    - tts_models/en/ljspeech/glow-tts (faster)
    - tts_models/en/vctk/vits (multi-speaker)
    """
    try:
        from TTS.api import TTS
        tts = TTS(model_name=model_name, progress_bar=False)
        tts.tts_to_file(text=text, file_path=output_path)
        return True
    except ImportError:
        print("Install: pip install TTS")
        return False
    except Exception as e:
        print(f"Coqui TTS error: {e}")
        return False


# ============================================================
# PROVIDER 5: Google Cloud TTS (Premium, Neural2/WaveNet voices)
# ============================================================
def generate_google_tts(text, output_path, voice_name="en-US-Neural2-F", credentials_path=None):
    """
    Premium Google Cloud voices. Best for kids:
    - en-US-Neural2-F - Warm, friendly female (default)
    - en-US-Neural2-C - Energetic female
    - en-US-Neural2-A - Natural female
    - en-US-Neural2-D - Deep female
    - en-US-Wavenet-F - Natural female (WaveNet)
    - en-US-Wavenet-C - Energetic female (WaveNet)
    - en-GB-Neural2-A - British female
    - en-AU-Neural2-A - Australian female

    Requires: pip install google-cloud-texttospeech
    And: GOOGLE_APPLICATION_CREDENTIALS env var or credentials_path
    """
    try:
        from google.cloud import texttospeech

        # Set credentials if provided
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
            volume_gain_db=0.0
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open(output_path, "wb") as f:
            f.write(response.audio_content)
        return True
    except ImportError:
        print("Install: pip install google-cloud-texttospeech")
        return False
    except Exception as e:
        print(f"Google Cloud TTS error: {e}")
        return False


# ============================================================
# SCRIPT LOADING
# ============================================================
SCRIPTS = {
    1: """A is for Alligator, snapping his jaws. B is for Bear, climbing up paws. C is for Cat, curled up so tight. D is for Dog, barking all night. E is for Elephant, trunk swinging wide. F is for Fox, with a bushy tail to hide. G is for Giraffe, reaching up high. H is for Hippo, splashing nearby. I is for Iguana, basking in sun. J is for Jaguar, having such fun. K is for Kangaroo, hopping around. L is for Lion, the king of the ground. M is for Monkey, swinging on vine. N is for Nightingale, singing so fine. O is for Owl, hooting at moon. P is for Penguin, waddling in tune. Q is for Quail, running so fast. R is for Rabbit, hopping at last. S is for Snake, sliding along. T is for Tiger, brave and so strong. U is for Unicorn, magical and bright. V is for Vulture, soaring in flight. W is for Whale, swimming so deep. X is for X-ray fish, secrets to keep. Y is for Yak, with shaggy long hair. Z is for Zebra, stripes everywhere! Now you know your A to Z. Animals are friends, you and me. Sing it again, sing it with glee. Learning letters is easy as can be!""",

    2: """One, one, clap your hands! Two, two, touch your shoes! Three, three, touch your knee! Four, four, touch the floor! Five, five, give a high-five! Six, six, do some kicks! Seven, seven, point to heaven! Eight, eight, skate like great! Nine, nine, draw a line! Ten, ten, do it again! One, two, three, four, five. Six, seven, eight, nine, ten. Count with me, count with you. Numbers are fun to do! Let's count backwards, don't be slow. Ten, nine, eight, seven, six. Five, four, three, two, one. Blast off! We're done!""",

    7: """Head, shoulders, knees, and toes. Knees and toes! Head, shoulders, knees, and toes. Knees and toes! Eyes and ears and mouth and nose. Head, shoulders, knees, and toes. Knees and toes! Now let's dance, move your body! Touch your head, touch your shoulders. Touch your knees, touch your toes. Spin around, touch the ground. Jump up high, reach the sky! Head, shoulders, knees, and toes. Knees and toes! Head, shoulders, knees, and toes. Knees and toes! Eyes and ears and mouth and nose. Head, shoulders, knees, and toes. Knees and toes! Faster now! Ready, set, go! Head, shoulders, knees, and toes! Super fast! Head, shoulders, knees, and toes! You did it! Great job!""",

    8: """Big elephant, small little mouse. Big and small, in this house! Fast cheetah, slow snail crawls. Fast and slow, up the walls! Up goes the balloon in the sky. Down comes the rain, falling by. Hot soup warming in the bowl. Cold ice cream, sweet and cold! Happy face with a great big smile. Sad face crying for a while. Loud drum beating boom boom boom. Quiet whisper in the room. Open the door, come on in. Close the door, let's begin. Daytime bright with sunny light. Nighttime dark with stars so bright! Opposites everywhere, look and see. How many pairs can you find with me? Big, Small. Fast, Slow. Up, Down. Hot, Cold. Happy, Sad. Loud, Quiet. Open, Close. Day, Night. Opposites are right!""",
}


TOPIC_NAMES = {
    1: "alphabet_adventure",
    2: "counting_1to10",
    7: "body_parts_dance",
    8: "opposites",
}


def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio for kids rhymes")
    parser.add_argument("--topic", type=int, choices=[1, 2, 7, 8], required=True, help="Topic number")
    parser.add_argument("--provider", choices=["elevenlabs", "openai", "edge", "coqui", "google"], default="edge", help="TTS provider")
    parser.add_argument("--voice", type=str, help="Voice ID/name (provider-specific)")
    parser.add_argument("--api-key", type=str, help="API key (for ElevenLabs/OpenAI)")
    parser.add_argument("--credentials", type=str, help="Path to Google Cloud credentials JSON (for Google TTS)")
    parser.add_argument("--output-dir", type=str, default="assets/audio", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = SCRIPTS[args.topic]
    topic_name = TOPIC_NAMES[args.topic]
    output_path = output_dir / f"topic_{args.topic:02d}_{topic_name}.mp3"

    print(f"Generating TTS for topic {args.topic} ({topic_name}) using {args.provider}...")
    print(f"Output: {output_path}")

    success = False

    if args.provider == "elevenlabs":
        voice = args.voice or "21m00Tcm4TlvDq8ikWAM"  # Rachel
        success = generate_elevenlabs(text, str(output_path), voice, args.api_key)

    elif args.provider == "openai":
        voice = args.voice or "nova"
        success = generate_openai(text, str(output_path), voice, args.api_key)

    elif args.provider == "edge":
        voice = args.voice or "en-US-JennyNeural"
        import asyncio
        success = asyncio.run(generate_edge_tts(text, str(output_path), voice))

    elif args.provider == "coqui":
        success = generate_coqui(text, str(output_path))

    elif args.provider == "google":
        voice = args.voice or "en-US-Neural2-F"
        success = generate_google_tts(text, str(output_path), voice, args.credentials)

    if success:
        print(f"✅ Audio saved to {output_path}")
    else:
        print("❌ Generation failed")


if __name__ == "__main__":
    main()