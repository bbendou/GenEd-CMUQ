"""
this script is the entry point for the FastAPI application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import courses, requirements, departments, analytics

app = FastAPI(
    title="GenEd API",
    description="Backend for the GenEd project",
    version="1.0.0",
    openapi_url="/api/openapi.json",  # Explicit OpenAPI JSON path
    docs_url="/api/docs",  # Swagger UI path
    redoc_url="/api/redoc",  # Alternative ReDoc UI
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(requirements.router)
app.include_router(departments.router)
app.include_router(analytics.router)
