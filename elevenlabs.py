import os
import requests

def generate_elevenlabs_audio(text):
    # Load voice ID and Railway URL from .env
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "hGb0Exk8cp4vQEnwolxa")
    railway_url = os.getenv("RAILWAY_URL", "http://localhost:5000")
    
    # ElevenLabs API endpoint
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }
    
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    # Send request to ElevenLabs
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")
    
    # Save audio to static folder
    audio_path = "static/output.mp3"
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    # Return public URL for Twilio playback
    return f"{railway_url}/static/output.mp3"
