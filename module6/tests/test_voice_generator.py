"""
Tests for Voice Generator
=========================

Test suite for Module 6 Voice Generator functionality.
"""

import pytest
import asyncio
import os
from pathlib import Path

from tools.voice_generator import VoiceGenerator


class TestVoiceGenerator:
    """Test VoiceGenerator class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = VoiceGenerator()
        self.output_dir = Path("test_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def teardown_method(self):
        """Cleanup test files."""
        if self.output_dir.exists():
            for file in self.output_dir.glob("*"):
                file.unlink()
            self.output_dir.rmdir()
    
    def test_initialization(self):
        """Test generator initialization."""
        assert self.generator is not None
        assert hasattr(self.generator, "THAI_VOICES")
        assert hasattr(self.generator, "ENGLISH_VOICES")
    
    @pytest.mark.asyncio
    async def test_thai_voice_generation(self):
        """Test Thai voice generation."""
        output_file = self.output_dir / "test_thai.mp3"
        
        result = await self.generator.generate(
            text="สวัสดีครับ",
            voice="th-TH-NiwatNeural",
            output_file=str(output_file)
        )
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0
    
    @pytest.mark.asyncio
    async def test_english_voice_generation(self):
        """Test English voice generation."""
        output_file = self.output_dir / "test_english.mp3"
        
        result = await self.generator.generate(
            text="Hello world",
            voice="en-US-GuyNeural",
            output_file=str(output_file)
        )
        
        assert output_file.exists()
        assert output_file.stat().st_size > 0
    
    @pytest.mark.asyncio
    async def test_voice_with_subtitles(self):
        """Test voice generation with subtitles."""
        audio_file = self.output_dir / "test_with_subs.mp3"
        srt_file = self.output_dir / "test_with_subs.srt"
        
        audio, srt, vtt = await self.generator.generate_with_subtitles(
            text="สวัสดีครับ วันนี้อากาศดี",
            voice="th-TH-NiwatNeural",
            output_audio=str(audio_file),
            output_srt=str(srt_file)
        )
        
        assert Path(audio).exists()
        assert Path(srt).exists()
    
    @pytest.mark.asyncio
    async def test_list_voices(self):
        """Test listing available voices."""
        voices = await self.generator.list_voices(language="th-TH")
        
        assert isinstance(voices, list)
        assert len(voices) > 0
        assert all("Locale" in v for v in voices)
    
    def test_get_thai_voices(self):
        """Test getting Thai voice IDs."""
        thai_voices = self.generator.get_thai_voices()
        
        assert "male" in thai_voices
        assert "female" in thai_voices
        assert "Neural" in thai_voices["male"]
    
    def test_get_english_voices(self):
        """Test getting English voice IDs."""
        english_voices = self.generator.get_english_voices()
        
        assert "male" in english_voices
        assert "female" in english_voices


class TestVoiceGeneratorTimestamps:
    """Test timestamp formatting."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.generator = VoiceGenerator()
    
    def test_srt_timestamp_format(self):
        """Test SRT timestamp formatting."""
        # 1 second = 10,000,000 in offset units
        offset = 10_000_000  # 1 second
        
        timestamp = self.generator._format_timestamp_srt(offset)
        
        assert timestamp == "00:00:01,000"
    
    def test_vtt_timestamp_format(self):
        """Test VTT timestamp formatting."""
        offset = 10_000_000  # 1 second
        
        timestamp = self.generator._format_timestamp_vtt(offset)
        
        assert timestamp == "00:00:01.000"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
