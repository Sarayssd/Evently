from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import func

from database import engine, Base, SessionLocal
from models import event
from models import registration
from models.event import Event
from models.registration import Registration
from routes.events import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Evently API",
    description="API para gestión de eventos universitarios con control de aforo",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

def create_demo_event_if_empty():
    db = SessionLocal()
    try:
        existing_event = db.query(Event.id).first()
        if existing_event is None:
            demo_event = Event(
                title="Hackathon Evently",
                description="Competencia universitaria de programación",
                location="Auditorio Principal",
                capacity=20
            )
            db.add(demo_event)
            db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup():
    create_demo_event_if_empty()


app.include_router(router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    db = SessionLocal()
    events = db.query(Event).all()

    registration_counts = db.query(
        Registration.event_id,
        func.count(Registration.id).label("registered_count")
    ).group_by(Registration.event_id).all()

    registration_counts = {
        event_id: count for event_id, count in registration_counts
    }

    db.close()

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "events": events,
            "registration_counts": registration_counts
        }
    )