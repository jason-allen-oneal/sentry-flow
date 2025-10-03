from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from ..lib.database import SessionLocal
from ..lib import schemas, models, scoring, enrichment, auth
import hashlib
from typing import List
import csv
from io import StringIO

router = APIRouter(prefix="/indicators", tags=["indicators"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.IndicatorOut)
def create_indicator(
    ind: schemas.IndicatorCreate,
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key)
):
    canonical = ind.value.strip().lower()
    value_hash = hashlib.sha256(canonical.encode()).hexdigest()

    enrich_data = {}
    if ind.type == models.IndicatorType.ip:
        enrich_data = enrichment.enrich_ip(canonical)
    elif ind.type == models.IndicatorType.domain:
        enrich_data = enrichment.enrich_domain(canonical)

    new = models.Indicator(
        type=ind.type,
        value_raw=ind.value,
        canonical_value=canonical,
        value_hash=value_hash,
        tags=ind.tags,
        asn=enrich_data.get("asn"),
        country=enrich_data.get("country"),
        score=scoring.score_indicator(
            source_rep=10,
            sightings=1,
            enrichment_hits=1 if enrich_data else 0
        )
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@router.post("/bulk", response_model=schemas.BulkResponse)
def create_indicators_bulk(
    indicators: List[schemas.IndicatorCreate],
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key)
):
    created = []
    errors = []

    for ind in indicators:
        try:
            canonical = ind.value.strip().lower()
            value_hash = hashlib.sha256(canonical.encode()).hexdigest()

            enrich_data = {}
            if ind.type == models.IndicatorType.ip:
                enrich_data = enrichment.enrich_ip(canonical)
            elif ind.type == models.IndicatorType.domain:
                enrich_data = enrichment.enrich_domain(canonical)

            new = models.Indicator(
                type=ind.type,
                value_raw=ind.value,
                canonical_value=canonical,
                value_hash=value_hash,
                tags=ind.tags,
                asn=enrich_data.get("asn"),
                country=enrich_data.get("country"),
                score=scoring.score_indicator(
                    source_rep=10,
                    sightings=1,
                    enrichment_hits=1 if enrich_data else 0
                )
            )
            db.add(new)
            db.commit()
            db.refresh(new)
            created.append(new)
        except Exception as e:
            db.rollback()
            errors.append({"value": ind.value, "error": str(e)})

    return {"created": created, "errors": errors}

@router.post("/bulk_csv", response_model=schemas.BulkResponse)
async def create_indicators_bulk_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    api_key: models.ApiKey = Depends(auth.require_api_key)
):
    created = []
    errors = []

    try:
        content = await file.read()
        decoded = content.decode("utf-8")
        reader = csv.DictReader(StringIO(decoded))

        for row in reader:
            try:
                ind_type = row.get("type")
                value = row.get("value")
                tags = row.get("tags", "").split(",") if row.get("tags") else []

                if not ind_type or not value:
                    errors.append({"row": row, "error": "Missing type or value"})
                    continue

                canonical = value.strip().lower()
                value_hash = hashlib.sha256(canonical.encode()).hexdigest()

                enrich_data = {}
                if ind_type == models.IndicatorType.ip:
                    enrich_data = enrichment.enrich_ip(canonical)
                elif ind_type == models.IndicatorType.domain:
                    enrich_data = enrichment.enrich_domain(canonical)

                new = models.Indicator(
                    type=ind_type,
                    value_raw=value,
                    canonical_value=canonical,
                    value_hash=value_hash,
                    tags=tags,
                    asn=enrich_data.get("asn"),
                    country=enrich_data.get("country"),
                    score=scoring.score_indicator(
                        source_rep=10,
                        sightings=1,
                        enrichment_hits=1 if enrich_data else 0
                    )
                )
                db.add(new)
                db.commit()
                db.refresh(new)
                created.append(new)
            except Exception as e:
                db.rollback()
                errors.append({"row": row, "error": str(e)})
    except Exception as e:
        errors.append({"file_error": str(e)})

    return {"created": created, "errors": errors}
