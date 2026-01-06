"""
Hybrid Retriever: Vector Search + BM25 Keyword Search
Combines semantic similarity with keyword matching for best retrieval quality
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional, Tuple
import time
from collections import defaultdict

from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from module5.embedding_models import get_embedder
from module5.mongodb_vector import MongoDBVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download NLTK data if needed
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)


class HybridRetriever:
    """
    Hybrid Retrieval Strategy: Vector Search + BM25
    
    How it works:
    1. Vector Search: Find semantically similar documents
    2. BM25 Search: Find keyword-matched documents
    3. Reciprocal Rank Fusion (RRF): Combine and re-rank results
    
    Benefits:
    - Best of both worlds: semantic + exact match
    - Better handling of specific terms/names
    - More robust retrieval
    
    Use cases:
    - Queries with specific product names
    - Mixed semantic + keyword queries
    - When exact match matters
    """
    
    def __init__(
        self,
        embedder_type: str = "sentence-transformers",
        vector_store: Optional[MongoDBVectorStore] = None,
        bm25_weight: float = 0.5,
        vector_weight: float = 0.5
    ):
        """
        Args:
            embedder_type: Type of embedder to use
            vector_store: Existing vector store (or create new)
            bm25_weight: Weight for BM25 scores (0-1)
            vector_weight: Weight for vector scores (0-1)
        """
        self.embedder = get_embedder(embedder_type)
        self.vector_store = vector_store or MongoDBVectorStore()
        self.bm25_weight = bm25_weight
        self.vector_weight = vector_weight
        
        # BM25 index (will be built from MongoDB documents)
        self.bm25_index = None
        self.documents = []
        self.doc_ids = []
        
        logger.info(f"🔍 Initialized HybridRetriever")
        logger.info(f"   Embedder: {self.embedder}")
        logger.info(f"   Weights: Vector={vector_weight}, BM25={bm25_weight}")
    
    def build_bm25_index(self, doc_type: str = "child"):
        """
        Build BM25 index from MongoDB documents
        
        Args:
            doc_type: Type of documents to index ("child" or "parent")
        """
        logger.info(f"🔨 Building BM25 index for {doc_type} documents...")
        
        # Fetch all documents
        docs = list(self.vector_store.collection.find({"doc_type": doc_type}))
        
        if not docs:
            logger.warning("⚠️ No documents found for BM25 indexing")
            return
        
        # Tokenize documents
        tokenized_corpus = []
        self.documents = []
        self.doc_ids = []
        
        for doc in docs:
            text = doc.get("text", "")
            # Tokenize (lowercase, split by words)
            tokens = word_tokenize(text.lower())
            tokenized_corpus.append(tokens)
            self.documents.append(doc)
            self.doc_ids.append(str(doc.get("_id")))
        
        # Build BM25 index
        self.bm25_index = BM25Okapi(tokenized_corpus)
        
        logger.info(f"✅ BM25 index built with {len(self.documents)} documents")
    
    def bm25_search(
        self,
        query: str,
        k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        BM25 keyword search
        
        Args:
            query: Search query
            k: Number of results
            filter_dict: Metadata filters
            
        Returns:
            List of (document, score) tuples
        """
        if self.bm25_index is None:
            logger.warning("⚠️ BM25 index not built, building now...")
            self.build_bm25_index()
        
        # Tokenize query
        query_tokens = word_tokenize(query.lower())
        
        # Get BM25 scores
        scores = self.bm25_index.get_scores(query_tokens)
        
        # Get top-k results
        top_indices = scores.argsort()[-k:][::-1]
        
        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            score = float(scores[idx])
            
            # Apply filters
            if filter_dict:
                match = all(doc.get(key) == value for key, value in filter_dict.items())
                if not match:
                    continue
            
            results.append((doc, score))
        
        return results[:k]
    
    def vector_search(
        self,
        query: str,
        k: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Vector similarity search
        
        Args:
            query: Search query
            k: Number of results
            filter_dict: Metadata filters
            
        Returns:
            List of (document, score) tuples
        """
        # Embed query
        query_embedding = self.embedder.embed_text(query)
        
        # Vector search
        results = self.vector_store.vector_search(
            query_embedding=query_embedding,
            k=k,
            filter_dict=filter_dict
        )
        
        # Convert to (doc, score) tuples
        return [(doc, doc.get("score", 0.0)) for doc in results]
    
    def reciprocal_rank_fusion(
        self,
        vector_results: List[Tuple[Dict[str, Any], float]],
        bm25_results: List[Tuple[Dict[str, Any], float]],
        k: int = 60
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Reciprocal Rank Fusion (RRF)
        
        RRF formula: score = sum(1 / (k + rank)) for each retrieval method
        
        Args:
            vector_results: Results from vector search
            bm25_results: Results from BM25 search
            k: RRF constant (typically 60)
            
        Returns:
            Fused and re-ranked results
        """
        # Build score maps
        rrf_scores = defaultdict(float)
        doc_map = {}
        
        # Vector results
        for rank, (doc, score) in enumerate(vector_results):
            doc_id = str(doc.get("_id"))
            rrf_scores[doc_id] += self.vector_weight * (1.0 / (k + rank + 1))
            doc_map[doc_id] = doc
        
        # BM25 results
        for rank, (doc, score) in enumerate(bm25_results):
            doc_id = str(doc.get("_id"))
            rrf_scores[doc_id] += self.bm25_weight * (1.0 / (k + rank + 1))
            if doc_id not in doc_map:
                doc_map[doc_id] = doc
        
        # Sort by RRF score
        sorted_items = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return documents with scores
        results = [(doc_map[doc_id], score) for doc_id, score in sorted_items]
        
        return results
    
    def retrieve(
        self,
        query: str,
        k: int = 3,
        brand_filter: Optional[str] = None,
        return_scores: bool = False,
        method: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval: Vector + BM25 + RRF
        
        Args:
            query: Search query
            k: Number of parent documents to return
            brand_filter: Filter by specific brand name
            return_scores: Include relevance scores
            method: "hybrid", "vector", or "bm25"
            
        Returns:
            List of parent documents
        """
        start_time = time.time()
        
        logger.info(f"🔍 Hybrid retrieval: {query[:100]}...")
        logger.info(f"   Method: {method}, k={k}")
        
        # Build filters
        filter_dict = {"doc_type": "child"}
        if brand_filter:
            filter_dict["brand_name"] = brand_filter
        
        # Search based on method
        if method == "vector":
            # Vector only
            child_results = self.vector_search(query, k=k*3, filter_dict=filter_dict)
            
        elif method == "bm25":
            # BM25 only
            child_results = self.bm25_search(query, k=k*3, filter_dict=filter_dict)
            
        else:  # hybrid
            # Both searches
            vector_results = self.vector_search(query, k=k*3, filter_dict=filter_dict)
            bm25_results = self.bm25_search(query, k=k*3, filter_dict=filter_dict)
            
            # Fuse results
            child_results = self.reciprocal_rank_fusion(
                vector_results=vector_results,
                bm25_results=bm25_results,
                k=60
            )
        
        if not child_results:
            logger.warning("⚠️ No matching children found")
            return []
        
        logger.info(f"   Found {len(child_results)} matching child chunks")
        
        # Fetch unique parent documents
        seen_parents = set()
        parent_docs = []
        child_scores = {}
        
        for child, score in child_results:
            parent_id = child.get("parent_id")
            if not parent_id or parent_id in seen_parents:
                continue
            
            # Fetch parent document
            parent_doc = self.vector_store.get_parent_document(parent_id)
            if parent_doc:
                # Track best score
                if parent_id not in child_scores or score > child_scores[parent_id]:
                    child_scores[parent_id] = score
                
                if return_scores:
                    parent_doc["relevance_score"] = score
                    parent_doc["matched_child_text"] = child.get("text", "")
                
                parent_docs.append(parent_doc)
                seen_parents.add(parent_id)
                
                if len(parent_docs) >= k:
                    break
        
        # Sort by relevance score
        if return_scores and child_scores:
            parent_docs.sort(
                key=lambda x: child_scores.get(str(x.get("_id")), 0.0),
                reverse=True
            )
        
        elapsed = time.time() - start_time
        logger.info(f"✅ Retrieved {len(parent_docs)} parent documents in {elapsed:.3f}s")
        
        return parent_docs
    
    def close(self):
        """Clean up resources"""
        self.vector_store.close()


class HybridProductionRAG:
    """
    Production-ready Hybrid RAG compatible with Module 4 interface
    
    Drop-in replacement for Module 4's simple RAG:
    - Module 4: rag = SimpleRAG(brands_file)
    - Module 5: rag = HybridProductionRAG()
    """
    
    def __init__(
        self,
        embedder_type: str = "sentence-transformers",
        mongo_uri: Optional[str] = None,
        bm25_weight: float = 0.5,
        vector_weight: float = 0.5
    ):
        """
        Args:
            embedder_type: "sentence-transformers" or "openai"
            mongo_uri: MongoDB connection URI (default from env)
            bm25_weight: Weight for BM25 scores
            vector_weight: Weight for vector scores
        """
        # Get MongoDB URI
        if mongo_uri is None:
            mongo_uri = os.environ.get("MONGO_URI")
            if not mongo_uri:
                raise ValueError("MONGO_URI environment variable not set")
        
        # Initialize vector store
        vector_store = MongoDBVectorStore(
            connection_string=mongo_uri,
            database_name="ai_director",
            collection_name="brand_vectors"
        )
        
        # Initialize hybrid retriever
        self.retriever = HybridRetriever(
            embedder_type=embedder_type,
            vector_store=vector_store,
            bm25_weight=bm25_weight,
            vector_weight=vector_weight
        )
        
        # Build BM25 index
        self.retriever.build_bm25_index()
    
    def retrieve(
        self,
        query: str,
        k: int = 3,
        brand_filter: Optional[str] = None,
        method: str = "hybrid"
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant brand information
        
        Args:
            query: Natural language query or brand name
            k: Number of results to return
            brand_filter: Filter by specific brand name
            method: "hybrid", "vector", or "bm25"
            
        Returns:
            List of brand documents with context
        """
        return self.retriever.retrieve(
            query=query,
            k=k,
            brand_filter=brand_filter,
            return_scores=True,
            method=method
        )
    
    def close(self):
        """Clean up resources"""
        self.retriever.close()
