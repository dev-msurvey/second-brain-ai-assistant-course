"""
Data Extraction Script
Extract data from various sources (JSON, TXT, SRT files)

Module 2: ETL Pipeline
AI Director v3.4
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger


class DataExtractor:
    """Extract data from various file formats"""
    
    def __init__(self, data_dir: Path = Path("data/raw")):
        self.data_dir = Path(data_dir)
        logger.info(f"Initialized DataExtractor with directory: {self.data_dir}")
    
    def extract_brands(self, filename: str = "brands.json") -> List[Dict[str, Any]]:
        """
        Extract brand data from JSON file
        
        Args:
            filename: Name of JSON file containing brand data
            
        Returns:
            List of brand dictionaries
        """
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                brands = json.load(f)
            
            logger.info(f"✅ Extracted {len(brands)} brands from {filename}")
            return brands
        
        except FileNotFoundError:
            logger.error(f"❌ File not found: {filepath}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error in {filename}: {e}")
            return []
    
    def extract_campaigns(self, filename: str = "campaigns.json") -> List[Dict[str, Any]]:
        """
        Extract campaign data from JSON file
        
        Args:
            filename: Name of JSON file containing campaign data
            
        Returns:
            List of campaign dictionaries
        """
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                campaigns = json.load(f)
            
            logger.info(f"✅ Extracted {len(campaigns)} campaigns from {filename}")
            return campaigns
        
        except FileNotFoundError:
            logger.error(f"❌ File not found: {filepath}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON decode error in {filename}: {e}")
            return []
    
    def extract_text_file(self, filename: str) -> str:
        """
        Extract text content from file
        
        Args:
            filename: Name of text file
            
        Returns:
            File content as string
        """
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"✅ Extracted text from {filename} ({len(content)} characters)")
            return content
        
        except FileNotFoundError:
            logger.error(f"❌ File not found: {filepath}")
            return ""
    
    def extract_srt_transcript(self, filename: str) -> List[Dict[str, Any]]:
        """
        Extract transcript from SRT file
        
        Args:
            filename: Name of SRT file
            
        Returns:
            List of segment dictionaries with start, end, text
        """
        filepath = self.data_dir / "transcripts" / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            segments = []
            blocks = content.strip().split('\n\n')
            
            for block in blocks:
                lines = block.strip().split('\n')
                if len(lines) >= 3:
                    # Line 0: index
                    # Line 1: timestamps
                    # Line 2+: text
                    try:
                        index = int(lines[0])
                        times = lines[1].split(' --> ')
                        start = self._srt_time_to_seconds(times[0])
                        end = self._srt_time_to_seconds(times[1])
                        text = ' '.join(lines[2:])
                        
                        segments.append({
                            "id": index,
                            "start": start,
                            "end": end,
                            "text": text
                        })
                    except (ValueError, IndexError) as e:
                        logger.warning(f"⚠️ Skipping malformed SRT block: {e}")
                        continue
            
            logger.info(f"✅ Extracted {len(segments)} segments from {filename}")
            return segments
        
        except FileNotFoundError:
            logger.error(f"❌ File not found: {filepath}")
            return []
    
    def _srt_time_to_seconds(self, time_str: str) -> float:
        """Convert SRT timestamp to seconds"""
        # Format: 00:00:10,500 or 00:00:10.500
        time_str = time_str.replace(',', '.')
        parts = time_str.split(':')
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = float(parts[2])
        
        return hours * 3600 + minutes * 60 + seconds


def demo_extraction():
    """Demonstrate extraction functionality"""
    logger.info("=" * 70)
    logger.info("📦 DATA EXTRACTION DEMO")
    logger.info("=" * 70)
    
    extractor = DataExtractor()
    
    # Extract brands
    logger.info("\n🏢 Extracting brands...")
    brands = extractor.extract_brands()
    if brands:
        logger.info(f"Sample brand: {brands[0]['name']}")
        logger.info(f"Description: {brands[0]['description'][:100]}...")
    
    # Extract campaigns
    logger.info("\n📢 Extracting campaigns...")
    campaigns = extractor.extract_campaigns()
    if campaigns:
        logger.info(f"Sample campaign: {campaigns[0]['campaign_name']}")
        logger.info(f"Brand: {campaigns[0]['brand_name']}")
        logger.info(f"Objectives: {campaigns[0]['objectives']}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ EXTRACTION DEMO COMPLETE")
    logger.info("=" * 70)


if __name__ == "__main__":
    # Configure logger
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="{message}",
        level="INFO"
    )
    
    demo_extraction()
