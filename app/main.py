from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from prometheus_fastapi_instrumentator import Instrumentator
from starlette.responses import PlainTextResponse
from utils import predict
from fastapi.responses import JSONResponse


app = FastAPI()


@app.post("/")
def predict(island: str,
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


metrics = {}

@app.post("/predict")
def predict_route(island: str,
                  bill_length_mm: float,
                  bill_depth_mm: float,
                  flipper_length_mm: float,
                  body_mass_g: float,
                  sex: str):
    global metrics
    try:
        result, metrics = predict(island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex)
        return result
    except Exception as e:
        print(e)
        return None

@app.get("/metrics")
def get_metrics():
    return JSONResponse(content=metrics)
