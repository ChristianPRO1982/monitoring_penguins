from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from prometheus_fastapi_instrumentator import Instrumentator
from utils import predict


app = FastAPI()


@app.post("/")
def home(island: str,
        bill_length_mm: float,
        bill_depth_mm: float,
        flipper_length_mm: float,
        body_mass_g: float,
        sex: str):
    
    try:
        return predict(island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex)
    except Exception as e:
        print(e)
        return None
    

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crée un endpoint /metric qui va écrire toutes les métriques
# Instrumentator().instrument(app).expose(app)
