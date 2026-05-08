# AI Voice Assistant

A practical AI voice assistant demo built with **Vapi**, **FastAPI**, and a simple **HTML + JavaScript frontend**.

This project lets a website visitor talk to an AI assistant directly from the browser.  
The assistant can answer questions, collect customer details, and send call data to a backend webhook after the call ends.

---

## Overview

The project has three main parts:

### 1. Frontend

The frontend is a basic webpage with buttons to:

- Start the AI voice assistant
- Stop the AI voice assistant
- Connect the browser to a Vapi assistant

### 2. Assistant Configuration

Python scripts are used to create or update the Vapi assistant.

These scripts control things like:

- First message
- System prompt
- LLM model
- Voice provider
- Voice style
- Response length

### 3. Webhook Backend

The backend is built using FastAPI.

It receives webhook events from Vapi, such as:

- User transcript
- Assistant messages
- End-of-call report
- Call summary
- Structured call data

After the call ends, the backend extracts useful customer information and saves it.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | Webhook API server |
| Vapi | Voice assistant platform |
| OpenAI / LLM provider | AI response generation |
| ElevenLabs / OpenAI Voice | Text-to-speech voice |
| HTML | Frontend structure |
| JavaScript | Start/stop assistant from browser |
| dotenv | Load secret keys from `.env` |
| JSONL | Store call logs line by line |

---

## Project Structure

```txt
AI-voice-Assistant/
│
├── index.html
├── creating_assistant.py
├── update_assistant.py
├── webhook_backend.py
├── calls.jsonl
│
└── prompts/
    ├── system_prompt.txt
    └── first_message.txt
```

---

## File Explanation

| File | What It Does |
|---|---|
| `index.html` | Simple frontend to start and stop the voice assistant |
| `creating_assistant.py` | Creates a new Vapi assistant |
| `update_assistant.py` | Updates an existing Vapi assistant using `.env` values and prompt files |
| `webhook_backend.py` | FastAPI backend that receives Vapi webhook events |
| `calls.jsonl` | Stores final call details, one call per line |
| `prompts/system_prompt.txt` | Main behavior instructions for the assistant |
| `prompts/first_message.txt` | First message spoken by the assistant |

---

## Main Features

- Browser-based AI voice assistant
- Start and stop assistant from a webpage
- Vapi Web SDK integration
- Python script to create assistant
- Python script to update assistant
- Custom system prompt support
- Custom first message support
- FastAPI webhook backend
- Bearer token validation for webhook security
- Transcript collection during calls
- End-of-call summary extraction
- Customer name extraction
- Spoken email extraction
- Phone number extraction
- Call data saved in JSONL format

---

## How It Works

```txt
User opens website
        ↓
User clicks "Start Assistant"
        ↓
Vapi starts voice call in browser
        ↓
User talks with AI assistant
        ↓
Vapi sends call events to FastAPI webhook
        ↓
Backend stores transcript parts
        ↓
Call ends
        ↓
Backend extracts customer info and summary
        ↓
Backend saves final data into calls.jsonl
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
# Vapi private/server API key
VAPI_API_KEY_PRIVATE=your_private_vapi_key_here

# Optional older key used in creating_assistant.py
VAPI_API_KEY=your_private_vapi_key_here

# Existing Vapi assistant ID
VAPI_ASSISTANT_ID_1=your_assistant_id_here

# Webhook security token
VAPI_CUSTOM_CRED=your_custom_webhook_secret_here

# LLM settings
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
MAX_LLM_TOKENS=80

# Voice settings
VOICE_PROVIDER=11labs
VOICE_ID_11LABS=your_voice_id_here
VOICE_STYLE=0.5
```

Important:

Do **not** push your `.env` file to GitHub.

Your `.env` file contains private keys.  
Private keys are like the password to your project. Keep them locked away.

---

## Frontend Setup

In `index.html`, replace these values:

```js
const publicKey = "your_vapi_public_key";
const assistantId = "your_vapi_assistant_id";
```

### Important Key Difference

| Key Type | Safe in Frontend? | Meaning |
|---|---:|---|
| Public Key | Yes | Used by browser to start the assistant |
| Assistant ID | Yes | Tells Vapi which assistant to use |
| Private API Key | No | Used only on backend/server |

Never put your private API key inside `index.html`.

---

## Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/rezzraj/AI-voice-Assistant.git
cd AI-voice-Assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

A virtual environment is a separate Python box for this project.  
It keeps this project's packages away from your other Python projects.

### 3. Activate the Virtual Environment

For Windows PowerShell:

```bash
venv\Scripts\activate
```

For Linux/Mac:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv vapi_server_sdk
```

---

## Create Prompt Files

Create a folder named `prompts`.

```bash
mkdir prompts
```

Create this file:

```txt
prompts/system_prompt.txt
```

Example content:

```txt
You are a short, polite, and helpful website voice assistant.
Keep replies under 2 sentences.
Ask for the user's name, business type, email, and phone number when needed.
Do not give long answers.
```

Create this file:

```txt
prompts/first_message.txt
```

Example content:

```txt
Hi! I am your AI assistant. How can I help you today?
```

---

## Run the Backend

Start the FastAPI server:

```bash
uvicorn webhook_backend:app --reload --port 8000
```

Open this URL in the browser:

```txt
http://127.0.0.1:8000
```

Expected response:

```json
{
  "message": "server active"
}
```

---

## Expose Local Backend Using Ngrok

Vapi needs a public URL to send webhook data to your local backend.

Run:

```bash
ngrok http 8000
```

Ngrok will give a URL like this:

```txt
https://your-ngrok-url.ngrok-free.app
```

Use this webhook URL in Vapi:

```txt
https://your-ngrok-url.ngrok-free.app/vapi/webhook
```

---

## Webhook Security

The backend checks this header:

```txt
Authorization: Bearer your_custom_webhook_secret_here
```

This means the webhook only accepts requests that have the correct token.

Simple meaning:

- Correct token: request allowed
- Wrong token: request blocked
- No token: request blocked

Tiny security guard at the backend gate. 🛡️

---

## Create a New Vapi Assistant

Run:

```bash
python creating_assistant.py
```

This creates a new assistant and prints the assistant ID.

Copy the assistant ID and use it in:

- `.env`
- `index.html`

---

## Update an Existing Vapi Assistant

Run:

```bash
python update_assistant.py
```

This updates the assistant using:

- `prompts/system_prompt.txt`
- `prompts/first_message.txt`
- `.env` model settings
- `.env` voice settings

This is useful when you want to improve the assistant without creating a new assistant every time.

---

## Run the Frontend

You can directly open `index.html` in your browser.

Or you can run a simple local server:

```bash
python -m http.server 5500
```

Then open:

```txt
http://localhost:5500
```

Use the buttons:

| Button | Action |
|---|---|
| Start Assistant | Starts the voice assistant |
| Stop Assistant | Ends the voice assistant |

---

## Saved Call Format

Each completed call is saved in `calls.jsonl`.

Example:

```json
{
  "saved_at": "2026-05-07T19:46:16.896083",
  "customer_name": "John",
  "email": "john@gmail.com",
  "phone": "9876543210",
  "summary": "John asked about using the AI assistant for appointment booking and call handling."
}
```

---

## What is JSONL?

JSONL means **JSON Lines**.

Normal JSON usually stores data in one big object.

JSONL stores one JSON object per line.

Example:

```jsonl
{"name": "John", "phone": "9876543210"}
{"name": "Akshit", "phone": "9123456780"}
```

This is useful for logs because every call becomes one clean row.

---

## Data Extraction Logic

The backend tries to extract customer information from the transcript.

### 1. Customer Name

It checks phrases like:

```txt
my name is Akshit
this is Akshit
I am Akshit
I'm Akshit
```

### 2. Email

It supports spoken email formats.

Example spoken email:

```txt
akshit dot raj at gmail dot com
```

Converted into:

```txt
akshit.raj@gmail.com
```

### 3. Phone Number

It supports normal phone numbers:

```txt
9876543210
```

It also supports spoken numbers:

```txt
nine eight seven six five four three two one zero
```

Converted into:

```txt
9876543210
```

---

## API Endpoints

### Health Check

```txt
GET /
```

Response:

```json
{
  "message": "server active"
}
```

### Vapi Webhook

```txt
POST /vapi/webhook
```

Used by Vapi to send:

- Transcript events
- Assistant/user messages
- End-of-call report
- Call summary
- Structured call data

---

## Important Security Notes

Do not commit these files to GitHub:

```txt
.env
calls.jsonl
raw_webhooks.jsonl
```

Recommended `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
calls.jsonl
raw_webhooks.jsonl
```

These files can contain:

- API keys
- Customer names
- Phone numbers
- Email addresses
- Call summaries

Keep the privacy dragon inside the cave. 🐉

---

## Possible Improvements

Future improvements can include:

- Database storage instead of JSONL
- Admin dashboard for call logs
- Better email confirmation
- Better phone number confirmation
- Cleaner frontend design
- Deployment on Render, Railway, or Fly.io
- Webhook retry handling
- Better logging with timestamps
- Multiple assistants for different businesses
- CRM integration
- Automatic follow-up email sending

---

## What I Learned

Through this project, I learned:

- How browser-based voice assistants work
- How Vapi connects frontend and backend
- How webhooks send real-time call events
- How to use FastAPI for backend APIs
- How to protect secrets using environment variables
- How to extract useful customer details from transcripts
- How to save structured call data for later use

---

## Author

**Akshit Raj**

Built as a practical AI voice assistant demo using Vapi, FastAPI, and a lightweight frontend.
