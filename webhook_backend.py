from fastapi import FastAPI, Request, HTTPException
import json
import re
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


def messages_to_text(messages):
    lines = []

    for m in messages or []:
        role = m.get("role", "unknown")
        text = m.get("message") or m.get("content") or ""

        if text and role in ["user", "assistant", "bot"]:
            lines.append(f"{role}: {text}")

    return "\n".join(lines)


def extract_spoken_email(text: str):
    if not text:
        return None

    text = text.lower()

    # only take part after "email is"
    match = re.search(r"(email is|email address is|my email is)\s+(.+)", text)
    if match:
        text = match.group(2)

    replacements = {
        " at ": "@",
        " dot ": ".",
        " period ": ".",
        " underscore ": "_",
        " dash ": "-",
        " hyphen ": "-",
    }

    for spoken, symbol in replacements.items():
        text = text.replace(spoken, symbol)

    # remove spaces between single letters
    # "m a n i k" -> "manik"
    text = re.sub(r"\b([a-z])\s+(?=[a-z]\b)", r"\1", text)

    # remove remaining spaces around email symbols
    text = re.sub(r"\s*@\s*", "@", text)
    text = re.sub(r"\s*\.\s*", ".", text)
    text = text.replace(" ", "")

    # find email pattern
    match = re.search(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", text)

    return match.group(0) if match else None

def extract_phone(text: str):
    if not text:
        return None

    # normal digit phone: 9876543210
    digits = re.sub(r"\D", "", text)

    if len(digits) >= 10:
        return digits[-10:]

    # spoken digit phone: nine eight seven...
    return normalize_spoken_digits(text)










def save_raw_event(data):
    with open("raw_webhooks.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def normalize_spoken_digits(text: str):
    word_to_digit = {
        "zero": "0",
        "oh": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    words = re.findall(r"\b(zero|oh|one|two|three|four|five|six|seven|eight|nine)\b", text.lower())
    digits = "".join(word_to_digit[w] for w in words)

    if len(digits) >= 10:
        return digits[-10:]

    return None
def save_call(customer_name, email, phone, summary):
    record = {
        "saved_at": datetime.now().isoformat(),
        "customer_name": customer_name,
        "email": email,
        "phone": phone,
        "summary": summary
    }

    with open("calls.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def extract_name(transcript: str):
    if not transcript:
        return None

    patterns = [
        r"customer\s*:\s*([A-Za-z .'-]+)",
        r"my name is\s+([A-Za-z .'-]+)",
        r"this is\s+([A-Za-z .'-]+)",
        r"i am\s+([A-Za-z .'-]+)",
        r"i'm\s+([A-Za-z .'-]+)",
    ]

    stop_words = [
        r"\band my phone\b",
        r"\bmy phone\b",
        r"\bphone number\b",
        r"\bmobile number\b",
        r"\bnumber is\b",
        r"\bcontact number\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, transcript, re.IGNORECASE)

        if match:
            name = match.group(1).strip()

            # cut the name when phone info starts
            name = re.split("|".join(stop_words), name, flags=re.IGNORECASE)[0].strip()

            # cut at punctuation/new line
            name = re.split(r"[.\n,]", name)[0].strip()

            return name if name else None

    return None













#INIT FAST API
app = FastAPI()

#VALIDATION TOKEN
VAPI_CUSTOM_CRED=os.getenv("VAPI_CUSTOM_CRED")
if not VAPI_CUSTOM_CRED:
    raise RuntimeError("VAPI_CUSTOM_CRED missing from .env")

call_memory = {}





#API BLOCK
@app.get("/")
async def root():
    return {"message": "server active"}
@app.post("/vapi/webhook")
async def vapi_webhook(request: Request):

    #adding custom validation for security
    auth_header = request.headers.get("Authorization")
    if auth_header != f"Bearer {VAPI_CUSTOM_CRED}":
        raise HTTPException(status_code=401, detail="Unauthorized")


    #loading data
    data = await request.json()
    if data:
        print("received vapi data")
    else:
        print("no data received")
        raise HTTPException(status_code=400)





    #saving data into variable
    msg = data.get("message", {})

    call_id = (
            msg.get("call", {}).get("id")
            or msg.get("callId")
            or "unknown_call"
    )
    event_type = msg.get("type")

    # make memory for this call
    if call_id not in call_memory:
        call_memory[call_id] = []

    # collect transcript only
    if event_type == "transcript":
        role = msg.get("role", "unknown")
        text = msg.get("transcript") or ""

        if text:
            call_memory[call_id].append(f"{role}: {text}")

    # saving when the call ends
    if event_type == "end-of-call-report":
        print("inside end-of-call-report")

        manual_transcript = "\n".join(call_memory.get(call_id, []))

        artifact = msg.get("artifact", {})

        artifact_transcript = artifact.get("transcript", "")

        artifact_messages_text = messages_to_text(artifact.get("messages"))

        conversation_text = messages_to_text(msg.get("conversation"))

        regex_text = (
                manual_transcript
                or artifact_transcript
                or artifact_messages_text
                or conversation_text
                or ""
        )

        summary = (
                msg.get("analysis", {}).get("summary")
                or msg.get("call", {}).get("analysis", {}).get("summary")
                or ""
        )

        structured = (
                msg.get("analysis", {}).get("structuredData")
                or msg.get("call", {}).get("analysis", {}).get("structuredData")
                or {}
        )

        customer_name = (
                structured.get("customer_name")
                or extract_name(regex_text)
                or extract_name(summary)
                or "UNKNOWN"
        )

        email = extract_spoken_email(regex_text) or "UNKNOWN"
        phone = extract_phone(regex_text) or "UNKNOWN"

        print("Customer:", customer_name)
        print("Email:", email)
        print("Phone:", phone)
        print("Summary:", summary or "NO SUMMARY FOUND")
        print("Regex text:\n", regex_text or "NO TEXT FOUND")

        save_call(customer_name, email, phone, summary)

        call_memory.pop(call_id, None)
    else:
        print("no end of the call report")

    return {"status": "ok"}
