"""
Evaluation Script for Module 5 RAG System
Evaluates retrieval quality with various metrics
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import statistics
import json
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from module5.hybrid_retriever import HybridProductionRAG


class RAGEvaluator:
    """
    Evaluate RAG retrieval quality
    
    Metrics:
    - Precision@K: Relevant results / Retrieved results
    - Recall@K: Relevant results / Total relevant
    - MRR (Mean Reciprocal Rank): Average 1/rank of first relevant result
    - NDCG (Normalized Discounted Cumulative Gain): Ranking quality
    - Latency: Response time
    """
    
    def __init__(self):
        print("🔍 Initializing RAG Evaluator...")
        self.rag = HybridProductionRAG()
        print("✅ RAG system ready\n")
    
    def get_test_cases(self) -> List[Dict[str, Any]]:
        """
        Create test cases with ground truth
        
        Returns:
            List of test cases with queries and expected brands
        """
        return [
            {
                "query": "specialty coffee brand for young professionals",
                "expected_brands": ["CoffeeLab"],
                "category": "product_search",
                "difficulty": "easy"
            },
            {
                "query": "modern fitness center with technology",
                "expected_brands": ["FitFlow"],
                "category": "product_search",
                "difficulty": "easy"
            },
            {
                "query": "natural skincare with Thai ingredients",
                "expected_brands": ["GlowLab"],
                "category": "product_search",
                "difficulty": "medium"
            },
            {
                "query": "eco-friendly sustainable green brand",
                "expected_brands": ["GreenLeaf", "CoffeeLab"],
                "category": "values_search",
                "difficulty": "medium"
            },
            {
                "query": "minimalist Scandinavian furniture for urban millennials",
                "expected_brands": ["UrbanNest"],
                "category": "style_search",
                "difficulty": "medium"
            },
            {
                "query": "technology startup for professionals",
                "expected_brands": ["TechZone", "FitFlow"],
                "category": "audience_search",
                "difficulty": "medium"
            },
            {
                "query": "brand with blue and white color scheme",
                "expected_brands": ["FitFlow", "TechZone"],
                "category": "visual_search",
                "difficulty": "hard"
            },
            {
                "query": "family-oriented traditional values",
                "expected_brands": ["PetPals", "EduKid"],
                "category": "values_search",
                "difficulty": "hard"
            },
            {
                "query": "premium affordable luxury design",
                "expected_brands": ["UrbanNest", "CoffeeLab"],
                "category": "positioning_search",
                "difficulty": "hard"
            },
            {
                "query": "educational content for children",
                "expected_brands": ["EduKid"],
                "category": "product_search",
                "difficulty": "easy"
            }
        ]
    
    def calculate_precision_at_k(
        self,
        retrieved: List[str],
        relevant: List[str],
        k: int
    ) -> float:
        """
        Precision@K = (# relevant results in top-K) / K
        
        Args:
            retrieved: List of retrieved brand names
            relevant: List of relevant brand names (ground truth)
            k: Number of top results to consider
            
        Returns:
            Precision score (0-1)
        """
        if not retrieved or k == 0:
            return 0.0
        
        retrieved_at_k = set(retrieved[:k])
        relevant_set = set(relevant)
        
        relevant_retrieved = retrieved_at_k & relevant_set
        
        return len(relevant_retrieved) / k
    
    def calculate_recall_at_k(
        self,
        retrieved: List[str],
        relevant: List[str],
        k: int
    ) -> float:
        """
        Recall@K = (# relevant results in top-K) / (# total relevant)
        
        Args:
            retrieved: List of retrieved brand names
            relevant: List of relevant brand names (ground truth)
            k: Number of top results to consider
            
        Returns:
            Recall score (0-1)
        """
        if not relevant:
            return 0.0
        
        retrieved_at_k = set(retrieved[:k])
        relevant_set = set(relevant)
        
        relevant_retrieved = retrieved_at_k & relevant_set
        
        return len(relevant_retrieved) / len(relevant_set)
    
    def calculate_mrr(
        self,
        retrieved: List[str],
        relevant: List[str]
    ) -> float:
        """
        Mean Reciprocal Rank = 1 / (rank of first relevant result)
        
        Args:
            retrieved: List of retrieved brand names
            relevant: List of relevant brand names (ground truth)
            
        Returns:
            MRR score (0-1)
        """
        relevant_set = set(relevant)
        
        for rank, brand in enumerate(retrieved, 1):
            if brand in relevant_set:
                return 1.0 / rank
        
        return 0.0
    
    def calculate_ndcg_at_k(
        self,
        retrieved: List[str],
        relevant: List[str],
        k: int
    ) -> float:
        """
        Normalized Discounted Cumulative Gain@K
        Measures ranking quality
        
        Args:
            retrieved: List of retrieved brand names
            relevant: List of relevant brand names (ground truth)
            k: Number of top results to consider
            
        Returns:
            NDCG score (0-1)
        """
        def dcg(relevances: List[int]) -> float:
            """Calculate DCG"""
            return sum(
                (2**rel - 1) / (i + 2)  # i+2 because log2(1) = 0
                for i, rel in enumerate(relevances)
            )
        
        # Calculate relevance scores (1 if relevant, 0 if not)
        relevant_set = set(relevant)
        retrieved_relevances = [
            1 if brand in relevant_set else 0
            for brand in retrieved[:k]
        ]
        
        # Calculate DCG
        dcg_score = dcg(retrieved_relevances)
        
        # Calculate ideal DCG (best possible ranking)
        ideal_relevances = sorted([1] * len(relevant) + [0] * (k - len(relevant)), reverse=True)[:k]
        idcg_score = dcg(ideal_relevances)
        
        # Calculate NDCG
        if idcg_score == 0:
            return 0.0
        
        return dcg_score / idcg_score
    
    def evaluate_single_query(
        self,
        test_case: Dict[str, Any],
        method: str,
        k: int = 3
    ) -> Dict[str, Any]:
        """
        Evaluate single query
        
        Args:
            test_case: Test case dict
            method: Search method (vector, bm25, hybrid)
            k: Number of results
            
        Returns:
            Evaluation results
        """
        query = test_case["query"]
        expected_brands = test_case["expected_brands"]
        
        import time
        start_time = time.time()
        
        # Retrieve results
        results = self.rag.retrieve(query, k=k, method=method)
        
        latency_ms = (time.time() - start_time) * 1000
        
        # Extract brand names
        retrieved_brands = [doc.get("brand_name") for doc in results]
        
        # Calculate metrics
        precision = self.calculate_precision_at_k(retrieved_brands, expected_brands, k)
        recall = self.calculate_recall_at_k(retrieved_brands, expected_brands, k)
        mrr = self.calculate_mrr(retrieved_brands, expected_brands)
        ndcg = self.calculate_ndcg_at_k(retrieved_brands, expected_brands, k)
        
        # F1 score
        if precision + recall > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0.0
        
        return {
            "query": query,
            "expected_brands": expected_brands,
            "retrieved_brands": retrieved_brands,
            "metrics": {
                "precision@k": precision,
                "recall@k": recall,
                "f1": f1,
                "mrr": mrr,
                "ndcg@k": ndcg,
                "latency_ms": latency_ms
            },
            "success": precision > 0  # At least one relevant result
        }
    
    def evaluate_all(
        self,
        methods: List[str] = ["vector", "bm25", "hybrid"],
        k: int = 3
    ) -> Dict[str, Any]:
        """
        Evaluate all test cases for all methods
        
        Args:
            methods: List of search methods to evaluate
            k: Number of results per query
            
        Returns:
            Complete evaluation results
        """
        print("=" * 80)
        print("🧪 RAG SYSTEM EVALUATION")
        print("=" * 80)
        print(f"Methods: {', '.join(methods)}")
        print(f"Results per query (k): {k}")
        print(f"Total test cases: {len(self.get_test_cases())}\n")
        
        test_cases = self.get_test_cases()
        all_results = defaultdict(list)
        
        for method in methods:
            print(f"\n{'=' * 80}")
            print(f"📊 Evaluating: {method.upper()}")
            print(f"{'=' * 80}\n")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"[{i}/{len(test_cases)}] {test_case['query'][:60]}...")
                
                result = self.evaluate_single_query(test_case, method, k)
                all_results[method].append(result)
                
                # Show result
                metrics = result["metrics"]
                success_icon = "✅" if result["success"] else "❌"
                print(f"   {success_icon} P@{k}={metrics['precision@k']:.2f}, "
                      f"R@{k}={metrics['recall@k']:.2f}, "
                      f"MRR={metrics['mrr']:.2f}, "
                      f"NDCG={metrics['ndcg@k']:.2f} "
                      f"({metrics['latency_ms']:.1f}ms)")
                print(f"   Retrieved: {', '.join(result['retrieved_brands'])}")
        
        # Calculate aggregate statistics
        print(f"\n\n{'=' * 80}")
        print("📈 AGGREGATE RESULTS")
        print(f"{'=' * 80}\n")
        
        summary = {}
        
        for method in methods:
            results = all_results[method]
            
            # Calculate averages
            avg_precision = statistics.mean(r["metrics"]["precision@k"] for r in results)
            avg_recall = statistics.mean(r["metrics"]["recall@k"] for r in results)
            avg_f1 = statistics.mean(r["metrics"]["f1"] for r in results)
            avg_mrr = statistics.mean(r["metrics"]["mrr"] for r in results)
            avg_ndcg = statistics.mean(r["metrics"]["ndcg@k"] for r in results)
            avg_latency = statistics.mean(r["metrics"]["latency_ms"] for r in results)
            success_rate = sum(1 for r in results if r["success"]) / len(results)
            
            summary[method] = {
                "precision@k": avg_precision,
                "recall@k": avg_recall,
                "f1": avg_f1,
                "mrr": avg_mrr,
                "ndcg@k": avg_ndcg,
                "latency_ms": avg_latency,
                "success_rate": success_rate
            }
            
            print(f"{method.upper()}:")
            print(f"  Precision@{k}: {avg_precision:.3f}")
            print(f"  Recall@{k}:    {avg_recall:.3f}")
            print(f"  F1 Score:      {avg_f1:.3f}")
            print(f"  MRR:           {avg_mrr:.3f}")
            print(f"  NDCG@{k}:      {avg_ndcg:.3f}")
            print(f"  Success Rate:  {success_rate:.1%}")
            print(f"  Avg Latency:   {avg_latency:.1f}ms")
            print()
        
        # Comparison
        print(f"{'=' * 80}")
        print("🏆 METHOD COMPARISON")
        print(f"{'=' * 80}\n")
        
        metrics_to_compare = ["precision@k", "recall@k", "f1", "mrr", "ndcg@k"]
        
        for metric in metrics_to_compare:
            print(f"{metric.upper().replace('_', ' ')}:")
            sorted_methods = sorted(
                methods,
                key=lambda m: summary[m][metric],
                reverse=True
            )
            for rank, method in enumerate(sorted_methods, 1):
                score = summary[method][metric]
                icon = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else "  "
                print(f"  {icon} {method:7s}: {score:.3f}")
            print()
        
        print("LATENCY:")
        sorted_by_latency = sorted(methods, key=lambda m: summary[m]["latency_ms"])
        for rank, method in enumerate(sorted_by_latency, 1):
            latency = summary[method]["latency_ms"]
            icon = "⚡" if rank == 1 else "  "
            print(f"  {icon} {method:7s}: {latency:.1f}ms")
        
        # Recommendations
        print(f"\n{'=' * 80}")
        print("💡 RECOMMENDATIONS")
        print(f"{'=' * 80}\n")
        
        best_quality = max(methods, key=lambda m: summary[m]["f1"])
        best_speed = min(methods, key=lambda m: summary[m]["latency_ms"])
        best_balanced = max(methods, key=lambda m: summary[m]["f1"] - summary[m]["latency_ms"]/1000)
        
        print(f"• Best Quality:  {best_quality.upper()} (F1: {summary[best_quality]['f1']:.3f})")
        print(f"• Best Speed:    {best_speed.upper()} ({summary[best_speed]['latency_ms']:.1f}ms)")
        print(f"• Best Balanced: {best_balanced.upper()}")
        print()
        
        return {
            "summary": summary,
            "detailed_results": dict(all_results),
            "test_cases": test_cases
        }
    
    def save_results(self, results: Dict[str, Any], output_file: str = "evaluation_results.json"):
        """Save evaluation results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
    
    def close(self):
        """Cleanup"""
        self.rag.close()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate RAG System Quality")
    parser.add_argument(
        "--methods",
        nargs="+",
        default=["vector", "bm25", "hybrid"],
        choices=["vector", "bm25", "hybrid"],
        help="Search methods to evaluate"
    )
    parser.add_argument(
        "-k",
        type=int,
        default=3,
        help="Number of results per query"
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save results to JSON file"
    )
    parser.add_argument(
        "--output",
        default="evaluation_results.json",
        help="Output file path"
    )
    
    args = parser.parse_args()
    
    try:
        evaluator = RAGEvaluator()
        
        # Run evaluation
        results = evaluator.evaluate_all(methods=args.methods, k=args.k)
        
        # Save if requested
        if args.save:
            evaluator.save_results(results, args.output)
        
        print("\n" + "=" * 80)
        print("✅ Evaluation completed!")
        print("=" * 80)
        
        evaluator.close()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Evaluation interrupted")
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
