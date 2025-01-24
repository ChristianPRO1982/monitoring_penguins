from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
# from prometheus_fastapi_instrumentator import Instrumentator
# from starlette import responses
from utils import predict
from drift_metrics import *
# from fastapi.responses import JSONResponse



app = FastAPI()


@app.post("/")
def api_predict(island: str,
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

@app.get("/drifts")
def drifts():
    if generate_metrics(False, False):
        return "test OK"
    else:
        return "test KO"


@app.get("/concept_drift")
def concept_drift():
    if generate_metrics(True, False):
        return "test OK"
    else:
        return "test KO"


@app.get("/data_drift")
def concept_drift():
    if generate_metrics(False, True):
        return "test OK"
    else:
        return "test KO"


@app.get("/metrics")
def get_metrics():
    group_by()

    metrics_data = get_metrics_by_json()

    prometheus_metrics = "# HELP drift_detected Indicates whether concept_drift or data_drift has been detected.\n"
    prometheus_metrics += "# TYPE drift_detected gauge\n"

    for record in metrics_data:
        timestamp = record["timestamp"]  # Pour information humaine, non inclus directement par Prometheus
        prometheus_metrics += f'drift_detected{{variable="concept_drift", group_by="{groupby}", timestamp="{timestamp}"}} {record["concept_drift"]}\n'
        prometheus_metrics += f'drift_detected{{variable="data_drift", group_by="{record["groupby"]}", timestamp="{timestamp}"}} {record["data_drift"]}\n'
    
    return Response(content=prometheus_metrics, media_type="text/plain")