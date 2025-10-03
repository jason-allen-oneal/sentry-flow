from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import IndicatorType

class IndicatorCreate(BaseModel):
    type: IndicatorType
    value: str
    tags: Optional[List[str]] = []

class IndicatorOut(BaseModel):
    id: UUID
    type: IndicatorType
    canonical_value: str
    score: int
    confidence: int
    tags: List[str]
    first_seen: datetime
    last_seen: datetime
    asn: Optional[str] = None
    country: Optional[str] = None

    class Config:
        from_attributes = True

class BulkResponse(BaseModel):
    created: List[IndicatorOut]
    errors: List[dict]

class ApiKeyOut(BaseModel):
    id: UUID
    key: str
    owner: str
    scopes: List[str]
    created_at: datetime
    last_used: Optional[datetime] = None

    class Config:
        from_attributes = True

# Intel Packages
class IntelPackageCreate(BaseModel):
    title: str
    summary: str
    techniques: Optional[List[str]] = []
    indicators: Optional[List[UUID]] = []

class IntelPackageOut(BaseModel):
    id: UUID
    title: str
    summary: str
    techniques: List[str]
    indicators: List[UUID]
    created_at: datetime

    class Config:
        from_attributes = True
