from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime
from database import Base

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    company_id = Column(String, index=True)
    customer_id = Column(String, index=True)
    user_id = Column(String, index=True)
    event_name = Column(String, index=True)
    properties = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)
