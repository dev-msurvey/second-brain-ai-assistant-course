"""
Parent-Child Ingestion Pipeline for Module 5
Loads brand data, creates chunks, establishes parent-child relationships, and stores with embeddings
"""

import os
import sys
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
from bson import ObjectId
import re

# Add module paths
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from module5.embedding_models import get_embedder
from module5.mongodb_vector import MongoDBVectorStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextChunker:
    """
    Split text into chunks for parent-child retrieval
    Small chunks = precise search, Parent docs = full context
    """
    
    def __init__(
        self,
        chunk_size: int = 256,
        chunk_overlap: int = 50,
        separators: List[str] = None
    ):
        """
        Args:
            chunk_size: Target size for each chunk (tokens/chars)
            chunk_overlap: Overlap between chunks for continuity
            separators: List of separators to split on (default: paragraph, sentence)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", "! ", "? ", ", "]
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        if not text or len(text) < self.chunk_size:
            return [text] if text else []
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Find end position
            end = start + self.chunk_size
            
            # If not at the end, try to break at separator
            if end < len(text):
                # Look for separator near the end
                best_break = end
                for separator in self.separators:
                    # Search backwards from end for separator
                    sep_pos = text.rfind(separator, start, end + 50)
                    if sep_pos > start:
                        best_break = sep_pos + len(separator)
                        break
                end = best_break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap if end < len(text) else end
        
        return chunks


class ParentChildIngestionPipeline:
    """
    Pipeline to ingest brand data with parent-child document structure
    
    Architecture:
        - Parent docs: Full brand information (for context)
        - Child docs: Small chunks with embeddings (for precise search)
        - Search children → Return parents
    """
    
    def __init__(
        self,
        embedder_type: str = "sentence-transformers",
        chunk_size: int = 256,
        chunk_overlap: int = 50
    ):
        """
        Args:
            embedder_type: "sentence-transformers" or "openai"
            chunk_size: Size of child chunks
            chunk_overlap: Overlap between chunks
        """
        self.embedder = get_embedder(embedder_type)
        self.chunker = TextChunker(chunk_size, chunk_overlap)
        self.vector_store = MongoDBVectorStore()
        
        logger.info(f"🚀 Initialized ingestion pipeline")
        logger.info(f"   Embedder: {self.embedder}")
        logger.info(f"   Chunk size: {chunk_size}, Overlap: {chunk_overlap}")
    
    def fetch_brands_from_mongodb(self) -> List[Dict[str, Any]]:
        """
        Fetch brand data from Module 2's MongoDB collection
        
        Returns:
            List of brand documents
        """
        try:
            # Connect to brands collection (from Module 2)
            brands_collection = self.vector_store.db["brands"]
            brands = list(brands_collection.find({}))
            
            logger.info(f"📥 Fetched {len(brands)} brands from MongoDB")
            return brands
            
        except Exception as e:
            logger.error(f"❌ Error fetching brands: {e}")
            return []
    
    def create_parent_document(
        self,
        brand: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create parent document with full brand information
        
        Args:
            brand: Brand data from Module 2
            
        Returns:
            Parent document
        """
        # Combine all brand information into comprehensive text
        parent_text_parts = []
        
        # Basic info
        if brand.get("name"):
            parent_text_parts.append(f"Brand Name: {brand['name']}")
        if brand.get("industry"):
            parent_text_parts.append(f"Industry: {brand['industry']}")
        if brand.get("description"):
            parent_text_parts.append(f"Description: {brand['description']}")
        
        # Target audience
        if brand.get("target_audience"):
            audience = brand["target_audience"]
            parent_text_parts.append(f"Target Audience: {audience.get('demographics', '')} - {audience.get('psychographics', '')}")
        
        # Tone and values
        if brand.get("tone_of_voice"):
            parent_text_parts.append(f"Tone of Voice: {brand['tone_of_voice']}")
        if brand.get("core_values"):
            values = ", ".join(brand["core_values"]) if isinstance(brand["core_values"], list) else brand["core_values"]
            parent_text_parts.append(f"Core Values: {values}")
        
        # Visual identity
        if brand.get("visual_identity"):
            visual = brand["visual_identity"]
            if visual.get("primary_colors"):
                colors = ", ".join(visual["primary_colors"]) if isinstance(visual["primary_colors"], list) else visual["primary_colors"]
                parent_text_parts.append(f"Primary Colors: {colors}")
            if visual.get("typography"):
                parent_text_parts.append(f"Typography: {visual['typography']}")
        
        # Messaging
        if brand.get("key_messaging"):
            messaging = brand["key_messaging"]
            if messaging.get("tagline"):
                parent_text_parts.append(f"Tagline: {messaging['tagline']}")
            if messaging.get("value_propositions"):
                props = messaging["value_propositions"]
                if isinstance(props, list):
                    parent_text_parts.append(f"Value Propositions: {', '.join(props)}")
        
        parent_text = "\n".join(parent_text_parts)
        
        # Create parent document (no embedding for parent)
        parent_doc = {
            "_id": ObjectId(),
            "brand_name": brand.get("name", "unknown"),
            "doc_type": "parent",
            "text": parent_text,
            "metadata": {
                "industry": brand.get("industry"),
                "target_audience": brand.get("target_audience"),
                "source": "module2_brands"
            },
            "original_brand_data": brand  # Keep original for reference
        }
        
        return parent_doc
    
    def create_child_documents(
        self,
        parent_doc: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Create child documents (chunks) from parent
        Each child gets an embedding
        
        Args:
            parent_doc: Parent document
            
        Returns:
            List of child documents
        """
        parent_text = parent_doc["text"]
        chunks = self.chunker.chunk_text(parent_text)
        
        logger.info(f"   Created {len(chunks)} chunks for {parent_doc['brand_name']}")
        
        # Generate embeddings for all chunks
        embeddings = self.embedder.embed_texts(chunks)
        
        # Create child documents
        child_docs = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            child_doc = {
                "_id": ObjectId(),
                "brand_name": parent_doc["brand_name"],
                "doc_type": "child",
                "parent_id": str(parent_doc["_id"]),
                "text": chunk,
                "embedding": embedding,
                "chunk_index": i,
                "metadata": parent_doc["metadata"]
            }
            child_docs.append(child_doc)
        
        return child_docs
    
    def process_brand(
        self,
        brand: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Process single brand: create parent + children
        
        Args:
            brand: Brand data
            
        Returns:
            Tuple of (parent_doc, child_docs)
        """
        parent_doc = self.create_parent_document(brand)
        child_docs = self.create_child_documents(parent_doc)
        return parent_doc, child_docs
    
    def run_ingestion(
        self,
        clear_existing: bool = True
    ) -> Dict[str, int]:
        """
        Run full ingestion pipeline
        
        Args:
            clear_existing: Clear existing vector data
            
        Returns:
            Statistics dictionary
        """
        logger.info("🚀 Starting parent-child ingestion pipeline...")
        
        # Fetch brands
        brands = self.fetch_brands_from_mongodb()
        if not brands:
            logger.error("❌ No brands found")
            return {"brands": 0, "parents": 0, "children": 0}
        
        # Process all brands
        all_documents = []
        parent_count = 0
        child_count = 0
        
        for brand in brands:
            try:
                parent_doc, child_docs = self.process_brand(brand)
                all_documents.append(parent_doc)
                all_documents.extend(child_docs)
                parent_count += 1
                child_count += len(child_docs)
                
                logger.info(f"✅ Processed: {brand.get('name', 'unknown')} → 1 parent + {len(child_docs)} children")
                
            except Exception as e:
                logger.error(f"❌ Error processing brand {brand.get('name')}: {e}")
                continue
        
        # Insert to MongoDB
        if all_documents:
            inserted = self.vector_store.insert_documents(all_documents, clear_existing=clear_existing)
            logger.info(f"\n✅ Ingestion complete!")
            logger.info(f"   Total documents: {inserted}")
            logger.info(f"   Parent docs: {parent_count}")
            logger.info(f"   Child docs: {child_count}")
            
            # Show stats
            stats = self.vector_store.get_collection_stats()
            logger.info(f"\n📊 Collection Stats:")
            for key, value in stats.items():
                logger.info(f"   {key}: {value}")
            
            return {
                "brands": len(brands),
                "parents": parent_count,
                "children": child_count,
                "total_inserted": inserted
            }
        
        return {"brands": 0, "parents": 0, "children": 0}
    
    def close(self):
        """Clean up resources"""
        self.vector_store.close()


def main():
    """Run ingestion pipeline"""
    pipeline = ParentChildIngestionPipeline(
        embedder_type="sentence-transformers",
        chunk_size=256,
        chunk_overlap=50
    )
    
    try:
        stats = pipeline.run_ingestion(clear_existing=True)
        
        print("\n" + "="*60)
        print("📊 INGESTION SUMMARY")
        print("="*60)
        print(f"Brands processed: {stats['brands']}")
        print(f"Parent documents: {stats['parents']}")
        print(f"Child documents: {stats['children']}")
        print(f"Total inserted: {stats['total_inserted']}")
        print("="*60)
        
    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
