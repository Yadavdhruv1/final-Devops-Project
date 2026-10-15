# 🚀 FinPilot — Personal Finance Management Platform

> **DevOps Capstone Project** — A full-stack personal finance SaaS application with complete DevOps infrastructure, CI/CD pipeline, cloud deployment, and observability.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![React](https://img.shields.io/badge/React-18.3-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Terraform](https://img.shields.io/badge/Terraform-AWS-purple)
![Kubernetes](https://img.shields.io/badge/K8s-Helm-blue)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technology Stack](#-technology-stack)
- [Repository Structure](#-repository-structure)
- [Prerequisites](#-prerequisites)
- [Quick Start — Local Development](#-quick-start--local-development)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Database Migrations](#-database-migrations)
- [Testing](#-testing)
- [Docker](#-docker)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Security Scanning (Trivy)](#-security-scanning-trivy)
- [GHCR Images](#-ghcr-images)
- [Terraform — AWS Infrastructure](#-terraform--aws-infrastructure)
- [Kubernetes & Helm Deployment](#-kubernetes--helm-deployment)
- [Ingress & HPA](#-ingress--hpa)
- [ArgoCD — GitOps](#-argocd--gitops)
- [Monitoring — Prometheus & Grafana](#-monitoring--prometheus--grafana)
- [Troubleshooting Guide](#-troubleshooting-guide)
- [Known Limitations](#-known-limitations)
- [Cost Warning](#-cost-warning)

---

## 🎯 Project Overview

**FinPilot** is a personal finance management SaaS application that provides a polished dashboard for tracking transactions, managing budgets, and visualizing spending analytics. Built as an original capstone project demonstrating end-to-end DevOps practices.

**This is NOT a copy of the TaskBoard reference project.** FinPilot has its own domain (personal finance), data models (transactions, budgets, analytics), and business logic.

## ✨ Features

- **Transaction Management** — Full CRUD for income and expense tracking
- **Budget Tracking** — Set monthly budget limits per category with spending progress
- **Analytics Dashboard** — Spending breakdowns, monthly trends, and financial overview
- **15 Expense Categories** — Salary, food, transport, housing, entertainment, etc.
- **Search & Filtering** — Filter by type, category, date range, and text search
- **Pagination** — Efficient data loading for large transaction histories
- **Responsive Design** — Premium dark theme with glassmorphism and animations
- **Health Monitoring** — `/health`, `/ready`, `/metrics` endpoints
- **Prometheus Metrics** — HTTP request count, latency, in-progress, and DB status

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    User Browser                           │
└──────────────────────┬────────────────────────────────────┘
                       │
            ┌──────────▼──────────┐
            │   Nginx Ingress     │
            │   / → Frontend      │
            │   /api → Backend    │
            └──────┬──────┬───────┘
                   │      │
      ┌────────────▼┐  ┌──▼────────────┐
      │  React/Vite  │  │  FastAPI      │
      │  Frontend    │  │  Backend      │◄──── Prometheus
      │  (Nginx)     │  │  Port 8000    │      Scraping
      │  Port 3000   │  │               │
      └──────────────┘  └──────┬────────┘
                               │
                    ┌──────────▼──────────┐
                    │   PostgreSQL 16     │
                    │   Port 5432         │
                    │   (Persistent Vol)  │
                    └─────────────────────┘
```

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite 5, Recharts, Nginx |
| **Backend** | Python 3.12, FastAPI, SQLAlchemy, Alembic |
| **Database** | PostgreSQL 16 |
| **Testing** | Pytest (SQLite isolation) |
| **Containers** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Security** | Trivy (HIGH/CRITICAL scan) |
| **Registry** | GitHub Container Registry (GHCR) |
| **IaC** | Terraform (AWS VPC + EKS) |
| **Orchestration** | Kubernetes, Helm |
| **GitOps** | ArgoCD |
| **Monitoring** | Prometheus, Grafana |

## 📁 Repository Structure

```
finpilot-devops-capstone/
├── frontend/                  # React/Vite application
│   ├── src/components/        # UI components
│   ├── Dockerfile             # Multi-stage: Node build → Nginx
│   └── nginx.conf             # SPA + API proxy config
├── backend/                   # FastAPI application
│   ├── app/
│   │   ├── main.py            # App entry + health/metrics
│   │   ├── api/               # Route handlers
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic validation
│   │   ├── services/          # Business logic
│   │   └── database.py        # DB configuration
│   ├── alembic/versions/      # Database migrations
│   ├── tests/                 # Pytest test suite
│   └── Dockerfile             # Python with non-root user
├── terraform/                 # AWS VPC + EKS
├── helm/finpilot/             # Helm chart + templates
├── k8s/                       # Namespace manifest
├── monitoring/                # Prometheus + Grafana values
├── argocd/                    # ArgoCD Application manifest
├── troubleshooting/           # 5 troubleshooting exercises
├── .github/workflows/         # CI/CD pipeline
├── scripts/                   # Seed data utility
├── demo/evidence/             # Screenshots and logs
├── docker-compose.yml         # Local 3-service stack
├── Makefile                   # Task runner
└── README.md                  # This file
```

## 📋 Prerequisites

- **Docker** & **Docker Compose** v2+
- **Node.js** 20+ (for local frontend dev)
- **Python** 3.12+ (for local backend dev)
- **AWS CLI** configured (for Terraform)
- **Terraform** 1.5+
- **kubectl** & **Helm** 3 (for K8s deployment)

## 🚀 Quick Start — Local Development

```bash
# 1. Clone the repository
git clone https://github.com/Yadavdhruv1/final-Devops-Project.git
cd final-Devops-Project

# 2. Create environment file
cp .env.example .env

# 3. Start all services
docker compose up --build -d

# 4. Verify services
docker compose ps
docker compose logs backend

# 5. Seed sample data (optional)
docker compose exec backend python -c "
from scripts import seed_data; seed_data.seed()
" 2>/dev/null || python scripts/seed-data.py

# 6. Open the application
# Frontend:  http://localhost:3000
# API Docs:  http://localhost:3000/docs
# Health:    http://localhost:3000/health
# Metrics:   http://localhost:3000/metrics

# 7. Stop services
docker compose down
```

## 🔐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://finpilot:finpilot_secret@db:5432/finpilot` |
| `POSTGRES_USER` | Database username | `finpilot` |
| `POSTGRES_PASSWORD` | Database password | `finpilot_secret` |
| `POSTGRES_DB` | Database name | `finpilot` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,http://localhost:5173` |

## 📡 API Documentation

Interactive Swagger docs available at `/docs` when the backend is running.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Liveness probe |
| `GET` | `/ready` | Readiness probe (DB check) |
| `GET` | `/metrics` | Prometheus metrics |
| `GET` | `/api/transactions/` | List transactions (paginated, filterable) |
| `POST` | `/api/transactions/` | Create transaction |
| `GET` | `/api/transactions/{id}` | Get transaction |
| `PUT` | `/api/transactions/{id}` | Update transaction |
| `DELETE` | `/api/transactions/{id}` | Delete transaction |
| `GET` | `/api/budgets/` | List budgets |
| `POST` | `/api/budgets/` | Create budget |
| `GET` | `/api/budgets/spending` | Budgets with actual spending |
| `PUT` | `/api/budgets/{id}` | Update budget |
| `DELETE` | `/api/budgets/{id}` | Delete budget |
| `GET` | `/api/analytics/dashboard` | Dashboard overview |
| `GET` | `/api/analytics/trends` | Monthly trends |

## 🗄️ Database Migrations

```bash
# Run migrations
cd backend
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Rollback
alembic downgrade -1
```

## 🧪 Testing

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/ -v

# Test coverage: 21 test cases across 5 endpoints
# - Transaction CRUD (15 tests)
# - Budget CRUD (6 tests)
# - Health/Metrics/Docs (5 tests)
# Uses isolated SQLite in-memory DB (no PostgreSQL needed)
```

## 🐳 Docker

**Backend Dockerfile**: Python 3.12-slim, non-root user, layer-cached deps
**Frontend Dockerfile**: Multi-stage (Node 20 build → Nginx 1.27 serve), non-root

```bash
docker compose config          # Validate config
docker compose up --build      # Build and start
docker compose ps              # Check status
docker compose logs -f         # Stream logs
docker compose down            # Stop
docker compose down -v         # Stop + remove volumes
```

## ⚙️ CI/CD Pipeline

**File**: `.github/workflows/ci-cd.yaml`
**Trigger**: Push to `main`

| Stage | Steps |
|-------|-------|
| **1. Test** | Python 3.12 setup → pip install → pytest |
| **2. Build Frontend** | Node 20 setup → npm install → npm run build |
| **3. Docker + Scan** | Build both images → Trivy HIGH/CRITICAL scan |
| **4. Publish** | Push to GHCR with `${{ github.sha }}` tag |

Test failures block image promotion. Trivy failures block publishing.

## 🔒 Security Scanning (Trivy)

Both images scanned for HIGH and CRITICAL vulnerabilities:
```yaml
- uses: aquasecurity/trivy-action@master
  with:
    severity: "CRITICAL,HIGH"
    exit-code: "1"           # Fail pipeline on findings
    ignore-unfixed: true     # Skip unfixed CVEs
```

## 📦 GHCR Images

```
ghcr.io/yadavdhruv1/finpilot-backend:<commit-sha>
ghcr.io/yadavdhruv1/finpilot-frontend:<commit-sha>
```

Images tagged with full Git commit SHA for immutable deployments.

## ☁️ Terraform — AWS Infrastructure

Creates: VPC + 2 public/2 private subnets + IGW + NAT + EKS cluster + managed node group

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply        # ⚠️ Incurs AWS costs
terraform output
terraform destroy      # Clean up after evaluation
```

## ☸️ Kubernetes & Helm Deployment

```bash
kubectl apply -f k8s/namespace.yaml
helm lint helm/finpilot
helm upgrade --install finpilot ./helm/finpilot \
  --namespace finpilot --create-namespace
kubectl get pods,svc,ingress,hpa -n finpilot
```

**Includes**: 2 replicas per deployment, ClusterIP services, liveness/readiness probes, resource limits, Secrets/ConfigMaps, PostgreSQL with PVC.

## 🌐 Ingress & HPA

- **Ingress**: `/` → frontend, `/api` → backend (nginx ingress class)
- **HPA**: Backend scales 2–5 replicas at 70% CPU utilization

## 🔄 ArgoCD — GitOps

```bash
kubectl apply -f argocd/application.yaml
# ArgoCD watches helm/finpilot/ in main branch
# Auto-sync with self-heal and pruning enabled
```

**GitOps Flow**: Push to `main` → CI builds + publishes images → Update image tag in values.yaml → ArgoCD detects change → Syncs to cluster

## 📊 Monitoring — Prometheus & Grafana

```bash
# Install monitoring stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f monitoring/prometheus-values.yaml

# Verify
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
# Check Targets page for finpilot-backend

# Grafana
kubectl port-forward svc/prometheus-grafana -n monitoring 3001:80
# Login: admin/admin
```

**Dashboard panels**: Request rate, p95 latency, requests in progress, DB status, error rate.

## 🔧 Troubleshooting Guide

See [`troubleshooting/README.md`](troubleshooting/README.md) for 5 exercises:
1. **ImagePullBackOff** — Incorrect image reference
2. **Service Selector Mismatch** — No endpoints
3. **Readiness Failure** — PostgreSQL unavailable
4. **Ingress Routing** — 404/502 errors
5. **Prometheus Target DOWN** — Scraping failure

## ⚠️ Known Limitations

- No authentication/authorization (out of scope for DevOps capstone)
- Single PostgreSQL instance (not HA)
- Budget category uniqueness constraint per table, not per month/year
- Seed data uses random values (for demonstration purposes)

## 💰 Cost Warning

⚠️ **Running AWS infrastructure incurs charges:**
- EKS Control Plane: ~$0.10/hr (~$73/month)
- NAT Gateway: ~$0.045/hr (~$33/month)
- t3.medium nodes (×2): ~$0.042/hr each (~$61/month)
- **Estimated total: ~$170/month**

**Always run `terraform destroy` after evaluation to avoid unexpected charges.**

---

**Built by Dhruv Yadav** — DevOps Capstone Project 2026
