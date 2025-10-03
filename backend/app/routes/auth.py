from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..lib.database import SessionLocal
from ..lib import models, schemas
import secrets

router = APIRouter(prefix="/apikeys", tags=["apikeys"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", response_model=schemas.ApiKeyOut)
def create_apikey(owner: str, db: Session = Depends(get_db)):
    key_value = secrets.token_hex(32)
    new_key = models.ApiKey(key=key_value, owner=owner, scopes=["indicators:write", "feeds:read"])
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    return new_key
