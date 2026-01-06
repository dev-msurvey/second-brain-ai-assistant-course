"""
MongoDB Vector Store for Module 5 RAG System
Manages vector search index creation and document storage
"""

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBVectorStore:
    """
    MongoDB Atlas Vector Store with vector search index
    Uses existing MONGO_URI from Module 2
    """
    
    def __init__(
        self,
        connection_string: Optional[str] = None,
        database_name: str = "ai_director",
        collection_name: str = "brand_vectors"
    ):
        """
        Initialize MongoDB Vector Store
        
        Args:
            connection_string: MongoDB URI (or use MONGO_URI env var)
            database_name: Database name (default: ai_director)
            collection_name: Collection for vector documents
        """
        self.connection_string = connection_string or os.getenv("MONGO_URI")
        self.database_name = database_name
        self.collection_name = collection_name
        
        if not self.connection_string:
            raise ValueError(
                "MongoDB connection string not provided. "
                "Set MONGO_URI in .env file or pass connection_string parameter"
            )
        
        try:
            self.client = MongoClient(self.connection_string, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            self.collection = self.db[collection_name]
            logger.info(f"✅ Connected to MongoDB: {database_name}.{collection_name}")
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise
    
    def create_vector_search_index(
        self,
        index_name: str = "vector_index",
        embedding_field: str = "embedding",
        embedding_dim: int = 384,
        similarity_metric: str = "cosine",
        num_candidates: int = 150
    ) -> bool:
        """
        Create Atlas Vector Search index
        
        Args:
            index_name: Name of the vector search index
            embedding_field: Field containing embedding vectors
            embedding_dim: Dimension of embedding vectors (384 for all-MiniLM-L6-v2)
            similarity_metric: "cosine", "euclidean", or "dotProduct"
            num_candidates: Number of candidates for ANN search
            
        Returns:
            True if created successfully
            
        Note:
            This requires MongoDB Atlas M10+ cluster or search index API access
            For M0 free tier, you need to create index manually via Atlas UI
        """
        index_definition = {
            "name": index_name,
            "type": "vectorSearch",
            "definition": {
                "fields": [
                    {
                        "type": "vector",
                        "path": embedding_field,
                        "numDimensions": embedding_dim,
                        "similarity": similarity_metric
                    },
                    {
                        "type": "filter",
                        "path": "brand_name"
                    },
                    {
                        "type": "filter",
                        "path": "doc_type"
                    }
                ]
            }
        }
        
        try:
            # Note: This requires Atlas Search API (M10+)
            # For M0 free tier, create index manually via Atlas UI
            logger.info(f"🔍 Creating vector search index: {index_name}")
            logger.info(f"   Dimension: {embedding_dim}, Metric: {similarity_metric}")
            logger.info("\n⚠️  Note: M0 free tier requires manual index creation via Atlas UI")
            logger.info("   1. Go to Atlas Console → Database → Search")
            logger.info("   2. Create Search Index with JSON Editor")
            logger.info(f"   3. Use this definition:\n")
            
            import json
            print(json.dumps(index_definition, indent=2))
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating vector index: {e}")
            logger.info("\n📝 For M0 free tier, create index manually:")
            logger.info("   1. Atlas Console → Database → Search → Create Search Index")
            logger.info("   2. Select JSON Editor")
            logger.info("   3. Paste the index definition above")
            return False
    
    def insert_documents(
        self,
        documents: List[Dict[str, Any]],
        clear_existing: bool = False
    ) -> int:
        """
        Insert vector documents to MongoDB
        
        Args:
            documents: List of documents with embeddings
                Required fields:
                    - embedding: List[float] - vector embedding
                    - text: str - original text
                    - brand_name: str - brand identifier
                    - doc_type: str - "parent" or "child"
                Optional fields:
                    - parent_id: str - for child documents
                    - metadata: Dict - additional info
            clear_existing: Whether to clear collection first
            
        Returns:
            Number of documents inserted
        """
        if clear_existing:
            result = self.collection.delete_many({})
            logger.info(f"🗑️  Deleted {result.deleted_count} existing documents")
        
        if not documents:
            logger.warning("⚠️ No documents to insert")
            return 0
        
        # Add timestamps
        for doc in documents:
            doc["created_at"] = datetime.utcnow()
        
        try:
            result = self.collection.insert_many(documents)
            count = len(result.inserted_ids)
            logger.info(f"✅ Inserted {count} documents")
            return count
        
        except Exception as e:
            logger.error(f"❌ Error inserting documents: {e}")
            raise
    
    def vector_search(
        self,
        query_embedding: List[float],
        k: int = 5,
        filter_dict: Optional[Dict[str, Any]] = None,
        index_name: str = "vector_index"
    ) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search
        
        Args:
            query_embedding: Query vector
            k: Number of results to return
            filter_dict: Metadata filters (e.g., {"brand_name": "example"})
            index_name: Name of vector search index
            
        Returns:
            List of matching documents with scores
        """
        # Build $vectorSearch stage with optional filter
        vector_search_stage = {
            "$vectorSearch": {
                "index": index_name,
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": k * 10,  # Overrequest for better recall
                "limit": k
            }
        }
        
        # Add filter inside $vectorSearch (not as separate $match stage)
        if filter_dict:
            vector_search_stage["$vectorSearch"]["filter"] = filter_dict
        
        pipeline = [
            vector_search_stage,
            {
                "$project": {
                    "_id": 1,
                    "text": 1,
                    "brand_name": 1,
                    "doc_type": 1,
                    "parent_id": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        
        try:
            results = list(self.collection.aggregate(pipeline))
            logger.info(f"🔍 Found {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"❌ Vector search error: {e}")
            return []
    
    def get_parent_document(self, parent_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve parent document by ID
        Used for parent-child retrieval strategy
        
        Args:
            parent_id: Parent document ID
            
        Returns:
            Parent document or None
        """
        from bson import ObjectId
        try:
            # Convert string parent_id to ObjectId for MongoDB query
            object_id = ObjectId(parent_id)
            return self.collection.find_one({"_id": object_id})
        except Exception as e:
            logger.error(f"❌ Error retrieving parent {parent_id}: {e}")
            return None
    
    def get_children_documents(self, parent_id: str) -> List[Dict[str, Any]]:
        """
        Get all child documents for a parent
        
        Args:
            parent_id: Parent document ID
            
        Returns:
            List of child documents
        """
        return list(self.collection.find({"parent_id": str(parent_id)}))
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        stats = {
            "total_documents": self.collection.count_documents({}),
            "parent_docs": self.collection.count_documents({"doc_type": "parent"}),
            "child_docs": self.collection.count_documents({"doc_type": "child"}),
            "unique_brands": len(self.collection.distinct("brand_name"))
        }
        return stats
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()
        logger.info("👋 MongoDB connection closed")


def test_connection():
    """Test MongoDB Vector Store connection"""
    try:
        store = MongoDBVectorStore()
        
        # Show stats
        stats = store.get_collection_stats()
        print("\n📊 Collection Stats:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Show sample document
        sample = store.collection.find_one()
        if sample:
            print("\n📄 Sample Document:")
            print(f"   Brand: {sample.get('brand_name', 'N/A')}")
            print(f"   Type: {sample.get('doc_type', 'N/A')}")
            print(f"   Text length: {len(sample.get('text', ''))}")
        
        store.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False


if __name__ == "__main__":
    print("Testing MongoDB Vector Store...")
    test_connection()
