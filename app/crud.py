from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def get_incident(db: Session, incident_id: int):
    return db.query(models.Incident).filter(models.Incident.id == incident_id).first()

def get_incidents(db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Incident)
    if status:
        query = query.filter(models.Incident.status == status)
    return query.offset(skip).limit(limit).all()

def create_incident(db: Session, incident: schemas.IncidentCreate):
    db_incident = models.Incident(
        description=incident.description,
        status=incident.status,
        source=incident.source
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def update_incident_status(db: Session, incident_id: int, status: str):
    db_incident = get_incident(db, incident_id)
    if db_incident:
        db_incident.status = status
        db.commit()
        db.refresh(db_incident)
    return db_incident