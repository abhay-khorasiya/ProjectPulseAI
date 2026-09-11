# ProjectPulse AI — Architecture

## System Overview

ProjectPulse AI uses a simple three-layer architecture:

```text
┌───────────────────────────────┐
│         React Frontend        │
│                               │
│ Dashboard                     │
│ Analyze Conversation          │
│ Project Memory                │
└───────────────┬───────────────┘
                │
                │ HTTP / JSON
                ▼
┌───────────────────────────────┐
│        FastAPI Backend        │
│                               │
│ API Routes                    │
│ Validation                    │
│ Analysis Pipeline             │
│ Project Memory Logic          │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│            SQLite             │
│                               │
│ Conversations                 │
│ Tasks                         │
│ Decisions                     │
│ Approvals                     │
└───────────────────────────────┘
```

---

## Frontend

The frontend is built with React and Vite.

Primary screens:

### Dashboard

Displays project intelligence statistics and recent information.

### Analyze Conversation

Allows users to:

1. Select a communication source
2. Paste unstructured communication
3. Analyze the conversation
4. View extracted structured information
5. Automatically save results

### Project Memory

Allows users to search stored project intelligence.

---

## Backend

The backend uses FastAPI.

Responsibilities include:

- Receiving frontend requests
- Validating request data
- Processing project communication
- Extracting structured information
- Saving conversations
- Saving project memory
- Searching project memory
- Calculating dashboard statistics

---

## Intelligence Pipeline

The communication analyzer processes text using multiple stages.

```text
Raw Communication
       ↓
Text Cleaning
       ↓
Conversation Splitting
       ↓
Speaker Detection
       ↓
Acknowledgement Filtering
       ↓
Task Detection
       ↓
Responsibility Detection
       ↓
Deadline Detection
       ↓
Decision Detection
       ↓
Pending Approval Detection
       ↓
Summary Generation
       ↓
Attention Detection
```

---

## Data Flow

```text
User
 ↓
React
 ↓
POST /api/analyze-and-save
 ↓
FastAPI
 ↓
Analyzer
 ↓
Structured Result
 ↓
SQLAlchemy
 ↓
SQLite
 ↓
JSON Response
 ↓
React Results UI
```

---

## Project Memory

Every analyzed conversation can generate multiple structured memory items.

Example:

```text
Conversation #12

├── Task
│   ├── Content
│   ├── Responsible person
│   ├── Deadline
│   └── Status
│
├── Decision
│   ├── Content
│   └── Status
│
└── Approval
    ├── Content
    └── Status
```

These items can later be searched independently of the original conversation.

---

## Search

Project Memory currently supports keyword-based search across:

- Content
- Responsible person
- Deadline
- Status
- Memory item type

This makes previous project information easier to retrieve than manually searching through communication history.

---

## Design Decisions

### SQLite

SQLite was selected because the hackathon prototype requires:

- Fast setup
- Zero infrastructure cost
- Local operation
- Simple deployment
- Reliable relational storage

For a production system it could be replaced by PostgreSQL.

### FastAPI

FastAPI provides:

- Strong request validation
- Automatic Swagger documentation
- Simple Python integration
- High development speed

### React

React allows the project to provide an interactive dashboard and modular UI.

### Local Intelligence Pipeline

The initial prototype deliberately avoids requiring paid AI APIs.

The processing pipeline is deterministic and lightweight, while the architecture remains ready for integration with an LLM or local language model later.

---

## Scalability Path

A production version could evolve into:

```text
React / Mobile Client
        ↓
API Gateway
        ↓
Authentication
        ↓
FastAPI Services
        ↓
LLM / NLP Service
        ↓
PostgreSQL
        ↓
Vector Database
        ↓
Notification Services
```

This would enable multi-user project teams, semantic memory search, automated integrations and higher-scale processing.