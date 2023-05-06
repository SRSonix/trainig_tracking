from typing import Union

from fastapi import FastAPI, status

from api.routers import skills

app = FastAPI()

app.include_router(skills.router)

@app.get('/health', status_code=status.HTTP_200_OK)
def perform_healthcheck():
    return {"status": "up"}
