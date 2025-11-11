import os
import requests

def generate_elevenlabs_audio(text):
    print("🔊 Generating ElevenLabs audio for:", text)

    api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "").strip()
    railway_url = os.getenv("RAILWAY_URL", "").strip()

    if not api_key or not voice_id or not railway_url:
        print("❌ Missing ElevenLabs config — check API key, voice ID, or Railway URL")
        raise Exception("Missing ElevenLabs configuration")

    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code != 200:
        print("❌ ElevenLabs error:", response.status_code, response.text)
        raise Exception("ElevenLabs audio generation failed")

    # Save audio to static/output.mp3
    audio_path = "static/output.mp3"
    with open(audio_path, "wb") as f:
        f.write(response.content)

    audio_url = f"{railway_url}/static/output.mp3"
    print("✅ Audio URL:", audio_url)
    return audio_url
