from openai import OpenAI
import os

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_gpt_reply(user_query):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Ayasha, a helpful voice assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", str(e))
        return "Sorry, I couldn't generate a reply right now."
