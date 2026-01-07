"""
Example: Batch Production
=========================

Demonstrates batch processing of multiple content briefs.

Usage:
    python example_batch_production.py
"""

import asyncio
import json
from pathlib import Path
import sys

# Add module paths
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))
sys.path.insert(0, str(Path(__file__).parent.parent / "pipelines"))

from ai_director import AIDirector, DirectorConfig, Brief
from content_generation import ContentPipeline


# Sample briefs
SAMPLE_BRIEFS = [
    {
        "brand": "CoffeeLab",
        "product": "Cold Brew Premium",
        "duration": 15.0,
        "platform": "instagram",
        "language": "thai",
        "tone": "premium"
    },
    {
        "brand": "CoffeeLab",
        "product": "Espresso Blend",
        "duration": 30.0,
        "platform": "youtube",
        "language": "thai",
        "tone": "professional"
    },
    {
        "brand": "TeaHouse",
        "product": "Matcha Latte",
        "duration": 10.0,
        "platform": "tiktok",
        "language": "thai",
        "tone": "casual"
    },
    {
        "brand": "JuiceBar",
        "product": "Green Smoothie",
        "duration": 15.0,
        "platform": "instagram",
        "language": "thai",
        "tone": "healthy"
    },
    {
        "brand": "BakeryShop",
        "product": "Sourdough Bread",
        "duration": 20.0,
        "platform": "youtube",
        "language": "thai",
        "tone": "artisanal"
    }
]


async def main():
    """Run batch production example."""
    print("\n" + "="*60)
    print("📦 AI DIRECTOR: Batch Production Example")
    print("="*60 + "\n")
    
    # Step 1: Configure
    print("📋 Step 1: Configuring AI Director...")
    
    config = DirectorConfig(
        output_dir="output/batch_production",
        temp_dir="temp/batch",
        cache_enabled=False
    )
    
    print("✅ Configuration complete\n")
    
    # Step 2: Initialize
    print("📋 Step 2: Initializing AI Director...")
    
    director = AIDirector(config)
    pipeline = ContentPipeline(director)
    
    print("✅ Director initialized\n")
    
    # Step 3: Load Briefs
    print("📋 Step 3: Loading briefs...")
    
    briefs = [Brief(**b) for b in SAMPLE_BRIEFS]
    
    print(f"✅ Loaded {len(briefs)} briefs:")
    for i, brief in enumerate(briefs, 1):
        print(f"   {i}. {brief.brand} - {brief.product} ({brief.duration}s, {brief.platform})")
    print()
    
    # Step 4: Process Batch
    print("📋 Step 4: Processing batch...")
    print("   Mode: Sequential (safer for limited resources)\n")
    
    results = await pipeline.process_batch(briefs, parallel=False)
    
    # Step 5: Display Results
    print("\n" + "="*60)
    print("✅ BATCH PROCESSING COMPLETE!")
    print("="*60)
    
    stats = pipeline.get_statistics()
    
    print(f"\n📊 Statistics:")
    print(f"   Total Briefs: {stats['total_briefs']}")
    print(f"   Successful: {len(results)}")
    print(f"   Failed: {stats['total_briefs'] - len(results)}")
    print(f"   Total Time: {stats['total_processing_time']:.2f}s")
    print(f"   Average Time: {stats['average_processing_time']:.2f}s per brief")
    print(f"   Total Videos: {stats['total_videos']}")
    print(f"   Total Images: {stats['total_images']}")
    
    print(f"\n📱 Platforms:")
    for platform in stats['platforms']:
        count = sum(1 for r in results if r.metadata['brief']['platform'] == platform)
        print(f"   {platform}: {count} videos")
    
    print(f"\n🏢 Brands:")
    for brand in stats['brands']:
        count = sum(1 for r in results if r.metadata['brief']['brand'] == brand)
        print(f"   {brand}: {count} videos")
    
    print(f"\n💾 Output Files:")
    for i, result in enumerate(results, 1):
        brief_data = result.metadata['brief']
        print(f"\n   {i}. {brief_data['brand']} - {brief_data['product']}")
        print(f"      Video: {Path(result.video_path).name}")
        print(f"      Images: {len(result.images)} files")
        print(f"      Duration: {result.duration}s")
        print(f"      Time: {result.metadata['processing_time']:.2f}s")
    
    # Step 6: Export Results
    print(f"\n📋 Step 6: Exporting results...")
    
    output_file = "output/batch_production/batch_results.json"
    pipeline.export_results(output_file)
    
    print(f"✅ Results exported to {output_file}")
    
    print("\n" + "="*60 + "\n")


async def example_parallel_processing():
    """Example: Parallel batch processing (faster but resource-intensive)."""
    print("\n" + "="*60)
    print("⚡ Parallel Processing Example")
    print("="*60 + "\n")
    
    config = DirectorConfig(
        output_dir="output/batch_parallel",
        temp_dir="temp/parallel"
    )
    
    director = AIDirector(config)
    pipeline = ContentPipeline(director)
    
    # Use smaller batch for parallel processing
    briefs = [Brief(**b) for b in SAMPLE_BRIEFS[:3]]
    
    print(f"📋 Processing {len(briefs)} briefs in parallel...\n")
    
    results = await pipeline.process_batch(briefs, parallel=True)
    
    stats = pipeline.get_statistics()
    
    print(f"\n✅ Parallel processing complete:")
    print(f"   Total Time: {stats['total_processing_time']:.2f}s")
    print(f"   Average Time: {stats['average_processing_time']:.2f}s per brief")
    print(f"   Speedup: ~{len(briefs)}x (theoretical)")


def load_briefs_from_file(file_path: str) -> list[Brief]:
    """
    Load briefs from JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        List of Brief objects
    """
    with open(file_path, "r") as f:
        data = json.load(f)
    
    return [Brief(**b) for b in data]


if __name__ == "__main__":
    # Run sequential batch processing
    asyncio.run(main())
    
    # Uncomment to run parallel processing:
    # asyncio.run(example_parallel_processing())
