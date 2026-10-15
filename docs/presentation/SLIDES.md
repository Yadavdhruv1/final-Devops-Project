# 📊 FinPilot — DevOps Capstone Presentation Slides

> **Course**: DevOps Final Capstone Project (Session 21)  
> **Student**: Dhruv Yadav  
> **Platform**: FinPilot Personal Finance SaaS Platform  
> **Repository**: [https://github.com/Yadavdhruv1/final-Devops-Project](https://github.com/Yadavdhruv1/final-Devops-Project)  

---

## Slide 1: Title & Executive Summary
### FinPilot: Enterprise-Grade Cloud-Native Personal Finance Platform
* **Mission**: Deliver a resilient, scalable, full-stack financial platform with end-to-end automated DevOps infrastructure.
* **Core Philosophy**: Zero-touch GitOps deployment, 100% Infrastructure as Code, shift-left DevSecOps, and continuous observability.
* **Rubric Coverage**: 10 Modules, 100 Marks verified across FastAPI, React, PostgreSQL, Docker, GitHub Actions, Trivy, Terraform, AWS EKS, Helm, ArgoCD, Prometheus, and Grafana.

> **Speaker Notes**:  
> Welcome to the final defense of FinPilot. Rather than a basic CRUD demo, FinPilot demonstrates a production-grade multi-tier SaaS platform engineered with standard enterprise DevOps patterns. Every layer—from code linting to cloud autoscaling and Grafana alerting—is automated and auditable.

---

## Slide 2: Application Architecture & Domain Design
### Full-Stack Microservices Architecture
* **Backend**: FastAPI (Python 3.12), SQLAlchemy 2.0 ORM, Pydantic v2 data validation.
* **Database**: PostgreSQL 16 managed via declarative Alembic schema migrations.
* **Frontend**: React 18 SPA bundled via Vite, featuring interactive Chart.js analytics.
* **API Capabilities**:
  * Complete Transaction CRUD (`/api/transactions/`) with pagination, type, and date filtering.
  * Budget Management (`/api/budgets/`) with real-time threshold calculations and spending vs limit trackers.
  * Analytics Engine (`/api/analytics/dashboard`, `/trends`) providing financial cash-flow insights.

> **Speaker Notes**:  
> FinPilot addresses personal financial tracking. We opted for FastAPI due to native async performance, automatic OpenAPI documentation, and strict Pydantic schemas. Alembic enforces zero schema drift, while the React frontend connects seamlessly through an Nginx reverse-proxy.

---

## Slide 3: Containerization & Security Hardening
### Production Multi-Stage Docker Architecture
* **Backend Image** (`python:3.12-slim`):
  * Multi-stage caching: dependency layer isolated from source code.
  * Security: Runs as dedicated unprivileged user `appuser` (UID/GID 1000).
  * Layer footprint: ~165 MB.
* **Frontend Image** (`node:20-alpine` → `nginx:1.27-alpine`):
  * Stage 1 builds static React bundle; Node runtime is discarded.
  * Stage 2 serves assets via unprivileged Nginx daemon (`USER nginx`, port 3000).
  * Custom reverse-proxy routes `/api`, `/health`, `/metrics`, and handles SPA client-side routing.
* **Docker Compose**: Orchestrates PostgreSQL, API, and Web UI with isolated networking, persistent volumes, and health checks.

> **Speaker Notes**:  
> Notice that both containers run as unprivileged, non-root users. The frontend uses a multi-stage build where the heavy Node.js compiler is discarded, leaving only a lightweight 25MB Nginx Alpine image in production.

---

## Slide 4: Testing & Code Quality Assurance
### Automated Pytest Suite & Coverage
* **Test Architecture**: 24 unit and integration tests executing across 5 core endpoint groups.
* **Isolation**: In-memory SQLite with `StaticPool` prevents any mutation of production databases during automated runs.
* **Coverage**: **83% code coverage** achieved (exceeding the 80% rubric threshold).
* **Endpoints Tested**:
  * Transactions (Creation, Retrieval, Filtering, Updates, Deletion, Validation Failures).
  * Budgets (Monthly limits, Category validation, Spending calculations).
  * System Health (`/health` liveness, `/ready` database probe, `/metrics` Prometheus feed).

> **Speaker Notes**:  
> Every commit executes the test suite in less than 2 seconds. The tests mock database transactions and verify both happy paths and edge cases like negative transaction amounts and invalid month boundaries.

---

## Slide 5: CI/CD Pipeline (GitHub Actions)
### Automated Build, Test, Scan & Publish Lifecycle
* **Trigger**: Automated on pull requests and pushes to `main`.
* **Stage 1 (Test)**: Python 3.12 setup, pip dependency caching, and pytest gate.
* **Stage 2 (Build Frontend)**: Node 20 setup, npm ci, and Vite production bundle generation.
* **Stage 3 (Docker & Security)**: Docker Buildx builds test images and passes them to Trivy container vulnerability scanner.
* **Stage 4 (Publish)**: Successful scans publish immutable images to GitHub Container Registry (GHCR) tagged with the exact Git commit SHA `${{ github.sha }}`.

> **Speaker Notes**:  
> We adhere strictly to immutable deployment principles. We never deploy `latest` tags in Kubernetes; each artifact is tagged with its Git SHA, ensuring 100% traceability from running pod back to source commit.

---

## Slide 6: DevSecOps & Vulnerability Management
### Shift-Left Security with Aqua Security Trivy
* **Vulnerability Scanning**: Automated inspection of OS packages and third-party dependencies.
* **Policy Gate**: Pipeline fails immediately (`exit-code: 1`) on any `HIGH` or `CRITICAL` severity finding.
* **Security Case Study**: Addressed CVE risks by selecting hardened minimal base images (`alpine` and `debian-slim`).
* **Continuous Scanning**: Security gates run prior to container registry push, ensuring contaminated images are never promoted.

> **Speaker Notes**:  
> DevSecOps is not an afterthought in FinPilot. Trivy scans run inside the pipeline before images are pushed to GHCR. If a developer introduces a package with a known High or Critical CVE, the build halts immediately.

---

## Slide 7: Infrastructure as Code (Terraform & AWS EKS)
### Declarative Cloud Infrastructure
* **VPC Networking**:
  * Dual-AZ deployment across `ap-south-1a` and `ap-south-1b`.
  * 2 Public subnets with Internet Gateway and ALB routing tags (`kubernetes.io/role/elb=1`).
  * 2 Private subnets with NAT Gateway for secure worker node isolation (`kubernetes.io/role/internal-elb=1`).
* **Amazon EKS Cluster**:
  * Kubernetes control plane v1.29 with IAM OIDC provider integration.
  * Managed Node Group (2x `t3.medium`) with auto-scaling security groups.
* **Clean Lifecycle**: Fully tested with `terraform init`, `validate`, and documented teardown procedures.

> **Speaker Notes**:  
> Our Terraform configuration provisions a production VPC spanning two availability zones. The EKS worker nodes reside in private subnets, shielded from the public internet, and route outbound traffic through a managed NAT Gateway.

---

## Slide 8: Kubernetes Orchestration & Helm Packaging
### Cloud-Native Deployment Architecture
* **Helm Packaging**: Parameterized `finpilot` chart supporting environments via `values.yaml` and `values-dev.yaml`.
* **Workload Resilience**:
  * Frontend & Backend Deployments provisioned with **2 replicas** across separate nodes.
  * Liveness (`/health`) and Readiness (`/ready`) HTTP probes ensure zero-downtime rolling updates.
  * Resource requests & limits prevent noisy-neighbor memory exhaustion.
* **Horizontal Pod Autoscaling (HPA)**: Backend scales dynamically from 2 to 5 replicas based on 70% CPU threshold.
* **Ingress Routing**: NGINX Ingress Controller directs root traffic `/` to frontend and path-prefix `/api` to backend.

> **Speaker Notes**:  
> Using Helm allows us to manage FinPilot as a single release unit. Both the API and Web tiers run multi-replica deployments with active readiness probes. When traffic spikes, the Kubernetes HPA automatically scales worker pods.

---

## Slide 9: GitOps Continuous Delivery (ArgoCD)
### Declarative Sync & Automated Reconciliation
* **Repository Source**: ArgoCD continuously polls the GitHub repository branch `main` watching `helm/finpilot/`.
* **Reconciliation Loop**:
  * Detects drift between live cluster state and desired Git state.
  * `automated.selfHeal = true`: Reverts manual changes or accidental kubectl edits automatically.
  * `automated.prune = true`: Deletes orphaned resources when manifests are removed from Git.
* **Deployment Pattern**: CI updates Helm values with new image tag → ArgoCD synchronizes cluster state.

> **Speaker Notes**:  
> We achieve true GitOps maturity with ArgoCD. Developers do not require direct kubectl access to the production cluster. The Git repository is the single source of truth, and ArgoCD continuously enforces that reality.

---

## Slide 10: Observability, SRE Runbook & Conclusion
### Production Telemetry & Verification
* **Prometheus Instrumentation**:
  * Custom metrics in FastAPI: `finpilot_http_requests_total`, `finpilot_http_request_duration_seconds`, and `finpilot_database_up`.
  * Target status: Continuously scraped and verified UP via `/metrics`.
* **Grafana Dashboards**: Live visualization of request throughput, p95 latency, error rates, and database health.
* **Incident Runbook**: Comprehensive documentation in `troubleshooting/README.md` covering ImagePullBackOff, Service selector mismatch, database connectivity drop, and scraping failures.
* **Cost Controls**: Estimated AWS run-rate ($170/mo) with explicit teardown commands to prevent accidental cloud spending.

> **Speaker Notes**:  
> Observability completes the operational loop. Custom Prometheus metrics expose real-time application behavior directly to Grafana dashboards. With automated tests, GitOps delivery, and proven runbooks, FinPilot achieves 100/100 capstone readiness.
