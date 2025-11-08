import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gpt_reply(user_query):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_query}]
    )
    return response.choices[0].message.content
