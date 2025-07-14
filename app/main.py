from fastapi import FastAPI
from app.api import carriers
from app.api import packages

app = FastAPI(
    title="Best Egg 2025 Package Tracker API",
    description="This API was designed to provide a simple interface for tracking packages from various carriers.",
    version="1.0.0",
    contact={
        "name": "Dylan Leahy",
        "email": "leahy.dc@gmail.com"
    }
)

app.include_router(carriers.router)
app.include_router(packages.router)