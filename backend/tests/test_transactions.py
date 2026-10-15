"""
FinPilot Tests - Transaction API Tests

Tests cover: POST, GET (list), GET (single), PUT, DELETE
with both success and error scenarios across 3 endpoints.
"""


class TestCreateTransaction:
    """Tests for POST /api/transactions/"""

    def test_create_transaction_success(self, client, sample_transaction):
        """Test creating a valid income transaction."""
        response = client.post("/api/transactions/", json=sample_transaction)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Monthly Salary"
        assert data["amount"] == 5000.00
        assert data["type"] == "income"
        assert data["category"] == "salary"
        assert "id" in data
        assert "created_at" in data

    def test_create_expense_transaction(self, client, sample_expense):
        """Test creating a valid expense transaction."""
        response = client.post("/api/transactions/", json=sample_expense)
        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "expense"
        assert data["category"] == "food"
        assert data["amount"] == 150.50

    def test_create_transaction_invalid_amount(self, client):
        """Test that negative amounts are rejected."""
        payload = {
            "title": "Bad Transaction",
            "amount": -100,
            "type": "expense",
            "category": "food",
            "date": "2026-10-15",
        }
        response = client.post("/api/transactions/", json=payload)
        assert response.status_code == 422

    def test_create_transaction_missing_title(self, client):
        """Test that missing required fields are rejected."""
        payload = {
            "amount": 100,
            "type": "income",
            "category": "salary",
        }
        response = client.post("/api/transactions/", json=payload)
        assert response.status_code == 422


class TestListTransactions:
    """Tests for GET /api/transactions/"""

    def test_list_transactions_empty(self, client):
        """Test listing transactions when none exist."""
        response = client.get("/api/transactions/")
        assert response.status_code == 200
        data = response.json()
        assert data["transactions"] == []
        assert data["total"] == 0

    def test_list_transactions_with_data(self, client, sample_transaction, sample_expense):
        """Test listing transactions after creating some."""
        client.post("/api/transactions/", json=sample_transaction)
        client.post("/api/transactions/", json=sample_expense)

        response = client.get("/api/transactions/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["transactions"]) == 2

    def test_list_transactions_filter_by_type(self, client, sample_transaction, sample_expense):
        """Test filtering transactions by type."""
        client.post("/api/transactions/", json=sample_transaction)
        client.post("/api/transactions/", json=sample_expense)

        response = client.get("/api/transactions/?type=income")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["transactions"][0]["type"] == "income"


class TestGetTransaction:
    """Tests for GET /api/transactions/{id}"""

    def test_get_transaction_success(self, client, sample_transaction):
        """Test getting a specific transaction."""
        create_resp = client.post("/api/transactions/", json=sample_transaction)
        txn_id = create_resp.json()["id"]

        response = client.get(f"/api/transactions/{txn_id}")
        assert response.status_code == 200
        assert response.json()["id"] == txn_id
        assert response.json()["title"] == "Monthly Salary"

    def test_get_transaction_not_found(self, client):
        """Test getting a non-existent transaction returns 404."""
        response = client.get("/api/transactions/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTransaction:
    """Tests for PUT /api/transactions/{id}"""

    def test_update_transaction_success(self, client, sample_transaction):
        """Test updating a transaction's title and amount."""
        create_resp = client.post("/api/transactions/", json=sample_transaction)
        txn_id = create_resp.json()["id"]

        update_data = {"title": "Updated Salary", "amount": 6000.00}
        response = client.put(f"/api/transactions/{txn_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()["title"] == "Updated Salary"
        assert response.json()["amount"] == 6000.00

    def test_update_transaction_not_found(self, client):
        """Test updating a non-existent transaction returns 404."""
        response = client.put("/api/transactions/99999", json={"title": "Nope"})
        assert response.status_code == 404


class TestDeleteTransaction:
    """Tests for DELETE /api/transactions/{id}"""

    def test_delete_transaction_success(self, client, sample_transaction):
        """Test deleting an existing transaction."""
        create_resp = client.post("/api/transactions/", json=sample_transaction)
        txn_id = create_resp.json()["id"]

        response = client.delete(f"/api/transactions/{txn_id}")
        assert response.status_code == 204

        # Verify it's gone
        get_resp = client.get(f"/api/transactions/{txn_id}")
        assert get_resp.status_code == 404

    def test_delete_transaction_not_found(self, client):
        """Test deleting a non-existent transaction returns 404."""
        response = client.delete("/api/transactions/99999")
        assert response.status_code == 404
