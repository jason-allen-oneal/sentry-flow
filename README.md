# SentryFlow

**SentryFlow** is a community-driven threat intelligence sharing platform.  
It collects, normalizes, enriches, and scores Indicators of Compromise (IOCs), and distributes curated feeds via JSON and STIX 2.1.  
Includes a FastAPI backend and a modern Next.js frontend for researchers, blue teams, and SOCs.

---

## ✨ Features

- 🔍 **IOC Ingestion** – Submit single or bulk IOCs (CSV/JSON) via API or UI  
- 🧩 **Normalization & Enrichment** – GeoIP (ASN, country), tagging, type parsing  
- ⚖️ **Scoring** – Rule-based precision scoring with source reputation, sightings, enrichment hits  
- 📡 **Feeds** – Export curated JSON or STIX 2.1 bundles (indicators, sightings, observed-data, intel packages as reports)  
- 🔑 **API Keys** – Role-based access (scopes for indicators/feeds)  
- 📦 **Intel Packages** – Mini threat reports with ATT&CK techniques + grouped IOCs  
- ⚡ **Alerts** – Define webhook/email/Discord alerts on high-confidence IOCs  
- 📊 **Metrics** – Prometheus `/metrics` + `/health` endpoints for ops  
- 🌐 **Frontend** – Next.js (App Router) + Tailwind for clean UX: submission forms, indicator search, package browser, feed configurator, key management, alerts  

---

## 📂 Monorepo Structure

```plaintext
sentry-flow/
├── backend/       # FastAPI + SQLAlchemy backend
│   └── app/
│       ├── lib/          # Database, models, schemas, scoring, enrichment
│       ├── routes/       # Indicators, feeds, packages, auth, alerts
│       └── main.py       # FastAPI entrypoint
│
├── frontend/      # Next.js (App Router) + Tailwind frontend
│   └── app/
│       ├── submit/       # IOC submission form
│       ├── indicators/   # Browse/search indicators
│       ├── packages/     # Intel packages view
│       ├── feeds/        # Feed configurator
│       ├── apikeys/      # API key management
│       └── alerts/       # Alerts management
│
├── .gitignore     # Monorepo ignores (Python, Node, env, logs)
├── README.md      # This file
└── docker-compose.yml (planned) # Containerized deploy
```
---

## 🚀 Getting Started

## Backend (FastAPI)

```
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload
```

Runs on http://127.0.0.1:8000

Endpoints:  
/indicators – submit/bulk upload IOCs  
/feeds – JSON feed  
/feeds/stix – STIX 2.1 bundle  
/packages – intel packages  
/apikeys/create – generate API keys  
/health + /metrics – monitoring 


## Frontend (Next.js) 
```
cd frontend
npm install
npm run dev
```

Runs on http://localhost:3000 

Pages:  
/submit – IOC submission form  
/indicators – browse/search table  
/packages – view intel packages  
/feeds – generate JSON/STIX feed URLs  
/apikeys – create/manage API keys  
/alerts – define alert rules

---

## 🔒 Authentication

All submission + feed endpoints require an API key (X-API-Key header). 

Keys are created via /apikeys/create?owner=<name> with scopes: 
```
indicators:write 
feeds:read 
```

The frontend stores the key in localStorage for API calls.

---

## 🛠 Roadmap

[x] IOC ingestion + enrichment
[x] Scoring + deduplication
[x] Feeds in JSON + STIX
[x] Intel packages → STIX reports
[x] Alerts (email/webhook/discord)
[x] Prometheus metrics + healthcheck
[x] Next.js frontend (App Router)
[ ] Docker Compose for one-command deploy
[ ] TAXII 2.1 server for enterprise interop
[ ] Graph views of infrastructure reuse
[ ] ML-assisted IOC clustering

---

## 📜 License
Apache 2.0 (recommended for adoption)
or AGPL-3.0 (if you want to enforce open contributions). 

---

## 🌊 Why SentryFlow?

MISP is powerful but heavyweight. Commercial TIPs are expensive.
SentryFlow is designed to be: 
Lightweight – sane defaults, simple setup, fast APIs 
Usable – clean frontend, mobile-friendly submission 
Precise – opinionated scoring → less junk intel 
Open – JSON + STIX feeds, Prometheus metrics, extensible enrichments


**Think MISP-lite, but with modern UX and no BS.**




