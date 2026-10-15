"""
FinPilot Backend - Main Application Entry Point

A personal-finance management API built with FastAPI, SQLAlchemy, and PostgreSQL.
"""
import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
)
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal, get_db
from app.api.transactions import router as transactions_router
from app.api.budgets import router as budgets_router
from app.api.analytics import router as analytics_router

# ─── Prometheus Metrics ───

REQUEST_COUNT = Counter(
    "finpilot_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)
REQUEST_LATENCY = Histogram(
    "finpilot_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)
REQUESTS_IN_PROGRESS = Gauge(
    "finpilot_http_requests_in_progress",
    "HTTP requests currently being processed",
    ["method"]
)
DB_STATUS = Gauge(
    "finpilot_database_up",
    "Database connectivity status (1=up, 0=down)"
)

APP_VERSION = "1.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    if not os.getenv("TESTING"):
        try:
            Base.metadata.create_all(bind=engine)
        except Exception:
            pass
    yield


app = FastAPI(
    title="FinPilot API",
    description="Personal Finance Management API — Track transactions, manage budgets, and visualize spending analytics.",
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── CORS Middleware ───

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Prometheus Middleware ───

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    """Collect Prometheus metrics for every request."""
    if request.url.path == "/metrics":
        return await call_next(request)

    method = request.method
    path = request.url.path

    REQUESTS_IN_PROGRESS.labels(method=method).inc()
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    status = str(response.status_code)

    REQUEST_COUNT.labels(method=method, endpoint=path, status_code=status).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=path).observe(duration)
    REQUESTS_IN_PROGRESS.labels(method=method).dec()

    return response


# ─── Routers ───

app.include_router(transactions_router)
app.include_router(budgets_router)
app.include_router(analytics_router)


# ─── Health, Readiness, Metrics ───

@app.get("/health", tags=["Health"])
def health_check():
    """Liveness probe — confirms the application is running."""
    return {
        "status": "healthy",
        "service": "finpilot-api",
        "version": APP_VERSION,
    }


@app.get("/ready", tags=["Health"])
def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe — verifies database connectivity."""
    try:
        db.execute(text("SELECT 1"))
        DB_STATUS.set(1)
        return {
            "status": "ready",
            "database": "connected",
        }
    except Exception as e:
        DB_STATUS.set(0)
        return {
            "status": "not_ready",
            "database": "disconnected",
            "details": str(e),
        }


@app.get("/metrics", tags=["Monitoring"])
def metrics():
    """Prometheus-formatted application metrics."""
    return PlainTextResponse(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.get("/", tags=["Root"])
def root():
    """API root endpoint."""
    return {
        "service": "FinPilot API",
        "version": APP_VERSION,
        "docs": "/docs",
        "health": "/health",
        "ready": "/ready",
        "metrics": "/metrics",
    }
