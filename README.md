# 🧠 AI Notes Assistant

An AI-powered notes generator with two modes — summarize pasted text into structured notes, or generate study notes on any topic from scratch — with free-text style customization instead of rigid, hardcoded formatting options.

This is Project 5 of a 12-month self-directed AI Engineering roadmap — built to understand *why* AI-powered apps are structured the way they are, not just to produce working code.

---

## Features

- 📄 **Summarize mode** — paste raw text or lecture notes, get back clear, structured notes
- 💡 **Topic mode** — enter a topic, generate study notes from the model's own knowledge
- ✍️ **Free-text style instructions** — instead of a fixed dropdown of styles, users type their own formatting preference in plain language (e.g., "keep it short," "focus on exam-relevant points") — the model interprets it directly, no hardcoded branching logic
- ⏳ Staged status feedback while generating (`st.status`), with generation time shown
- 🛡️ Layered error handling for auth failures, rate limits, and connection issues — no raw tracebacks
- 💾 Download generated notes as a `.txt` file
- 🧭 Simple multi-page navigation (Home → Summarize / Topic → Back) using `st.session_state` as a router

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| Streamlit | Web UI |
| Groq API (`groq` SDK) | LLM inference (`llama-3.3-70b-versatile`) |
| python-dotenv | Secure API key management |

---

## Architecture

```
User
  ↓
Streamlit UI (mode selection: Summarize / Topic)
  ↓
prompts.py (builds the right prompt for the mode + user's instructions)
  ↓
groq_client.py → Groq API (single-shot, non-streaming call)
  ↓
Structured markdown notes rendered + downloadable
```

Unlike a chatbot, this app has **no multi-turn memory** — each generation is a single, independent request. There's no growing `messages` list; `groq_client.py` accepts a plain prompt string and internally wraps it into the format the Groq API requires.

---

## Project Structure

```
ai-note-generator/
├── app.py              # Streamlit UI — orchestration layer
├── groq_client.py       # Groq API logic — business logic layer
├── prompts.py            # Prompt-building functions — isolated from UI and API logic
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup & Run

1. Clone the repo and navigate into the project folder:
   ```bash
   git clone <your-repo-url>
   cd ai-note-generator
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_api_key_here
   ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Key Design Decisions

**Why free-text instructions instead of a fixed dropdown of styles?**
An early design considered a dropdown (Default / Short / Key Terms Only / Long Form) — but that's really just hardcoded Python branching wearing a UI. It only supports whatever styles were anticipated in advance. Instead, users type their own instruction in plain language, and that text is passed directly into the prompt sent to the model. The model — not the application code — interprets what "short," "exam-focused," or "beginner-friendly" actually means. This mirrors how a real conversational request works: the flexibility lives in the model's language understanding, not in a rigid menu of pre-coded options.

**Why does `prompts.py` exist as its own file?**
Prompt wording is something that gets iterated on constantly — tested, tweaked, refined — completely independently of UI or API logic. Keeping prompt construction isolated means changes to phrasing never risk touching UI code, and vice versa. The same separation-of-concerns principle applied throughout every project in this roadmap.

**Why does `groq_client.py` take a plain string instead of a message list?**
This app has no conversational memory — each generation is fully independent. The public function `get_notes(prompt)` accepts a plain string; the Groq API's required `messages=[...]` list format is an internal implementation detail handled entirely inside `groq_client.py`, not something the UI layer needs to know or construct.

**Why `st.status()` with staged messages instead of a plain spinner?**
A single-shot generation task (versus a conversational chatbot) benefits from feedback that acknowledges the multi-step nature of what's happening (understanding the request → generating → formatting), even though the actual API call is one request. It also cleanly reflects success vs. failure state at the end, rather than just disappearing.

**Why is a `success` flag used inside a `try/except/finally` block for the status update?**
The status box needs to reflect the outcome (success or failure) regardless of which code path executes. Using `finally` guarantees the status update always runs exactly once, branching its message based on a flag set only when the `try` block fully succeeds — avoiding both a stuck "in progress" state on failure and duplicated status-update calls across every except branch.

---

## What I Learned

- The difference between a prompt that *labels* its content (task instruction + explicit `text:`/`topic:` sections) versus one that hands the model an ambiguous blob — and why explicit structure produces more reliable output
- How to let a model handle flexible, free-form user intent instead of trying to anticipate and hardcode every possible request
- Why `try/except/else` and `try/except/finally` solve different problems, and when code after an exception handler still needs protecting from variables that were never assigned
- The importance of testing UI state bugs by deliberately interacting with unrelated widgets, not just the "happy path" button
- Why a single-shot generation tool has a fundamentally different state-management shape than a multi-turn chatbot, despite reusing much of the same API-layer code

---

*Part of a 12-month AI Engineering self-development roadmap — Month 2, Project 5.*
