from typing import Union

from fastapi import FastAPI, status
from training_tracking.api.routers import skills, exercises

app = FastAPI()


app.include_router(skills.router)
app.include_router(exercises.router)

@app.get('/health', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {"status": "up"}
