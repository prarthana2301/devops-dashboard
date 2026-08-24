# DevOps Dashboard

A small Flask app used as the base for a full DevOps lifecycle demo:
Git → Docker → Jenkins → Ansible → Cloud → Prometheus/Grafana.

## Endpoints
- `/` — Human-facing dashboard (status, version, environment, host info)
- `/health` — Health check endpoint (used later by Docker, Jenkins, and monitoring)
- `/api/info` — JSON version of dashboard data

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Visit http://localhost:5000

## Environment variables
- `APP_VERSION` — shown on dashboard (default: 0.1.0)
- `APP_ENV` — development / staging / production (default: development)
