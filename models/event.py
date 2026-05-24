from sqlalchemy import Column, Integer, String, Date,Time
from sqlalchemy.orm import relationship
from database import Base
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    location = Column(String)
    category = Column(String)
    capacity = Column(Integer)
    event_date = Column(Date)
    event_time = Column(Time)
    
    registrations = relationship(
        "Registration",
        back_populates="event",
        cascade="all, delete-orphan"
    )