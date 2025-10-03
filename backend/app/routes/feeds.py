from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..lib.database import SessionLocal
from ..lib import models, schemas, auth
from typing import List
from uuid import uuid4
from datetime import datetime

router = APIRouter(prefix="/feeds", tags=["feeds"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schemas.IndicatorOut])
def get_feed(
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key),
    min_score: int = 50,
    tag: str = None
):
    if "feeds:read" not in api_key.scopes:
        raise HTTPException(status_code=403, detail="API key missing feeds:read scope")

    q = db.query(models.Indicator).filter(models.Indicator.score >= min_score)
    if tag:
        q = q.filter(models.Indicator.tags.contains([tag]))
    return q.all()

@router.get("/stix")
def get_feed_stix(
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key),
    min_score: int = 50,
    tag: str = None
):
    if "feeds:read" not in api_key.scopes:
        raise HTTPException(status_code=403, detail="API key missing feeds:read scope")

    q = db.query(models.Indicator).filter(models.Indicator.score >= min_score)
    if tag:
        q = q.filter(models.Indicator.tags.contains([tag]))
    indicators = q.all()

    packages = db.query(models.IntelPackage).all()

    objects = []

    # Indicators, sightings, observed-data
    for ind in indicators:
        ind_obj = {
            "type": "indicator",
            "spec_version": "2.1",
            "id": f"indicator--{ind.id}",
            "created": ind.first_seen.isoformat() + "Z",
            "modified": ind.last_seen.isoformat() + "Z",
            "name": f"IOC {ind.type}: {ind.canonical_value}",
            "pattern_type": "stix",
            "pattern": f"[{ind.type.upper()}_VALUE = '{ind.canonical_value}']",
            "valid_from": ind.first_seen.isoformat() + "Z",
            "labels": ind.tags or [],
            "confidence": ind.confidence,
            "lang": "en"
        }
        objects.append(ind_obj)

        sighting_obj = {
            "type": "sighting",
            "spec_version": "2.1",
            "id": f"sighting--{uuid4()}",
            "created": ind.first_seen.isoformat() + "Z",
            "modified": ind.last_seen.isoformat() + "Z",
            "first_seen": ind.first_seen.isoformat() + "Z",
            "last_seen": ind.last_seen.isoformat() + "Z",
            "count": 1,
            "sighting_of_ref": f"indicator--{ind.id}"
        }
        objects.append(sighting_obj)

        obs_obj = {
            "type": "observed-data",
            "spec_version": "2.1",
            "id": f"observed-data--{uuid4()}",
            "created": ind.first_seen.isoformat() + "Z",
            "modified": ind.last_seen.isoformat() + "Z",
            "first_observed": ind.first_seen.isoformat() + "Z",
            "last_observed": ind.last_seen.isoformat() + "Z",
            "number_observed": 1,
            "objects": {
                "0": {
                    "type": ind.type,
                    "value": ind.canonical_value,
                    "asn": ind.asn,
                    "country": ind.country,
                    "tags": ind.tags or []
                }
            }
        }
        objects.append(obs_obj)

    # Intel Packages as STIX report objects
    for pkg in packages:
        report_obj = {
            "type": "report",
            "spec_version": "2.1",
            "id": f"report--{pkg.id}",
            "created": pkg.created_at.isoformat() + "Z",
            "modified": pkg.created_at.isoformat() + "Z",
            "name": pkg.title,
            "description": pkg.summary,
            "report_types": ["threat-report"],
            "object_refs": [f"indicator--{ioc}" for ioc in pkg.indicators],
            "labels": pkg.techniques or [],
            "published": pkg.created_at.isoformat() + "Z",
            "lang": "en"
        }
        objects.append(report_obj)

    bundle = {
        "type": "bundle",
        "id": f"bundle--{uuid4()}",
        "objects": objects
    }

    return bundle
