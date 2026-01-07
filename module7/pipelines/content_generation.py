"""
Module 7: Content Generation Pipeline
=====================================

End-to-end content generation workflow.

Author: AI Director Team
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import asyncio
import json
from datetime import datetime
import sys

# Add module paths
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from ai_director import AIDirector, DirectorConfig, Brief, ContentOutput

logger = logging.getLogger(__name__)


class ContentPipeline:
    """
    Content generation pipeline orchestrator.
    
    Manages multi-brief batch processing and workflow optimization.
    """
    
    def __init__(self, director: AIDirector):
        """
        Initialize pipeline.
        
        Args:
            director: AI Director instance
        """
        self.director = director
        self.results: List[ContentOutput] = []
    
    async def process_brief(self, brief: Brief) -> ContentOutput:
        """
        Process single brief.
        
        Args:
            brief: Content brief
            
        Returns:
            Content output
        """
        logger.info(f"📝 Processing brief: {brief.brand} - {brief.product}")
        
        try:
            result = await self.director.create_content(brief)
            self.results.append(result)
            return result
            
        except Exception as e:
            logger.error(f"❌ Brief processing failed: {e}")
            raise
    
    async def process_batch(self, briefs: List[Brief], parallel: bool = False) -> List[ContentOutput]:
        """
        Process multiple briefs.
        
        Args:
            briefs: List of briefs
            parallel: Process in parallel (default: sequential)
            
        Returns:
            List of content outputs
        """
        logger.info(f"📋 Processing batch of {len(briefs)} briefs")
        logger.info(f"   Mode: {'Parallel' if parallel else 'Sequential'}")
        
        if parallel:
            # Process in parallel
            tasks = [self.process_brief(brief) for brief in briefs]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions
            outputs = [r for r in results if isinstance(r, ContentOutput)]
            errors = [r for r in results if isinstance(r, Exception)]
            
            if errors:
                logger.warning(f"⚠️  {len(errors)} briefs failed")
            
            return outputs
        else:
            # Process sequentially
            outputs = []
            for brief in briefs:
                try:
                    result = await self.process_brief(brief)
                    outputs.append(result)
                except Exception as e:
                    logger.error(f"❌ Brief failed: {e}")
            
            return outputs
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get pipeline statistics.
        
        Returns:
            Statistics dictionary
        """
        if not self.results:
            return {"total": 0}
        
        total_time = sum(r.metadata["processing_time"] for r in self.results)
        avg_time = total_time / len(self.results)
        
        return {
            "total_briefs": len(self.results),
            "total_processing_time": total_time,
            "average_processing_time": avg_time,
            "total_videos": len(self.results),
            "total_images": sum(len(r.images) for r in self.results),
            "platforms": list(set(r.metadata["brief"]["platform"] for r in self.results)),
            "brands": list(set(r.metadata["brief"]["brand"] for r in self.results))
        }
    
    def export_results(self, output_file: str):
        """
        Export results to JSON.
        
        Args:
            output_file: Output file path
        """
        data = {
            "statistics": self.get_statistics(),
            "results": [r.to_dict() for r in self.results],
            "timestamp": datetime.now().isoformat()
        }
        
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"💾 Results exported to {output_file}")


# Example usage
async def example_single_brief():
    """Example: Process single brief."""
    # Configure
    config = DirectorConfig(
        output_dir="output/pipeline_single"
    )
    
    # Initialize director
    director = AIDirector(config)
    pipeline = ContentPipeline(director)
    
    # Create brief
    brief = Brief(
        brand="CoffeeLab",
        product="Cold Brew",
        duration=15.0,
        platform="instagram"
    )
    
    # Process
    result = await pipeline.process_brief(brief)
    
    print(f"\n✅ Content created: {result.video_path}")


async def example_batch_processing():
    """Example: Process multiple briefs."""
    # Configure
    config = DirectorConfig(
        output_dir="output/pipeline_batch"
    )
    
    # Initialize director
    director = AIDirector(config)
    pipeline = ContentPipeline(director)
    
    # Create briefs
    briefs = [
        Brief(
            brand="CoffeeLab",
            product="Cold Brew",
            duration=15.0,
            platform="instagram"
        ),
        Brief(
            brand="TeaHouse",
            product="Matcha Latte",
            duration=30.0,
            platform="youtube"
        ),
        Brief(
            brand="JuiceBar",
            product="Green Smoothie",
            duration=10.0,
            platform="tiktok"
        )
    ]
    
    # Process batch (sequential)
    results = await pipeline.process_batch(briefs, parallel=False)
    
    # Get statistics
    stats = pipeline.get_statistics()
    
    print(f"\n✅ Batch processing complete:")
    print(f"   Total: {stats['total_briefs']} briefs")
    print(f"   Time: {stats['total_processing_time']:.2f}s")
    print(f"   Average: {stats['average_processing_time']:.2f}s per brief")
    
    # Export results
    pipeline.export_results("output/batch_results.json")


if __name__ == "__main__":
    # Run example
    asyncio.run(example_batch_processing())
