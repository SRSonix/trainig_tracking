from typing import Union

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from training_tracking.api.routers import skills, exercises

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://192.168.178.26:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skills.router)
app.include_router(exercises.router)


@app.get('/health', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {"status": "up"}
