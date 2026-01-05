#!/usr/bin/env python3
"""
Test Out-of-Distribution (OOD) Inputs for Fine-tuned Model

ทดสอบว่า model จะทำงานอย่างไรเมื่อได้ input ที่ไม่เคย train
"""

import json
from pathlib import Path


def load_training_data():
    """Load training data เพื่อดูว่า train อะไรไปบ้าง"""
    train_path = Path("../module3/data/generated/train_v2.jsonl")
    
    with open(train_path, 'r') as f:
        train_data = [json.loads(line) for line in f]
    
    return train_data


def analyze_training_coverage():
    """วิเคราะห์ว่า training data ครอบคลุมอะไรบ้าง"""
    train_data = load_training_data()
    
    # Extract unique values
    brands = set()
    tasks = set()
    contexts = set()
    
    for sample in train_data:
        metadata = sample.get('metadata', {})
        brands.add(metadata.get('brand'))
        tasks.add(metadata.get('task'))
        contexts.add(metadata.get('context', 'none'))
    
    print("=== Training Data Coverage ===\n")
    print(f"Brands trained: {sorted(brands)}")
    print(f"Tasks trained: {sorted(tasks)}")
    print(f"Contexts trained: {sorted(contexts)}\n")
    
    return brands, tasks, contexts


def test_ood_scenarios():
    """
    ทดสอบ scenarios ที่อาจเจอ แต่ไม่เคย train
    """
    brands_trained, tasks_trained, contexts_trained = analyze_training_coverage()
    
    print("=== Out-of-Distribution Test Cases ===\n")
    
    # Test Case 1: Brand ใหม่ (ไม่เคย train)
    print("❌ Test 1: Brand ใหม่ (NOT TRAINED)")
    print("Input: เขียน caption สำหรับ TechGadget")
    print("Expected: อาจได้ output ที่ไม่ match brand voice")
    print("Risk Level: 🔴 HIGH\n")
    
    # Test Case 2: Task ใหม่ (ไม่เคย train)
    print("❌ Test 2: Task ใหม่ (NOT TRAINED)")
    print("Input: เขียน video script สำหรับ CoffeeLab")
    print("Expected: อาจได้ format ที่ไม่เหมาะสมกับ video")
    print("Risk Level: 🟡 MEDIUM\n")
    
    # Test Case 3: Context ใหม่
    print("⚠️  Test 3: Context ใหม่")
    print("Input: เขียน caption สำหรับ Black Friday sale")
    print("Expected: ควร generalize ได้ เพราะ base model เก่ง")
    print("Risk Level: 🟢 LOW\n")
    
    # Test Case 4: ภาษาไม่ตรง
    print("❌ Test 4: ภาษาอังกฤษ (trained บนภาษาไทย)")
    print("Input: Write a caption for CoffeeLab in English")
    print("Expected: อาจได้ Thaiglish หรือ mixed language")
    print("Risk Level: 🟡 MEDIUM\n")
    
    # Test Case 5: Format ไม่ตรง
    print("⚠️  Test 5: Input format ต่าง")
    print("Input: ไม่มี Brand: field")
    print("Expected: Model อาจสับสน")
    print("Risk Level: 🟢 LOW (ถ้ามี validation)\n")


def recommend_solutions():
    """แนะนำวิธีแก้ปัญหา OOD"""
    print("=== Solutions for OOD Inputs ===\n")
    
    print("1. 🛡️ INPUT VALIDATION")
    print("   ✅ ตรวจสอบ brand ก่อน generate")
    print("   ✅ ตรวจสอบ task type ที่ support")
    print("   ✅ Reject requests ที่ไม่ support\n")
    
    print("2. 🔄 FALLBACK STRATEGIES")
    print("   ✅ Use base model (Qwen) ถ้า brand ใหม่")
    print("   ✅ Use template-based generation")
    print("   ✅ Return error message with suggestions\n")
    
    print("3. 📊 CONFIDENCE SCORING")
    print("   ✅ คำนวณ confidence score")
    print("   ✅ Warn user ถ้า confidence ต่ำ")
    print("   ✅ Log OOD requests สำหรับ future training\n")
    
    print("4. 🎯 INCREMENTAL LEARNING")
    print("   ✅ Collect feedback จาก OOD cases")
    print("   ✅ Add to training data")
    print("   ✅ Re-train periodically\n")
    
    print("5. 🤝 HYBRID APPROACH")
    print("   ✅ Use RAG สำหรับ brand info ใหม่")
    print("   ✅ Combine fine-tuned model + prompt engineering")
    print("   ✅ Use few-shot examples in prompt\n")


def main():
    """Run OOD analysis"""
    print("=" * 70)
    print("Out-of-Distribution (OOD) Analysis for AI Director")
    print("=" * 70 + "\n")
    
    # Analyze training coverage
    analyze_training_coverage()
    
    # Test OOD scenarios
    test_ood_scenarios()
    
    # Recommend solutions
    recommend_solutions()
    
    print("=" * 70)
    print("📝 Recommendation: Implement input validation + fallback strategies")
    print("=" * 70)


if __name__ == "__main__":
    main()
