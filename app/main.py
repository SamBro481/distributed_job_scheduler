from fastapi import FastAPI

from app.api import jobs

app = FastAPI()

app.include_router(jobs.router)