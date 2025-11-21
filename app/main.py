"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import members, plans, subscriptions, attendance

app = FastAPI(
    title="Service Membership System API",
    description="Backend API for managing memberships, subscriptions, and attendance",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(members.router, prefix="/members", tags=["Members"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Service Membership System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "ok"
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}