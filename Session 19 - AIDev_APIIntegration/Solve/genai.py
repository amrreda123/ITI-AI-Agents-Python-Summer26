import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()
chat_session = client.chats.create(
    model="gemini-3.7-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant."
    )
)

def send(user_input):
    stream = chat_session.send_message_stream(user_input)
    full_reply = ""
    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_reply += chunk.text
    print()
    return full_reply

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    send(user_input)