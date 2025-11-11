from dotenv import load_dotenv
load_dotenv()

from elevenlabs import generate_elevenlabs_audio

text = "Namaste Sir, kal ka update yeh hai — basement ka kaam complete ho gaya hai."
url = generate_elevenlabs_audio(text)
print("Audio URL:", url)
