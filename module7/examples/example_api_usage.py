"""
Example: API Client Usage
=========================

Demonstrates how to use the AI Director API.

Usage:
    # Start API server first:
    python -m module7.api.main
    
    # Then run this example:
    python example_api_usage.py
"""

import requests
import json
import time
from pathlib import Path


# API Configuration
API_BASE_URL = "http://localhost:8000"
API_VERSION = "v1"


class AIDirectorClient:
    """Client for AI Director API."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        """
        Initialize client.
        
        Args:
            base_url: API base URL
        """
        self.base_url = base_url
        self.api_url = f"{base_url}/api/{API_VERSION}"
    
    def health_check(self) -> dict:
        """Check API health."""
        response = requests.get(f"{self.api_url}/health")
        response.raise_for_status()
        return response.json()
    
    def generate_content(
        self,
        brand: str,
        product: str,
        duration: float,
        platform: str,
        language: str = "thai",
        tone: str = "professional"
    ) -> dict:
        """
        Generate complete content.
        
        Args:
            brand: Brand name
            product: Product name
            duration: Duration in seconds
            platform: Platform name
            language: Content language
            tone: Content tone
            
        Returns:
            Content generation result
        """
        payload = {
            "brand": brand,
            "product": product,
            "duration": duration,
            "platform": platform,
            "language": language,
            "tone": tone
        }
        
        response = requests.post(
            f"{self.api_url}/generate",
            json=payload,
            timeout=300  # 5 minutes
        )
        response.raise_for_status()
        return response.json()
    
    def search_rag(self, query: str, top_k: int = 3) -> dict:
        """
        Search brand context.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            Search results
        """
        payload = {
            "query": query,
            "top_k": top_k
        }
        
        response = requests.post(
            f"{self.api_url}/rag/search",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def generate_image(
        self,
        prompt: str,
        style: str = "product",
        width: int = 1024,
        height: int = 1024
    ) -> dict:
        """
        Generate image.
        
        Args:
            prompt: Image prompt
            style: Style preset
            width: Image width
            height: Image height
            
        Returns:
            Image generation result
        """
        payload = {
            "prompt": prompt,
            "style": style,
            "width": width,
            "height": height
        }
        
        response = requests.post(
            f"{self.api_url}/media/image",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    def generate_voice(
        self,
        text: str,
        voice: str = "th-TH-NiwatNeural",
        rate: str = "+0%"
    ) -> dict:
        """
        Generate voice.
        
        Args:
            text: Text to speak
            voice: Voice ID
            rate: Speech rate
            
        Returns:
            Voice generation result
        """
        payload = {
            "text": text,
            "voice": voice,
            "rate": rate
        }
        
        response = requests.post(
            f"{self.api_url}/media/voice",
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()
    
    def smart_cut(
        self,
        video_path: str,
        remove_silence: bool = True,
        target_duration: float = None
    ) -> dict:
        """
        Apply smart editing.
        
        Args:
            video_path: Input video path
            remove_silence: Remove silent parts
            target_duration: Target duration
            
        Returns:
            Smart cut result
        """
        payload = {
            "video_path": video_path,
            "remove_silence": remove_silence,
            "target_duration": target_duration
        }
        
        response = requests.post(
            f"{self.api_url}/edit/smart-cut",
            json=payload,
            timeout=300
        )
        response.raise_for_status()
        return response.json()
    
    def download_file(
        self,
        file_type: str,
        filename: str,
        output_path: str
    ):
        """
        Download file.
        
        Args:
            file_type: File type (video, image, audio)
            filename: File name
            output_path: Local output path
        """
        response = requests.get(
            f"{self.api_url}/download/{file_type}/{filename}",
            stream=True
        )
        response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


def example_health_check():
    """Example: Health check."""
    print("\n" + "="*60)
    print("🏥 Health Check Example")
    print("="*60 + "\n")
    
    client = AIDirectorClient()
    
    try:
        health = client.health_check()
        
        print(f"Status: {health['status']}")
        print(f"Version: {health['version']}")
        print(f"\nModules:")
        for module, available in health['modules'].items():
            status = "✅" if available else "❌"
            print(f"  {status} {module}")
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")


def example_full_pipeline():
    """Example: Full content generation."""
    print("\n" + "="*60)
    print("🎬 Full Pipeline Example")
    print("="*60 + "\n")
    
    client = AIDirectorClient()
    
    try:
        print("📋 Generating content...")
        start_time = time.time()
        
        result = client.generate_content(
            brand="CoffeeLab",
            product="Cold Brew Premium",
            duration=15.0,
            platform="instagram",
            language="thai",
            tone="premium"
        )
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Content generated in {elapsed:.2f}s")
        print(f"\nResults:")
        print(f"  Video: {result['video_path']}")
        print(f"  Images: {len(result['images'])} files")
        print(f"  Audio: {result['audio_path']}")
        print(f"  Duration: {result['duration']}s")
        print(f"  Processing: {result['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")


def example_rag_search():
    """Example: RAG search."""
    print("\n" + "="*60)
    print("🔍 RAG Search Example")
    print("="*60 + "\n")
    
    client = AIDirectorClient()
    
    try:
        results = client.search_rag(
            query="CoffeeLab brand guidelines",
            top_k=3
        )
        
        print(f"Query: {results['query']}")
        print(f"Found: {results['count']} results\n")
        
        for i, doc in enumerate(results['results'], 1):
            print(f"{i}. Score: {doc.get('score', 'N/A')}")
            print(f"   {doc.get('content', '')[:100]}...")
            print()
        
    except Exception as e:
        print(f"❌ Search failed: {e}")


def example_image_generation():
    """Example: Image generation."""
    print("\n" + "="*60)
    print("🎨 Image Generation Example")
    print("="*60 + "\n")
    
    client = AIDirectorClient()
    
    try:
        print("📋 Generating image...")
        
        result = client.generate_image(
            prompt="Premium cold brew coffee, professional product photography",
            style="product",
            width=1024,
            height=1024
        )
        
        print(f"\n✅ Image generated:")
        print(f"  Path: {result['image_path']}")
        print(f"  Size: {result['size']}")
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")


def example_voice_generation():
    """Example: Voice generation."""
    print("\n" + "="*60)
    print("🎙️  Voice Generation Example")
    print("="*60 + "\n")
    
    client = AIDirectorClient()
    
    try:
        print("📋 Generating voice...")
        
        result = client.generate_voice(
            text="สวัสดีครับ วันนี้เรามาแนะนำ Cold Brew Premium จาก CoffeeLab",
            voice="th-TH-NiwatNeural",
            rate="+0%"
        )
        
        print(f"\n✅ Voice generated:")
        print(f"  Path: {result['audio_path']}")
        print(f"  Voice: {result['voice']}")
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")


if __name__ == "__main__":
    print("\n🚀 AI Director API Client Examples\n")
    
    # Run examples
    example_health_check()
    
    # Uncomment to run other examples:
    # example_rag_search()
    # example_image_generation()
    # example_voice_generation()
    # example_full_pipeline()
    
    print("\n" + "="*60)
    print("✅ Examples complete")
    print("="*60 + "\n")
