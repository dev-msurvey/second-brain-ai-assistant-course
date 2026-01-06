"""
Module 6: Voice Generator - Edge-TTS Integration
=================================================

Generate high-quality voiceovers using Microsoft Edge TTS.

Features:
- Thai voices (th-TH-NiwatNeural, th-TH-PremwadeeNeural)
- English voices (multiple)
- Adjustable rate, pitch, volume
- Subtitle generation (.srt, .vtt)
- Word-level timestamps
- Batch processing

Author: AI Director Team
License: MIT
"""

import asyncio
import edge_tts
import os
import logging
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
import re
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceGenerator:
    """
    Generate voiceovers using Microsoft Edge TTS.
    
    Supports:
    - Thai voices: th-TH-NiwatNeural (male), th-TH-PremwadeeNeural (female)
    - English voices: en-US-GuyNeural (male), en-US-JennyNeural (female)
    - And many more languages...
    
    Example:
        >>> generator = VoiceGenerator()
        >>> await generator.generate(
        ...     text="สวัสดีครับ วันนี้เรามาแนะนำกาแฟ",
        ...     voice="th-TH-NiwatNeural",
        ...     output_file="voiceover.mp3"
        ... )
    """
    
    THAI_VOICES = {
        "male": "th-TH-NiwatNeural",
        "female": "th-TH-PremwadeeNeural"
    }
    
    ENGLISH_VOICES = {
        "male": "en-US-GuyNeural",
        "female": "en-US-JennyNeural",
        "male_uk": "en-GB-RyanNeural",
        "female_uk": "en-GB-SoniaNeural"
    }
    
    def __init__(self):
        """Initialize VoiceGenerator."""
        logger.info("✅ VoiceGenerator initialized")
    
    async def generate(
        self,
        text: str,
        voice: str = "th-TH-NiwatNeural",
        rate: str = "+0%",
        pitch: str = "+0Hz",
        volume: str = "+0%",
        output_file: str = "output.mp3"
    ) -> str:
        """
        Generate voice from text.
        
        Args:
            text: Text to convert to speech
            voice: Voice ID (e.g., "th-TH-NiwatNeural")
            rate: Speaking rate adjustment (-50% to +100%)
            pitch: Pitch adjustment (-50Hz to +50Hz)
            volume: Volume adjustment (-50% to +50%)
            output_file: Output audio file path
            
        Returns:
            Path to generated audio file
        """
        # Create output directory
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎙️ Generating voice: {voice}")
        logger.info(f"📝 Text: {text[:50]}..." if len(text) > 50 else f"📝 Text: {text}")
        
        # Create TTS communicate
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )
        
        # Save audio
        await communicate.save(output_file)
        
        logger.info(f"✅ Voice saved to: {output_file}")
        return output_file
    
    async def generate_with_subtitles(
        self,
        text: str,
        voice: str = "th-TH-NiwatNeural",
        rate: str = "+0%",
        output_audio: str = "output.mp3",
        output_srt: Optional[str] = None,
        output_vtt: Optional[str] = None
    ) -> Tuple[str, Optional[str], Optional[str]]:
        """
        Generate voice with subtitle files.
        
        Args:
            text: Text to convert to speech
            voice: Voice ID
            rate: Speaking rate adjustment
            output_audio: Output audio file path
            output_srt: Output SRT subtitle file path (optional)
            output_vtt: Output VTT subtitle file path (optional)
            
        Returns:
            Tuple of (audio_path, srt_path, vtt_path)
        """
        # Create output directory
        output_path = Path(output_audio)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🎙️ Generating voice with subtitles: {voice}")
        
        # Create TTS communicate
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate
        )
        
        # Collect subtitles
        subtitles = []
        
        # Save audio and collect subtitle data
        with open(output_audio, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    subtitles.append(chunk)
        
        logger.info(f"✅ Voice saved to: {output_audio}")
        
        # Generate SRT if requested
        srt_path = None
        if output_srt:
            srt_path = self._generate_srt(subtitles, output_srt)
            logger.info(f"✅ SRT subtitles saved to: {srt_path}")
        
        # Generate VTT if requested
        vtt_path = None
        if output_vtt:
            vtt_path = self._generate_vtt(subtitles, output_vtt)
            logger.info(f"✅ VTT subtitles saved to: {vtt_path}")
        
        return output_audio, srt_path, vtt_path
    
    def _generate_srt(self, subtitles: List[Dict], output_file: str) -> str:
        """Generate SRT subtitle file from word boundaries."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Group words into lines (approximately 5-7 words per line)
        lines = []
        current_line = []
        words_per_line = 6
        
        for i, sub in enumerate(subtitles):
            current_line.append(sub)
            
            if len(current_line) >= words_per_line or i == len(subtitles) - 1:
                if current_line:
                    lines.append(current_line)
                    current_line = []
        
        # Write SRT file
        with open(output_file, "w", encoding="utf-8") as f:
            for i, line in enumerate(lines, start=1):
                start_time = self._format_timestamp_srt(line[0]["offset"])
                end_time = self._format_timestamp_srt(line[-1]["offset"] + line[-1]["duration"])
                text = " ".join([word.get("text", "") for word in line])
                
                f.write(f"{i}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        return output_file
    
    def _generate_vtt(self, subtitles: List[Dict], output_file: str) -> str:
        """Generate VTT subtitle file from word boundaries."""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Group words into lines
        lines = []
        current_line = []
        words_per_line = 6
        
        for i, sub in enumerate(subtitles):
            current_line.append(sub)
            
            if len(current_line) >= words_per_line or i == len(subtitles) - 1:
                if current_line:
                    lines.append(current_line)
                    current_line = []
        
        # Write VTT file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            
            for line in lines:
                start_time = self._format_timestamp_vtt(line[0]["offset"])
                end_time = self._format_timestamp_vtt(line[-1]["offset"] + line[-1]["duration"])
                text = " ".join([word.get("text", "") for word in line])
                
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")
        
        return output_file
    
    def _format_timestamp_srt(self, offset: int) -> str:
        """Format timestamp for SRT (HH:MM:SS,mmm)."""
        seconds = offset / 10_000_000
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _format_timestamp_vtt(self, offset: int) -> str:
        """Format timestamp for VTT (HH:MM:SS.mmm)."""
        seconds = offset / 10_000_000
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    async def list_voices(self, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available voices.
        
        Args:
            language: Filter by language code (e.g., "th-TH", "en-US")
            
        Returns:
            List of voice information dictionaries
        """
        voices = await edge_tts.list_voices()
        
        if language:
            voices = [v for v in voices if v["Locale"].startswith(language)]
        
        return voices
    
    async def generate_batch(
        self,
        texts: List[str],
        voice: str = "th-TH-NiwatNeural",
        output_dir: str = "output",
        **kwargs
    ) -> List[str]:
        """
        Generate multiple voiceovers.
        
        Args:
            texts: List of texts to convert
            voice: Voice ID
            output_dir: Output directory for audio files
            **kwargs: Additional arguments passed to generate()
            
        Returns:
            List of output file paths
        """
        output_files = []
        
        for i, text in enumerate(texts):
            output_file = os.path.join(output_dir, f"voice_{i+1:03d}.mp3")
            
            try:
                await self.generate(
                    text=text,
                    voice=voice,
                    output_file=output_file,
                    **kwargs
                )
                output_files.append(output_file)
            except Exception as e:
                logger.error(f"❌ Failed to generate voice {i+1}: {str(e)}")
                output_files.append(None)
        
        logger.info(f"✅ Generated {len([f for f in output_files if f])} out of {len(texts)} voices")
        return output_files
    
    def get_thai_voices(self) -> Dict[str, str]:
        """Get available Thai voices."""
        return self.THAI_VOICES
    
    def get_english_voices(self) -> Dict[str, str]:
        """Get available English voices."""
        return self.ENGLISH_VOICES


# Example usage
async def main():
    """Test voice generation."""
    generator = VoiceGenerator()
    
    # Test Thai voice
    print("\n🇹🇭 Testing Thai voice...")
    await generator.generate(
        text="สวัสดีครับ วันนี้เรามาแนะนำกาแฟ Cold Brew Premium จาก CoffeeLab",
        voice="th-TH-NiwatNeural",
        rate="+0%",
        output_file="test_thai.mp3"
    )
    
    # Test English voice
    print("\n🇬🇧 Testing English voice...")
    await generator.generate(
        text="Welcome to CoffeeLab. Experience premium coffee like never before.",
        voice="en-US-GuyNeural",
        rate="+0%",
        output_file="test_english.mp3"
    )
    
    # Test with subtitles
    print("\n📝 Testing with subtitles...")
    await generator.generate_with_subtitles(
        text="เริ่มต้นเช้าวันใหม่ด้วยกาแฟ Cold Brew จาก CoffeeLab คาเฟ่ที่ดีที่สุดในเมือง",
        voice="th-TH-PremwadeeNeural",
        output_audio="test_with_subs.mp3",
        output_srt="test_with_subs.srt",
        output_vtt="test_with_subs.vtt"
    )
    
    # List available voices
    print("\n📋 Available Thai voices:")
    voices = await generator.list_voices(language="th-TH")
    for voice in voices:
        print(f"  - {voice['ShortName']}: {voice['Gender']}")


if __name__ == "__main__":
    asyncio.run(main())
