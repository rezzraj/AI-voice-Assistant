import os
from dotenv import load_dotenv
from vapi import Vapi

load_dotenv()

client = Vapi(token=os.getenv("VAPI_API_KEY"))

assistant = client.assistants.create(
    name="Website Demo Agent",
    first_message="Hi! How can I help you?",
    model={
        "provider": "openai",
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a short and polite website voice assistant. Keep replies under 2 sentences."
            }
        ],
    },
    voice={
        "provider": "openai",
        "voice_id": "alloy",
    },
)

print(assistant.id)
