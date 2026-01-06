"""
Example: Image Generation
=========================

Demonstrates how to generate images using HuggingFace Inference API.

Features demonstrated:
- Single image generation
- Batch generation
- Style presets
- Different models (SDXL, Flux)

Usage:
    python examples/example_image_generation.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.image_generator import ImageGenerator


def example_single_image():
    """Generate a single image."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Image Generation")
    print("="*60)
    
    # Initialize generator
    generator = ImageGenerator(model="sdxl")
    
    # Generate product image
    prompt = "A premium coffee cup on white marble surface, professional product photography, soft lighting, 4K, high quality"
    
    image = generator.generate(
        prompt=prompt,
        negative_prompt="blurry, low quality, watermark, text",
        width=1024,
        height=1024,
        style_preset="product",
        output_file="output/coffee_product.png"
    )
    
    print(f"\n✅ Image generated: output/coffee_product.png")
    print(f"   Size: {image.size}")
    print(f"   Mode: {image.mode}")


def example_batch_generation():
    """Generate multiple images."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Batch Image Generation")
    print("="*60)
    
    generator = ImageGenerator(model="sdxl")
    
    # Define prompts for different scenes
    prompts = [
        "Morning coffee on wooden table, sunrise lighting, cozy atmosphere",
        "Iced coffee with ice cubes, studio photography, dark background",
        "Coffee beans scattered on black surface, macro photography, dramatic lighting"
    ]
    
    # Generate all images
    images = generator.generate_batch(
        prompts=prompts,
        style_preset="product",
        width=1024,
        height=1024
    )
    
    # Save images
    for i, image in enumerate(images):
        if image:
            output_file = f"output/coffee_scene_{i+1}.png"
            image.save(output_file)
            print(f"✅ Saved: {output_file}")


def example_different_styles():
    """Generate images with different style presets."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Different Style Presets")
    print("="*60)
    
    generator = ImageGenerator(model="sdxl")
    
    base_prompt = "A coffee shop interior"
    
    # Test different styles
    styles = ["minimal", "cinematic", "realistic"]
    
    for style in styles:
        print(f"\n🎨 Generating {style} style...")
        
        image = generator.generate(
            prompt=base_prompt,
            style_preset=style,
            width=1024,
            height=1024,
            output_file=f"output/coffee_shop_{style}.png"
        )
        
        print(f"✅ Saved: output/coffee_shop_{style}.png")


def example_flux_model():
    """Generate images using Flux model."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Flux Model Generation")
    print("="*60)
    
    # Initialize with Flux Schnell (faster)
    generator = ImageGenerator(model="flux-schnell")
    
    prompt = "A beautiful latte art in a white ceramic cup, top view, professional cafe"
    
    image = generator.generate(
        prompt=prompt,
        width=1024,
        height=1024,
        output_file="output/latte_art_flux.png"
    )
    
    print(f"✅ Image generated with Flux: output/latte_art_flux.png")


def example_cost_estimation():
    """Estimate cost for image generation."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Cost Estimation")
    print("="*60)
    
    generator = ImageGenerator(model="sdxl")
    
    # Estimate cost for 100 images
    estimation = generator.estimate_cost(num_images=100)
    
    print("\n📊 Cost Estimation:")
    print(f"   Images: {estimation['num_images']}")
    print(f"   Estimated Time: {estimation['estimated_time_seconds']}s (~{estimation['estimated_time_seconds']/60:.1f} minutes)")
    print(f"   Cost: ${estimation['cost_usd']:.2f}")
    print(f"   Rate Limit: {estimation['rate_limit']}")
    print(f"   Note: {estimation['note']}")


def main():
    """Run all examples."""
    # Create output directory
    os.makedirs("output", exist_ok=True)
    
    print("\n" + "="*60)
    print("MODULE 6: IMAGE GENERATION EXAMPLES")
    print("="*60)
    
    # Check for API token
    if not os.getenv("HF_TOKEN"):
        print("\n❌ Error: HF_TOKEN environment variable not set")
        print("   Please set your HuggingFace API token:")
        print("   export HF_TOKEN='your_token_here'")
        print("\n   Get your token from: https://huggingface.co/settings/tokens")
        return
    
    try:
        # Run examples
        example_single_image()
        # example_batch_generation()  # Uncomment to run
        # example_different_styles()  # Uncomment to run
        # example_flux_model()        # Uncomment to run
        example_cost_estimation()
        
        print("\n" + "="*60)
        print("✅ ALL EXAMPLES COMPLETED!")
        print("="*60)
        print("\nGenerated files saved in: output/")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
