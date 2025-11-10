from flask import Flask, request
from dotenv import load_dotenv
import os
from openai_agent import get_gpt_reply
from elevenlabs import generate_elevenlabs_audio

load_dotenv()
app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice_reply():
    # Optional: validate webhook secret
    if request.headers.get("X-Twilio-Secret") != os.getenv("TWILIO_WEBHOOK_SECRET"):
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
    return f'<Response><Play>{audio_url}</Play></Response>', 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
