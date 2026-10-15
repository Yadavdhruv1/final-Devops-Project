"""
FinPilot Tests - Health & Metrics Endpoint Tests
"""


class TestHealthEndpoints:
    """Tests for health and operational endpoints."""

    def test_health_endpoint(self, client):
        """Test GET /health returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "finpilot-api"
        assert "version" in data

    def test_root_endpoint(self, client):
        """Test GET / returns service info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "FinPilot API"
        assert "docs" in data

    def test_metrics_endpoint(self, client):
        """Test GET /metrics returns Prometheus format."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "finpilot_http_requests_total" in response.text
        assert "finpilot_http_request_duration_seconds" in response.text

    def test_readiness_endpoint(self, client):
        """Test GET /ready returns database status."""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data

    def test_docs_endpoint(self, client):
        """Test that /docs (Swagger UI) is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200
