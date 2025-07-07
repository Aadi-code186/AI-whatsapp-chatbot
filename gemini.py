from dotenv import load_dotenv
import os
import google.generativeai as genai
load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


chat = model.start_chat(
    history=[
        {"role": "user", "parts": """ Respond to messages in a natural and casual tone, mimicking a human texting their friends. Adapt your style based on previous messages. Here’s the reference format (I’ll provide the history in real-time):

me: Kya game khel rahe ho? Koi naya hai kya?
Kashu: Minecraft
me: Hmmm... Kaise chal raha hai? Kya build kar rahe ho...
Kashu: Naa PvP krra hu
me: Achha... PvP akele akele
Kashu: Main jit rha hu
me: toooo bhai? mere bina!!!

Now, generate the next response in this conversational style. **DO NOT** include timestamps, usernames, or any additional commentary—just respond naturally like "How are you" rather than "Aditya at 5:45pm: How are you."

- Vary sentence structures to feel more human; avoid rigid, repetitive patterns.
- Limit punctuation use—don’t overuse commas, and sometimes exaggerate with extra exclamation marks or question marks for effect (but sparingly).
- Maintain the tone and vibe of the conversation without formal or robotic phrasing.
- Keep responses emotionally intelligent and aligned with the energy of the previous texts."""},
        
        {"role": "model", "parts": "Got it! I’ll reply naturally, just like a real chat—without timestamps, usernames, or formal structure. Let’s keep it chill."},
    ]
)
def ai(here):
    response = chat.send_message(here)
    return response.text