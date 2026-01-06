"""
Example: Multimodal Strategy Generation (Text + Image)
Shows how T5Gemma 2 can use reference images for strategy generation

Module 1: Dual-Model Architecture
AI Director v3.4 - NEW MULTIMODAL CAPABILITY
"""

import sys
from pathlib import Path
import importlib.util
from PIL import Image
import requests
from io import BytesIO

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Dynamic import
def import_module_by_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

thinker_mod = import_module_by_path("t5gemma_thinker", parent_dir / "01_t5gemma_thinker.py")
agent_mod = import_module_by_path("ai_director_agent", parent_dir / "03_ai_director_agent.py")

T5GemmaThinker = thinker_mod.T5GemmaThinker
AIDirectorAgent = agent_mod.AIDirectorAgent


def example_1_image_analysis():
    """Example 1: Analyze a reference image"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: IMAGE ANALYSIS (Multimodal)")
    print("=" * 70)
    print()
    
    # Initialize thinker
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    # Load sample image from Unsplash
    print("📥 Loading sample coffee product image...")
    image_url = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400"
    
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        print(f"✅ Image loaded: {image.size}")
        print()
        
        # Analyze different aspects
        tasks = [
            ("describe", "General Description"),
            ("brand_analysis", "Brand Analysis"),
            ("composition", "Photo Composition"),
            ("mood", "Mood & Atmosphere")
        ]
        
        for task, title in tasks:
            print("-" * 70)
            print(f"🔍 {title}:")
            print("-" * 70)
            
            analysis = thinker.analyze_image(image, task=task)
            print(analysis)
            print()
        
        print("=" * 70)
        print("✅ Image Analysis Complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️  Make sure you have internet connection to load sample image")


def example_2_strategy_with_image():
    """Example 2: Generate strategy using reference image"""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 2: STRATEGY WITH REFERENCE IMAGE")
    print("=" * 70)
    print()
    
    # Initialize thinker
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    # Load image
    print("📥 Loading reference image...")
    image_url = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400"
    
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        print(f"✅ Image loaded: {image.size}")
        print()
        
        # Create brief
        brief = """
        Product: CoffeeLab Cold Brew Premium
        Platform: Instagram Reel (15 seconds)
        Target: Young professionals 25-35 years old
        Goal: Launch new product, highlight premium quality
        
        Please use the reference image to inform your strategy
        for visual style, color palette, and mood.
        """
        
        print("📝 Brief:")
        print(brief)
        print()
        
        print("-" * 70)
        print("🧠 Generating strategy with image context...")
        print("-" * 70)
        print()
        
        # Generate with image
        strategy = thinker.generate_strategy(
            brief=brief,
            reference_image=image
        )
        
        print("✅ Strategy Generated (using reference image):")
        print(strategy)
        print()
        
        print("=" * 70)
        print("✅ Strategy Generation Complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️  Make sure you have internet connection")


def example_3_full_agent_with_image():
    """Example 3: Complete AI Director workflow with image"""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 3: FULL AI DIRECTOR WITH MULTIMODAL INPUT")
    print("=" * 70)
    print()
    
    # Initialize agent
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=True)
    
    # Load image
    print("\n📥 Loading reference image...")
    image_url = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400"
    
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        print(f"✅ Image loaded: {image.size}")
        
        # Process brief with image
        brief = """
        Product: CoffeeLab Cold Brew Premium
        Platform: Instagram Reel (15 seconds)
        Target: Young professionals
        
        Use the reference image for:
        - Visual style inspiration
        - Color palette guidance
        - Overall mood and aesthetic
        """
        
        result = agent.process_brief(
            brief=brief,
            reference_image=image
        )
        
        print("\n\n📊 FINAL RESULT:")
        print("=" * 70)
        print(f"✅ Strategy generated: {len(result['strategy'])} characters")
        print(f"✅ Tool calls parsed: {len(result['tool_calls'])}")
        print(f"✅ Has reference image: {result['has_reference_image']}")
        print(f"⏱️  Duration: {result['duration_seconds']:.2f}s")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️  Make sure you have internet connection")


def example_4_comparison():
    """Example 4: Compare text-only vs text+image"""
    print("\n\n" + "=" * 70)
    print("EXAMPLE 4: COMPARISON - TEXT ONLY vs TEXT + IMAGE")
    print("=" * 70)
    print()
    
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    brief = "Create Instagram Reel for CoffeeLab Cold Brew - premium coffee product"
    
    # Test 1: Text only
    print("📝 TEST 1: Text-Only Strategy")
    print("-" * 70)
    strategy_text_only = thinker.generate_strategy(brief)
    print(f"Result length: {len(strategy_text_only)} characters")
    print(f"Preview: {strategy_text_only[:200]}...")
    print()
    
    # Test 2: Text + Image
    print("📝 TEST 2: Text + Image Strategy")
    print("-" * 70)
    
    try:
        print("Loading reference image...")
        image_url = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400"
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        
        strategy_with_image = thinker.generate_strategy(
            brief=brief,
            reference_image=image
        )
        
        print(f"Result length: {len(strategy_with_image)} characters")
        print(f"Preview: {strategy_with_image[:200]}...")
        print()
        
        print("=" * 70)
        print("📊 COMPARISON SUMMARY:")
        print("=" * 70)
        print(f"Text-only: {len(strategy_text_only)} chars")
        print(f"Text+Image: {len(strategy_with_image)} chars")
        print(f"Difference: {len(strategy_with_image) - len(strategy_text_only):+d} chars")
        print()
        print("✅ Text+Image strategy should have more visual detail!")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️  Skipping image test")


if __name__ == "__main__":
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 10 + "🖼️  T5GEMMA 2 MULTIMODAL EXAMPLES" + " " * 23 + "║")
    print("║" + " " * 10 + "NEW: Text + Image Input Support" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    
    print("\n⚠️  NOTE: These examples require internet connection")
    print("           to load sample images from Unsplash")
    print()
    
    # Run all examples
    try:
        example_1_image_analysis()
        example_2_strategy_with_image()
        example_3_full_agent_with_image()
        example_4_comparison()
        
        print("\n\n" + "=" * 70)
        print("🎉 ALL MULTIMODAL EXAMPLES COMPLETE!")
        print("=" * 70)
        print("\n💡 TIP: You can now pass PIL.Image objects to:")
        print("   - thinker.generate_strategy(brief, reference_image=img)")
        print("   - thinker.analyze_image(img, task='brand_analysis')")
        print("   - agent.process_brief(brief, reference_image=img)")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⏸️  Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("⚠️  Some examples may have failed")
