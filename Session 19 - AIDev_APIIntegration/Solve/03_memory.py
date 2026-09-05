from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

chat_session = client.chats.create(
    model="gemini-3.7-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a friendly assistant."
    )
)

def ask(user_input):
    response = chat_session.send_message(user_input)
    return response.text

print(ask("My favorite color is blue."))
print(ask("What is my favorite color?"))
