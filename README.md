# Nythera Platform

Nythera is a **Situational Intelligence & Governance Analytics Platform** designed to provide real-time dashboards and analytics for regional and governance monitoring.

The system combines a **FastAPI backend** with a **React + Vite dashboard frontend**.

---

## Architecture

```
Nythera/

backend/
 └── agent/
      ├── api/
      ├── cache/
      ├── data/
      └── main.py

frontend/
 └── District-Watch/
      ├── client/
      ├── server/
      └── package.json
```

---

## Tech Stack

Backend

* Python
* FastAPI

Frontend

* React
* Vite
* TypeScript

---

## Running the System (Local Development)

### Backend

```
cd backend/agent
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend will run at:

```
http://localhost:8000
```

---

### Frontend

```
cd frontend/District-Watch
npm install
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

## Production

Frontend can be built using:

```
npm run build
```

The generated `dist/` folder can be served through FastAPI or Nginx.

---

## Project Goal

Nythera aims to build a **planet-scale situational awareness system** integrating:

* Public Sentiment
* Media Verification
* Environmental Context
* Governance Responsiveness
* Intelligence Fusion

---

## License

Internal research / prototype system.
