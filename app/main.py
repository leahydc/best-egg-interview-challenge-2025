from fastapi import FastAPI
from app.api import carriers
from app.api import packages

app = FastAPI(title="Package Tracker API")

app.include_router(carriers.router)
app.include_router(packages.router)
