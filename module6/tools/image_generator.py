"""
Module 6: Image Generator - HuggingFace Inference API Integration
================================================================

Generate images using SDXL or Flux models via HuggingFace Inference API.

Features:
- SDXL 1.0 base model support
- Flux model support (dev/schnell)
- Negative prompts
- Configurable parameters
- Batch generation
- Style presets

Author: AI Director Team
License: MIT
"""

import os
import time
import requests
from typing import Optional, List, Dict, Any
from pathlib import Path
from io import BytesIO
from PIL import Image
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageGenerator:
    """
    Generate images using HuggingFace Inference API.
    
    Supports:
    - SDXL 1.0 (stabilityai/stable-diffusion-xl-base-1.0)
    - Flux Dev (black-forest-labs/FLUX.1-dev)
    - Flux Schnell (black-forest-labs/FLUX.1-schnell)
    
    Example:
        >>> generator = ImageGenerator(model="sdxl")
        >>> image = generator.generate(
        ...     prompt="A premium coffee cup on marble surface",
        ...     width=1024,
        ...     height=1024
        ... )
        >>> image.save("output.png")
    """
    
    MODELS = {
        "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
        "flux-dev": "black-forest-labs/FLUX.1-dev",
        "flux-schnell": "black-forest-labs/FLUX.1-schnell",
    }
    
    STYLE_PRESETS = {
        "product": {
            "positive": "professional photography, 4K, high quality, studio lighting, sharp focus",
            "negative": "blurry, low quality, watermark, text, distorted"
        },
        "cinematic": {
            "positive": "cinematic lighting, dramatic, film grain, depth of field, anamorphic",
            "negative": "cartoon, anime, illustration, oversaturated"
        },
        "minimal": {
            "positive": "minimalist, clean, simple, elegant, white background",
            "negative": "cluttered, busy, complex, noisy"
        },
        "realistic": {
            "positive": "photorealistic, realistic, detailed, natural lighting, raw photo",
            "negative": "painting, drawing, artificial, CGI, 3D render"
        }
    }
    
    def __init__(
        self,
        model: str = "sdxl",
        api_token: Optional[str] = None,
        timeout: int = 60,
        retry_attempts: int = 3
    ):
        """
        Initialize ImageGenerator.
        
        Args:
            model: Model name ("sdxl", "flux-dev", "flux-schnell")
            api_token: HuggingFace API token (or set HF_TOKEN env var)
            timeout: API request timeout in seconds
            retry_attempts: Number of retry attempts on failure
        """
        self.model_name = model
        self.model_id = self.MODELS.get(model, model)
        self.api_token = api_token or os.getenv("HF_TOKEN")
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        
        if not self.api_token:
            raise ValueError(
                "HuggingFace API token required. "
                "Set HF_TOKEN environment variable or pass api_token parameter."
            )
        
        # HuggingFace Serverless Inference API is deprecated/restricted
        # Fallback to placeholder generation for now
        # TODO: Use Replicate API or local Stable Diffusion
        self.api_url = None  # Disabled
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        
        logger.warning("⚠️  HF Inference API unavailable - using placeholder generation")
        logger.info(f"✅ ImageGenerator initialized with model: {self.model_id} (placeholder mode)")
    
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 50,
        guidance_scale: float = 7.5,
        style_preset: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> Image.Image:
        """
        Generate a single image.
        
        Args:
            prompt: Text prompt describing the image
            negative_prompt: What to avoid in the image
            width: Image width in pixels
            height: Image height in pixels
            num_inference_steps: Number of denoising steps (higher = better quality)
            guidance_scale: How closely to follow the prompt (7-15 recommended)
            style_preset: Apply style preset ("product", "cinematic", "minimal", "realistic")
            output_file: Optional path to save the image
            
        Returns:
            PIL Image object
        """
        # Apply style preset
        if style_preset and style_preset in self.STYLE_PRESETS:
            preset = self.STYLE_PRESETS[style_preset]
            prompt = f"{prompt}, {preset['positive']}"
            negative_prompt = f"{negative_prompt}, {preset['negative']}" if negative_prompt else preset['negative']
        
        # Prepare payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "negative_prompt": negative_prompt,
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale
            }
        }
        
        logger.info(f"🎨 Generating image: {prompt[:50]}...")
        
        # HF API unavailable - use placeholder
        if not self.api_url:
            logger.warning("⚠️  Using placeholder image (HF API unavailable)")
            return self._create_placeholder(prompt, width, height, output_file)
        
        # Make request with retries
        for attempt in range(self.retry_attempts):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    # Load image from bytes
                    image = Image.open(BytesIO(response.content))
                    
                    # Save if output path specified
                    if output_file:
                        output_path = Path(output_file)
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        image.save(output_file)
                        logger.info(f"✅ Image saved to: {output_file}")
                    
                    return image
                
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    logger.warning(f"⏳ Model loading, retrying in 10s (attempt {attempt + 1}/{self.retry_attempts})")
                    time.sleep(10)
                    continue
                
                else:
                    # Try to get error message from JSON, fallback to text
                    try:
                        error_msg = response.json().get("error", response.text)
                    except:
                        error_msg = response.text or f"HTTP {response.status_code}"
                    raise RuntimeError(f"API Error ({response.status_code}): {error_msg}")
                    
            except requests.exceptions.Timeout:
                logger.warning(f"⏱️ Request timeout, retrying (attempt {attempt + 1}/{self.retry_attempts})")
                if attempt == self.retry_attempts - 1:
                    raise
                time.sleep(5)
                continue
                
            except Exception as e:
                logger.error(f"❌ Generation failed: {str(e)}")
                if attempt == self.retry_attempts - 1:
                    raise
                time.sleep(5)
                continue
        
        raise RuntimeError(f"Failed to generate image after {self.retry_attempts} attempts")
    
    def generate_batch(
        self,
        prompts: List[str],
        batch_size: int = 1,
        **kwargs
    ) -> List[Image.Image]:
        """
        Generate multiple images.
        
        Args:
            prompts: List of text prompts
            batch_size: Number of images to generate in parallel (currently limited to 1 by API)
            **kwargs: Additional arguments passed to generate()
            
        Returns:
            List of PIL Image objects
        """
        images = []
        
        for i, prompt in enumerate(prompts):
            logger.info(f"📊 Generating image {i+1}/{len(prompts)}")
            
            try:
                image = self.generate(prompt, **kwargs)
                images.append(image)
            except Exception as e:
                logger.error(f"❌ Failed to generate image {i+1}: {str(e)}")
                images.append(None)
        
        logger.info(f"✅ Generated {len([img for img in images if img])} out of {len(prompts)} images")
        return images
    
    def _create_placeholder(
        self,
        prompt: str,
        width: int,
        height: int,
        output_file: Optional[str] = None
    ) -> Image.Image:
        """Create a placeholder image when API is unavailable."""
        from PIL import ImageDraw, ImageFont
        
        # Create colored image based on prompt hash
        import hashlib
        prompt_hash = int(hashlib.md5(prompt.encode()).hexdigest()[:6], 16)
        colors = [
            (52, 152, 219),   # Blue
            (46, 204, 113),   # Green
            (155, 89, 182),   # Purple
            (241, 196, 15),   # Yellow
            (231, 76, 60),    # Red
            (26, 188, 156),   # Turquoise
        ]
        color = colors[prompt_hash % len(colors)]
        
        # Create image
        image = Image.new('RGB', (width, height), color)
        draw = ImageDraw.Draw(image)
        
        # Add text
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = f"Placeholder\n{prompt[:50]}"
        
        # Draw text with background
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Background rectangle
        padding = 20
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(0, 0, 0, 128)
        )
        
        # Text
        draw.text((x, y), text, fill='white', font=font)
        
        # Save if requested
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            image.save(output_file)
            logger.info(f"✅ Placeholder saved to: {output_file}")
        
        return image
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        return list(self.MODELS.keys())
    
    def estimate_cost(self, num_images: int) -> Dict[str, Any]:
        """
        Estimate cost for generating images (Free tier).
        
        Args:
            num_images: Number of images to generate
            
        Returns:
            Cost estimation dictionary
        """
        # HuggingFace Inference API is free with rate limits
        # Rate limits: ~1000 requests/hour on free tier
        
        return {
            "num_images": num_images,
            "estimated_time_seconds": num_images * 10,  # ~10s per image
            "cost_usd": 0.0,
            "rate_limit": "~1000 images/hour (free tier)",
            "note": "Unlimited with Pro subscription ($9/month)"
        }


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = ImageGenerator(model="sdxl")
    
    # Test prompts
    test_prompts = [
        "A premium coffee cup on marble surface, professional photography, 4K",
        "Modern laptop on wooden desk, minimalist setup, soft lighting",
        "Luxury watch on black background, studio photography, dramatic lighting"
    ]
    
    # Generate images
    for i, prompt in enumerate(test_prompts):
        try:
            image = generator.generate(
                prompt=prompt,
                style_preset="product",
                output_file=f"test_image_{i+1}.png"
            )
            print(f"✅ Generated: test_image_{i+1}.png")
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
