# FinPilot Troubleshooting Lab

## Exercise 1: ImagePullBackOff — Incorrect Image Reference

### Initial Symptoms
```
Pod status: ImagePullBackOff / ErrImagePull
```

### Diagnostic Commands
```bash
kubectl get pods -n finpilot
kubectl describe pod <pod-name> -n finpilot
kubectl get events -n finpilot --sort-by=.metadata.creationTimestamp
```

### Expected Observations
- Events show: `Failed to pull image "ghcr.io/yadavdhruv1/finpilot-backend:wrongtag"`
- Pod stuck in `ImagePullBackOff`

### Root Cause
Image tag does not exist in GHCR. The deployment references a non-existent image tag.

### Corrective Action
```bash
# Fix the image tag in values.yaml or via helm upgrade
helm upgrade finpilot ./helm/finpilot --namespace finpilot \
  --set backend.image.tag=<correct-sha-tag>
```

### Verification
```bash
kubectl get pods -n finpilot  # Should show Running
kubectl logs <pod-name> -n finpilot  # Should show application startup
```

---

## Exercise 2: Service Selector Mismatch — No Endpoints

### Initial Symptoms
```
Service has no endpoints. Application unreachable through the Service.
```

### Diagnostic Commands
```bash
kubectl get svc finpilot-backend -n finpilot
kubectl get endpoints finpilot-backend -n finpilot
kubectl get pods -n finpilot --show-labels
kubectl describe svc finpilot-backend -n finpilot
```

### Expected Observations
- `kubectl get endpoints` shows `<none>`
- Service selector labels don't match any Pod labels

### Root Cause
The Service's `selector` field (e.g., `app: finpilot-api`) doesn't match the Pod's labels (e.g., `app: finpilot-backend`).

### Corrective Action
```bash
# Ensure Service selector matches Pod labels
kubectl edit svc finpilot-backend -n finpilot
# Change selector to: app: finpilot-backend
```

### Verification
```bash
kubectl get endpoints finpilot-backend -n finpilot  # Should show IP:port
curl http://<service-ip>:8000/health  # Should return healthy
```

---

## Exercise 3: Readiness Failure — PostgreSQL Unavailable

### Initial Symptoms
```
Backend pods show 0/1 Ready. Application returns errors.
```

### Diagnostic Commands
```bash
kubectl get pods -n finpilot
kubectl describe pod <backend-pod> -n finpilot
kubectl logs <backend-pod> -n finpilot
kubectl get pods -n finpilot -l app=finpilot-postgresql
kubectl logs <postgresql-pod> -n finpilot
```

### Expected Observations
- Backend pod: `0/1 Running` (readiness probe failing)
- Logs show: `connection refused` or `could not connect to server`
- PostgreSQL pod may be `CrashLoopBackOff` or missing

### Root Cause
PostgreSQL is not running or the `DATABASE_URL` secret contains incorrect credentials.

### Corrective Action
```bash
# Check PostgreSQL is running
kubectl get pods -n finpilot -l app=finpilot-postgresql

# If PostgreSQL is down, check its logs
kubectl logs <pg-pod> -n finpilot

# Verify the secret
kubectl get secret finpilot-secrets -n finpilot -o yaml

# Restart PostgreSQL if needed
kubectl rollout restart deployment finpilot-postgresql -n finpilot
```

### Verification
```bash
kubectl get pods -n finpilot  # All pods should be 1/1 Ready
kubectl exec <backend-pod> -n finpilot -- python -c "from app.database import engine; engine.connect()"
curl http://<backend-svc>:8000/ready  # Should return "ready"
```

---

## Exercise 4: Ingress Routing Issue

### Initial Symptoms
```
Application not reachable via Ingress URL. Returns 404 or 502.
```

### Diagnostic Commands
```bash
kubectl get ingress -n finpilot
kubectl describe ingress finpilot-ingress -n finpilot
kubectl get pods -n ingress-nginx
kubectl logs <ingress-controller-pod> -n ingress-nginx
kubectl get svc -n finpilot
```

### Expected Observations
- Ingress shows no ADDRESS assigned
- Ingress controller pod may not exist
- Backend services may not have endpoints

### Root Cause
1. Ingress controller not installed in the cluster
2. Incorrect path configuration in Ingress rules
3. Backend services not ready

### Corrective Action
```bash
# Install ingress controller if missing
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace

# Verify Ingress paths match service configuration
kubectl get ingress finpilot-ingress -n finpilot -o yaml

# Check backend service endpoints
kubectl get endpoints -n finpilot
```

### Verification
```bash
kubectl get ingress -n finpilot  # Should show ADDRESS
curl http://<ingress-ip>/health  # Should proxy to backend
curl http://<ingress-ip>/  # Should serve frontend
```

---

## Exercise 5: Prometheus Target DOWN

### Initial Symptoms
```
Prometheus Targets page shows finpilot-backend as DOWN.
Grafana dashboard panels show "No data".
```

### Diagnostic Commands
```bash
# Check if metrics endpoint works
kubectl exec <backend-pod> -n finpilot -- wget -qO- http://localhost:8000/metrics

# Check Prometheus scrape config
kubectl get configmap -n monitoring
kubectl get servicemonitor -n finpilot 2>/dev/null

# Check Prometheus targets
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
# Visit http://localhost:9090/targets
```

### Expected Observations
- Target shows state: DOWN
- Error: `connection refused` or `no endpoints`
- Prometheus cannot reach the backend's `/metrics` endpoint

### Root Cause
1. Service port name doesn't match ServiceMonitor port selector
2. Namespace label selectors don't include the finpilot namespace
3. Network policy blocking Prometheus scrape traffic

### Corrective Action
```bash
# Verify backend service has correct port name
kubectl get svc finpilot-backend -n finpilot -o yaml

# Add labels to namespace if using label selectors
kubectl label namespace finpilot monitoring=enabled

# Verify scrape config includes the finpilot namespace
kubectl get configmap prometheus-kube-prometheus-prometheus -n monitoring -o yaml
```

### Verification
```bash
# Port-forward to Prometheus
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090
# Check Targets page — finpilot-backend should be UP

# Verify metrics in Prometheus query
# Query: finpilot_http_requests_total
# Should return results
```
