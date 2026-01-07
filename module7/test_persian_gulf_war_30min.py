#!/usr/bin/env python3
"""
Test AI Director: Persian Gulf War Documentary - 30 Minutes
วิดีโอสารคดีเรื่อง สงครามอ่าวเปอร์เซีย ความยาว 30 นาที
"""

import asyncio
import os
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "module6" / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

from core.ai_director import AIDirector, Brief, DirectorConfig

async def main():
    print("=" * 80)
    print("🎬 AI DIRECTOR: PERSIAN GULF WAR DOCUMENTARY - 30 MINUTES")
    print("=" * 80)
    
    # Output directory
    output_dir = Path(__file__).parent / "output" / "persian_gulf_war_30min"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Brief: Persian Gulf War Documentary
    brief = Brief(
        brand="History Documentary Series",
        product="สงครามอ่าวเปอร์เซีย: สารคดีประวัติศาสตร์ (1990-1991)",
        duration=1800,  # 30 minutes
        platform="youtube",
        language="th",
        tone="สารคดีประวัติศาสตร์ให้ความรู้อย่างเป็นกลาง มีข้อมูลที่ตรวจสอบได้ น้ำเสียงจริงจัง มีน้ำหนัก",
        additional_notes="สงครามอ่าวเปอร์เซียเป็นเหตุการณ์สำคัญในประวัติศาสตร์โลกสมัยใหม่ ครอบคลุมการรุกรานคูเวตของอิรัก การตอบโต้ของสหประชาชาติ Operation Desert Storm และผลกระทบต่อภูมิภาคตะวันออกกลาง เหมาะสำหรับนักเรียน นักศึกษา และผู้สนใจประวัติศาสตร์"
    )
    
    print(f"\n📋 Brief Overview:")
    print(f"   Brand: {brief.brand}")
    print(f"   Product: {brief.product}")
    print(f"   Duration: {brief.duration} seconds ({brief.duration / 60:.0f} minutes)")
    print(f"   Platform: {brief.platform}")
    print(f"   Language: {brief.language}")
    print(f"   Tone: {brief.tone}")
    
    # Config
    config = DirectorConfig(
        hf_token=None,
        image_model="sdxl",
        voice_language="thai"
    )
    
    print(f"\n⚙️ Configuration:")
    print(f"   Image Source: Placeholder (Solid Color)")
    print(f"   Voice Language: {config.voice_language}")
    
    # Initialize AI Director
    print("\n🎬 Initializing AI Director...")
    director = AIDirector(config=config)
    
    # Step 1: Get brand context (empty for documentary)
    print("\n" + "=" * 80)
    print("STEP 1: RETRIEVE BRAND CONTEXT")
    print("=" * 80)
    print("\n   (Skipping for documentary content)")
    
    brand_context = {
        "brand_name": brief.brand,
        "documents": [],
        "source": "Documentary"
    }
    
    # Step 2: Generate Creative Strategy
    print("\n" + "=" * 80)
    print("STEP 2: GENERATE CREATIVE STRATEGY")
    print("=" * 80)
    print("\n🧠 Generating Persian Gulf War documentary strategy...")
    print("   This includes:")
    print("   - Visual scenes (6 key moments)")
    print("   - 30-minute Thai voiceover script (~15,600 characters)")
    print("   - Historical narrative structure")
    
    strategy = director.generate_creative_strategy(brief, brand_context)
    
    print(f"\n✅ Strategy generated:")
    print(f"   Visual Scenes: {len(strategy.visual_scenes)}")
    print(f"   Script Length: {len(strategy.voiceover_script):,} characters")
    print(f"   Estimated Duration: {len(strategy.voiceover_script) / 520:.1f} minutes")
    
    # Display scenes
    print(f"\n📸 Visual Scenes:")
    for i, scene in enumerate(strategy.visual_scenes[:6], 1):
        print(f"   {i}. {scene[:80]}...")
    
    # Display script preview
    print(f"\n📝 Script Preview (first 500 chars):")
    print(f"   {strategy.voiceover_script[:500]}...")
    
    # Step 3: Generate Images
    print("\n" + "=" * 80)
    print("STEP 3: GENERATE IMAGES")
    print("=" * 80)
    print("\n🎨 Generating placeholder images (solid color)...")
    
    image_files = []
    image_gen = director._get_image_generator()
    
    for i, scene_prompt in enumerate(strategy.visual_scenes[:6], 1):
        print(f"   Generating scene {i}/6: {scene_prompt[:60]}...")
        
        image_path = output_dir / f"scene_{i}.png"
        image_gen.generate(
            prompt=scene_prompt,
            width=1920,
            height=1080,
            output_file=str(image_path)
        )
        
        image_files.append(str(image_path))
        print(f"   ✅ Saved: {image_path.name}")
    
    print(f"\n✅ All 6 images generated")
    
    # Step 4: Generate Voiceover
    print("\n" + "=" * 80)
    print("STEP 4: GENERATE VOICEOVER (Thai TTS)")
    print("=" * 80)
    print(f"\n🎙️ Generating Thai voiceover...")
    print(f"   Script: {len(strategy.voiceover_script):,} characters")
    print(f"   Estimated: {len(strategy.voiceover_script) / 520:.1f} minutes")
    print(f"   Voice: th-TH-PremwadeeNeural")
    
    voiceover_path = output_dir / "voiceover.mp3"
    
    # Use Edge-TTS for Thai voiceover
    import edge_tts
    
    communicate = edge_tts.Communicate(
        text=strategy.voiceover_script,
        voice="th-TH-PremwadeeNeural"
    )
    
    await communicate.save(str(voiceover_path))
    
    print(f"   ✅ Saved: {voiceover_path.name}")
    
    # Get audio duration
    from moviepy.editor import AudioFileClip
    audio = AudioFileClip(str(voiceover_path))
    actual_duration = audio.duration
    audio.close()
    
    print(f"   Actual Duration: {actual_duration:.1f} seconds ({actual_duration / 60:.1f} minutes)")
    
    # Step 5: Compose Video
    print("\n" + "=" * 80)
    print("STEP 5: COMPOSE FINAL VIDEO")
    print("=" * 80)
    print("\n🎬 Composing video with images and voiceover...")
    
    video_path = output_dir / "persian_gulf_war_documentary_30min.mp4"
    
    from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
    
    # Calculate duration per image
    duration_per_image = actual_duration / len(image_files)
    print(f"   Images: {len(image_files)}")
    print(f"   Duration per image: {duration_per_image:.1f} seconds")
    
    # Create video clips
    clips = []
    for img_path in image_files:
        clip = ImageClip(img_path).set_duration(duration_per_image)
        clips.append(clip)
    
    # Concatenate
    video = concatenate_videoclips(clips, method="compose")
    
    # Add audio
    audio = AudioFileClip(str(voiceover_path))
    video = video.set_audio(audio)
    
    # Export
    print(f"\n   Exporting video...")
    video.write_videofile(
        str(video_path),
        fps=24,
        codec='libx264',
        audio_codec='aac',
        temp_audiofile='temp-audio.m4a',
        remove_temp=True,
        logger=None
    )
    
    video.close()
    audio.close()
    
    print(f"   ✅ Video saved: {video_path}")
    
    # Final Summary
    print("\n" + "=" * 80)
    print("✅ PRODUCTION COMPLETE!")
    print("=" * 80)
    print(f"\n📊 Summary:")
    print(f"   Project: {brief.project_name}")
    print(f"   Images: {len(image_files)} placeholder images")
    print(f"   Script: {len(strategy.voiceover_script):,} characters")
    print(f"   Voiceover: {actual_duration:.1f} seconds ({actual_duration / 60:.1f} minutes)")
    print(f"   Video: 1920×1080 @ 24fps")
    print(f"\n📁 Output:")
    print(f"   {video_path}")
    print(f"\n🎬 Ready to watch!")

if __name__ == "__main__":
    asyncio.run(main())
