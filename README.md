# AI Customer Support Copilot

Full-stack AI support assistant built with:
- **Backend:** FastAPI + LangGraph + LangChain + Chroma
- **Frontend:** React + TypeScript + Vite

It supports:
- RAG answers over policy documents
- deterministic tool routing for orders/tickets/customers
- session memory
- escalation detection
- two frontend modes:
  - **User View** (clean product chat)
  - **Developer/Demo View** (technical details: action, memory, tools, raw sources)

---

## What’s In This Project

### Backend capabilities
- `/api/v1/chat` runs a LangGraph workflow:
  1. save user message
  2. load memory
  3. route to RAG or tool
  4. check escalation
  5. finalize answer
  6. save assistant message
- `/api/v1/ingest` ingests support docs (`.pdf`) into Chroma.
- `/api/v1/sessions/{session_id}` retrieves or clears in-memory session history.
- `/api/v1/tools/...` test endpoints for tool lookups.

### Frontend capabilities
- modern chat-style interface
- answer-first assistant cards
- collapsible details for advanced info
- session sidebar with **New Chat**
- loading + typing polish
- mode toggle:
  - **User View:** hides technical/debug details
  - **Developer/Demo View:** reveals technical sections and raw source snippets

---

## Project Structure

```text
AI_Customer_Support_Copilot/
├─ backend/
│  └─ app/
│     ├─ api/v1/routes/       # chat, health, ingest, sessions, tools
│     ├─ graph/               # LangGraph workflow + state
│     ├─ services/            # routing, rag, memory, escalation, tools
│     ├─ repositories/        # in-memory session + mock data repos
│     ├─ rag/                 # loader, splitter, embeddings, retriever, vectorstore
│     ├─ data/
│     │  ├─ docs/             # support policy docs (pdf + md)
│     │  └─ mock/             # orders, tickets, customers
│     └─ main.py
├─ frontend/
│  ├─ src/
│  │  ├─ pages/               # SupportCopilotPage
│  │  ├─ components/          # AnswerCard, ChatInput, MessageBubble, SourceList
│  │  ├─ api/                 # axios client
│  │  └─ index.css
│  └─ package.json
└─ README.md
```

---

## Prerequisites

- **Python** 3.10+
- **Node.js** 18+ and npm
- **OpenAI API key**

---

## Backend Setup (FastAPI)

From project root:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic pydantic-settings langgraph langchain-openai langchain-community langchain-core langchain-text-splitters chromadb pypdf
```

Create `backend/.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
EMBEDDING_MODEL=text-embedding-3-small
```

Run backend:

```powershell
uvicorn app.main:app --reload
```

Backend base URL:
- `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`

---

## Ingest Knowledge Docs

After backend is running, ingest docs once:

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/ingest
```

This indexes PDFs from `backend/app/data/docs` into Chroma (`backend/app/data/chroma`).

---

## Frontend Setup (React + Vite)

From project root:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:
- `http://127.0.0.1:5173` (or `http://localhost:5173`)

Note: frontend API base is currently hardcoded in `frontend/src/api/chat.ts`:
- `http://127.0.0.1:8000/api/v1`

---

## API Quick Reference

- `GET /api/v1/health` → service status
- `POST /api/v1/chat` → main assistant response
- `POST /api/v1/ingest` → index support docs
- `GET /api/v1/sessions/{session_id}` → session history + summary
- `DELETE /api/v1/sessions/{session_id}` → clear session history
- `GET /api/v1/tools/orders/{order_id}`
- `GET /api/v1/tools/tickets/{ticket_id}`
- `GET /api/v1/tools/customers/{customer_id}`

Sample chat request:

```json
{
  "session_id": "session_123",
  "message": "What is the refund policy?"
}
```

---

## Frontend Modes

### User View
- clean product chat
- technical/debug details hidden
- answer remains the main focus

### Developer/Demo View
- shows route/action
- shows tools used
- shows memory summary
- shows escalation reasoning
- shows raw source snippets

---

## Useful Frontend Commands

```powershell
cd frontend
npm run dev
npm run build
npm run lint
npm run preview
```

---

## Current Limitations

- session memory is **in-memory** (resets when backend restarts)
- backend dependencies are not pinned in a `requirements.txt` yet
- tool routing and escalation are deterministic rule-based logic

---

## Suggested Next Improvements

- add pinned Python dependency file (`requirements.txt` or `pyproject.toml`)
- persist session memory (Redis/DB)
- add backend + frontend tests
- add auth and multi-user session ownership
