from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, schemas, models
from .database import get_db, create_tables

app = FastAPI(
    title="Incident Tracking API",
    description="A simple API for tracking incidents reported from various sources",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    create_tables()

@app.post("/incidents/", response_model=schemas.IncidentResponse, status_code=201)
def create_incident(incident: schemas.IncidentCreate, db: Session = Depends(get_db)):
 
    return crud.create_incident(db=db, incident=incident)

@app.get("/incidents/", response_model=List[schemas.IncidentResponse])
def read_incidents(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
 
    incidents = crud.get_incidents(db, status=status, skip=skip, limit=limit)
    return incidents

@app.put("/incidents/{incident_id}", response_model=schemas.IncidentResponse)
def update_incident(
    incident_id: int,
    incident_update: schemas.IncidentUpdate,
    db: Session = Depends(get_db)
):
 
    db_incident = crud.update_incident_status(db, incident_id=incident_id, status=incident_update.status)
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return db_incident

@app.get("/")
def read_root():
    return {"message": "Incident Tracking API is running"}