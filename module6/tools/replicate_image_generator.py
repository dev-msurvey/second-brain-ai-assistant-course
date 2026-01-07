"""
Replicate API Image Generator
==============================

Alternative image generator using Replicate API (with free tier support).
Uses Stable Diffusion XL for high-quality image generation.

Author: AI Director Team
License: MIT
"""

import logging
import os
from typing import Optional, List, Dict, Any
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO

logger = logging.getLogger(__name__)


class ReplicateImageGenerator:
    """Generate images using Replicate API."""
    
    # Available models on Replicate
    MODELS = {
        "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
        "sdxl-lightning": "bytedance/sdxl-lightning-4step:5599ed30703defd1d160a25a63321b4dec97101d98b4674bcc56e41f62f35637",
    }
    
    def __init__(
        self,
        model: str = "sdxl",
        api_token: Optional[str] = None
    ):
        """
        Initialize Replicate image generator.
        
        Args:
            model: Model identifier (sdxl, sdxl-lightning)
            api_token: Replicate API token (or set REPLICATE_API_TOKEN env var)
        """
        self.model = model
        self.model_id = self.MODELS.get(model, self.MODELS["sdxl"])
        
        # Get API token
        self.api_token = api_token or os.environ.get("REPLICATE_API_TOKEN")
        
        if not self.api_token:
            logger.warning("⚠️  No Replicate API token found - will use placeholder generation")
            logger.info("💡 Get free token at: https://replicate.com/account/api-tokens")
            self.api_token = None
        else:
            logger.info(f"✅ ReplicateImageGenerator initialized with model: {model}")
    
    def generate(
        self,
        prompt: str,
        negative_prompt: str = "ugly, deformed, low quality, blurry",
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        output_file: Optional[str] = None
    ) -> Image.Image:
        """
        Generate a single image.
        
        Args:
            prompt: Text prompt describing the image
            negative_prompt: What to avoid in the image
            width: Image width in pixels
            height: Image height in pixels
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt
            output_file: Optional path to save the image
            
        Returns:
            PIL Image object
        """
        logger.info(f"🎨 Generating image: {prompt[:50]}...")
        
        # If no API token, use placeholder
        if not self.api_token:
            logger.warning("⚠️  Using placeholder image (no Replicate API token)")
            return self._create_placeholder(prompt, width, height, output_file)
        
        try:
            import replicate
            
            # Run prediction
            output = replicate.run(
                self.model_id,
                input={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "width": width,
                    "height": height,
                    "num_inference_steps": num_inference_steps,
                    "guidance_scale": guidance_scale,
                }
            )
            
            # Output is a list of URLs
            if isinstance(output, list) and len(output) > 0:
                image_url = output[0]
            else:
                image_url = output
            
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            
            # Save if requested
            if output_file:
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(output_file)
                logger.info(f"✅ Image saved to: {output_file}")
            
            return image
            
        except Exception as e:
            logger.error(f"❌ Replicate generation failed: {e}")
            logger.warning("⚠️  Falling back to placeholder")
            return self._create_placeholder(prompt, width, height, output_file)
    
    def generate_batch(
        self,
        prompts: List[str],
        **kwargs
    ) -> List[Image.Image]:
        """
        Generate multiple images.
        
        Args:
            prompts: List of text prompts
            **kwargs: Additional arguments passed to generate()
            
        Returns:
            List of PIL Image objects
        """
        images = []
        
        logger.info(f"🎨 Generating {len(prompts)} images...")
        
        for i, prompt in enumerate(prompts, 1):
            logger.info(f"   Image {i}/{len(prompts)}")
            
            try:
                image = self.generate(prompt, **kwargs)
                images.append(image)
            except Exception as e:
                logger.error(f"❌ Failed to generate image {i}: {str(e)}")
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
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            font = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Title
        title = "Placeholder Image"
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 - 100
        
        # Background for better readability
        padding = 30
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + 100 + padding],
            fill=(0, 0, 0, 200)
        )
        
        # Draw text
        draw.text((x, y), title, fill='white', font=font)
        
        # Prompt preview
        prompt_preview = prompt[:80] + "..." if len(prompt) > 80 else prompt
        draw.text((x, y + 60), prompt_preview, fill='white', font=font_small)
        
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


# Example usage
if __name__ == "__main__":
    # Initialize generator
    generator = ReplicateImageGenerator(model="sdxl")
    
    # Test prompt
    prompt = "A futuristic flying car soaring through clouds, sleek design, photorealistic, 8k"
    
    try:
        image = generator.generate(
            prompt=prompt,
            width=1024,
            height=1024,
            output_file="test_flying_car.png"
        )
        print("✅ Generated test image")
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
