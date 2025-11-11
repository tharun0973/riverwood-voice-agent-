from flask import Flask, request, Response
from dotenv import load_dotenv
import os
from openai_agent import get_gpt_reply
from elevenlabs import generate_elevenlabs_audio

load_dotenv()
app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice_reply():
    # Accept secret from query param (fallback for Twilio trial accounts)
    expected_secret = os.getenv("TWILIO_WEBHOOK_SECRET")
    received_secret = request.args.get("secret") or request.headers.get("X-Twilio-Secret")

    if expected_secret and received_secret != expected_secret:
        return "Unauthorized", 403

    # Get user query from Twilio
    user_query = request.form.get("SpeechResult", "Hello, how can I help?")
    print("User said:", user_query)

    # Generate GPT-4o reply
    reply_text = get_gpt_reply(user_query)
    print("GPT-4o replied:", reply_text)

    # Generate Ayasha voice .mp3
    audio_url = generate_elevenlabs_audio(reply_text)
    print("Audio URL:", audio_url)

    # Return TwiML response
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{audio_url}</Play>
</Response>"""

    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
