"""
FinPilot Tests - Budget API Tests
"""


class TestCreateBudget:
    """Tests for POST /api/budgets/"""

    def test_create_budget_success(self, client, sample_budget):
        """Test creating a valid budget."""
        response = client.post("/api/budgets/", json=sample_budget)
        assert response.status_code == 201
        data = response.json()
        assert data["category"] == "food"
        assert data["monthly_limit"] == 500.00
        assert data["month"] == 10

    def test_create_budget_invalid_month(self, client):
        """Test that invalid month is rejected."""
        payload = {
            "category": "food",
            "monthly_limit": 500.00,
            "month": 13,
            "year": 2026,
        }
        response = client.post("/api/budgets/", json=payload)
        assert response.status_code == 422


class TestListBudgets:
    """Tests for GET /api/budgets/"""

    def test_list_budgets_empty(self, client):
        """Test listing budgets when none exist."""
        response = client.get("/api/budgets/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_budgets_with_data(self, client, sample_budget):
        """Test listing budgets after creating one."""
        client.post("/api/budgets/", json=sample_budget)
        response = client.get("/api/budgets/")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestDeleteBudget:
    """Tests for DELETE /api/budgets/{id}"""

    def test_delete_budget_success(self, client, sample_budget):
        """Test deleting an existing budget."""
        create_resp = client.post("/api/budgets/", json=sample_budget)
        budget_id = create_resp.json()["id"]

        response = client.delete(f"/api/budgets/{budget_id}")
        assert response.status_code == 204

    def test_delete_budget_not_found(self, client):
        """Test deleting a non-existent budget."""
        response = client.delete("/api/budgets/99999")
        assert response.status_code == 404
