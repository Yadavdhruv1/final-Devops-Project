#!/usr/bin/env bash
# ==============================================================================
# FinPilot DevOps Capstone — Automated Independent Audit Script (Bash)
# ==============================================================================
set -eo pipefail

FAILED_CHECKS=0
PASSED_CHECKS=0

report_check() {
    local module="$1"
    local desc="$2"
    local status="$3"
    if [ "$status" -eq 0 ]; then
        echo -e "\033[0;32m  [PASS] ($module) $desc\033[0m"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "\033[0;31m  [FAIL] ($module) $desc\033[0m"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
    fi
}

echo -e "\033[0;36m============================================================\033[0m"
echo -e "\033[0;36m       FinPilot DevOps Capstone — Independent Audit Script   \033[0m"
echo -e "\033[0;36m============================================================\033[0m"

# M1 & M2
echo "--> Checking Backend & Tests..."
python -m compileall backend/app -q && report_check "M1" "Backend Python syntax" 0 || report_check "M1" "Backend Python syntax" 1
(cd backend && python -m pytest tests/ -v --tb=short) && report_check "M2" "Pytest execution (24 tests)" 0 || report_check "M2" "Pytest execution" 1
(cd backend && python -m pytest tests/ --cov=app --cov-report=term) && report_check "M2" "Pytest coverage >= 80%" 0 || report_check "M2" "Pytest coverage" 1

# M1 Frontend
echo "--> Checking Frontend Build..."
(cd frontend && npm run build) && report_check "M1" "Frontend Vite build" 0 || report_check "M1" "Frontend Vite build" 1

# M3 Git Commits
echo "--> Checking Git Commits..."
COMMIT_COUNT=$(git log --oneline | wc -l)
[ "$COMMIT_COUNT" -ge 10 ] && report_check "M3" "Git conventional commits >= 10 (Found: $COMMIT_COUNT)" 0 || report_check "M3" "Git conventional commits" 1

# M4 Docker Compose
echo "--> Checking Docker Compose..."
docker compose config --quiet && report_check "M4" "Docker Compose config validity" 0 || report_check "M4" "Docker Compose config" 1

# M7 Terraform
echo "--> Checking Terraform..."
docker run --rm -v "$(pwd)/terraform:/workspace" -w /workspace hashicorp/terraform:1.7 fmt -check && report_check "M7" "Terraform fmt check" 0 || report_check "M7" "Terraform fmt check" 1
docker run --rm -v "$(pwd)/terraform:/workspace" -w /workspace hashicorp/terraform:1.7 validate && report_check "M7" "Terraform validate" 0 || report_check "M7" "Terraform validate" 1

# M8 Helm
echo "--> Checking Helm Chart..."
docker run --rm -v "$(pwd)/helm/finpilot:/apps" alpine/helm:3.14.0 lint /apps && report_check "M8" "Helm lint" 0 || report_check "M8" "Helm lint" 1
docker run --rm -v "$(pwd)/helm/finpilot:/apps" alpine/helm:3.14.0 template finpilot /apps --namespace finpilot > /dev/null && report_check "M8" "Helm template" 0 || report_check "M8" "Helm template" 1

# M10 Docs
[ -f "README.md" ] && report_check "M10" "Root README.md exists" 0 || report_check "M10" "Root README.md" 1
[ -f "docs/presentation/SLIDES.md" ] && report_check "M10" "Slide deck exists" 0 || report_check "M10" "Slide deck" 1
[ -f "docs/security/TRIVY_CVE_ANALYSIS.md" ] && report_check "M6" "Trivy CVE report exists" 0 || report_check "M6" "Trivy CVE report" 1

echo ""
echo "============================================================"
echo "  Total Passed: $PASSED_CHECKS | Total Failed: $FAILED_CHECKS"
echo "============================================================"
[ "$FAILED_CHECKS" -eq 0 ] && exit 0 || exit 1
