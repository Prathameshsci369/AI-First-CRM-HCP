from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Text
from database import Base
import datetime

class HCPInteraction(Base):
    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True, index=True)
    
    # 1. HCP Info
    hcp_name = Column(String(255), nullable=False)
    interaction_type = Column(String(50), nullable=False) # e.g., "Meeting", "Call"
    
    # 2. Date & Time
    interaction_date = Column(Date, default=datetime.date.today)
    interaction_time = Column(Time, default=datetime.datetime.now().time)
    
    # 3. Details
    attendees = Column(Text, nullable=True) 
    topics_discussed = Column(Text, nullable=True)
    
    # 4. Voice Notes
    voice_note_summary = Column(Text, nullable=True)
    voice_note_consent = Column(Boolean, default=False) 
    
    # 5. Materials & Sentiment
    shared_materials = Column(Text, nullable=True) 
    hcp_sentiment = Column(String(50), nullable=True) 
    
    # 6. Outcome
    outcome_next_steps = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(Date, default=datetime.date.today)