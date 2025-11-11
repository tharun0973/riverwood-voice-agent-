import os
import requests

def generate_elevenlabs_audio(text):
    # Load API keys and voice ID from environment
    api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    voice_id = os.getenv("ELEVENLABS_VOICE_ID")
    railway_url = os.getenv("RAILWAY_URL")  # e.g. https://riverwood-voice-agent-production.up.railway.app

    # ElevenLabs API endpoint
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

    if response.status_code == 200:
        # Save audio to static/output.mp3
        audio_path = "static/output.mp3"
        with open(audio_path, "wb") as f:
            f.write(response.content)

        # Return public URL for Twilio playback
        return f"{railway_url}/static/output.mp3"
    else:
        print("ElevenLabs error:", response.status_code, response.text)
        return ""
