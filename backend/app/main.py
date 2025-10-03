from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .routes import indicators, feeds, auth, packages
from .lib.database import Base, engine, SessionLocal
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from .lib import errors, enrichment
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SentryFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics counters
INDICATOR_REQUESTS = Counter("indicators_requests_total", "Total indicator submissions")
FEEDS_REQUESTS = Counter("feeds_requests_total", "Total feed requests")
HEALTH_CHECKS = Counter("health_checks_total", "Total health endpoint hits")

# Routers
app.include_router(indicators.router)
app.include_router(feeds.router)
app.include_router(auth.router)
app.include_router(packages.router)

# Error handlers
app.add_exception_handler(StarletteHTTPException, errors.http_exception_handler)
app.add_exception_handler(RequestValidationError, errors.request_validation_exception_handler)
app.add_exception_handler(ResponseValidationError, errors.response_validation_exception_handler)
app.add_exception_handler(Exception, errors.generic_exception_handler)

# Middleware hook to increment counters
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    response = await call_next(request)

    path = request.url.path
    if path.startswith("/indicators"):
        INDICATOR_REQUESTS.inc()
    elif path.startswith("/feeds"):
        FEEDS_REQUESTS.inc()
    elif path.startswith("/health"):
        HEALTH_CHECKS.inc()

    return response

# Healthcheck route
@app.get("/health")
def healthcheck():
    try:
        db: Session = SessionLocal()
        db.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False
    finally:
        db.close()

    return {
        "status": "ok" if db_ok and enrichment.GEOIP_AVAILABLE else "degraded",
        "database": "ok" if db_ok else "error",
        "enrichment": "loaded" if enrichment.GEOIP_AVAILABLE else "not available"
    }

# Prometheus metrics route
@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
