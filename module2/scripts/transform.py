"""
Data Transformation Script
Clean, validate, and enrich extracted data

Module 2: ETL Pipeline
AI Director v3.4
"""

import re
from datetime import datetime
from typing import Dict, List, Any
from loguru import logger
from pydantic import BaseModel, Field, ValidationError


# Data Models for Validation
class Brand(BaseModel):
    """Brand data model"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10)
    tone: str
    colors: List[str] = Field(default_factory=list)
    fonts: List[str] = Field(default_factory=list)
    target_audience: str
    brand_values: List[str] = Field(default_factory=list)
    social_media: Dict[str, str] = Field(default_factory=dict)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class Campaign(BaseModel):
    """Campaign data model"""
    brand_name: str
    campaign_name: str
    brief: str = Field(..., min_length=10)
    objectives: List[str] = Field(default_factory=list)
    target_metrics: Dict[str, Any] = Field(default_factory=dict)
    content_requirements: Dict[str, Any] = Field(default_factory=dict)
    status: str = Field(default="draft")
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class DataTransformer:
    """Transform and enrich data"""
    
    def __init__(self):
        logger.info("Initialized DataTransformer")
    
    def transform_brands(self, brands: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform brand data: clean, validate, enrich
        
        Args:
            brands: List of raw brand dictionaries
            
        Returns:
            List of transformed and validated brand dictionaries
        """
        transformed = []
        
        for brand_data in brands:
            try:
                # Clean data
                clean_brand = self._clean_brand_data(brand_data)
                
                # Calculate quality score
                quality = self._calculate_quality_score(
                    clean_brand.get('description', ''),
                    clean_brand.get('tone', ''),
                    len(clean_brand.get('brand_values', []))
                )
                clean_brand['quality_score'] = quality
                
                # Validate with Pydantic
                brand = Brand(**clean_brand)
                
                # Convert to dict
                transformed.append(brand.model_dump())
                
                logger.info(f"✅ Transformed brand: {brand.name} (quality: {quality:.2f})")
            
            except ValidationError as e:
                logger.error(f"❌ Validation error for brand {brand_data.get('name', 'unknown')}: {e}")
                continue
        
        logger.info(f"✅ Transformed {len(transformed)}/{len(brands)} brands successfully")
        return transformed
    
    def transform_campaigns(self, campaigns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform campaign data: clean, validate, enrich
        
        Args:
            campaigns: List of raw campaign dictionaries
            
        Returns:
            List of transformed and validated campaign dictionaries
        """
        transformed = []
        
        for campaign_data in campaigns:
            try:
                # Clean data
                clean_campaign = self._clean_campaign_data(campaign_data)
                
                # Calculate quality score
                quality = self._calculate_quality_score(
                    clean_campaign.get('brief', ''),
                    clean_campaign.get('campaign_name', ''),
                    len(clean_campaign.get('objectives', []))
                )
                clean_campaign['quality_score'] = quality
                
                # Validate with Pydantic
                campaign = Campaign(**clean_campaign)
                
                # Convert to dict
                transformed.append(campaign.model_dump())
                
                logger.info(f"✅ Transformed campaign: {campaign.campaign_name} (quality: {quality:.2f})")
            
            except ValidationError as e:
                logger.error(f"❌ Validation error for campaign {campaign_data.get('campaign_name', 'unknown')}: {e}")
                continue
        
        logger.info(f"✅ Transformed {len(transformed)}/{len(campaigns)} campaigns successfully")
        return transformed
    
    def _clean_brand_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean brand data"""
        cleaned = {}
        
        # Required fields
        cleaned['name'] = str(data.get('name', '')).strip()
        cleaned['description'] = str(data.get('description', '')).strip()
        cleaned['tone'] = str(data.get('tone', '')).strip()
        cleaned['target_audience'] = str(data.get('target_audience', '')).strip()
        
        # Optional lists
        cleaned['colors'] = [c.strip() for c in data.get('colors', []) if c.strip()]
        cleaned['fonts'] = [f.strip() for f in data.get('fonts', []) if f.strip()]
        cleaned['brand_values'] = [v.strip() for v in data.get('brand_values', []) if v.strip()]
        
        # Social media
        cleaned['social_media'] = data.get('social_media', {})
        
        return cleaned
    
    def _clean_campaign_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean campaign data"""
        cleaned = {}
        
        # Required fields
        cleaned['brand_name'] = str(data.get('brand_name', '')).strip()
        cleaned['campaign_name'] = str(data.get('campaign_name', '')).strip()
        cleaned['brief'] = str(data.get('brief', '')).strip()
        
        # Optional fields
        cleaned['objectives'] = data.get('objectives', [])
        cleaned['target_metrics'] = data.get('target_metrics', {})
        cleaned['content_requirements'] = data.get('content_requirements', {})
        cleaned['status'] = data.get('status', 'draft')
        
        return cleaned
    
    def _calculate_quality_score(self, text: str, secondary_text: str = "", extra_items: int = 0) -> float:
        """
        Calculate content quality score (0-1)
        
        Criteria:
        - Text length (40%)
        - Secondary text quality (30%)
        - Extra items count (30%)
        
        Args:
            text: Primary text content
            secondary_text: Secondary text (tone, name, etc.)
            extra_items: Number of extra items (values, objectives, etc.)
            
        Returns:
            Quality score between 0 and 1
        """
        score = 0.0
        
        # Text length score (40%)
        # 0-50 chars: 0, 50-100: 0.5, 100+: 1.0
        text_len = len(text)
        if text_len >= 100:
            score += 0.4
        elif text_len >= 50:
            score += 0.2
        
        # Secondary text score (30%)
        # Has content: +0.3
        if len(secondary_text) > 5:
            score += 0.3
        
        # Extra items score (30%)
        # 0 items: 0, 1-2: 0.15, 3+: 0.3
        if extra_items >= 3:
            score += 0.3
        elif extra_items >= 1:
            score += 0.15
        
        return round(score, 2)
    
    def add_timestamps(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add creation and update timestamps"""
        now = datetime.now()
        data['created_at'] = now
        data['updated_at'] = now
        return data


def demo_transformation():
    """Demonstrate transformation functionality"""
    logger.info("=" * 70)
    logger.info("🔄 DATA TRANSFORMATION DEMO")
    logger.info("=" * 70)
    
    transformer = DataTransformer()
    
    # Sample brand data
    sample_brand = {
        "name": "TestBrand",
        "description": "A premium test brand for quality products and services",
        "tone": "professional, friendly",
        "colors": ["#FF0000", "#00FF00"],
        "fonts": ["Arial", "Helvetica"],
        "target_audience": "young professionals 25-35",
        "brand_values": ["quality", "innovation", "trust"],
        "social_media": {
            "instagram": "@testbrand",
            "facebook": "TestBrand"
        }
    }
    
    logger.info("\n🏢 Transforming sample brand...")
    transformed_brands = transformer.transform_brands([sample_brand])
    
    if transformed_brands:
        brand = transformed_brands[0]
        logger.info(f"\n📊 Transformed Brand:")
        logger.info(f"   Name: {brand['name']}")
        logger.info(f"   Quality Score: {brand['quality_score']}")
        logger.info(f"   Created At: {brand['created_at']}")
        logger.info(f"   Brand Values: {', '.join(brand['brand_values'])}")
    
    # Sample campaign data
    sample_campaign = {
        "brand_name": "TestBrand",
        "campaign_name": "Summer Launch 2025",
        "brief": "Launch new summer product line with emphasis on sustainability and modern design. Target young urban professionals.",
        "objectives": ["awareness", "sales", "engagement"],
        "target_metrics": {
            "reach": 100000,
            "engagement_rate": 0.05
        },
        "content_requirements": {
            "image_count": 5,
            "video_count": 2
        },
        "status": "draft"
    }
    
    logger.info("\n📢 Transforming sample campaign...")
    transformed_campaigns = transformer.transform_campaigns([sample_campaign])
    
    if transformed_campaigns:
        campaign = transformed_campaigns[0]
        logger.info(f"\n📊 Transformed Campaign:")
        logger.info(f"   Name: {campaign['campaign_name']}")
        logger.info(f"   Brand: {campaign['brand_name']}")
        logger.info(f"   Quality Score: {campaign['quality_score']}")
        logger.info(f"   Objectives: {', '.join(campaign['objectives'])}")
    
    logger.info("\n" + "=" * 70)
    logger.info("✅ TRANSFORMATION DEMO COMPLETE")
    logger.info("=" * 70)


if __name__ == "__main__":
    # Configure logger
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="{message}",
        level="INFO"
    )
    
    demo_transformation()
