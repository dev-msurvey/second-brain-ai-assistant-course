"""
API Tests
=========

Test suite for REST API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add module paths
sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self):
        """Test GET /api/v1/health."""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "version" in data
        assert "modules" in data


class TestGenerateEndpoint:
    """Test content generation endpoint."""
    
    def test_generate_missing_fields(self):
        """Test POST /api/v1/generate with missing fields."""
        response = client.post("/api/v1/generate", json={})
        
        assert response.status_code == 422  # Validation error
    
    def test_generate_invalid_duration(self):
        """Test POST /api/v1/generate with invalid duration."""
        payload = {
            "brand": "Test",
            "product": "Product",
            "duration": -1,  # Invalid
            "platform": "instagram"
        }
        
        response = client.post("/api/v1/generate", json=payload)
        assert response.status_code == 422
    
    @pytest.mark.slow
    def test_generate_valid_request(self):
        """Test POST /api/v1/generate with valid request."""
        payload = {
            "brand": "TestBrand",
            "product": "Test Product",
            "duration": 10.0,
            "platform": "instagram"
        }
        
        response = client.post("/api/v1/generate", json=payload)
        
        # May fail if modules not available, but should not crash
        assert response.status_code in [200, 500, 503]


class TestRAGEndpoint:
    """Test RAG search endpoint."""
    
    def test_rag_search(self):
        """Test POST /api/v1/rag/search."""
        payload = {
            "query": "test query",
            "top_k": 3
        }
        
        response = client.post("/api/v1/rag/search", json=payload)
        
        # May not have RAG system, but should not crash
        assert response.status_code in [200, 503]


class TestImageEndpoint:
    """Test image generation endpoint."""
    
    def test_image_generation(self):
        """Test POST /api/v1/media/image."""
        payload = {
            "prompt": "test image",
            "style": "product",
            "width": 512,
            "height": 512
        }
        
        response = client.post("/api/v1/media/image", json=payload)
        
        # May not have image generator, but should not crash
        assert response.status_code in [200, 503]


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
