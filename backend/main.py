from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime

# --- Database & Model Imports ---
from database import engine, get_db, Base
from models import HCPInteraction

# --- Agent / AI Imports ---
# We import the compiled LangGraph app
from agent import app as agent_app
from langchain_core.messages import HumanMessage

# --- 1. Database Initialization ---
# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# --- 2. FastAPI App Setup ---
app = FastAPI(title="AI-First CRM Backend")

# Allow CORS (So your React frontend can talk to this backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Pydantic Schemas (Data Validation) ---

class InteractionCreate(BaseModel):
    """Schema for manually creating an interaction via API"""
    hcp_name: str
    interaction_type: str
    interaction_date: date
    interaction_time: time
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    voice_note_summary: Optional[str] = None
    voice_note_consent: bool = False
    shared_materials: Optional[str] = None
    hcp_sentiment: Optional[str] = None
    outcome_next_steps: Optional[str] = None

class ChatRequest(BaseModel):
    """Schema for the Chat Endpoint"""
    message: str

# --- 4. API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Backend is running", "version": "1.0"}

# --- Manual Interaction Endpoints (Direct DB access) ---

@app.get("/interactions/")
def get_interactions(db: Session = Depends(get_db)):
    """Fetch all logged interactions from the database"""
    try:
        interactions = db.query(HCPInteraction).all()
        return interactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/interactions/")
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """Manually save a new interaction to the database"""
    try:
        db_interaction = HCPInteraction(
            hcp_name=interaction.hcp_name,
            interaction_type=interaction.interaction_type,
            interaction_date=interaction.interaction_date,
            interaction_time=interaction.interaction_time,
            attendees=interaction.attendees,
            topics_discussed=interaction.topics_discussed,
            voice_note_summary=interaction.voice_note_summary,
            voice_note_consent=interaction.voice_note_consent,
            shared_materials=interaction.shared_materials,
            hcp_sentiment=interaction.hcp_sentiment,
            outcome_next_steps=interaction.outcome_next_steps
        )
        
        db.add(db_interaction)
        db.commit()
        db.refresh(db_interaction)
        
        return {"message": "Interaction Saved", "data": db_interaction}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- AI Agent Endpoint (LangGraph Integration) ---


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Sends a user message to the LangGraph Agent.
    Returns the response and the details of any tools used (for form filling).
    """
    try:
        initial_state = {
            "messages": [HumanMessage(content=request.message)]
        }
        
        final_state = agent_app.invoke(initial_state, config={"recursion_limit": 50})
        
        last_message = final_state["messages"][-1]
        response_content = last_message.content
        
        # NEW: Capture detailed tool info (Name + Arguments)
        tool_calls_details = []
        for msg in final_state["messages"]:
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls_details.append({
                        "name": tc['name'],
                        "args": tc['args'] # This contains the data for the form!
                    })

        return {
            "response": response_content,
            "tool_calls": tool_calls_details
        }

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")