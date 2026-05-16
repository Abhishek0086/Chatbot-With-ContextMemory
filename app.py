"""
Chatbot with Context Memory
Built using: Python, Flask, Anthropic Claude API
Context memory is maintained by passing the full conversation history with every API call.
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from anthropic import Anthropic

app = Flask(__name__, template_folder="templates", static_folder="static")

# Anthropic client — reads ANTHROPIC_API_KEY from environment
client = Anthropic()

# In-memory session store  { session_id: [ {role, content, timestamp}, ... ] }
sessions = {}

SYSTEM_PROMPT = """You are ARIA (Adaptive Reasoning & Intelligent Assistant), an intelligent conversational AI with context memory.

You were built as a capstone project during an AI internship at SuprMentr, using:
- Python & Flask for the backend
- Anthropic Claude API (claude-sonnet-4-20250514) as the LLM
- Context memory implemented by maintaining and replaying full conversation history
- NumPy, Pandas, scikit-learn concepts learned during the internship

Your personality:
- Warm, curious, and articulate
- You remember everything said earlier in the conversation and reference it naturally
- When asked how you work, explain the context memory mechanism clearly
- Be concise but thorough; avoid unnecessary filler

You have deep knowledge of:
- Python programming, data science, machine learning
- NLP, transformers, LLMs, and prompt engineering
- The internship curriculum covering numpy, pandas, sklearn, matplotlib, seaborn
- AI concepts: supervised/unsupervised learning, neural networks, CNNs, clustering
"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat")
def chat_page():
    return render_template("chat.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON body"}), 400

    session_id = data.get("session_id", "default")
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Initialise session if new
    if session_id not in sessions:
        sessions[session_id] = []

    # Append user turn
    sessions[session_id].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })

    # Build messages list for the API (role + content only)
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in sessions[session_id]
    ]

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=api_messages
        )
        assistant_reply = response.content[0].text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Append assistant turn to memory
    sessions[session_id].append({
        "role": "assistant",
        "content": assistant_reply,
        "timestamp": datetime.now().isoformat()
    })

    return jsonify({
        "reply": assistant_reply,
        "memory_turns": len(sessions[session_id]) // 2,
        "session_id": session_id
    })


@app.route("/api/history/<session_id>", methods=["GET"])
def get_history(session_id):
    history = sessions.get(session_id, [])
    return jsonify({"history": history, "turns": len(history) // 2})


@app.route("/api/clear/<session_id>", methods=["POST"])
def clear_session(session_id):
    if session_id in sessions:
        del sessions[session_id]
    return jsonify({"status": "cleared"})


@app.route("/api/export/<session_id>", methods=["GET"])
def export_session(session_id):
    history = sessions.get(session_id, [])
    export_data = {
        "exported_at": datetime.now().isoformat(),
        "session_id": session_id,
        "total_turns": len(history) // 2,
        "conversation": history
    }
    return jsonify(export_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
