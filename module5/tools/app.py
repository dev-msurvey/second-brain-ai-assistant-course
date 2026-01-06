"""
FastAPI Production API for Module 5 RAG System
REST API endpoints for vector search and content retrieval
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import time

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Add module5 to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from module5.parent_child_retriever import ProductionRAG
from module5.hybrid_retriever import HybridProductionRAG


# Pydantic models for request/response
class SearchRequest(BaseModel):
    """Search request payload"""
    query: str = Field(..., description="Search query", min_length=1)
    k: int = Field(3, description="Number of results", ge=1, le=10)
    brand_filter: Optional[str] = Field(None, description="Filter by brand name")
    method: str = Field("hybrid", description="Search method: vector, bm25, or hybrid")


class BrandContext(BaseModel):
    """Brand context response"""
    brand_name: str
    relevance_score: float
    text: str
    matched_chunk: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response payload"""
    query: str
    method: str
    results: List[BrandContext]
    latency_ms: float
    total_results: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    rag_system: str
    database: str


# Initialize FastAPI app
app = FastAPI(
    title="AI Director RAG API",
    description="Production RAG System with Vector Search and Hybrid Retrieval",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG instance
rag: Optional[HybridProductionRAG] = None


@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag
    
    print("🚀 Starting AI Director RAG API...")
    print("📦 Initializing Hybrid RAG system...")
    
    try:
        rag = HybridProductionRAG()
        print("✅ RAG system initialized successfully!")
        print("🔍 Vector Search: Ready")
        print("🔍 BM25 Search: Ready")
        print("🔍 Hybrid Search: Ready")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global rag
    
    if rag:
        print("👋 Shutting down RAG system...")
        rag.close()
        print("✅ Cleanup complete")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "service": "AI Director RAG API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if rag else "unhealthy",
        version="1.0.0",
        rag_system="Hybrid (Vector + BM25)",
        database="MongoDB Atlas"
    )


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search for relevant brand information
    
    - **query**: Search query (natural language)
    - **k**: Number of results (1-10)
    - **brand_filter**: Optional brand name filter
    - **method**: Search method (vector, bm25, or hybrid)
    """
    if not rag:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    # Validate method
    if request.method not in ["vector", "bm25", "hybrid"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid method: {request.method}. Must be: vector, bm25, or hybrid"
        )
    
    start_time = time.time()
    
    try:
        # Perform search
        results = rag.retrieve(
            query=request.query,
            k=request.k,
            brand_filter=request.brand_filter,
            method=request.method
        )
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Format results
        brand_contexts = []
        for doc in results:
            brand_contexts.append(
                BrandContext(
                    brand_name=doc.get("brand_name", "Unknown"),
                    relevance_score=doc.get("relevance_score", 0.0),
                    text=doc.get("text", ""),
                    matched_chunk=doc.get("matched_child_text")
                )
            )
        
        return SearchResponse(
            query=request.query,
            method=request.method,
            results=brand_contexts,
            latency_ms=round(latency_ms, 2),
            total_results=len(brand_contexts)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.get("/search/simple")
async def search_simple(
    query: str = Query(..., description="Search query"),
    k: int = Query(3, description="Number of results", ge=1, le=10),
    brand: Optional[str] = Query(None, description="Filter by brand name"),
    method: str = Query("hybrid", description="Search method")
):
    """
    Simple GET endpoint for search
    
    Example: /search/simple?query=luxury+coffee&k=3&method=hybrid
    """
    request = SearchRequest(
        query=query,
        k=k,
        brand_filter=brand,
        method=method
    )
    
    return await search(request)


@app.get("/brands")
async def list_brands():
    """List all available brands in the database"""
    if not rag:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        # Get collection stats
        stats = rag.retriever.vector_store.get_collection_stats()
        
        # Get unique brands
        brands = list(rag.retriever.vector_store.collection.distinct("brand_name"))
        
        return {
            "brands": sorted(brands),
            "total_brands": len(brands),
            "total_documents": stats.get("total_documents", 0),
            "parent_documents": stats.get("parent_docs", 0),
            "child_documents": stats.get("child_docs", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list brands: {str(e)}")


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    if not rag:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        stats = rag.retriever.vector_store.get_collection_stats()
        
        return {
            "database": "MongoDB Atlas",
            "collection": "brand_vectors",
            "total_documents": stats.get("total_documents", 0),
            "parent_documents": stats.get("parent_docs", 0),
            "child_documents": stats.get("child_docs", 0),
            "unique_brands": stats.get("unique_brands", 0),
            "search_methods": ["vector", "bm25", "hybrid"],
            "embedding_model": "all-MiniLM-L6-v2",
            "embedding_dimensions": 384
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


def main():
    """Run the API server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Director RAG API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚀 AI DIRECTOR RAG API")
    print("=" * 60)
    print(f"📡 Starting server on http://{args.host}:{args.port}")
    print(f"📖 API Documentation: http://{args.host}:{args.port}/docs")
    print(f"🔍 Health Check: http://{args.host}:{args.port}/health")
    print("=" * 60)
    
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
