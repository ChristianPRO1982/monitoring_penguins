from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from utils import ookk

app = FastAPI()


@app.get("/")
def home():
    if ookk():
        return "Hello, World!"
    else:
        return "Nope!"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crée un endpoint /metric qui va écrire toutes les métriques
Instrumentator().instrument(app).expose(app)
