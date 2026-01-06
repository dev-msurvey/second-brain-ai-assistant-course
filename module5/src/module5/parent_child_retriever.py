"""
Parent-Child Retriever for Module 5
Search small chunks (children) for precision, return full documents (parents) for context
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from module5.embedding_models import get_embedder
from module5.mongodb_vector import MongoDBVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParentChildRetriever:
    """
    Parent-Child Retrieval Strategy
    
    How it works:
    1. User query → Embed query
    2. Vector search on CHILD documents (small chunks, precise matches)
    3. For each matching child, fetch its PARENT document
    4. Return unique parent documents (full context)
    
    Benefits:
    - Precise matching (small chunks)
    - Rich context (full documents)
    - Better than chunking alone
    """
    
    def __init__(
        self,
        embedder_type: str = "sentence-transformers",
        vector_store: Optional[MongoDBVectorStore] = None
    ):
        """
        Args:
            embedder_type: Type of embedder to use
            vector_store: Existing vector store (or create new)
        """
        self.embedder = get_embedder(embedder_type)
        self.vector_store = vector_store or MongoDBVectorStore()
        
        logger.info(f"🔍 Initialized ParentChildRetriever")
        logger.info(f"   Embedder: {self.embedder}")
    
    def retrieve(
        self,
        query: str,
        k: int = 3,
        brand_filter: Optional[str] = None,
        return_scores: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents using parent-child strategy
        
        Args:
            query: Search query
            k: Number of parent documents to return
            brand_filter: Filter by specific brand name
            return_scores: Include relevance scores
            
        Returns:
            List of parent documents with full context
        """
        start_time = time.time()
        
        # 1. Embed query
        query_embedding = self.embedder.embed_text(query)
        logger.info(f"🔍 Query: {query[:100]}...")
        
        # 2. Search CHILD documents (with higher k to ensure enough parents)
        search_k = k * 3  # Over-request children to get k unique parents
        filter_dict = {"doc_type": "child"}
        if brand_filter:
            filter_dict["brand_name"] = brand_filter
        
        child_results = self.vector_store.vector_search(
            query_embedding=query_embedding,
            k=search_k,
            filter_dict=filter_dict
        )
        
        if not child_results:
            logger.warning("⚠️ No matching children found")
            return []
        
        logger.info(f"   Found {len(child_results)} matching child chunks")
        
        # 3. Fetch unique parent documents
        seen_parents = set()
        parent_docs = []
        child_scores = {}  # Track best score for each parent
        
        for child in child_results:
            parent_id = child.get("parent_id")
            if not parent_id or parent_id in seen_parents:
                continue
            
            # Fetch parent document
            parent_doc = self.vector_store.get_parent_document(parent_id)
            if parent_doc:
                # Track best (highest) score from children
                child_score = child.get("score", 0.0)
                if parent_id not in child_scores or child_score > child_scores[parent_id]:
                    child_scores[parent_id] = child_score
                
                # Add score to parent if requested
                if return_scores:
                    parent_doc["relevance_score"] = child_score
                    parent_doc["matched_child_text"] = child.get("text", "")
                
                parent_docs.append(parent_doc)
                seen_parents.add(parent_id)
                
                # Stop when we have enough parents
                if len(parent_docs) >= k:
                    break
        
        # Sort by relevance score (if available)
        if return_scores and child_scores:
            parent_docs.sort(
                key=lambda x: child_scores.get(str(x.get("_id")), 0.0),
                reverse=True
            )
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Retrieved {len(parent_docs)} parent documents in {elapsed:.3f}s")
        
        return parent_docs
    
    def retrieve_with_children(
        self,
        query: str,
        k: int = 3,
        brand_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve parents along with their matching children
        Useful for understanding which parts of the document matched
        
        Args:
            query: Search query
            k: Number of results
            brand_filter: Filter by brand
            
        Returns:
            List of dicts with 'parent' and 'matching_children' keys
        """
        # Embed query
        query_embedding = self.embedder.embed_text(query)
        
        # Search children
        filter_dict = {"doc_type": "child"}
        if brand_filter:
            filter_dict["brand_name"] = brand_filter
        
        child_results = self.vector_store.vector_search(
            query_embedding=query_embedding,
            k=k * 3,
            filter_dict=filter_dict
        )
        
        # Group children by parent
        parent_children_map = {}
        for child in child_results:
            parent_id = child.get("parent_id")
            if parent_id not in parent_children_map:
                parent_children_map[parent_id] = []
            parent_children_map[parent_id].append(child)
        
        # Fetch parents and combine with children
        results = []
        for parent_id, children in list(parent_children_map.items())[:k]:
            parent_doc = self.vector_store.get_parent_document(parent_id)
            if parent_doc:
                results.append({
                    "parent": parent_doc,
                    "matching_children": children,
                    "num_matches": len(children),
                    "best_score": max(c.get("score", 0.0) for c in children)
                })
        
        # Sort by best score
        results.sort(key=lambda x: x["best_score"], reverse=True)
        
        return results
    
    def close(self):
        """Clean up resources"""
        self.vector_store.close()


class ProductionRAG:
    """
    Production-ready RAG system using parent-child retrieval
    Drop-in replacement for Module 4's SimpleRAG
    """
    
    def __init__(
        self,
        embedder_type: str = "sentence-transformers"
    ):
        """
        Args:
            embedder_type: Type of embedder
        """
        self.retriever = ParentChildRetriever(embedder_type=embedder_type)
        logger.info("🚀 Initialized ProductionRAG with parent-child retrieval")
    
    def retrieve(
        self,
        query: str,
        brand_name: Optional[str] = None,
        k: int = 3
    ) -> List[str]:
        """
        Retrieve relevant brand information
        Compatible with Module 4's inference interface
        
        Args:
            query: Search query or instruction
            brand_name: Optional brand filter
            k: Number of results
            
        Returns:
            List of relevant text chunks
        """
        # Retrieve parent documents
        results = self.retriever.retrieve(
            query=query,
            k=k,
            brand_filter=brand_name,
            return_scores=True
        )
        
        # Extract text from parents
        texts = []
        for doc in results:
            text = doc.get("text", "")
            if text:
                # Add brand context
                brand = doc.get("brand_name", "")
                score = doc.get("relevance_score", 0.0)
                texts.append(f"[Brand: {brand}, Score: {score:.3f}]\n{text}")
        
        return texts
    
    def retrieve_for_brand(
        self,
        brand_name: str,
        instruction: Optional[str] = None
    ) -> str:
        """
        Get brand information (compatible with Module 4)
        
        Args:
            brand_name: Brand to retrieve
            instruction: Optional instruction/query
            
        Returns:
            Brand information as string
        """
        query = instruction or f"information about {brand_name}"
        results = self.retrieve(query=query, brand_name=brand_name, k=1)
        
        if results:
            return results[0]
        else:
            return f"No information found for brand: {brand_name}"
    
    def close(self):
        """Clean up"""
        self.retriever.close()


def test_retriever():
    """Test parent-child retriever"""
    retriever = ParentChildRetriever()
    
    # Test queries
    test_queries = [
        "luxury fashion brands with elegant tone",
        "technology startups targeting millennials",
        "eco-friendly sustainable brands",
        "brands with blue and white colors"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print('='*60)
        
        results = retriever.retrieve(query=query, k=2, return_scores=True)
        
        for i, doc in enumerate(results, 1):
            print(f"\n{i}. {doc.get('brand_name', 'Unknown')}")
            print(f"   Score: {doc.get('relevance_score', 0.0):.3f}")
            print(f"   Text preview: {doc.get('text', '')[:200]}...")
            if doc.get('matched_child_text'):
                print(f"   Matched chunk: {doc['matched_child_text'][:150]}...")
    
    retriever.close()


if __name__ == "__main__":
    print("Testing Parent-Child Retriever...")
    test_retriever()
