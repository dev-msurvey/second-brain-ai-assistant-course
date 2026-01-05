"""
Example: Strategy Generation with T5Gemma 2

This example shows how to use T5Gemma 2 for:
- Marketing strategy generation
- Image prompt creation
- Voice script writing

Module 1: Dual-Model Architecture Design
"""

import sys
sys.path.append('..')

from t5gemma_thinker import T5GemmaThinker


def example_marketing_strategy():
    """Generate complete marketing strategy from brief"""
    print("=" * 70)
    print("📝 EXAMPLE 1: Marketing Strategy Generation")
    print("=" * 70)
    print()
    
    # Initialize thinker
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    # Marketing brief
    brief = """
    Brand: TechStart - Startup Accelerator
    Campaign: Launch Event Announcement
    Target: Entrepreneurs & Investors
    Platform: LinkedIn + Email
    Goal: Register 500+ attendees
    Style: Professional, inspiring, innovative
    """
    
    brand_context = """
    TechStart helps startups scale faster.
    We provide mentorship, funding, and connections.
    Our values: Innovation, Collaboration, Impact
    Tone: Professional but approachable
    Colors: Blue (#0066CC), Orange (#FF6B35)
    """
    
    print("📋 Brief:")
    print(brief)
    print()
    print("🏢 Brand Context:")
    print(brand_context)
    print()
    print("⏳ Generating strategy...")
    print()
    
    # Generate strategy
    strategy = thinker.generate_strategy(
        brief=brief,
        brand_context=brand_context,
        max_length=600,
        temperature=0.7
    )
    
    print("✅ Generated Strategy:")
    print("-" * 70)
    print(strategy)
    print("-" * 70)
    print()


def example_image_prompt():
    """Generate SDXL prompt for product photography"""
    print("=" * 70)
    print("📸 EXAMPLE 2: Image Prompt Generation")
    print("=" * 70)
    print()
    
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    # Different scenarios
    scenarios = [
        {
            "brief": "Premium coffee beans in glass jar",
            "style": "minimal",
            "aspect_ratio": "1:1"
        },
        {
            "brief": "Modern office workspace with laptop and coffee",
            "style": "cinematic",
            "aspect_ratio": "16:9"
        },
        {
            "brief": "Young entrepreneur presenting at tech conference",
            "style": "realistic",
            "aspect_ratio": "9:16"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📷 Scenario {i}:")
        print(f"   Brief: {scenario['brief']}")
        print(f"   Style: {scenario['style']}")
        print(f"   Ratio: {scenario['aspect_ratio']}")
        print()
        
        prompt = thinker.generate_image_prompt(
            brief=scenario['brief'],
            style=scenario['style'],
            aspect_ratio=scenario['aspect_ratio']
        )
        
        print(f"✅ SDXL Prompt:")
        print(f"   {prompt}")
        print()


def example_voice_script():
    """Generate voiceover scripts for different durations"""
    print("=" * 70)
    print("🎤 EXAMPLE 3: Voice Script Generation")
    print("=" * 70)
    print()
    
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    # Different video formats
    formats = [
        {
            "concept": "TechStart helps startups grow faster with mentorship and funding",
            "duration": 15,
            "tone": "excited",
            "language": "Thai"
        },
        {
            "concept": "Join our launch event - meet investors, learn from experts",
            "duration": 30,
            "tone": "professional",
            "language": "Thai"
        },
        {
            "concept": "Success stories from TechStart alumni startups",
            "duration": 60,
            "tone": "inspiring",
            "language": "Thai"
        }
    ]
    
    for i, format_spec in enumerate(formats, 1):
        print(f"\n🎬 Format {i}: {format_spec['duration']}s {format_spec['tone']} video")
        print(f"   Concept: {format_spec['concept']}")
        print()
        
        script = thinker.generate_voice_script(
            concept=format_spec['concept'],
            duration=format_spec['duration'],
            tone=format_spec['tone'],
            language=format_spec['language']
        )
        
        print(f"✅ Voice Script ({format_spec['language']}):")
        print(f"{script}")
        print()


def example_combined_workflow():
    """Complete workflow: Strategy → Image → Voice"""
    print("=" * 70)
    print("🎬 EXAMPLE 4: Complete Content Creation Workflow")
    print("=" * 70)
    print()
    
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    # Step 1: Generate strategy
    print("STEP 1: Generate Strategy")
    print("-" * 70)
    
    brief = """
    Product: EcoBottle - Sustainable Water Bottle
    Platform: Instagram Reel (15s)
    Target: Environment-conscious millennials
    Message: Reduce plastic waste while staying hydrated
    """
    
    strategy = thinker.generate_strategy(brief, max_length=300)
    print(f"Strategy:\n{strategy}\n")
    
    # Step 2: Generate image prompt
    print("STEP 2: Generate Image Prompt")
    print("-" * 70)
    
    image_prompt = thinker.generate_image_prompt(
        brief="Eco-friendly water bottle in nature setting",
        style="realistic",
        aspect_ratio="9:16"
    )
    print(f"Image Prompt:\n{image_prompt}\n")
    
    # Step 3: Generate voice script
    print("STEP 3: Generate Voice Script")
    print("-" * 70)
    
    voice_script = thinker.generate_voice_script(
        concept="EcoBottle keeps you hydrated while saving the planet",
        duration=15,
        tone="friendly",
        language="Thai"
    )
    print(f"Voice Script:\n{voice_script}\n")
    
    print("=" * 70)
    print("✅ Complete workflow finished!")
    print("   Next: Pass to FunctionGemma for tool calling")
    print("=" * 70)


if __name__ == "__main__":
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "🧠 T5GEMMA 2 STRATEGY EXAMPLES" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    # Run examples
    example_marketing_strategy()
    example_image_prompt()
    example_voice_script()
    example_combined_workflow()
    
    print("\n🎉 All examples completed!\n")
