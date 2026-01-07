"""
Module 7 Integration Tests
==========================

Test suite for AI Director integration.
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path

# Add module paths
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from ai_director import AIDirector, DirectorConfig, Brief


@pytest.fixture
def config():
    """Test configuration."""
    return DirectorConfig(
        mongodb_uri=os.getenv("MONGODB_URI"),
        hf_token=os.getenv("HF_TOKEN"),
        output_dir="test_output",
        temp_dir="test_temp"
    )


@pytest.fixture
def director(config):
    """Test director instance."""
    return AIDirector(config)


@pytest.fixture
def sample_brief():
    """Sample content brief."""
    return Brief(
        brand="TestBrand",
        product="Test Product",
        duration=10.0,
        platform="instagram",
        language="thai"
    )


class TestAIDirector:
    """Test AIDirector class."""
    
    def test_initialization(self, config):
        """Test director initialization."""
        director = AIDirector(config)
        assert director is not None
        assert director.config == config
    
    def test_lazy_loading(self, director):
        """Test lazy loading of modules."""
        # Modules should be None initially
        assert director._rag_system is None
        assert director._image_generator is None
        assert director._voice_generator is None
        assert director._video_composer is None
        assert director._smart_cut is None
    
    @pytest.mark.asyncio
    async def test_brand_context_retrieval(self, director):
        """Test brand context retrieval."""
        context = await director.retrieve_brand_context("TestBrand")
        
        assert context is not None
        assert "brand_name" in context
        assert context["brand_name"] == "TestBrand"
    
    def test_creative_strategy_generation(self, director, sample_brief):
        """Test creative strategy generation."""
        context = {"brand_name": "TestBrand", "documents": []}
        strategy = director.generate_creative_strategy(sample_brief, context)
        
        assert strategy is not None
        assert strategy.concept
        assert len(strategy.visual_scenes) > 0
        assert strategy.script


class TestBrief:
    """Test Brief class."""
    
    def test_brief_creation(self):
        """Test brief creation."""
        brief = Brief(
            brand="Test",
            product="Product",
            duration=15.0,
            platform="instagram"
        )
        
        assert brief.brand == "Test"
        assert brief.product == "Product"
        assert brief.duration == 15.0
        assert brief.platform == "instagram"
    
    def test_brief_to_dict(self, sample_brief):
        """Test brief serialization."""
        data = sample_brief.to_dict()
        
        assert isinstance(data, dict)
        assert data["brand"] == "TestBrand"
        assert data["product"] == "Test Product"


class TestContentPipeline:
    """Test content pipeline."""
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_full_pipeline(self, director, sample_brief):
        """Test full content generation pipeline."""
        result = await director.create_content(sample_brief)
        
        assert result is not None
        assert result.video_path
        assert result.duration == sample_brief.duration
        assert "processing_time" in result.metadata


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
