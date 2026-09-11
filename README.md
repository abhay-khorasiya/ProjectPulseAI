# ProjectPulse AI

### Intelligent Project Communication Layer

ProjectPulse AI is a full-stack web application built for the **ArchScale Guild Hackathon – Problem Statement AS-02: Make project communication intelligent, not overwhelming**.

Project teams communicate through WhatsApp messages, emails, meetings, transcripts, notes and many other channels. Important tasks, deadlines, decisions and approvals can easily become buried inside that communication.

ProjectPulse converts unstructured project communication into structured, searchable and actionable project information.

---

## Problem

Modern projects generate large amounts of communication between:

- Clients
- Architects
- Designers
- Contractors
- Vendors
- Project managers
- Internal teams

A single conversation may contain several important pieces of information:

- A new task
- A responsible person
- A deadline
- A confirmed decision
- A pending approval
- A follow-up requirement

Manually converting these conversations into project tasks and records is slow and error-prone.

---

## Solution

ProjectPulse provides one simple workflow:

```text
Project Conversation
        ↓
Communication Processing
        ↓
Summary
        ↓
Action Items
        ↓
Responsibility Detection
        ↓
Deadline Detection
        ↓
Decisions & Approvals
        ↓
Searchable Project Memory
```

Users can paste unstructured communication from sources such as WhatsApp, email or meeting notes.

ProjectPulse processes the communication and extracts useful project intelligence.

---

## Core Features

### Conversation Capture

Supports text input representing:

- WhatsApp conversations
- Emails
- Meeting notes
- Transcripts
- Other project communication

### Intelligent Summary

Creates a concise summary focused on important project information.

### Action Extraction

Detects actionable statements inside project communication.

### Responsibility Detection

Attempts to determine which person is expected to perform an action.

### Deadline Detection

Detects expressions such as:

- by Friday
- tomorrow
- before 15 September
- next Monday
- end of day
- ISO and common date formats

### Decision Extraction

Identifies confirmed decisions and approvals.

### Pending Approval Detection

Highlights items that are still waiting for approval.

### Attention Needed

Surfaces tasks with deadlines and pending approvals so important information is less likely to be buried.

### Searchable Project Memory

Structured tasks, decisions and approvals are stored in SQLite and can later be searched.

### Dashboard

Displays live statistics including:

- Conversations processed
- Open tasks
- Decisions
- Pending approvals

### Report Export

Users can copy an analysis summary or download a conversation intelligence report.

---

## Example

Input:

```text
Rahul: Client approved Italian marble for the lobby.
Priya: Abhay, please update the material schedule by Friday.
Rahul: Abhay, please confirm supplier availability before 15 September.
Priya: Bathroom tiles are still pending approval.
```

ProjectPulse extracts:

### Tasks

```text
Update the material schedule
Responsible: Abhay
Deadline: Friday

Confirm supplier availability
Responsible: Abhay
Deadline: Before 15 September
```

### Decision

```text
Client approved Italian marble for the lobby.
```

### Pending Approval

```text
Bathroom tiles are still pending approval.
```

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS
- Fetch API

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Database

- SQLite

### Communication Intelligence

The current prototype uses a lightweight local NLP-style processing pipeline based on deterministic text analysis, pattern recognition and extraction rules.

This allows the prototype to run without requiring a paid AI API.

The architecture can later be extended with local language models or external LLM providers.

---

## Why Local Processing?

The hackathon prototype was designed with a **₹0 operating-cost goal**.

The current intelligence pipeline:

- Requires no paid AI API
- Requires no API key
- Can run locally
- Provides deterministic output
- Is easy to demonstrate
- Keeps the architecture lightweight

---

## Project Structure

```text
ProjectPulseAI/
│
├── backend/
│   ├── analyzer.py
│   ├── api_router.py
│   ├── database.py
│   ├── main.py
│   ├── memory_models.py
│   ├── memory_routes.py
│   ├── memory_schemas.py
│   ├── models.py
│   ├── requirements.txt
│   └── schemas.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisResults.jsx
│   │   │   └── Sidebar.jsx
│   │   │
│   │   ├── pages/
│   │   │   ├── AnalyzePage.jsx
│   │   │   ├── DashboardPage.jsx
│   │   │   └── MemoryPage.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── styles/
│   │   │   ├── main.css
│   │   │   └── results.css
│   │   │
│   │   ├── utils/
│   │   │   └── reportExport.js
│   │   │
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   └── package.json
│
├── .gitignore
├── ARCHITECTURE.md
└── README.md
```

---

# Running Locally

You need **two terminals**.

## Backend

Open a terminal:

```powershell
cd C:\Abhay\ProjectPulseAI\backend
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start FastAPI:

```powershell
python -m uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

Open another terminal:

```powershell
cd C:\Abhay\ProjectPulseAI\frontend
```

Install dependencies:

```powershell
npm install
```

Start Vite:

```powershell
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## Main API Endpoints

```text
POST /api/analyze
POST /api/analyze-and-save

GET /api/conversations
GET /api/memory
GET /api/memory/search
GET /api/memory/stats
```

---

## End-to-End Workflow

```text
User selects communication source
              ↓
User pastes conversation
              ↓
Frontend sends communication to FastAPI
              ↓
Analyzer processes unstructured text
              ↓
Summary is generated
              ↓
Tasks are extracted
              ↓
Responsible people are identified
              ↓
Deadlines are detected
              ↓
Decisions are extracted
              ↓
Pending approvals are detected
              ↓
Structured information is stored in SQLite
              ↓
Dashboard statistics are updated
              ↓
Project Memory becomes searchable
```

---

## Hackathon Problem Statement Coverage

| Requirement | ProjectPulse Implementation |
|---|---|
| Communication input | WhatsApp, email, meeting notes, transcripts |
| Unstructured communication | Raw text processing |
| Intelligent summarization | Local summary generation |
| Action extraction | Task extraction pipeline |
| Responsibility detection | Person identification |
| Deadline detection | Date and deadline extraction |
| Decision extraction | Confirmed decision detection |
| Approval extraction | Pending approval detection |
| Conversation-to-task | Structured task objects |
| Search/history | SQLite Project Memory |
| End-to-end demo | Fully connected React + FastAPI workflow |

---

## Future Improvements

Future versions could include:

- Real WhatsApp integration
- Gmail integration
- Meeting transcription
- Voice-note processing
- PDF/document processing
- Local LLM integration
- Semantic/vector search
- Multi-project workspaces
- Authentication and team permissions
- Notifications and reminders
- Automatic meeting minutes
- Duplicate task detection
- Conflict detection between conversations
- Project-specific stakeholder directory

---

## Hackathon

**ArchScale Guild Intern Technology Hackathon**

Problem Statement:

**AS-02 — Make project communication intelligent, not overwhelming**

---

## Author

**Abhay Khorasiya**

BCA Graduate  
Full Stack Developer | Aspiring AI Engineer

---

## License

This project was created as a hackathon prototype for educational and demonstration purposes.