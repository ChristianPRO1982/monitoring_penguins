# monitoring_penguins
Study project for monitoring the dataset penguins (by seaborn)

## to generate drift monitoring on Grafana

### 1. Make Predictions
Use the `/predict` endpoint to generate species predictions based on input features.

### 2. Generate Drift Reports
The API provides three endpoints to generate drift reports:
- **`/drifts`**: Provides an overall drift report.
- **`/concept_drift`**: Detects concept drift in the model.
- **`/data_drift`**: Detects data drift in the dataset.

### 3. Generate Metrics for Grafana
The `/metrics` endpoint exposes drift-related metrics in a Prometheus-compatible format. Grafana is automatically updated with these metrics.

## Integration with Grafana
Prometheus scrapes the `/metrics` endpoint to collect drift data, and Grafana visualizes these metrics for real-time monitoring.

## example to generate species predictions

| species | island    | bill_length_mm | bill_depth_mm | flipper_length_mm | body_mass_g | sex    |
|---------|----------|---------------|--------------|------------------|------------|--------|
| Adelie  | Torgersen | 39.1          | 18.7         | 181.0            | 3750.0     | Male   |
| Adelie  | Torgersen | 39.5          | 17.4         | 186.0            | 3800.0     | Female |
| Adelie  | Torgersen | 40.3          | 18.0         | 195.0            | 3250.0     | Female |
| Adelie  | Torgersen | NaN           | NaN          | NaN              | NaN        | NaN    |
| Adelie  | Torgersen | 36.7          | 19.3         | 193.0            | 3450.0     | Female |

## Notes
The root file (requirements.txt) is for testing only, without docker.

### URL
* http://localhost:8000/docs
* http://localhost:8000/metrics (pour afficher les metrics de Evidently AI)
* http://localhost:9090/targets
* http://localhost:9090/metrics
* http://localhost:9100/metrics
* http://localhost:3000/dashboard/
---
* https://hub.docker.com/r/prom/node-exporter/

### Brief
* https://zippy-twig-11a.notion.site/Monitoring-d-une-application-avec-Evidently-AI-Prometheus-et-Grafana-1801f9041c96801a9d82e35be19e219b

### .env for debug without docker
```dotenv
DEBUG=2 # 0: off, 1: on, 2: on with debug messages, 3: on with only SQL queriesTorgersen

PATH_MODEL='./model/'
TIME_LIMIT=300 # seconds
```

for testing :
```bash
cd app
python3 testing.py
```