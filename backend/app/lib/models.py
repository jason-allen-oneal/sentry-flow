from sqlalchemy import Column, String, Integer, DateTime, Enum, JSON, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
import uuid, enum
from datetime import datetime
from .database import Base

class IndicatorType(str, enum.Enum):
    ip = "ip"
    domain = "domain"
    url = "url"
    hash_md5 = "hash_md5"
    hash_sha1 = "hash_sha1"
    hash_sha256 = "hash_sha256"
    email = "email"
    wallet = "wallet"
    registry_key = "registry_key"

class Indicator(Base):
    __tablename__ = "indicators"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(IndicatorType), nullable=False)
    value_raw = Column(String, nullable=False)
    canonical_value = Column(String, nullable=False, index=True)
    value_hash = Column(String, index=True)
    score = Column(Integer, default=0)
    confidence = Column(Integer, default=0)
    status = Column(String, default="active")
    tags = Column(JSON, default=list)
    asn = Column(String, nullable=True)
    country = Column(String, nullable=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class ApiKey(Base):
    __tablename__ = "apikeys"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, nullable=False, index=True)
    owner = Column(String, nullable=False)
    scopes = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)

class IntelPackage(Base):
    __tablename__ = "intel_packages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    techniques = Column(JSON, default=list)       # list of MITRE ATT&CK IDs
    indicators = Column(JSON, default=list)       # list of indicator UUIDs
    created_at = Column(DateTime, default=datetime.utcnow)
