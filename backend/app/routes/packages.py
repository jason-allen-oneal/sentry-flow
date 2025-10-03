from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..lib.database import SessionLocal
from ..lib import models, schemas, auth
from typing import List

router = APIRouter(prefix="/packages", tags=["packages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.IntelPackageOut)
def create_package(
    pkg: schemas.IntelPackageCreate,
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key)
):
    if "indicators:write" not in api_key.scopes:
        raise HTTPException(status_code=403, detail="API key missing indicators:write scope")

    new_pkg = models.IntelPackage(
        title=pkg.title,
        summary=pkg.summary,
        techniques=pkg.techniques,
        indicators=[str(i) for i in pkg.indicators]
    )
    db.add(new_pkg)
    db.commit()
    db.refresh(new_pkg)
    return new_pkg

@router.get("/", response_model=List[schemas.IntelPackageOut])
def list_packages(
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key)
):
    return db.query(models.IntelPackage).all()

@router.get("/{pkg_id}", response_model=schemas.IntelPackageOut)
def get_package(
    pkg_id: str,
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key)
):
    pkg = db.query(models.IntelPackage).filter(models.IntelPackage.id == pkg_id).first()
    if not pkg:
        raise HTTPException(status_code=404, detail="Intel package not found")
    return pkg
