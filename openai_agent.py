import os
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=openai_api_key)

def get_gpt_reply(user_query):
    print("📡 Calling OpenAI with:", user_query)

    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Ayasha, an energetic Indian voice assistant working for Riverwood. "
                        "Always begin with this greeting: 'Hi, thanks for calling Riverwood. This is Ayasha. How can I help you today?' "
                        "Then respond helpfully to the user's query in a warm, conversational tone."
                    )
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )
        reply = chat_completion.choices[0].message.content
        print("🧠 GPT-4o replied:", reply)
        return reply
    except Exception as e:
        print("❌ OpenAI error:", e)
        return "Sorry, I couldn't generate a reply right now."
