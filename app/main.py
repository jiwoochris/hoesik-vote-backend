from fastapi import FastAPI
from app.api import event
from app.api import menu
from app.api import vote

app = FastAPI()

app.include_router(event.router)
app.include_router(menu.router)
app.include_router(vote.router)
