from pydantic import BaseModel
from datetime import date
from datetime import date, time


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    capacity: int
    event_date: date
    event_time: time
    category: str

class EventUpdate(BaseModel):
    title: str
    description: str
    location: str
    capacity: int
    event_date: date
    event_time: time
    category: str
