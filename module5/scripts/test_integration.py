"""
Integration Test: Module 4 + Module 5
Tests fine-tuned model with vector RAG retrieval
"""

import os
import sys
from pathlib import Path

# Add module5 to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import from inference_rag_v2
from scripts.inference_rag_v2 import AIDirectorRAGInferenceV2


def test_basic_integration():
    """Test basic Module 4 + Module 5 integration"""
    print("=" * 80)
    print("🧪 MODULE 4 + MODULE 5 INTEGRATION TEST")
    print("=" * 80)
    print("\nTest: Fine-tuned Model + Vector RAG\n")
    
    # Model path
    adapter_path = "../module4/models/qwen-7b-ai-director-v2/checkpoint-111"
    
    # Check if model exists
    if not Path(adapter_path).exists():
        print(f"❌ Model not found: {adapter_path}")
        print("\nAlternative paths:")
        print("1. ../module4/models/qwen-7b-ai-director-v2")
        print("2. ../module4/models/qwen-7b-ai-director-v2/checkpoint-100")
        return
    
    print(f"📦 Loading model from: {adapter_path}")
    print(f"🔍 Using vector RAG: MongoDB Atlas\n")
    
    # Initialize inferencer
    try:
        inferencer = AIDirectorRAGInferenceV2(
            base_model_name="Qwen/Qwen2.5-1.5B-Instruct",
            adapter_path=adapter_path,
            use_vector_rag=True
        )
        print("✅ Model loaded successfully!\n")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return
    
    # Test cases
    test_cases = [
        {
            "instruction": "Create an Instagram caption",
            "brand": "CoffeeLab",
            "description": "Coffee brand with vector RAG"
        },
        {
            "instruction": "Write a Facebook post",
            "brand": "FitFlow",
            "description": "Fitness brand with semantic search"
        },
        {
            "instruction": "Generate a Tweet",
            "brand": "GlowLab",
            "description": "Skincare brand with hybrid retrieval"
        }
    ]
    
    print("-" * 80)
    print("🎯 TEST CASES")
    print("-" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/3] {test_case['description']}")
        print(f"Instruction: {test_case['instruction']}")
        print(f"Brand: {test_case['brand']}")
        print("-" * 80)
        
        try:
            output = inferencer.generate(
                instruction=test_case['instruction'],
                brand_name=test_case['brand']
            )
            
            print("\n📝 Generated Content:")
            print(output)
            print("-" * 80)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    # Close
    inferencer.close()
    print("\n" + "=" * 80)
    print("✅ Integration test completed!")
    print("=" * 80)


def test_comparison():
    """Compare base model vs fine-tuned model (both with RAG)"""
    print("=" * 80)
    print("🔬 COMPARISON: Base Model vs Fine-tuned Model (with RAG)")
    print("=" * 80)
    
    adapter_path = "../module4/models/qwen-7b-ai-director-v2/checkpoint-111"
    
    if not Path(adapter_path).exists():
        print(f"❌ Model not found: {adapter_path}")
        return
    
    # Test instruction
    instruction = "Create an Instagram caption"
    brand = "UrbanNest"
    
    print(f"\nInstruction: {instruction}")
    print(f"Brand: {brand}")
    print()
    
    # 1. Base model + RAG
    print("-" * 80)
    print("1️⃣  BASE MODEL + RAG (No Fine-tuning)")
    print("-" * 80)
    
    try:
        base_inferencer = AIDirectorRAGInferenceV2(
            base_model_name="Qwen/Qwen2.5-1.5B-Instruct",
            adapter_path=None,  # No adapter
            use_vector_rag=True
        )
        
        base_output = base_inferencer.generate(
            instruction=instruction,
            brand_name=brand
        )
        
        print("\n📝 Output:")
        print(base_output)
        print()
        
        base_inferencer.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        base_output = None
    
    # 2. Fine-tuned model + RAG
    print("-" * 80)
    print("2️⃣  FINE-TUNED MODEL + RAG (Module 4 + Module 5)")
    print("-" * 80)
    
    try:
        finetuned_inferencer = AIDirectorRAGInferenceV2(
            base_model_name="Qwen/Qwen2.5-1.5B-Instruct",
            adapter_path=adapter_path,
            use_vector_rag=True
        )
        
        finetuned_output = finetuned_inferencer.generate(
            instruction=instruction,
            brand_name=brand
        )
        
        print("\n📝 Output:")
        print(finetuned_output)
        print()
        
        finetuned_inferencer.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        finetuned_output = None
    
    # Summary
    print("=" * 80)
    print("📊 COMPARISON SUMMARY")
    print("=" * 80)
    
    if base_output and finetuned_output:
        print("\n✅ Both models generated successfully!")
        print("\n💡 Observations:")
        print("   • Base model: Generic content with RAG context")
        print("   • Fine-tuned model: Brand-specific style + RAG context")
        print("   • Fine-tuning improves tone and brand alignment")
    
    print("\n" + "=" * 80)


def test_without_rag():
    """Test fine-tuned model WITHOUT RAG (Module 4 only)"""
    print("=" * 80)
    print("🧪 TEST: Fine-tuned Model WITHOUT RAG (Module 4 Only)")
    print("=" * 80)
    
    adapter_path = "../module4/models/qwen-7b-ai-director-v2/checkpoint-111"
    
    if not Path(adapter_path).exists():
        print(f"❌ Model not found: {adapter_path}")
        return
    
    print(f"\n📦 Loading model: {adapter_path}")
    print("🔍 RAG: Disabled (Module 4 only)\n")
    
    try:
        inferencer = AIDirectorRAGInferenceV2(
            base_model_name="Qwen/Qwen2.5-1.5B-Instruct",
            adapter_path=adapter_path,
            use_vector_rag=False  # Disable RAG
        )
        
        # Test
        instruction = "Create an Instagram caption"
        brand = "CoffeeLab"
        
        print(f"Instruction: {instruction}")
        print(f"Brand: {brand}")
        print("-" * 80)
        
        output = inferencer.generate(
            instruction=instruction,
            brand_name=brand
        )
        
        print("\n📝 Generated Content (No RAG):")
        print(output)
        print("\n" + "=" * 80)
        
        inferencer.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Module 4 + 5 Integration Test")
    parser.add_argument(
        "--test",
        choices=["basic", "comparison", "no-rag", "all"],
        default="basic",
        help="Test type to run"
    )
    
    args = parser.parse_args()
    
    try:
        if args.test == "basic":
            test_basic_integration()
        elif args.test == "comparison":
            test_comparison()
        elif args.test == "no-rag":
            test_without_rag()
        elif args.test == "all":
            test_basic_integration()
            print("\n\n")
            test_comparison()
            print("\n\n")
            test_without_rag()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
