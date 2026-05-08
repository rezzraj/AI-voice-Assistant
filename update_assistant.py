import os
from dotenv import load_dotenv
from vapi import Vapi

load_dotenv()

#loading prompts from the file
with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()
with open("prompts/first_message.txt", "r", encoding="utf-8") as f:
    first_message = f.read()

#vapi private key
client = Vapi(token=os.getenv('VAPI_API_KEY_PRIVATE'))

#creating assistant
assistant = client.assistants.update(
    os.getenv("VAPI_ASSISTANT_ID_1"),
    first_message=f"{first_message}",
    model={
        "provider": f"{os.getenv('LLM_PROVIDER')}",
        "model": f"{os.getenv('LLM_MODEL')}",
        "temperature": 0.2,
        "max_tokens": int(os.getenv("MAX_LLM_TOKENS",80)),
        "messages": [
            {
                "role": "system",
                "content": f"""""{system_prompt}"""""
            }
        ],
    },
    voice={
        "provider": f"{os.getenv('VOICE_PROVIDER')}",
        "voice_id": f"{os.getenv('VOICE_ID_11LABS')}",
        #how dramatic
        "style": float(os.getenv("VOICE_STYLE",0.5)),
    },
)

print("Updated assistant:", assistant.id)
