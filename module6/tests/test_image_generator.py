"""
Tests for Image Generator
=========================

Test suite for Module 6 Image Generator functionality.
"""

import pytest
import os
from pathlib import Path
from PIL import Image

# Mock imports if HF_TOKEN not set
try:
    from tools.image_generator import ImageGenerator
    HAS_HF_TOKEN = bool(os.getenv("HF_TOKEN"))
except Exception:
    HAS_HF_TOKEN = False


@pytest.mark.skipif(not HAS_HF_TOKEN, reason="HF_TOKEN not set")
class TestImageGenerator:
    """Test ImageGenerator class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = ImageGenerator(model="sdxl")
        self.output_dir = Path("test_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Cleanup test files."""
        if self.output_dir.exists():
            for file in self.output_dir.glob("*"):
                file.unlink()
            self.output_dir.rmdir()
    
    def test_initialization(self):
        """Test generator initialization."""
        assert self.generator.model_name == "sdxl"
        assert self.generator.api_token is not None
        assert "stabilityai" in self.generator.model_id
    
    def test_generate_image(self):
        """Test single image generation."""
        output_file = self.output_dir / "test_image.png"
        
        image = self.generator.generate(
            prompt="A simple red circle on white background",
            width=512,
            height=512,
            num_inference_steps=20,  # Faster for testing
            output_file=str(output_file)
        )
        
        assert isinstance(image, Image.Image)
        assert output_file.exists()
        assert image.size == (512, 512)
    
    def test_style_preset(self):
        """Test style preset application."""
        output_file = self.output_dir / "test_style.png"
        
        image = self.generator.generate(
            prompt="A coffee cup",
            style_preset="product",
            width=512,
            height=512,
            num_inference_steps=20,
            output_file=str(output_file)
        )
        
        assert isinstance(image, Image.Image)
        assert output_file.exists()
    
    def test_available_models(self):
        """Test getting available models."""
        models = self.generator.get_available_models()
        
        assert isinstance(models, list)
        assert "sdxl" in models
        assert "flux-dev" in models
    
    def test_cost_estimation(self):
        """Test cost estimation."""
        estimate = self.generator.estimate_cost(num_images=10)
        
        assert estimate["num_images"] == 10
        assert estimate["cost_usd"] == 0.0
        assert "estimated_time_seconds" in estimate


class TestImageGeneratorUnit:
    """Unit tests that don't require API calls."""
    
    def test_model_mapping(self):
        """Test model ID mapping."""
        assert "sdxl" in ImageGenerator.MODELS
        assert "flux-dev" in ImageGenerator.MODELS
        assert ImageGenerator.MODELS["sdxl"] == "stabilityai/stable-diffusion-xl-base-1.0"
    
    def test_style_presets(self):
        """Test style preset definitions."""
        assert "product" in ImageGenerator.STYLE_PRESETS
        assert "cinematic" in ImageGenerator.STYLE_PRESETS
        assert "minimal" in ImageGenerator.STYLE_PRESETS
        
        product_preset = ImageGenerator.STYLE_PRESETS["product"]
        assert "positive" in product_preset
        assert "negative" in product_preset


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
