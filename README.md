# AI Interviewer

A technical interview app. A React frontend talks to a Flask backend, and the backend runs three AutoGen agents against Groq.

## Features

- Interviews for a technology and a position you choose
- You bring your own Groq API key. The server does not store a shared key
- Three agents:
  - **Interviewer**: asks one technical question at a time
  - **Coach**: says what to improve in the answer
  - **Scorer**: scores the answer from 0 to 10

## Setup

1. **Python dependencies** (from the repo root, with a virtualenv active):

   ```bash
   pip install -r backend/requirements.txt
   ```

2. **Frontend dependencies:**

   ```bash
   cd frontend
   npm install
   ```

No API key goes in `.env`. Each person pastes their own Groq key. It stays in that browser tab until the tab is closed. Get one at https://console.groq.com/keys

## Run

Use two terminals.

Backend (port 5001), from `backend`:

```bash
../venv/bin/python run.py
```

Frontend (http://localhost:3000), from `frontend`:

```bash
npm run dev
```

## Usage

1. Enter the technology (for example Python or JavaScript)
2. Enter the position (for example Senior Developer)
3. Paste your Groq API key (kept for this tab only)
4. Start the interview and answer one question at a time
5. Read the coach feedback and the score after each answer
6. End the interview to see the summary

The model is not on the form. Interviews use `openai/gpt-oss-120b`.

To try another Groq model, set it in the browser console before you start, then start the interview:

```js
localStorage.setItem('interviewModel', 'openai/gpt-oss-20b')
```

Remove it to go back to the default:

```js
localStorage.removeItem('interviewModel')
```

The footer shows the model that interview used.

## Requirements

- Python 3.12
- Node.js (for the Vite dev server)
- A Groq API key
- Internet connection

## Key dependencies

- `flask[async]==3.1.0`
- `autogen-agentchat==0.7.5`
- `autogen-ext[openai]==0.7.5`
- React 18 and Vite 6
