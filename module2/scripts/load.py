"""
Data Loading Script
Load transformed data into MongoDB Atlas

Module 2: ETL Pipeline
AI Director v3.4
"""

import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from loguru import logger
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MongoDBLoader:
    """Load data into MongoDB Atlas"""
    
    def __init__(self, 
                 connection_string: Optional[str] = None,
                 database_name: str = "ai_director"):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB connection URI
            database_name: Name of database to use
        """
        self.connection_string = connection_string or os.getenv("MONGO_URI")
        self.database_name = database_name
        
        if not self.connection_string:
            raise ValueError("MongoDB connection string not provided. Set MONGO_URI in .env file")
        
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            logger.info(f"✅ Connected to MongoDB: {database_name}")
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def load_brands(self, brands: List[Dict[str, Any]], clear_existing: bool = True) -> Dict[str, int]:
        """
        Load brand data to MongoDB
        
        Args:
            brands: List of brand documents
            clear_existing: Whether to clear existing data
            
        Returns:
            Dictionary with insert statistics
        """
        collection = self.db["brands"]
        
        if clear_existing:
            result = collection.delete_many({})
            logger.info(f"🗑️  Deleted {result.deleted_count} existing brands")
        
        if not brands:
            logger.warning("⚠️ No brands to insert")
            return {"inserted": 0}
        
        try:
            result = collection.insert_many(brands)
            count = len(result.inserted_ids)
            logger.info(f"✅ Inserted {count} brands")
            
            # Create indexes
            self._create_brand_indexes(collection)
            
            return {"inserted": count}
        
        except OperationFailure as e:
            logger.error(f"❌ Failed to insert brands: {e}")
            return {"inserted": 0}
    
    def load_campaigns(self, campaigns: List[Dict[str, Any]], clear_existing: bool = True) -> Dict[str, int]:
        """
        Load campaign data to MongoDB
        
        Args:
            campaigns: List of campaign documents
            clear_existing: Whether to clear existing data
            
        Returns:
            Dictionary with insert statistics
        """
        collection = self.db["campaigns"]
        
        if clear_existing:
            result = collection.delete_many({})
            logger.info(f"🗑️  Deleted {result.deleted_count} existing campaigns")
        
        if not campaigns:
            logger.warning("⚠️ No campaigns to insert")
            return {"inserted": 0}
        
        try:
            result = collection.insert_many(campaigns)
            count = len(result.inserted_ids)
            logger.info(f"✅ Inserted {count} campaigns")
            
            # Create indexes
            self._create_campaign_indexes(collection)
            
            return {"inserted": count}
        
        except OperationFailure as e:
            logger.error(f"❌ Failed to insert campaigns: {e}")
            return {"inserted": 0}
    
    def load_transcripts(self, transcripts: List[Dict[str, Any]], clear_existing: bool = True) -> Dict[str, int]:
        """
        Load transcript data to MongoDB
        
        Args:
            transcripts: List of transcript documents
            clear_existing: Whether to clear existing data
            
        Returns:
            Dictionary with insert statistics
        """
        collection = self.db["transcripts"]
        
        if clear_existing:
            result = collection.delete_many({})
            logger.info(f"🗑️  Deleted {result.deleted_count} existing transcripts")
        
        if not transcripts:
            logger.warning("⚠️ No transcripts to insert")
            return {"inserted": 0}
        
        try:
            result = collection.insert_many(transcripts)
            count = len(result.inserted_ids)
            logger.info(f"✅ Inserted {count} transcripts")
            
            # Create indexes
            self._create_transcript_indexes(collection)
            
            return {"inserted": count}
        
        except OperationFailure as e:
            logger.error(f"❌ Failed to insert transcripts: {e}")
            return {"inserted": 0}
    
    def _create_brand_indexes(self, collection):
        """Create indexes for brands collection"""
        try:
            collection.create_index([("name", ASCENDING)], unique=True)
            collection.create_index([("quality_score", DESCENDING)])
            collection.create_index([("created_at", DESCENDING)])
            logger.info("✅ Created brand indexes")
        except Exception as e:
            logger.warning(f"⚠️ Index creation failed: {e}")
    
    def _create_campaign_indexes(self, collection):
        """Create indexes for campaigns collection"""
        try:
            collection.create_index([("brand_name", ASCENDING)])
            collection.create_index([("campaign_name", ASCENDING)])
            collection.create_index([("status", ASCENDING)])
            collection.create_index([("quality_score", DESCENDING)])
            collection.create_index([("created_at", DESCENDING)])
            logger.info("✅ Created campaign indexes")
        except Exception as e:
            logger.warning(f"⚠️ Index creation failed: {e}")
    
    def _create_transcript_indexes(self, collection):
        """Create indexes for transcripts collection"""
        try:
            collection.create_index([("video_id", ASCENDING)], unique=True)
            collection.create_index([("language", ASCENDING)])
            collection.create_index([("quality_score", DESCENDING)])
            collection.create_index([("created_at", DESCENDING)])
            logger.info("✅ Created transcript indexes")
        except Exception as e:
            logger.warning(f"⚠️ Index creation failed: {e}")
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get statistics about loaded data
        
        Returns:
            Dictionary with collection counts
        """
        stats = {
            "brands": self.db["brands"].count_documents({}),
            "campaigns": self.db["campaigns"].count_documents({}),
            "transcripts": self.db["transcripts"].count_documents({})
        }
        return stats
    
    def test_connection(self) -> bool:
        """
        Test MongoDB connection
        
        Returns:
            True if connection successful
        """
        try:
            self.client.admin.command('ping')
            logger.info("✅ MongoDB connection test successful")
            return True
        except Exception as e:
            logger.error(f"❌ MongoDB connection test failed: {e}")
            return False
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("🔌 MongoDB connection closed")


def demo_loading():
    """Demonstrate loading functionality"""
    logger.info("=" * 70)
    logger.info("📤 DATA LOADING DEMO")
    logger.info("=" * 70)
    
    # Check for connection string
    if not os.getenv("MONGO_URI"):
        logger.error("\n❌ MONGO_URI not found in environment variables")
        logger.info("📝 Please set MONGO_URI in .env file:")
        logger.info('   MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/"')
        return
    
    try:
        loader = MongoDBLoader()
        
        # Test connection
        logger.info("\n🔍 Testing connection...")
        if not loader.test_connection():
            logger.error("❌ Connection test failed")
            return
        
        # Sample data
        sample_brands = [
            {
                "name": "TestBrand1",
                "description": "Test brand 1 description",
                "tone": "professional",
                "colors": ["#FF0000"],
                "fonts": ["Arial"],
                "target_audience": "everyone",
                "brand_values": ["quality"],
                "social_media": {},
                "quality_score": 0.75,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]
        
        sample_campaigns = [
            {
                "brand_name": "TestBrand1",
                "campaign_name": "Test Campaign",
                "brief": "This is a test campaign brief",
                "objectives": ["awareness"],
                "target_metrics": {},
                "content_requirements": {},
                "status": "draft",
                "quality_score": 0.70,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]
        
        # Load data
        logger.info("\n📦 Loading sample data...")
        brand_result = loader.load_brands(sample_brands)
        campaign_result = loader.load_campaigns(sample_campaigns)
        
        # Get stats
        logger.info("\n📊 Database Statistics:")
        stats = loader.get_stats()
        for collection, count in stats.items():
            logger.info(f"   {collection}: {count} documents")
        
        # Close connection
        loader.close()
        
        logger.info("\n" + "=" * 70)
        logger.info("✅ LOADING DEMO COMPLETE")
        logger.info("=" * 70)
    
    except ValueError as e:
        logger.error(f"\n❌ Configuration error: {e}")
    except Exception as e:
        logger.error(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    # Configure logger
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="{message}",
        level="INFO"
    )
    
    demo_loading()
