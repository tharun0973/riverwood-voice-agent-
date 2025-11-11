from flask import Flask, request, Response
from elevenlabs import generate_elevenlabs_audio
from openai_agent import get_gpt_reply
from twilio.twiml.voice_response import VoiceResponse
import os

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice_reply():
    print("✅ Incoming call received at /voice")  # Step 1 logging

    secret = request.args.get("secret")
    if secret != "riverwood-demo-secret":
        return "Unauthorized", 403

    user_query = request.form.get("SpeechResult", "").strip()
    print("User said:", user_query)

    # Fallback if user didn't speak
    if not user_query:
        print("No user input detected")
        fallback_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>I didn’t catch that. Could you please repeat?</Say>
</Response>"""
        return Response(fallback_twiml, mimetype="text/xml")

    # Try GPT reply
    try:
        reply_text = get_gpt_reply(user_query)
        print("GPT-4o replied:", reply_text)
    except Exception as e:
        print("GPT error:", e)
        reply_text = "Sorry, I couldn't generate a reply right now."

    # Fallback if GPT failed
    if not reply_text or "couldn't generate" in reply_text.lower():
        print("Skipping audio — GPT failed")
        fallback_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Sorry, I couldn't generate a reply right now.</Say>
</Response>"""
        return Response(fallback_twiml, mimetype="text/xml")

    # Try ElevenLabs audio
    try:
        audio_url = generate_elevenlabs_audio(reply_text)
        print("Audio URL:", audio_url)
    except Exception as e:
        print("Audio generation failed:", e)
        fallback_twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{reply_text}</Say>
</Response>"""
        return Response(fallback_twiml, mimetype="text/xml")

    # Final TwiML with audio
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{audio_url}</Play>
</Response>"""
    return Response(twiml, mimetype="text/xml")

# Global error handler to catch unexpected crashes
@app.errorhandler(Exception)
def handle_exception(e):
    print("Unhandled exception:", e)
    fallback_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Sorry, something went wrong on our end.</Say>
</Response>"""
    return Response(fallback_twiml, mimetype="text/xml"), 500

if __name__ == "__main__":
    app.run(debug=True)
