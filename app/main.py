from fastapi import FastAPI
from app.api.endpoints import router  # Importing API routes

app = FastAPI(title="Radiology AI", description="An AI-powered radiology report generator")

# Include API routes
app.include_router(router)
