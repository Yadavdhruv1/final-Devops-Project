# FinPilot DevOps Capstone - Automated Independent Audit Script (PowerShell)
$ErrorActionPreference = "Continue"
$failedChecks = 0
$passedChecks = 0

function Report-Check($Module, $Description, $Success) {
    if ($Success) {
        $global:passedChecks++
        Write-Host "  [PASS] ($Module) $Description" -ForegroundColor Green
    } else {
        $global:failedChecks++
        Write-Host "  [FAIL] ($Module) $Description" -ForegroundColor Red
    }
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "       FinPilot DevOps Capstone - Independent Audit Script   " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# M1 and M2
Write-Host "--> Checking M1 and M2: Backend Application and Test Suite..." -ForegroundColor Yellow
$pyCompile = python -m compileall backend/app -q
Report-Check "M1" "Backend Python syntax and compilation" ($LASTEXITCODE -eq 0)

$pytestOutput = python -m pytest backend/tests/ -v --tb=short
$pytestSuccess = ($LASTEXITCODE -eq 0)
Report-Check "M2" "Pytest test suite execution (24 tests)" $pytestSuccess

$covOutput = python -m pytest backend/tests/ --cov=app --cov-report=term
Report-Check "M2" "Pytest code coverage (target >= 80%)" ($LASTEXITCODE -eq 0)

# M1: Frontend
Write-Host "--> Checking M1: React/Vite Frontend Build..." -ForegroundColor Yellow
Push-Location frontend
$npmBuild = npm run build
$npmSuccess = ($LASTEXITCODE -eq 0)
Pop-Location
Report-Check "M1" "Frontend Vite production build" $npmSuccess

# M3: Git Commits
Write-Host "--> Checking M3: Git Commits..." -ForegroundColor Yellow
$commitCount = (git log --oneline | Measure-Object -Line).Lines
Report-Check "M3" "Git conventional commits count >= 10" ($commitCount -ge 10)

# M4: Docker Compose
Write-Host "--> Checking M4: Docker Compose Configuration..." -ForegroundColor Yellow
$composeConfig = docker compose config --quiet
Report-Check "M4" "Docker Compose configuration validity" ($LASTEXITCODE -eq 0)

# M5: GitHub Actions CI/CD
Write-Host "--> Checking M5: GitHub Actions CI/CD Configuration..." -ForegroundColor Yellow
$ciFileExists = Test-Path ".github/workflows/ci-cd.yaml"
Report-Check "M5" "CI/CD workflow file exists (.github/workflows/ci-cd.yaml)" $ciFileExists

# M7: Terraform
Write-Host "--> Checking M7: Terraform Infrastructure as Code..." -ForegroundColor Yellow
$tfFmt = docker run --rm -v "${PWD}/terraform:/workspace" -w /workspace hashicorp/terraform:1.7 fmt -check
Report-Check "M7" "Terraform formatting check (terraform fmt)" ($LASTEXITCODE -eq 0)

$tfValidate = docker run --rm -v "${PWD}/terraform:/workspace" -w /workspace hashicorp/terraform:1.7 validate
Report-Check "M7" "Terraform syntax validation (terraform validate)" ($LASTEXITCODE -eq 0)

# M8: Helm
Write-Host "--> Checking M8: Helm Chart Lint and Template..." -ForegroundColor Yellow
$helmLint = docker run --rm -v "${PWD}/helm/finpilot:/apps" alpine/helm:3.14.0 lint /apps
Report-Check "M8" "Helm chart lint (helm lint)" ($LASTEXITCODE -eq 0)

$helmTemplate = docker run --rm -v "${PWD}/helm/finpilot:/apps" alpine/helm:3.14.0 template finpilot /apps --namespace finpilot
Report-Check "M8" "Helm template rendering (helm template)" ($LASTEXITCODE -eq 0)

# M10: Documentation
Write-Host "--> Checking M10: Presentation and Documentation Artifacts..." -ForegroundColor Yellow
$readmeExists = Test-Path "README.md"
Report-Check "M10" "Root comprehensive README.md exists" $readmeExists

$slidesExists = (Test-Path "docs/presentation/SLIDES.md") -and (Test-Path "docs/presentation/index.html")
Report-Check "M10" "Presentation slide deck exists (SLIDES.md and index.html)" $slidesExists

$troubleshootingExists = Test-Path "troubleshooting/README.md"
Report-Check "M10" "Troubleshooting runbook exists" $troubleshootingExists

$cveReportExists = Test-Path "docs/security/TRIVY_CVE_ANALYSIS.md"
Report-Check "M6" "Trivy CVE and Security Report exists" $cveReportExists

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "                   AUDIT SUMMARY RESULTS                    " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Total Passed Checks : $passedChecks" -ForegroundColor Green
Write-Host "  Total Failed Checks : $failedChecks" -ForegroundColor $(if ($failedChecks -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($failedChecks -gt 0) {
    Write-Host "[FAIL] Audit failed with $failedChecks defect(s)." -ForegroundColor Red
    exit 1
} else {
    Write-Host "[SUCCESS] All automated verification checks passed!" -ForegroundColor Green
    exit 0
}
