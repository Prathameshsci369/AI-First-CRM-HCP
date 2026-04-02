from langchain_core.tools import tool
from sqlalchemy.orm import Session
from database import SessionLocal
from models import HCPInteraction
from datetime import date, datetime
from typing import Optional
# --- TOOL 1: Log Interaction ---
@tool
def log_interaction(
    hcp_name: str, 
    interaction_type: str = "Meeting",
    topics_discussed: str = "", 
    hcp_sentiment: str = "Neutral",
    outcome_next_steps: str = ""
):
    """
    Logs a NEW interaction.
    Use this when the user describes a meeting or call that just happened.
    """
    print(f"--- TOOL: Logging {hcp_name} ---")
    db = SessionLocal()
    try:
        new_interaction = HCPInteraction(
            hcp_name=hcp_name,
            interaction_type=interaction_type,
            interaction_date=date.today(),
            interaction_time=datetime.now().time(),
            topics_discussed=topics_discussed,
            hcp_sentiment=hcp_sentiment,
            outcome_next_steps=outcome_next_steps
        )
        db.add(new_interaction)
        db.commit()
        db.refresh(new_interaction)
        return f"Success: Logged interaction ID {new_interaction.id}."
    except Exception as e:
        db.rollback()
        return f"Error: {str(e)}"
    finally:
        db.close()

# --- TOOL 2: Get History ---
@tool
def get_hcp_history(hcp_name: str):
    """Retrieves the list of all past interactions for a specific HCP."""
    print(f"--- TOOL: Getting history for {hcp_name} ---")
    db = SessionLocal()
    try:
        logs = db.query(HCPInteraction).filter(HCPInteraction.hcp_name == hcp_name).all()
        if not logs:
            return f"No history found for {hcp_name}."
        
        history_summary = f"Found {len(logs)} interactions:\n"
        for log in logs:
            history_summary += f"ID: {log.id} | Date: {log.interaction_date} | Topic: {log.topics_discussed}\n"
        return history_summary
    finally:
        db.close()

# --- TOOL 3: Edit by ID (Manual) ---



@tool
def edit_interaction_by_id(
    interaction_id: str, 
    updated_topics: Optional[str] = None,  # CHANGED: Optional[str]
    updated_outcome: Optional[str] = None  # CHANGED: Optional[str]
):
    """
    Edits an interaction using a SPECIFIC ID number.
    Use this ONLY if the user provides an ID (e.g., 'Edit ID 5').
    """
    print(f"--- TOOL: Editing ID {interaction_id} ---")
    db = SessionLocal()
    try:
        try:
            id_int = int(interaction_id)
        except ValueError:
            return "Error: ID must be a number."

        db_interaction = db.query(HCPInteraction).filter(HCPInteraction.id == id_int).first()
        if not db_interaction:
            return f"Error: ID {id_int} not found."
        
        # ROBUST CHECK: Only update if value is provided and not empty string
        if updated_topics:
            db_interaction.topics_discussed = updated_topics
        if updated_outcome:
            db_interaction.outcome_next_steps = updated_outcome
            
        db.commit()
        return f"Success: Updated ID {id_int}."
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        db.close()

# --- TOOL 4: Smart Edit (Robust Version) ---
@tool
def smart_edit_last_interaction(
    hcp_name: str, 
    updated_topics: Optional[str] = None,  # CHANGED: Optional[str]
    updated_outcome: Optional[str] = None  # CHANGED: Optional[str]
):
    """
    Automatically finds the MOST RECENT interaction for an HCP and updates it.
    Use this when the user says 'Update the last meeting' or 'Edit the previous one' without giving an ID.
    """
    print(f"--- TOOL: Smart Editing last for {hcp_name} ---")
    db = SessionLocal()
    try:
        # Find the latest ID for this HCP
        last_log = db.query(HCPInteraction).filter(
            HCPInteraction.hcp_name == hcp_name
        ).order_by(HCPInteraction.id.desc()).first()
        
        if not last_log:
            return f"Error: No previous interactions found for {hcp_name}."
        
        # ROBUST CHECK: Only update if value is provided
        if updated_topics:
            last_log.topics_discussed = updated_topics
        if updated_outcome:
            last_log.outcome_next_steps = updated_outcome
            
        db.commit()
        return f"Success: Updated the last interaction (ID {last_log.id}) for {hcp_name}."
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        db.close()

# --- TOOL 5: Search by Topic ---
@tool
def search_by_topic(keyword: str):
    """
    Searches for all interactions that contain a specific keyword in the topic or notes.
    Use this when the user asks 'Did we ever discuss X?' or 'Find logs about Y'.
    """
    print(f"--- TOOL: Searching for '{keyword}' ---")
    db = SessionLocal()
    try:
        # Search in topics and outcomes
        results = db.query(HCPInteraction).filter(
            (HCPInteraction.topics_discussed.contains(keyword)) | 
            (HCPInteraction.outcome_next_steps.contains(keyword))
        ).all()
        
        if not results:
            return f"No interactions found containing '{keyword}'."
            
        summary = f"Found {len(results)} interactions:\n"
        for r in results:
            summary += f"- ID: {r.id} | HCP: {r.hcp_name} | Topic: {r.topics_discussed}\n"
        return summary
    finally:
        db.close()



# ... (Keep imports and previous 5 tools exactly as they are) ...

# --- TOOL 6: Submit Sample Request ---
@tool
def submit_sample_request(hcp_name: str, drug_name: str):
    """
    Logs a request to send drug samples to an HCP.
    Use this when the user says 'send samples', 'request samples', or 'drop off samples'.
    """
    print(f"--- TOOL: Sample Request for {drug_name} to {hcp_name} ---")
    db = SessionLocal()
    try:
        # We log this as a new interaction of type 'Sample Request'
        # or append it to the outcome of the last interaction. 
        # For simplicity, we create a log entry.
        new_interaction = HCPInteraction(
            hcp_name=hcp_name,
            interaction_type="Sample Request",
            interaction_date=date.today(),
            interaction_time=datetime.now().time(),
            topics_discussed=f"Sample request for {drug_name}",
            outcome_next_steps=f"Ship samples of {drug_name} to {hcp_name}.",
            hcp_sentiment="Neutral"
        )
        db.add(new_interaction)
        db.commit()
        return f"Success: Sample request for {drug_name} logged for {hcp_name}."
    except Exception as e:
        db.rollback()
        return f"Error: {str(e)}"
    finally:
        db.close()

# --- TOOL 7: Get Statistics ---
@tool
def get_interaction_stats():
    """
    Returns a summary of all interactions in the database (Total count, Sentiment breakdown).
    Use this when the user asks for 'stats', 'summary', or 'how many calls did I make?'.
    """
    print(f"--- TOOL: Calculating Stats ---")
    db = SessionLocal()
    try:
        total = db.query(HCPInteraction).count()
        positive = db.query(HCPInteraction).filter(HCPInteraction.hcp_sentiment == "Positive").count()
        neutral = db.query(HCPInteraction).filter(HCPInteraction.hcp_sentiment == "Neutral").count()
        negative = db.query(HCPInteraction).filter(HCPInteraction.hcp_sentiment == "Negative").count()
        
        return (
            f"Database Statistics:\n"
            f"- Total Interactions: {total}\n"
            f"- Positive: {positive}\n"
            f"- Neutral: {neutral}\n"
            f"- Negative: {negative}"
        )
    finally:
        db.close()

# UPDATED LIST: Now 7 tools
tools = [
    log_interaction, 
    get_hcp_history, 
    edit_interaction_by_id, 
    smart_edit_last_interaction, 
    search_by_topic,
    submit_sample_request,    # New
    get_interaction_stats     # New
]
