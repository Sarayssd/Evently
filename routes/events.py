from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.event import Event
from models.registration import Registration

from schemas.event_schema import EventCreate, EventUpdate
from schemas.registration_schema import RegistrationCreate, RegistrationRead

router = APIRouter()

@router.post("/events")
def create_event(event: EventCreate):

    db: Session = SessionLocal()

    new_event = Event(
        title=event.title,
        description=event.description,
        location=event.location,
        category=event.category,
        capacity=event.capacity,
        event_date=event.event_date,
        event_time=event.event_time
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    db.close()

    return {
        "message": "Evento creado correctamente",
        "event": new_event
    }

@router.get("/events")
def get_events():

    db: Session = SessionLocal()
    events = db.query(Event).all()
    db.close()
    return events

@router.put("/events/{event_id}")
def update_event(event_id: int, event_data: EventUpdate):

    db: Session = SessionLocal()

    event = db.query(Event).filter(Event.id == event_id).first()

    if event is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Evento no encontrado"
        )

    event.title = event_data.title
    event.description = event_data.description
    event.location = event_data.location
    event.capacity = event_data.capacity
    event.event_date = event_data.event_date
    event.event_time = event_data.event_time

    db.commit()
    db.refresh(event)

    db.close()

    return {
        "message": "Evento actualizado correctamente",
        "event": event
    }

@router.delete("/events/{event_id}")
def delete_event(event_id: int):

    db: Session = SessionLocal()
    event = db.query(Event).filter(Event.id == event_id).first()

    if event is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Evento no encontrado"
        )

    db.delete(event)
    db.commit()

    db.close()

    return {
        "message": "Evento eliminado correctamente"
    }


@router.post("/events/{event_id}/register")
def register_user(event_id: int, registration: RegistrationCreate):

    db: Session = SessionLocal()
    event = db.query(Event).filter(Event.id == event_id).first()

    if event is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Evento no encontrado"
        )

    registered_count = db.query(Registration).filter(
        Registration.event_id == event_id
    ).count()

    if registered_count >= event.capacity:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="No hay cupos disponibles"
        )

    new_registration = Registration(
        first_name=registration.first_name,
        last_name=registration.last_name,
        document_id=registration.document_id,
        email=registration.email,
        event_id=event_id
    )

    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    available_spots = event.capacity - (registered_count + 1)

    db.close()

    return {
        "message": "Inscripción realizada correctamente",
        "registration_id": new_registration.id,
        "event_id": event_id,
        "cupos_disponibles": available_spots
    }


@router.get("/events/{event_id}/registrations", response_model=List[RegistrationRead])
def get_event_registrations(event_id: int):

    db: Session = SessionLocal()

    event = db.query(Event).filter(Event.id == event_id).first()

    if event is None:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Evento no encontrado"
        )

    registrations = db.query(Registration).filter(
        Registration.event_id == event_id
    ).all()

    db.close()

    return registrations