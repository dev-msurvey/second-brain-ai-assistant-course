"""
Test Hybrid Retrieval: Vector + BM25
Compare Vector-only vs BM25-only vs Hybrid
"""

import os
import sys
import time
import argparse
import logging
from typing import List, Dict, Any
import statistics

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from module5.hybrid_retriever import HybridRetriever, HybridProductionRAG
from module5.mongodb_vector import MongoDBVectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HybridBenchmark:
    """Benchmark Hybrid Retrieval performance"""
    
    def __init__(self):
        # MongoDB URI from environment
        mongo_uri = os.environ.get(
            "MONGO_URI",
            "mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?appName=ai-director"
        )
        
        # Initialize vector store
        vector_store = MongoDBVectorStore(
            connection_string=mongo_uri,
            database_name="ai_director",
            collection_name="brand_vectors"
        )
        
        # Initialize hybrid retriever
        self.retriever = HybridRetriever(vector_store=vector_store)
        
        # Build BM25 index
        print("🔨 Building BM25 index...")
        self.retriever.build_bm25_index()
        print("✅ BM25 index ready\n")
    
    def create_test_queries(self) -> List[Dict[str, Any]]:
        """Create diverse test queries"""
        return [
            {
                "query": "luxury fashion brand with elegant design",
                "type": "semantic",
                "description": "Semantic query (should favor vector)"
            },
            {
                "query": "CoffeeLab specialty coffee",
                "type": "keyword",
                "description": "Exact brand name (should favor BM25)"
            },
            {
                "query": "sustainable eco-friendly green brand",
                "type": "keyword_heavy",
                "description": "Multiple keywords (should favor BM25)"
            },
            {
                "query": "modern technology startup for millennials",
                "type": "semantic",
                "description": "Semantic audience query"
            },
            {
                "query": "FitFlow fitness workout training",
                "type": "keyword",
                "description": "Brand + keywords"
            },
            {
                "query": "premium high-end sophisticated brand",
                "type": "mixed",
                "description": "Mixed semantic + keywords"
            },
            {
                "query": "GlowLab natural skincare beauty",
                "type": "keyword",
                "description": "Brand + product keywords"
            },
            {
                "query": "family-oriented traditional values",
                "type": "semantic",
                "description": "Semantic values query"
            },
        ]
    
    def test_method(
        self,
        query: str,
        method: str,
        k: int = 3
    ) -> Dict[str, Any]:
        """
        Test single retrieval method
        
        Args:
            query: Search query
            method: "vector", "bm25", or "hybrid"
            k: Number of results
            
        Returns:
            Results dict with timing and brands
        """
        start_time = time.time()
        
        results = self.retriever.retrieve(
            query=query,
            k=k,
            return_scores=True,
            method=method
        )
        
        elapsed = time.time() - start_time
        
        # Extract brands and scores
        brands = []
        scores = []
        for doc in results:
            brand_name = doc.get("brand_name", "Unknown")
            score = doc.get("relevance_score", 0.0)
            brands.append(brand_name)
            scores.append(score)
        
        return {
            "brands": brands,
            "scores": scores,
            "latency_ms": elapsed * 1000,
            "num_results": len(results)
        }
    
    def compare_methods(
        self,
        test_case: Dict[str, Any],
        k: int = 3
    ) -> Dict[str, Any]:
        """
        Compare all three methods for a single query
        
        Args:
            test_case: Test case dict
            k: Number of results
            
        Returns:
            Comparison results
        """
        query = test_case["query"]
        
        # Test all methods
        vector_results = self.test_method(query, "vector", k)
        bm25_results = self.test_method(query, "bm25", k)
        hybrid_results = self.test_method(query, "hybrid", k)
        
        return {
            "query": query,
            "type": test_case["type"],
            "description": test_case["description"],
            "vector": vector_results,
            "bm25": bm25_results,
            "hybrid": hybrid_results
        }
    
    def run_benchmark(self, k: int = 3):
        """Run full benchmark suite"""
        print("=" * 80)
        print("🧪 HYBRID RETRIEVAL BENCHMARK")
        print("=" * 80)
        print(f"Comparing: Vector Search | BM25 | Hybrid (Vector + BM25)")
        print(f"Results per query (k): {k}\n")
        
        test_cases = self.create_test_queries()
        all_results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"[{i}/{len(test_cases)}] Testing: {test_case['query'][:60]}...")
            print(f"   Type: {test_case['type']} - {test_case['description']}")
            
            results = self.compare_methods(test_case, k)
            all_results.append(results)
            
            # Display results
            print(f"\n   📊 Results:")
            print(f"   Vector:  {', '.join(results['vector']['brands'][:3])}")
            print(f"            Latency: {results['vector']['latency_ms']:.1f}ms, "
                  f"Avg Score: {statistics.mean(results['vector']['scores']) if results['vector']['scores'] else 0:.3f}")
            
            print(f"   BM25:    {', '.join(results['bm25']['brands'][:3])}")
            print(f"            Latency: {results['bm25']['latency_ms']:.1f}ms, "
                  f"Avg Score: {statistics.mean(results['bm25']['scores']) if results['bm25']['scores'] else 0:.3f}")
            
            print(f"   Hybrid:  {', '.join(results['hybrid']['brands'][:3])}")
            print(f"            Latency: {results['hybrid']['latency_ms']:.1f}ms, "
                  f"Avg Score: {statistics.mean(results['hybrid']['scores']) if results['hybrid']['scores'] else 0:.3f}")
            print()
        
        # Summary statistics
        print("=" * 80)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 80)
        
        # Calculate average latencies
        vector_latencies = [r['vector']['latency_ms'] for r in all_results]
        bm25_latencies = [r['bm25']['latency_ms'] for r in all_results]
        hybrid_latencies = [r['hybrid']['latency_ms'] for r in all_results]
        
        print(f"\n⏱️  Average Latency:")
        print(f"   Vector:  {statistics.mean(vector_latencies):.1f}ms")
        print(f"   BM25:    {statistics.mean(bm25_latencies):.1f}ms")
        print(f"   Hybrid:  {statistics.mean(hybrid_latencies):.1f}ms")
        
        # Calculate result overlap
        print(f"\n🎯 Result Agreement (how often methods agree on top result):")
        vector_bm25_agreement = sum(
            1 for r in all_results 
            if r['vector']['brands'] and r['bm25']['brands'] 
            and r['vector']['brands'][0] == r['bm25']['brands'][0]
        ) / len(all_results) * 100
        
        vector_hybrid_agreement = sum(
            1 for r in all_results 
            if r['vector']['brands'] and r['hybrid']['brands']
            and r['vector']['brands'][0] == r['hybrid']['brands'][0]
        ) / len(all_results) * 100
        
        bm25_hybrid_agreement = sum(
            1 for r in all_results 
            if r['bm25']['brands'] and r['hybrid']['brands']
            and r['bm25']['brands'][0] == r['hybrid']['brands'][0]
        ) / len(all_results) * 100
        
        print(f"   Vector ↔ BM25:    {vector_bm25_agreement:.1f}%")
        print(f"   Vector ↔ Hybrid:  {vector_hybrid_agreement:.1f}%")
        print(f"   BM25 ↔ Hybrid:    {bm25_hybrid_agreement:.1f}%")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        print(f"   • Use Vector for semantic/conceptual queries")
        print(f"   • Use BM25 for exact brand names or keywords")
        print(f"   • Use Hybrid for best overall quality (recommended)")
        print()
        print("=" * 80)
        
        self.retriever.close()


def test_basic():
    """Quick basic test"""
    print("=" * 80)
    print("🧪 BASIC HYBRID RETRIEVAL TEST")
    print("=" * 80)
    
    # Initialize
    rag = HybridProductionRAG()
    
    # Test query
    query = "luxury fashion brand with elegant design"
    print(f"Query: {query}")
    print("-" * 80)
    
    # Test all methods
    for method in ["vector", "bm25", "hybrid"]:
        print(f"\n{method.upper()} Results:")
        results = rag.retrieve(query, k=3, method=method)
        
        for i, doc in enumerate(results, 1):
            brand = doc.get("brand_name", "Unknown")
            score = doc.get("relevance_score", 0.0)
            text_preview = doc.get("text", "")[:150]
            
            print(f"{i}. {brand} (score: {score:.3f})")
            print(f"   {text_preview}...")
            print()
    
    rag.close()
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Test Hybrid Retrieval")
    parser.add_argument(
        "--test",
        choices=["basic", "benchmark"],
        default="basic",
        help="Test type to run"
    )
    parser.add_argument(
        "-k",
        type=int,
        default=3,
        help="Number of results per query"
    )
    
    args = parser.parse_args()
    
    try:
        if args.test == "basic":
            test_basic()
        elif args.test == "benchmark":
            benchmark = HybridBenchmark()
            benchmark.run_benchmark(k=args.k)
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
