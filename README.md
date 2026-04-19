# AI Event Assistant
> **PromptWars — Physical Event Experience Challenge**  
> Built for Hack2Skill · Virtual PromptWars · Powered by Google Gemini

---

## Problem Statement
Design a solution that improves the physical event experience for attendees at large-scale sporting venues. The system should address challenges such as **crowd movement**, **waiting times**, and **real-time coordination**, while ensuring a seamless and enjoyable experience.

---

## Solution
An AI-powered stadium assistant combining a live D3.js crowd simulation with a Google Gemini-backed chat. The system reads real-time crowd density and answers attendee questions intelligently — with the API key stored securely on the server.

---

## Architecture

```
Browser (frontend/index.html)
        |
        |  POST /ask  { question + live stadium snapshot }
        v
Flask Server (app.py)
        |  reads system prompt from prompts/prompt.txt
        |  injects live crowd data into prompt
        |  Gemini API key stored securely in .env
        v
Google Gemini 2.0 Flash API
        |
        v
Flask Server returns { response }
        |
        v
Browser displays answer in chat
```

**Two-layer AI:**
- **Layer 1 — Local rule engine** (instant, no server call): handles common questions from live simulation data
- **Layer 2 — Gemini via app.py** (server-side): handles complex questions; API key never exposed to the browser

---

## How to Run

### Step 1 — Get a free Gemini API key
Go to https://aistudio.google.com/app/apikey, sign in, and create an API key.

### Step 2 — Create a .env file in the project root
```
GEMINI_API_KEY=your_actual_key_here
```

### Step 3 — Install dependencies
```
pip install -r requirements.txt
```

### Step 4 — Start the server
```
python app.py
```

### Step 5 — Open in browser
```
http://localhost:8000
```

---

## Project Structure

```
AI-Event-Assistant/
├── app.py               Flask server — holds API key, calls Gemini, serves frontend
├── frontend/
│   └── index.html       UI — D3 simulation + chat (calls /ask on app.py)
├── prompts/
│   └── prompt.txt       System prompt — read by app.py at startup
├── requirements.txt     Python dependencies
├── .env                 Your Gemini API key (do NOT commit to GitHub)
└── README.md
```

Add this to your .gitignore so the key is never pushed:
```
.env
```

---

## Features

- Live D3.js stadium with 6 crowd zones, color-coded by density
- Google Gemini 2.0 Flash answers questions grounded in live crowd data
- API key secured on server — never sent to the browser
- Local rule engine for instant answers (gates, food, exits, wait times)
- Live stats: attendance, busiest gate, best entry, zone bars
- Dark / light mode with localStorage persistence
- Simulation speed controls (1x, 3x, 10x) and pause/resume

---

## Tech Stack

- Frontend: HTML5, CSS3, Vanilla JS, D3.js v7
- Backend: Python, Flask, Flask-CORS, python-dotenv
- AI: Google Gemini 2.0 Flash (google-generativeai)

---

*Built by [G Surya Prakash](https://github.com/GSuryaP/) for PromptWars · Hack2Skill · 2026*
