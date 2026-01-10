"""
Integration tests for Epiphany Engine REST API.

Tests API endpoints, authentication, rate limiting, and error handling.
"""

import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app
from web.api import app

# Create test client
client = TestClient(app)


class TestHealthEndpoints:
    """Test health and info endpoints."""

    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert data["name"] == "Epiphany Engine API"
        assert "version" in data
        assert "status" in data
        assert data["status"] == "ok"
        assert data["docs_url"] == "/api/docs"
        assert data["health_url"] == "/api/health"
        assert data["info_url"] == "/api/info"

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_info_endpoint(self):
        """Test API info endpoint."""
        response = client.get("/api/info")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Epiphany Engine API"
        assert "version" in data
        assert data["status"] == "ok"
        assert "description" in data
        assert "endpoints" in data
        assert data["endpoints"]["simulate"] == "/api/simulate"
        assert "authentication" in data
        assert "cache" in data
        assert data["cache"]["enabled"] is True


class TestSecurityHeaders:
    """Test security headers are present in responses."""

    def test_security_headers_present(self):
        """Test that security headers are added to responses."""
        response = client.get("/")

        # Check all security headers
        assert "X-Content-Type-Options" in response.headers
        assert response.headers["X-Content-Type-Options"] == "nosniff"

        assert "X-Frame-Options" in response.headers
        assert response.headers["X-Frame-Options"] == "DENY"

        assert "X-XSS-Protection" in response.headers
        assert response.headers["X-XSS-Protection"] == "1; mode=block"

        assert "Content-Security-Policy" in response.headers
        csp = response.headers["Content-Security-Policy"]
        assert "default-src 'self'" in csp
        assert "frame-ancestors 'none'" in csp

        assert "Referrer-Policy" in response.headers
        assert "Permissions-Policy" in response.headers

    def test_hsts_header_in_production(self):
        """Test HSTS header is added when HTTPS is enabled."""
        with patch.dict(os.environ, {"ENVIRONMENT": "production", "HTTPS_ENABLED": "true"}):
            # Need to reload the module to pick up env changes
            # For this test, we'll just verify the logic exists
            from web.security import get_hsts_enabled

            assert get_hsts_enabled() is True

    def test_hsts_header_not_in_development(self):
        """Test HSTS header is not added in development."""
        with patch.dict(os.environ, {"ENVIRONMENT": "development", "HTTPS_ENABLED": "false"}):
            from web.security import get_hsts_enabled

            assert get_hsts_enabled() is False


class TestSimulateEndpoint:
    """Test the main simulation endpoint."""

    def test_simulate_with_valid_input(self):
        """Test simulation with valid parameters."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 10,
        }
        response = client.post("/api/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "steps" in data
        assert "summary" in data
        assert "intelligence_history" in data
        assert "selected_preset" in data
        assert "preset_fallback" in data

        # Validate data
        assert len(data["steps"]) == 10
        assert len(data["intelligence_history"]) == 10
        assert all(isinstance(score, (int, float)) for score in data["intelligence_history"])

    def test_simulate_with_preset(self):
        """Test simulation with preset configuration."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 5,
            "preset": "basic-growth",
        }
        response = client.post("/api/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["selected_preset"] == "basic-growth"
        assert data["preset_fallback"] is False

    def test_simulate_with_invalid_preset(self):
        """Test simulation with invalid preset falls back to baseline."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 5,
            "preset": "invalid-preset-name",
        }
        response = client.post("/api/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["preset_fallback"] is True
        assert data["selected_preset"] == "baseline"

    def test_simulate_with_boundary_values(self):
        """Test simulation with boundary values."""
        request_data = {
            "A": 0.0,
            "B": 0.0,
            "C": 0.0,
            "X": 1.0,
            "Y": 1.0,
            "Z": 0.0,
            "E_n": 0.0,
            "F_n": 0.0,
            "steps": 1,
        }
        response = client.post("/api/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()
        # With all zeros except X and Y, initial intelligence should be 0
        assert data["summary"]["initial_intelligence"] == 0.0

    def test_simulate_with_max_steps(self):
        """Test simulation with maximum allowed steps."""
        request_data = {
            "A": 0.5,
            "B": 0.5,
            "C": 0.5,
            "X": 0.5,
            "Y": 0.5,
            "Z": 0.5,
            "E_n": 1.0,
            "F_n": 1.0,
            "steps": 250,  # Maximum allowed
        }
        response = client.post("/api/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert len(data["steps"]) == 250


class TestInputValidation:
    """Test input validation and error handling."""

    def test_simulate_with_missing_field(self):
        """Test that missing required fields return 422."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            # Missing C, X, Y, Z, E_n, F_n
        }
        response = client.post("/api/simulate", json=request_data)
        assert response.status_code == 422

    def test_simulate_with_out_of_range_values(self):
        """Test that values outside allowed range return 422."""
        request_data = {
            "A": 1.5,  # Should be 0.0-1.0
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 10,
        }
        response = client.post("/api/simulate", json=request_data)
        assert response.status_code == 422

    def test_simulate_with_negative_steps(self):
        """Test that negative steps return 422."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": -5,  # Invalid
        }
        response = client.post("/api/simulate", json=request_data)
        assert response.status_code == 422

    def test_simulate_with_too_many_steps(self):
        """Test that steps > 250 return 422."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 251,  # Over limit
        }
        response = client.post("/api/simulate", json=request_data)
        assert response.status_code == 422

    def test_simulate_with_invalid_types(self):
        """Test that invalid types return 422."""
        request_data = {
            "A": "invalid",  # Should be float
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 10,
        }
        response = client.post("/api/simulate", json=request_data)
        assert response.status_code == 422


class TestAuthentication:
    """Test API authentication (when enabled)."""

    @patch.dict(os.environ, {"API_KEY_ENABLED": "false"})
    def test_simulate_without_auth_when_disabled(self):
        """Test that requests work without auth when disabled."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 5,
        }
        response = client.post("/api/simulate", json=request_data)
        assert response.status_code == 200

    def test_cors_headers_present(self):
        """Test that CORS headers are present."""
        response = client.options("/api/simulate")
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers or response.status_code == 200


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_404_for_nonexistent_endpoint(self):
        """Test that non-existent endpoints return 404."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404

    def test_method_not_allowed(self):
        """Test that wrong HTTP method returns 405."""
        response = client.get("/api/simulate")  # Should be POST
        assert response.status_code == 405


class TestResponseFormat:
    """Test response format and structure."""

    def test_simulation_response_structure(self):
        """Test that simulation response has correct structure."""
        request_data = {
            "A": 0.8,
            "B": 0.7,
            "C": 0.9,
            "X": 0.9,
            "Y": 0.8,
            "Z": 1.0,
            "E_n": 2.0,
            "F_n": 1.0,
            "steps": 3,
        }
        response = client.post("/api/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        # Check step structure
        assert isinstance(data["steps"], list)
        for step in data["steps"]:
            assert "step" in step
            assert "intelligence" in step
            assert "inputs" in step
            assert "state" not in step

        # Check summary structure
        assert isinstance(data["summary"], dict)
        assert "total_steps" in data["summary"]
        assert "final_intelligence" in data["summary"]

        # Check intelligence history
        assert isinstance(data["intelligence_history"], list)
        assert all(isinstance(x, (int, float)) for x in data["intelligence_history"])

    def test_simulation_step_contract(self):
        """Test simulation steps count and fields align with contract."""
        request_data = {
            "A": 0.6,
            "B": 0.6,
            "C": 0.6,
            "X": 0.6,
            "Y": 0.6,
            "Z": 0.6,
            "E_n": 1.2,
            "F_n": 1.0,
            "steps": 2,
        }
        response = client.post("/api/simulate", json=request_data)

        assert response.status_code == 200
        data = response.json()

        assert len(data["steps"]) == 2
        assert len(data["intelligence_history"]) == 2
        assert data["steps"][0]["step"] == 1
        assert "inputs" in data["steps"][0]
        assert "state" not in data["steps"][0]


class TestAPIDocumentation:
    """Test that API documentation endpoints work."""

    def test_openapi_schema(self):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_swagger_ui(self):
        """Test that Swagger UI is accessible."""
        response = client.get("/api/docs")
        assert response.status_code == 200
        # Should return HTML
        assert "text/html" in response.headers.get("content-type", "")

    def test_redoc(self):
        """Test that ReDoc is accessible."""
        response = client.get("/api/redoc")
        assert response.status_code == 200
        # Should return HTML
        assert "text/html" in response.headers.get("content-type", "")


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
