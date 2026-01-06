"""
Module 5: Production RAG System with Vector Database
Advanced retrieval strategies: Parent-Child, Contextual, Hybrid Search
"""

__version__ = "1.0.0"

from .embedding_models import get_embedder, SentenceTransformerEmbedder
from .mongodb_vector import MongoDBVectorStore
from .parent_child_retriever import ParentChildRetriever, ProductionRAG
from .hybrid_retriever import HybridRetriever, HybridProductionRAG

__all__ = [
    "get_embedder",
    "SentenceTransformerEmbedder",
    "MongoDBVectorStore",
    "ParentChildRetriever",
    "ProductionRAG",
    "HybridRetriever",
    "HybridProductionRAG",
]
