# Scrum-Flow Backend

Backend service for **Scrum-Flow**, powering Jira data ingestion, analytics, and **ML-driven sprint predictions**.  
This REST API is consumed by the [Scrum-Flow Frontend](https://scrum-flow.sfivaz.com/demo) to provide **estimation-accuracy insights**, progress tracking, and predictive planning for Scrum teams.

📖 **Bachelor Thesis Documentation:** [Read the Thesis](https://drive.google.com/file/d/1EY82UGGvyxoVaD3mCsQSy2KbAo3Hs4U1/view)

---

## 🚀 Features
- **Jira Integration (OAuth)** – Secure Atlassian OAuth flow to automatically fetch and normalize sprint/issue data.  
- **Analytics Endpoints** – Estimation accuracy metrics, team progress time-series, and historical sprint analysis.  
- **ML Predictions** – Machine-learning models to forecast workload and sprint duration.  
- **Admin & Ops Tools** – Django admin for operational tasks, plus health-check and structured logging for observability.  
- **Production-Ready** – uWSGI/Gunicorn, Docker, and PostgreSQL setup for scalable deployments.

---

## 🛠️ Tech Stack
- **Language:** Python 3.x  
- **Framework:** Django REST Framework  
- **Database:** PostgreSQL  
- **ML / Analytics:** scikit-learn (LinearRegression), NumPy, SciPy  
- **App Server:** Gunicorn (with uWSGI compatibility)  
- **Containerization & Deployment:** Docker, Docker Compose, Procfile-compatible (Heroku / Render), AWS-ready

---

## 📦 Installation


### 1️⃣ Run with Docker

The project includes a production-ready Dockerfile.

Build and run the container:

#### Build the image (tag it for clarity)
```bash

docker build -t scrum-flow-backend .

```

#### Run the container, mapping port 8000
```bash

docker run -d \
  --name scrum-flow-backend \
  -p 8000:8000 \
  --env-file .env \
  scrum-flow-backend
```

The container will automatically:
	•	Apply migrations
	•	Start the Gunicorn server bound to 0.0.0.0:8000

Access the API at: http://localhost:8000

⸻

### 2️⃣ Local Development (Virtualenv)

```bash

git clone https://github.com/yourusername/scrum-flow-backend.git
cd scrum-flow-backend

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

Create a .env file at the project root (see .env.example for guidance):

```bash

SECRET_KEY=your_secret_key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
CORS_ALLOWED_ORIGINS=https://scrum-flow.sfivaz.com

DATABASE_HOST=localhost
DATABASE_NAME=scrumflow
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_PORT=5432

```

Run migrations and start the server:

```bash

python manage.py migrate
python manage.py runserver

```

⸻

## 🌐 API Overview

Access the API documentation at: http://localhost:8000/api/docs

⸻

## 🧩 How It Works
	1.	Frontend authenticates with Jira (OAuth).
	2.	Backend ingests and normalizes sprint & issue data.
	3.	Analytics engine computes estimation accuracy and time-series metrics.
	4.	ML module forecasts upcoming sprint workload, returning predictions to the frontend dashboards.

⸻

## 🤝 Contribution

Contributions are welcome!
Open an issue or submit a pull request to propose improvements.

⸻

## 📜 License

Licensed under the MIT License – see the LICENSE file for details.
