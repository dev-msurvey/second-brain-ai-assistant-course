"""
Example: Complete AI Director Pipeline
======================================

Demonstrates end-to-end content generation using all modules.

Usage:
    python example_full_pipeline.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add module paths
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
sys.path.insert(0, str(Path(__file__).parent.parent / "pipelines"))

from ai_director import AIDirector, DirectorConfig, Brief
from content_generation import ContentPipeline


async def main():
    """Run complete pipeline example."""
    print("\n" + "="*60)
    print("🎬 AI DIRECTOR: Complete Pipeline Example")
    print("="*60 + "\n")
    
    # Step 1: Configure
    print("📋 Step 1: Configuring AI Director...")
    
    config = DirectorConfig(
        mongodb_uri=os.getenv("MONGODB_URI"),
        mongodb_database="ai_director",
        mongodb_collection="brand_vectors",
        hf_token=os.getenv("HF_TOKEN"),
        image_model="sdxl",
        voice_language="thai",
        video_fps=30,
        scene_detection_method="content",
        remove_silence=True,
        output_dir="output/full_pipeline",
        temp_dir="temp",
        cache_enabled=False
    )
    
    print("✅ Configuration complete\n")
    
    # Step 2: Initialize Director
    print("📋 Step 2: Initializing AI Director...")
    
    director = AIDirector(config)
    pipeline = ContentPipeline(director)
    
    print("✅ Director initialized\n")
    
    # Step 3: Create Brief
    print("📋 Step 3: Creating content brief...")
    
    brief = Brief(
        brand="CoffeeLab Thailand",
        product="Cold Brew Premium",
        duration=15.0,
        platform="instagram",
        language="thai",
        tone="premium",
        additional_notes="Focus on quality and craftsmanship"
    )
    
    print(f"✅ Brief created:")
    print(f"   Brand: {brief.brand}")
    print(f"   Product: {brief.product}")
    print(f"   Duration: {brief.duration}s")
    print(f"   Platform: {brief.platform}\n")
    
    # Step 4: Generate Content
    print("📋 Step 4: Generating content...\n")
    
    result = await pipeline.process_brief(brief)
    
    # Step 5: Display Results
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETE!")
    print("="*60)
    print(f"\n📊 Results:")
    print(f"   Video: {result.video_path}")
    print(f"   Images: {len(result.images)} files")
    print(f"   Audio: {result.audio_path}")
    print(f"   Duration: {result.duration}s")
    print(f"   Processing Time: {result.metadata['processing_time']:.2f}s")
    
    print(f"\n🎯 Creative Strategy:")
    strategy = result.metadata["strategy"]
    print(f"   Concept: {strategy['concept']}")
    print(f"   Scenes: {len(strategy['visual_scenes'])} scenes")
    
    print(f"\n📝 Script Preview:")
    script_lines = strategy["script"].split("\n")[:3]
    for line in script_lines:
        if line.strip():
            print(f"   {line.strip()}")
    
    print(f"\n💾 Files:")
    for i, img in enumerate(result.images, 1):
        print(f"   Image {i}: {Path(img).name}")
    print(f"   Audio: {Path(result.audio_path).name}")
    print(f"   Video: {Path(result.video_path).name}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # Set environment variables (for testing)
    if not os.getenv("MONGODB_URI"):
        print("⚠️  Warning: MONGODB_URI not set")
        print("   Some features may not work")
    
    if not os.getenv("HF_TOKEN"):
        print("⚠️  Warning: HF_TOKEN not set")
        print("   Image generation may not work")
    
    # Run pipeline
    asyncio.run(main())
