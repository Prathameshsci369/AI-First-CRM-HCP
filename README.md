

# AI-First CRM HCP Module

An intelligent Customer Relationship Management system designed specifically for Healthcare Professionals (HCP). This system demonstrates an "AI-First" approach by allowing field representatives to log interactions via a natural language chat interface, which automatically extracts structured data to fill CRM forms.



## 🌟 Key Features

*   **Conversational Data Entry:** Users can simply type "I had a meeting with Dr. Smith about Cardiac Drug X," and the AI extracts the entities to fill the form automatically.
*   **LangGraph Agent:** Implements a multi-step AI agent with **7 specific tools**:
    1.  `log_interaction`: Logs new meetings/calls.
    2.  `get_hcp_history`: Retrieves past interaction logs.
    3.  `edit_interaction_by_id`: Modifies specific records by ID.
    4.  `smart_edit_last_interaction`: Intelligently updates the most recent interaction.
    5.  `search_by_topic`: Searches logs for specific keywords.
    6.  `submit_sample_request`: Logs drug sample requests.
    7.  `get_interaction_stats`: Provides call volume and sentiment analysis.
*   **Dual Interface:** Seamlessly switch between Chat Mode and Manual Form Mode.
*   **Real-time State Management:** Built with React and Redux Toolkit for instant UI updates.

## 🛠 Tech Stack

### Backend
*   **Framework:** FastAPI
*   **Database:** SQLite (via SQLAlchemy ORM)
*   **AI/Agent Framework:** LangGraph
*   **LLM Integration:** LangChain with Groq API (Gemma2-9b-it / Llama-3.1-8b)
*   **Language:** Python 3.9+

### Frontend
*   **Framework:** React (Vite)
*   **State Management:** Redux Toolkit
*   **HTTP Client:** Axios
*   **Styling:** CSS3 (Inter Font)

## 📋 Prerequisites

Before running this project, ensure you have installed:

*   **Node.js** (v16 or higher)
*   **Python** (v3.9 or higher)
*   **pip** (Python package manager)
*   **Groq API Key:** Get a free key from [console.groq.com](https://console.groq.com/).

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd AI-First-CRM-HCP
```

### 2. Backend Setup

Navigate to the backend directory, create a virtual environment, and install dependencies.

```bash
cd backend

# Create virtual environment (Mac/Linux)
python3 -m venv venv
source venv/bin/activate

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Set your Groq API Key:**

You must set your API key as an environment variable so the agent can access the LLM.

*   **Mac/Linux:**
    ```bash
    export GROQ_API_KEY="gsk_..."
    ```
*   **Windows (PowerShell):**
    ```powershell
    $env:GROQ_API_KEY="gsk_..."
    ```

**Start the Backend Server:**

```bash
uvicorn main:app --reload
```
The backend will run on `http://127.0.0.1:8000`.

### 3. Frontend Setup

Open a new terminal window, navigate to the frontend directory, and install dependencies.

```bash
cd frontend
npm install
```

**Start the Frontend Server:**

```bash
npm run dev
```
The frontend will run on `http://localhost:5173`.

## 💻 Usage

1.  Open your browser and go to `http://localhost:5173`.
2.  **Chat Mode:** On the left side, type a natural language instruction.
    *   *Example:* "Log a meeting with Dr. Sarah. We discussed the new cardiac drug and she was very positive."
3.  **Observe:** The AI Agent will process the request (check your terminal logs for "Agent Thinking").
4.  **Form Auto-Fill:** Watch the "Log Interaction" form on the right side fill up automatically with the extracted data (Name, Type, Topic, Sentiment).
5.  **Manual Edit:** You can manually tweak the data in the form before clicking "Save Interaction".

## 📁 Project Structure

```text
/AI-First-CRM-HCP
│
├── backend/                 # Python FastAPI Server
│   ├── agent.py            # LangGraph Agent logic & State
│   ├── tools.py            # 7 LangChain Tools (DB interactions)
│   ├── main.py             # API Endpoints
│   ├── database.py         # DB Connection (SQLite)
│   ├── models.py           # SQLAlchemy Schemas
│   └── requirements.txt    # Python Dependencies
│
├── frontend/               # React Vite Application
│   ├── src/
│   │   ├── App.jsx        # Main UI Component
│   │   ├── main.jsx       # Entry Point & Redux Store
│   │   ├── api.js         # Axios API Calls
│   │   └── hcpSlice.js    # Redux State Management
│   └── package.json       # Node Dependencies
│
└── README.md
```

## 📝 Assignment Deliverables (Checklist)

- [x] **GitHub Submission:** Code uploaded to a single repository.
- [x] **LangGraph & LLM:** Agent uses Groq (Gemma/Llama) via LangGraph.
- [x] **5+ Tools:** Implemented 7 functional tools for CRM activities.
- [x] **Log & Edit:** Core requirements for logging and editing interactions are met.
- [x] **Video Recording:** Walkthrough of frontend, tool execution, and code flow (to be recorded separately).

## 🐛 Troubleshooting

*   **CORS Error:** Ensure the backend is running and CORS is enabled in `main.py`.
*   **Agent Hallucination:** If the AI chats but doesn't fill the form, check the terminal logs. It might have failed to call a tool. Try rephrasing your prompt to be more explicit (e.g., "Log this...").
*   **Module Not Found:** Ensure you activated the Python virtual environment before installing requirements.

## 📄 License

This project is created for educational and assessment purposes.

---
**Built for the Future of Life Sciences CRM. 🚀**
