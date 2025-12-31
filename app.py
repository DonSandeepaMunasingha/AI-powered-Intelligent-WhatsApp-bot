from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os
from rag import retrieve_context
from collections import defaultdict, deque
import hashlib
LAST_INTENT = {}
def get_intent(text):
    text = text.lower().strip()
    return hashlib.md5(text.encode()).hexdigest()


COMPANY_PROFILE = """
Company Name: Sandeepa Resturent
Business Type: Restaurant & Dining
Core Services:

Dine-in restaurant services

Takeout & delivery

Private events

Catering
Tone: Professional, helpful, welcoming, customer-focused

Assistant Identity:

You are the official virtual assistant of [Sandeepa Resturent]

Your name is DineMate

Your purpose is to assist customers with reservations, menu questions, hours, delivery, and all restaurant-related inquiries
"""
# Store last 6 messages per user (3 user + 3 bot)
conversation_memory = defaultdict(lambda: deque(maxlen=6))


app = Flask(__name__)

# 🔐 OpenRouter API Key
OPENROUTER_API_KEY = "ad your api key"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    user_id = request.values.get("From")

    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("Please send a message.")
        return str(resp)

    # 🔹 Intent detection (AFTER incoming_msg exists)
    intent = get_intent(incoming_msg)
    last_intent = LAST_INTENT.get(user_id)
    is_repeat = intent == last_intent
    LAST_INTENT[user_id] = intent

    # 🔹 Retrieve company knowledge (RAG)
    context = retrieve_context(incoming_msg)
    if not context.strip():
        context = "No direct Q&A found in company knowledge."

    # 🔹 Conversation history
    history = list(conversation_memory[user_id])

    # 🔹 Call AI
    ai_reply = call_openrouter(
        user_message=incoming_msg,
        context=context,
        conversation_history=history,
        is_repeat=is_repeat
    )

    # 🔹 Save conversation
    conversation_memory[user_id].append(f"User: {incoming_msg}")
    conversation_memory[user_id].append(f"Assistant: {ai_reply}")

    msg.body(ai_reply)
    return str(resp)


def call_openrouter(user_message, context, conversation_history, is_repeat):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "WhatsApp Advanced RAG Bot"
    }

    # 🧠 Build conversation memory text
    history_text = "\n".join(conversation_history)

    repeat_instruction = (
        "The user is repeating the same question. "
        "Respond more naturally: acknowledge it, rephrase the answer, "
        "or shorten it. Avoid repeating the same wording."
        if is_repeat else
        "Answer normally and helpfully."
    )
    # 🧠 SMART SYSTEM PROMPT
    system_prompt = f"""
You are a human-like WhatsApp business assistant. {repeat_instruction}

Assistant Identity:
- Your name is DineMate
- You represent {COMPANY_PROFILE}

Behavior Rules (VERY IMPORTANT):
- Sound natural, friendly, and human
- NEVER repeat the same wording if the user repeats a question
- If the user asks the same thing again, respond differently:
  - rephrase
  - shorten
  - acknowledge you already answered
- Sometimes be brief, sometimes detailed
- Do NOT behave like a script bot
- Do NOT copy answers word-for-word from knowledge
- Adapt tone based on conversation flow
- If information exists in company knowledge, use it
- If not, infer politely based on company services

Company Knowledge (use only if relevant):
{context}

Conversation History (use for awareness, not repetition):
{history_text}
"""
    payload = {
        "model": "qwen/qwen3-8b",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.85,
        "top_p": 0.9,
        "presence_penalty": 0.4,
        "max_tokens": 350
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        data = response.json()
        content = data["choices"][0]["message"].get("content", "").strip()

        return content if content else "Could you please clarify a bit more?"

    except Exception as e:
        return "I'm here to help, but I'm facing a temporary issue."

if __name__ == "__main__":
    app.run(port=5000)
