# ARIA — Chatbot with Context Memory

> **AI Internship Capstone Project** | SuprMentr × VTU | 2026

ARIA (Adaptive Reasoning & Intelligent Assistant) is a full-stack conversational AI chatbot with context memory, built as a capstone project applying everything learned during the 16-week AI internship at SuprMentr.

---

## What is Context Memory?

LLMs (like Claude) are **stateless** — each API call is independent with no built-in memory. Context memory is implemented by:

1. **Storing** the full conversation history server-side (per session)
2. **Replaying** the entire history with every new API call
3. The model reads all previous turns and responds accordingly

```python
# Every message sends the full conversation history
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=sessions[session_id]  # ← This IS context memory
)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Backend | Flask 3.x |
| LLM | Anthropic Claude (claude-sonnet-4-20250514) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| API Pattern | REST (JSON over HTTP) |
| Session Store | In-memory Python dict |

---

## Project Structure

```
Chatbot-With-ContextMemory/
├── app.py                  # Flask backend + Anthropic API integration
├── requirements.txt        # Python dependencies
├── README.md
└── templates/
    ├── index.html          # Landing page
    └── chat.html           # Chat interface
```

---

## Features

- **Context Memory** — Maintains full conversation history; model remembers everything
- **Session Management** — Unique session IDs per browser tab
- **Clear Memory** — Reset context anytime to start fresh
- **Export Chat** — Download full conversation as JSON with timestamps
- **Markdown Rendering** — Bold, italic, code blocks rendered in chat
- **Typing Indicator** — Animated indicator while AI is responding
- **Quick Suggestions** — Pre-built prompts to get started
- **Custom Persona** — ARIA has a distinct AI personality via system prompt

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Abhishek0086/Chatbot-With-ContextMemory.git
cd Chatbot-With-ContextMemory
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key
```bash
export ANTHROPIC_API_KEY=your_api_key_here   # Linux/Mac
set ANTHROPIC_API_KEY=your_api_key_here      # Windows
```

Get your key at: https://console.anthropic.com

### 5. Run the application
```bash
python app.py
```

Visit: **http://localhost:5000**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/chat` | Chat interface |
| POST | `/api/chat` | Send a message |
| GET | `/api/history/<id>` | Get conversation history |
| POST | `/api/clear/<id>` | Clear session memory |
| GET | `/api/export/<id>` | Export conversation as JSON |

### Chat request example
```json
POST /api/chat
{
  "session_id": "session_123",
  "message": "What is machine learning?"
}
```

---

## Internship Concepts Applied

| Concept | Where Used |
|---------|-----------|
| Python fundamentals | app.py — functions, dicts, loops |
| Flask/REST APIs | Backend routing and JSON handling |
| Prompt Engineering | System prompt design for ARIA persona |
| LLMs & Transformers | Claude API integration |
| Context Window | Conversation history management |
| NLP concepts | Text processing in chat |
| Git & GitHub | Version control |
| HTML/CSS/JS | Full frontend from scratch |

---

## Built By

**Abhishek** | AI Domain | VTU Internship 2026  
Mentored by **SuprMentr** — Building industry-ready engineers

---

## License

MIT
