# Scrum Flow Backend

Backend service for Scrum-Flow, providing Jira data ingestion, analytics, and ML-powered sprint predictions. It exposes REST APIs consumed by the frontend to deliver estimation accuracy insights, progress tracking, and planning support.

- Jira integration (OAuth or token-based)
- Analytics endpoints for estimation accuracy and team progress
- ML predictions for upcoming sprint workload
- Production-ready Docker setup (uWSGI) and PostgreSQL support

Frontend project for reference:
- Live Demo: https://scrum-flow.sfivaz.com/demo
- Thesis Documentation (Bachelor): https://drive.google.com/file/d/1EY82UGGvyxoVaD3mCsQSy2KbAo3Hs4U1/view

---

## Features

- Jira data synchronization and normalization
- Estimation accuracy metrics and time-series analytics
- Sprint prediction endpoints (e.g., estimated effort/time)
- Admin interface for operational tasks
- Healthcheck and logging for observability

---

## Tech Stack

- Language: Python 3.x
- Framework: Django (REST API)
- Database: PostgreSQL
- ML/Analytics: Python ecosystem
- App Server: uWSGI
- Containerization: Docker & Docker Compose
- Deployment: Docker, Procfile-compatible, AWS-ready

---

## Environment Variables

Create a `.env` file at the project root (you can use `.env.example` as a reference):

Required keys:
- SECRET_KEY
- DEBUG (True/False)
- ALLOWED_HOSTS (comma-separated)
- CORS_ALLOWED_ORIGINS (comma-separated)
- DATABASE_HOST, DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT

Example local values:

SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ALLOWED_ORIGINS=http://localhost:3000

DATABASE_HOST=localhost
DATABASE_NAME=scrumflow
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_PORT=5432
