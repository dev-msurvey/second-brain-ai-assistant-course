"""
Complete ETL Pipeline
Extract → Transform → Load

Module 2: ETL Pipeline
AI Director v3.4
"""

import sys
from pathlib import Path
from loguru import logger

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from extract import DataExtractor
from transform import DataTransformer
from load import MongoDBLoader


def run_etl_pipeline():
    """
    Run complete ETL pipeline
    
    Steps:
    1. Extract data from files
    2. Transform and validate data
    3. Load to MongoDB Atlas
    """
    logger.info("╔" + "═" * 68 + "╗")
    logger.info("║" + " " * 20 + "🚀 ETL PIPELINE START" + " " * 27 + "║")
    logger.info("╚" + "═" * 68 + "╝")
    logger.info("")
    
    # ========== STEP 1: EXTRACT ==========
    logger.info("=" * 70)
    logger.info("STEP 1: EXTRACT DATA")
    logger.info("=" * 70)
    logger.info("")
    
    extractor = DataExtractor()
    
    logger.info("📦 Extracting brands...")
    brands_raw = extractor.extract_brands()
    
    logger.info("📦 Extracting campaigns...")
    campaigns_raw = extractor.extract_campaigns()
    
    logger.info("")
    logger.info(f"📊 Extraction Summary:")
    logger.info(f"   • Brands: {len(brands_raw)}")
    logger.info(f"   • Campaigns: {len(campaigns_raw)}")
    logger.info("")
    
    if not brands_raw and not campaigns_raw:
        logger.error("❌ No data extracted. Check data/raw/ directory.")
        return
    
    # ========== STEP 2: TRANSFORM ==========
    logger.info("=" * 70)
    logger.info("STEP 2: TRANSFORM DATA")
    logger.info("=" * 70)
    logger.info("")
    
    transformer = DataTransformer()
    
    logger.info("🔄 Transforming brands...")
    brands_clean = transformer.transform_brands(brands_raw)
    
    logger.info("")
    logger.info("🔄 Transforming campaigns...")
    campaigns_clean = transformer.transform_campaigns(campaigns_raw)
    
    logger.info("")
    logger.info(f"📊 Transformation Summary:")
    logger.info(f"   • Brands validated: {len(brands_clean)}/{len(brands_raw)}")
    logger.info(f"   • Campaigns validated: {len(campaigns_clean)}/{len(campaigns_raw)}")
    
    if brands_clean:
        avg_brand_quality = sum(b['quality_score'] for b in brands_clean) / len(brands_clean)
        logger.info(f"   • Avg brand quality: {avg_brand_quality:.2f}")
    
    if campaigns_clean:
        avg_campaign_quality = sum(c['quality_score'] for c in campaigns_clean) / len(campaigns_clean)
        logger.info(f"   • Avg campaign quality: {avg_campaign_quality:.2f}")
    
    logger.info("")
    
    # ========== STEP 3: LOAD ==========
    logger.info("=" * 70)
    logger.info("STEP 3: LOAD DATA TO MONGODB")
    logger.info("=" * 70)
    logger.info("")
    
    try:
        loader = MongoDBLoader()
        
        # Test connection
        logger.info("🔍 Testing MongoDB connection...")
        if not loader.test_connection():
            logger.error("❌ MongoDB connection failed")
            logger.info("")
            logger.info("📝 Setup MongoDB Atlas:")
            logger.info("   1. Go to https://www.mongodb.com/cloud/atlas")
            logger.info("   2. Create free M0 cluster")
            logger.info("   3. Create database user")
            logger.info("   4. Whitelist IP: 0.0.0.0/0")
            logger.info("   5. Get connection string")
            logger.info("   6. Add to .env file: MONGO_URI=\"your_connection_string\"")
            logger.info("")
            return
        
        logger.info("")
        
        # Load brands
        if brands_clean:
            logger.info("📤 Loading brands to MongoDB...")
            brand_result = loader.load_brands(brands_clean, clear_existing=True)
            logger.info("")
        
        # Load campaigns
        if campaigns_clean:
            logger.info("📤 Loading campaigns to MongoDB...")
            campaign_result = loader.load_campaigns(campaigns_clean, clear_existing=True)
            logger.info("")
        
        # Get final stats
        logger.info("📊 Final Database Statistics:")
        stats = loader.get_stats()
        for collection, count in stats.items():
            logger.info(f"   • {collection}: {count} documents")
        
        # Close connection
        loader.close()
        logger.info("")
        
        # ========== COMPLETE ==========
        logger.info("=" * 70)
        logger.info("✅ ETL PIPELINE COMPLETE!")
        logger.info("=" * 70)
        logger.info("")
        logger.info("🎉 Data successfully loaded to MongoDB Atlas")
        logger.info("")
        logger.info("📋 Next steps:")
        logger.info("   • View data in MongoDB Atlas dashboard")
        logger.info("   • Test queries: python scripts/validate.py --sample-brands 3")
        logger.info("   • Continue to Module 3: Dataset Generation")
        logger.info("")
        
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        logger.info("")
        logger.info("📝 Please set MONGO_URI in .env file:")
        logger.info('   MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/"')
        logger.info("")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        logger.info("")


if __name__ == "__main__":
    # Configure logger
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="{message}",
        level="INFO"
    )
    
    try:
        run_etl_pipeline()
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Pipeline interrupted by user")
    except Exception as e:
        logger.error(f"\n\n❌ Pipeline failed: {e}")
        sys.exit(1)
