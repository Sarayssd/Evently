from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    document_id = Column(String, index=True)
    email = Column(String, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))

    event = relationship("Event", back_populates="registrations")
 