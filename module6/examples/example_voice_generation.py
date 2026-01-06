"""
Example: Voice Generation
=========================

Demonstrates how to generate voiceovers using Edge-TTS.

Features demonstrated:
- Thai voice generation
- English voice generation
- Voice with subtitles
- Batch generation
- Different voice styles

Usage:
    python examples/example_voice_generation.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.voice_generator import VoiceGenerator


async def example_thai_voice():
    """Generate Thai voiceover."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Thai Voice Generation")
    print("="*60)
    
    generator = VoiceGenerator()
    
    # Thai male voice
    text_male = """
    สวัสดีครับ วันนี้เรามาแนะนำกาแฟพรีเมียม Cold Brew จาก CoffeeLab
    รสชาติกลมกล่อม หอมหวาน เหมาะสำหรับการเริ่มต้นวันใหม่
    ลองสัมผัสประสบการณ์กาแฟคุณภาพสูงกับเรา
    """
    
    await generator.generate(
        text=text_male.strip(),
        voice="th-TH-NiwatNeural",
        rate="+0%",
        output_file="output/thai_male.mp3"
    )
    
    print("\n✅ Thai male voice generated: output/thai_male.mp3")
    
    # Thai female voice
    text_female = """
    สวัสดีค่ะ ยินดีต้อนรับสู่ CoffeeLab
    เราคือคาเฟ่ที่มอบประสบการณ์กาแฟพิเศษให้คุณ
    """
    
    await generator.generate(
        text=text_female.strip(),
        voice="th-TH-PremwadeeNeural",
        rate="+0%",
        output_file="output/thai_female.mp3"
    )
    
    print("✅ Thai female voice generated: output/thai_female.mp3")


async def example_english_voice():
    """Generate English voiceover."""
    print("\n" + "="*60)
    print("EXAMPLE 2: English Voice Generation")
    print("="*60)
    
    generator = VoiceGenerator()
    
    text = """
    Welcome to CoffeeLab, where premium coffee meets exceptional taste.
    Experience our signature Cold Brew, crafted with care and precision.
    Start your day right with CoffeeLab.
    """
    
    # American male voice
    await generator.generate(
        text=text.strip(),
        voice="en-US-GuyNeural",
        rate="+0%",
        output_file="output/english_male.mp3"
    )
    
    print("\n✅ English male voice generated: output/english_male.mp3")
    
    # American female voice
    await generator.generate(
        text=text.strip(),
        voice="en-US-JennyNeural",
        rate="+0%",
        output_file="output/english_female.mp3"
    )
    
    print("✅ English female voice generated: output/english_female.mp3")


async def example_with_subtitles():
    """Generate voice with subtitle files."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Voice with Subtitles")
    print("="*60)
    
    generator = VoiceGenerator()
    
    text = """
    เริ่มต้นเช้าวันใหม่ด้วยกาแฟ Cold Brew Premium จาก CoffeeLab
    คาเฟ่ที่ดีที่สุดในเมือง มีบรรยากาศสบายๆ และกาแฟคุณภาพสูง
    มาสัมผัสประสบการณ์กาแฟที่แตกต่างกับเรา
    """
    
    audio, srt, vtt = await generator.generate_with_subtitles(
        text=text.strip(),
        voice="th-TH-NiwatNeural",
        output_audio="output/with_subtitles.mp3",
        output_srt="output/with_subtitles.srt",
        output_vtt="output/with_subtitles.vtt"
    )
    
    print(f"\n✅ Voice generated: {audio}")
    print(f"✅ SRT subtitles: {srt}")
    print(f"✅ VTT subtitles: {vtt}")


async def example_different_speeds():
    """Generate voices with different speaking rates."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Different Speaking Rates")
    print("="*60)
    
    generator = VoiceGenerator()
    
    text = "สวัสดีครับ วันนี้เรามาพูดถึงกาแฟ Cold Brew จาก CoffeeLab"
    
    rates = {
        "slow": "-30%",
        "normal": "+0%",
        "fast": "+30%"
    }
    
    for speed, rate in rates.items():
        print(f"\n🎙️ Generating {speed} speed (rate={rate})...")
        
        await generator.generate(
            text=text,
            voice="th-TH-NiwatNeural",
            rate=rate,
            output_file=f"output/voice_{speed}.mp3"
        )
        
        print(f"✅ Saved: output/voice_{speed}.mp3")


async def example_batch_generation():
    """Generate multiple voiceovers in batch."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Batch Voice Generation")
    print("="*60)
    
    generator = VoiceGenerator()
    
    # Script segments
    segments = [
        "สวัสดีครับ ยินดีต้อนรับสู่ CoffeeLab",
        "วันนี้เรามีเมนูพิเศษสำหรับคุณ",
        "ลองสั่ง Cold Brew Premium ของเรา",
        "รสชาติกลมกล่อม หอมหวาน",
        "ขอบคุณที่อุดหนุนครับ"
    ]
    
    output_files = await generator.generate_batch(
        texts=segments,
        voice="th-TH-NiwatNeural",
        output_dir="output/batch"
    )
    
    print(f"\n✅ Generated {len([f for f in output_files if f])} voice files")
    for i, file in enumerate(output_files):
        if file:
            print(f"   {i+1}. {file}")


async def example_list_voices():
    """List available voices."""
    print("\n" + "="*60)
    print("EXAMPLE 6: List Available Voices")
    print("="*60)
    
    generator = VoiceGenerator()
    
    # List Thai voices
    print("\n🇹🇭 Thai Voices:")
    thai_voices = await generator.list_voices(language="th-TH")
    for voice in thai_voices:
        print(f"   - {voice['ShortName']}")
        print(f"     Gender: {voice['Gender']}")
        print(f"     Locale: {voice['Locale']}")
        print()
    
    # List English voices (first 5)
    print("🇬🇧 English Voices (first 5):")
    en_voices = await generator.list_voices(language="en-US")
    for voice in en_voices[:5]:
        print(f"   - {voice['ShortName']}")
        print(f"     Gender: {voice['Gender']}")
        print()


async def main():
    """Run all examples."""
    # Create output directory
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/batch", exist_ok=True)
    
    print("\n" + "="*60)
    print("MODULE 6: VOICE GENERATION EXAMPLES")
    print("="*60)
    
    try:
        # Run examples
        await example_thai_voice()
        await example_english_voice()
        await example_with_subtitles()
        await example_different_speeds()
        # await example_batch_generation()  # Uncomment to run
        await example_list_voices()
        
        print("\n" + "="*60)
        print("✅ ALL EXAMPLES COMPLETED!")
        print("="*60)
        print("\nGenerated files saved in: output/")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
