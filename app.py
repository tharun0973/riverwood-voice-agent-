print("🛠️ Railway container booted — app.py is executing")
from flask import Flask, request, Response, send_from_directory
from elevenlabs import generate_elevenlabs_audio
from openai_agent import get_gpt_reply
import os

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice_reply():
    try:
        print("✅ Incoming call received at /voice")

        secret = request.args.get("secret")
        if secret != "riverwood-demo-secret":
            print("❌ Invalid secret")
            return "Unauthorized", 403

        user_query = request.form.get("SpeechResult", "").strip()
        print("User said:", user_query)

        if not user_query:
            print("⚠️ No user input detected")
            fallback_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>I didn’t catch that. Could you please repeat?</Say>
</Response>"""
            return Response(fallback_twiml, mimetype="text/xml")

        reply_text = get_gpt_reply(user_query)
        print("🧠 GPT replied:", reply_text)

        audio_url = generate_elevenlabs_audio(reply_text)
        print("🔊 Audio URL:", audio_url)

        if not audio_url:
            print("⚠️ Audio generation failed — fallback to Say")
            fallback_twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{reply_text}</Say>
</Response>"""
            return Response(fallback_twiml, mimetype="text/xml")

        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Play>{audio_url}</Play>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    except Exception as e:
        print("❌ voice_reply crashed:", e)
        fallback_twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Sorry, something went wrong on our end.</Say>
</Response>"""
        return Response(fallback_twiml, mimetype="text/xml"), 500

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    print("🚀 Flask app is starting on Railway...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
