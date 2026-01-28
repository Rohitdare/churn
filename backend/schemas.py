from pydantic import BaseModel
from datetime import datetime
from typing import Dict

class EventCreate(BaseModel):
    company_id: str
    customer_id: str
    user_id: str
    event_name: str
    properties: Dict = {}
    timestamp: datetime
