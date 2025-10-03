from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import ApiKey
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def require_api_key(x_api_key: str = Header(...), db: Session = Depends(get_db)):
    key = db.query(ApiKey).filter(ApiKey.key == x_api_key).first()
    if not key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    # update last_used
    key.last_used = datetime.utcnow()
    db.commit()
    return key
