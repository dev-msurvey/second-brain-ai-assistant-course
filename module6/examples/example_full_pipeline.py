"""
Example: Full Pipeline
======================

Demonstrates end-to-end AI Director workflow:
1. Retrieve brand context from Vector RAG (Module 5)
2. Generate creative strategy with LLM (Module 4)
3. Generate images (Module 6)
4. Generate voiceover (Module 6)
5. Compose final video (Module 6)

Usage:
    python examples/example_full_pipeline.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.image_generator import ImageGenerator
from tools.voice_generator import VoiceGenerator
from tools.video_composer import VideoComposer


async def full_pipeline_demo():
    """
    Demonstrate full AI Director pipeline.
    
    Pipeline:
    1. Get brief: "Create a 15-second ad for CoffeeLab Cold Brew"
    2. Retrieve brand context (simulated - would use Module 5)
    3. Generate strategy (simulated - would use Module 4)
    4. Generate product image
    5. Generate voiceover
    6. Compose final video
    """
    print("\n" + "="*60)
    print("AI DIRECTOR: FULL PIPELINE DEMO")
    print("="*60)
    
    # Create output directory
    os.makedirs("output/pipeline", exist_ok=True)
    
    # ========================================
    # STEP 1: Brief
    # ========================================
    print("\n📋 STEP 1: BRIEF")
    print("-" * 60)
    
    brief = {
        "brand": "CoffeeLab",
        "product": "Cold Brew Premium",
        "duration": 15,
        "platform": "Instagram",
        "language": "Thai",
        "tone": "Premium, inviting"
    }
    
    print(f"Brand: {brief['brand']}")
    print(f"Product: {brief['product']}")
    print(f"Duration: {brief['duration']}s")
    print(f"Platform: {brief['platform']}")
    print(f"Language: {brief['language']}")
    
    # ========================================
    # STEP 2: Retrieve Brand Context (Module 5)
    # ========================================
    print("\n🔍 STEP 2: RETRIEVE BRAND CONTEXT")
    print("-" * 60)
    print("📌 [Simulated - Would use Module 5 Vector RAG]")
    
    brand_context = {
        "brand_name": "CoffeeLab",
        "target_audience": "Urban professionals, 25-35 years old",
        "brand_voice": "Premium yet approachable",
        "key_values": "Quality, Innovation, Experience",
        "visual_style": "Minimal, clean, professional"
    }
    
    print(f"Target: {brand_context['target_audience']}")
    print(f"Voice: {brand_context['brand_voice']}")
    print(f"Values: {brand_context['key_values']}")
    
    # ========================================
    # STEP 3: Generate Strategy (Module 4)
    # ========================================
    print("\n💡 STEP 3: GENERATE CREATIVE STRATEGY")
    print("-" * 60)
    print("📌 [Simulated - Would use Module 4 LLM]")
    
    strategy = {
        "concept": "Morning Ritual - Transform your morning with premium Cold Brew",
        "visual_scenes": [
            "Premium Cold Brew on marble surface, soft morning light",
            "Close-up of coffee being poured, professional product shot"
        ],
        "script_thai": """
        เริ่มต้นเช้าวันใหม่อย่างสดชื่น
        ด้วยกาแฟ Cold Brew Premium จาก CoffeeLab
        รสชาติกลมกล่อม หอมหวาน เหมาะกับทุกช่วงเวลา
        CoffeeLab - ประสบการณ์กาแฟที่แตกต่าง
        """,
        "music_mood": "Uplifting, gentle"
    }
    
    print(f"Concept: {strategy['concept']}")
    print(f"Scenes: {len(strategy['visual_scenes'])} scenes")
    print(f"Script: {len(strategy['script_thai'])} characters")
    
    # ========================================
    # STEP 4: Generate Images (Module 6)
    # ========================================
    print("\n🎨 STEP 4: GENERATE IMAGES")
    print("-" * 60)
    
    # Check for HF token
    if not os.getenv("HF_TOKEN"):
        print("⚠️  Skipping image generation (HF_TOKEN not set)")
        print("   Using placeholder images instead")
        
        # Create placeholder images
        from PIL import Image, ImageDraw, ImageFont
        
        for i, scene in enumerate(strategy['visual_scenes']):
            img = Image.new('RGB', (1080, 1080), color=(230, 230, 230))
            draw = ImageDraw.Draw(img)
            
            # Add text
            text = f"Scene {i+1}\n{scene[:40]}..."
            draw.text((100, 500), text, fill=(100, 100, 100))
            
            output_file = f"output/pipeline/scene_{i+1}.png"
            img.save(output_file)
            print(f"✅ Created placeholder: {output_file}")
        
        image_files = [
            "output/pipeline/scene_1.png",
            "output/pipeline/scene_2.png"
        ]
    else:
        # Generate real images
        image_generator = ImageGenerator(model="sdxl")
        image_files = []
        
        for i, scene in enumerate(strategy['visual_scenes']):
            print(f"\n🎨 Generating scene {i+1}/{len(strategy['visual_scenes'])}...")
            
            output_file = f"output/pipeline/scene_{i+1}.png"
            
            image = image_generator.generate(
                prompt=scene,
                style_preset="product",
                width=1080,
                height=1080,
                output_file=output_file
            )
            
            image_files.append(output_file)
            print(f"✅ Generated: {output_file}")
    
    # ========================================
    # STEP 5: Generate Voiceover (Module 6)
    # ========================================
    print("\n🎙️  STEP 5: GENERATE VOICEOVER")
    print("-" * 60)
    
    voice_generator = VoiceGenerator()
    
    voiceover_file = "output/pipeline/voiceover.mp3"
    subtitle_file = "output/pipeline/subtitles.srt"
    
    await voice_generator.generate_with_subtitles(
        text=strategy['script_thai'].strip(),
        voice="th-TH-NiwatNeural",
        rate="+0%",
        output_audio=voiceover_file,
        output_srt=subtitle_file
    )
    
    print(f"✅ Voiceover generated: {voiceover_file}")
    print(f"✅ Subtitles generated: {subtitle_file}")
    
    # ========================================
    # STEP 6: Compose Video (Module 6)
    # ========================================
    print("\n🎬 STEP 6: COMPOSE VIDEO")
    print("-" * 60)
    
    video_composer = VideoComposer()
    
    # Create ad video
    video = video_composer.create_ad(
        images=image_files,
        audio=voiceover_file,
        duration=15.0,
        title="CoffeeLab",
        style="minimal"
    )
    
    # Export video
    output_video = "output/pipeline/coffeelab_ad_15s.mp4"
    
    video_composer.export(
        video=video,
        output_file=output_video,
        fps=30,
        preset="medium"
    )
    
    print(f"✅ Video exported: {output_video}")
    
    # ========================================
    # SUMMARY
    # ========================================
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETED!")
    print("="*60)
    
    print("\n📊 DELIVERABLES:")
    print(f"   🎨 Images: {len(image_files)} files")
    for img in image_files:
        print(f"      - {img}")
    
    print(f"\n   🎙️  Audio:")
    print(f"      - {voiceover_file}")
    print(f"      - {subtitle_file}")
    
    print(f"\n   🎬 Video:")
    print(f"      - {output_video}")
    
    print("\n📈 PERFORMANCE:")
    print(f"   Duration: 15 seconds")
    print(f"   Resolution: 1080x1080 (Instagram)")
    print(f"   Format: MP4 (H.264 + AAC)")
    
    print("\n💰 COST:")
    print(f"   Total: $0.00 (Zero-cost stack!)")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Review generated content")
    print("   2. Make adjustments if needed")
    print("   3. Deploy to Instagram")
    print("   4. Track performance metrics")


async def main():
    """Run full pipeline demo."""
    try:
        await full_pipeline_demo()
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
