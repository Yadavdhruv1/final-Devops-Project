# ─── FinPilot Makefile ───

.PHONY: help dev build test clean docker-up docker-down docker-logs lint

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Local Development ───

dev: ## Start local development with Docker Compose
	docker compose up --build -d
	@echo "✅ FinPilot running at http://localhost:3000"

build: ## Build Docker images
	docker compose build

test: ## Run backend tests
	cd backend && pip install -r requirements.txt -q && python -m pytest tests/ -v

lint: ## Run linting
	cd backend && python -m py_compile app/main.py

# ─── Docker ───

docker-up: ## Start all services
	docker compose up --build -d

docker-down: ## Stop all services
	docker compose down

docker-logs: ## View service logs
	docker compose logs -f

docker-ps: ## Show running services
	docker compose ps

docker-clean: ## Remove all containers and volumes
	docker compose down -v --rmi all

# ─── Database ───

migrate: ## Run database migrations
	cd backend && alembic upgrade head

migrate-down: ## Rollback last migration
	cd backend && alembic downgrade -1

# ─── Terraform ───

tf-init: ## Initialize Terraform
	cd terraform && terraform init

tf-plan: ## Plan Terraform changes
	cd terraform && terraform plan

tf-apply: ## Apply Terraform changes
	cd terraform && terraform apply

tf-destroy: ## Destroy Terraform infrastructure
	cd terraform && terraform destroy

tf-fmt: ## Format Terraform files
	cd terraform && terraform fmt -check

# ─── Kubernetes ───

k8s-ns: ## Create Kubernetes namespace
	kubectl apply -f k8s/namespace.yaml

helm-lint: ## Lint Helm chart
	helm lint helm/finpilot

helm-install: ## Install/upgrade Helm release
	helm upgrade --install finpilot ./helm/finpilot --namespace finpilot --create-namespace

helm-uninstall: ## Uninstall Helm release
	helm uninstall finpilot -n finpilot

k8s-status: ## Show Kubernetes resources
	kubectl get pods,svc,ingress,hpa -n finpilot

# ─── Monitoring ───

monitoring-install: ## Install Prometheus + Grafana
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo update
	helm install prometheus prometheus-community/kube-prometheus-stack \
		-n monitoring --create-namespace -f monitoring/prometheus-values.yaml

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf frontend/dist frontend/node_modules 2>/dev/null || true
