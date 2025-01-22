# monitoring_penguins
Study project for monitoring the dataset penguins (by seaborn)

## Notes
The root file (requirements.txt) is for testing only, without docker.

### URL
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
DEBUG=2 # 0: off, 1: on, 2: on with debug messages, 3: on with only SQL queries
DOCKER=0
```