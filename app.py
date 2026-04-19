"""
AI Event Assistant — app.py
============================
Flask backend that:
  1. Serves frontend/index.html
  2. Reads the system prompt from prompts/prompt.txt
  3. Holds the Gemini API key securely (never exposed to the browser)
  4. Calls Google Gemini API and returns the response to the frontend

Setup:
    pip install -r requirements.txt

    Either set your API key in a .env file:
        GEMINI_API_KEY=your_key_here

    Or export it in your terminal:
        export GEMINI_API_KEY=your_key_here

    Get a free key at: https://aistudio.google.com/app/apikey

Run:
    python app.py

Then open: http://localhost:8000
"""

import os
import pathlib
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# ── Load environment variables from .env file if present ──────────────────────
load_dotenv()

app = Flask(__name__, static_folder="frontend")
CORS(app)  # allow requests from the browser

# ── Load Gemini API key ────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("\n⚠️  WARNING: GEMINI_API_KEY not set.")
    print("   Set it in a .env file or export it as an environment variable.")
    print("   Get a free key at: https://aistudio.google.com/app/apikey\n")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"\n✅ Gemini API key loaded successfully.\n")

# ── Load system prompt from prompts/prompt.txt ────────────────────────────────
PROMPT_PATH = pathlib.Path(__file__).parent / "prompts" / "prompt.txt"
try:
    SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8").strip()
    print(f"✅ System prompt loaded from {PROMPT_PATH}\n")
except FileNotFoundError:
    SYSTEM_PROMPT = "You are a helpful stadium event assistant. Answer concisely using the live data provided."
    print(f"⚠️  prompts/prompt.txt not found, using default prompt.\n")

# ── Gemini model ───────────────────────────────────────────────────────────────
MODEL_NAME = "gemini-2.0-flash"


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the frontend HTML."""
    return send_from_directory("frontend", "index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """
    Receive a question + live stadium snapshot from the frontend,
    call Gemini with the system prompt, and return the answer.

    Expected JSON body:
    {
        "question": "Which gate is least crowded?",
        "stadium": {
            "gateA": 85,
            "gateB": 52,
            "gateC": 28,
            "totalPeople": 24750,
            "bestGate": "C",
            "worstGate": "A"
        }
    }
    """
    if not GEMINI_API_KEY:
        return jsonify({"error": "Gemini API key not configured on server."}), 500

    data = request.get_json(force=True)
    question = data.get("question", "").strip()
    stadium  = data.get("stadium", {})

    if not question:
        return jsonify({"error": "No question provided."}), 400

    # Build the full prompt: system prompt + live data + user question
    live_data = (
        f"\nCurrent live stadium data:\n"
        f"- Gate A: {stadium.get('gateA', '?')}% capacity\n"
        f"- Gate B: {stadium.get('gateB', '?')}% capacity\n"
        f"- Gate C: {stadium.get('gateC', '?')}% capacity\n"
        f"- Total attendance: ~{stadium.get('totalPeople', '?')} of 45,000\n"
        f"- Best entry gate right now: Gate {stadium.get('bestGate', '?')}\n"
        f"- Busiest gate to avoid: Gate {stadium.get('worstGate', '?')}\n"
    )

    full_prompt = SYSTEM_PROMPT + live_data + f"\nAttendee question: {question}"

    try:
        model    = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            full_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=200,
                temperature=0.4,
            )
        )
        answer = response.text.strip()
        return jsonify({"response": answer})

    except Exception as e:
        print(f"Gemini error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    """Health check — confirms server + key + prompt are loaded."""
    return jsonify({
        "status":        "running",
        "model":         MODEL_NAME,
        "api_key_set":   bool(GEMINI_API_KEY),
        "prompt_loaded": bool(SYSTEM_PROMPT),
        "project":       "AI Event Assistant"
    })


# ── Start ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🏟  AI Event Assistant running at http://localhost:{port}")
    print(f"    Open http://localhost:{port} in your browser\n")
    app.run(debug=True, port=port)
