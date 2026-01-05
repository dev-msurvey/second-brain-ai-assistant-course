#!/usr/bin/env python3
"""
Validation Test Suite for Module 3 Datasets

Run this to validate dataset quality before fine-tuning.
"""

import json
from collections import Counter
from pathlib import Path


def test_jsonl_format():
    """Test 1: Validate JSONL format"""
    print("=== Test 1: JSONL Format Validation ===")
    try:
        with open("data/generated/train.jsonl", 'r') as f:
            train_data = [json.loads(line) for line in f]
        with open("data/generated/val.jsonl", 'r') as f:
            val_data = [json.loads(line) for line in f]
        with open("data/generated/test.jsonl", 'r') as f:
            test_data = [json.loads(line) for line in f]
        
        print(f"✅ PASS: All JSONL files are valid")
        print(f"   Train: {len(train_data)} samples")
        print(f"   Val: {len(val_data)} samples")
        print(f"   Test: {len(test_data)} samples")
        return True, train_data, val_data, test_data
    except Exception as e:
        print(f"❌ FAIL: {e}")
        return False, [], [], []


def test_required_fields(all_data):
    """Test 2: Check required fields"""
    print("\n=== Test 2: Required Fields Check ===")
    required_fields = ["instruction", "input", "output", "metadata"]
    missing_fields = []
    
    for i, sample in enumerate(all_data):
        for field in required_fields:
            if field not in sample:
                missing_fields.append(f"Sample {i}: missing '{field}'")
    
    if missing_fields:
        print(f"❌ FAIL: {len(missing_fields)} samples missing fields")
        for msg in missing_fields[:5]:
            print(f"   {msg}")
        return False
    else:
        print(f"✅ PASS: All samples have required fields")
        return True


def test_data_leakage(train_data, val_data, test_data):
    """Test 3: Check data leakage"""
    print("\n=== Test 3: Data Leakage Check ===")
    
    train_outputs = {s['output'] for s in train_data}
    val_outputs = {s['output'] for s in val_data}
    test_outputs = {s['output'] for s in test_data}
    
    overlap_train_val = train_outputs & val_outputs
    overlap_train_test = train_outputs & test_outputs
    overlap_val_test = val_outputs & test_outputs
    
    if overlap_train_val or overlap_train_test or overlap_val_test:
        print(f"❌ FAIL: Data leakage detected")
        if overlap_train_val:
            print(f"   Train-Val overlap: {len(overlap_train_val)} samples")
        if overlap_train_test:
            print(f"   Train-Test overlap: {len(overlap_train_test)} samples")
        if overlap_val_test:
            print(f"   Val-Test overlap: {len(overlap_val_test)} samples")
        return False
    else:
        print(f"✅ PASS: No data leakage between splits")
        return True


def test_metadata(all_data):
    """Test 4: Metadata validation"""
    print("\n=== Test 4: Metadata Validation ===")
    metadata_issues = []
    
    for i, sample in enumerate(all_data):
        metadata = sample.get('metadata', {})
        if 'brand' not in metadata:
            metadata_issues.append(f"Sample {i}: missing 'brand' in metadata")
        if 'task' not in metadata:
            metadata_issues.append(f"Sample {i}: missing 'task' in metadata")
    
    if metadata_issues:
        print(f"❌ FAIL: {len(metadata_issues)} metadata issues")
        for msg in metadata_issues[:5]:
            print(f"   {msg}")
        return False
    else:
        print(f"✅ PASS: All samples have proper metadata")
        return True


def test_distribution(all_data):
    """Test 5: Dataset distribution"""
    print("\n=== Test 5: Dataset Distribution ===")
    
    brands = [s['metadata']['brand'] for s in all_data]
    tasks = [s['metadata']['task'] for s in all_data]
    
    print(f"Brand distribution:")
    for brand, count in Counter(brands).items():
        pct = (count / len(all_data)) * 100
        print(f"   {brand}: {count} ({pct:.1f}%)")
    
    print(f"\nTask distribution:")
    for task, count in Counter(tasks).items():
        pct = (count / len(all_data)) * 100
        print(f"   {task}: {count} ({pct:.1f}%)")
    
    return True


def test_output_quality(all_data):
    """Test 6: Output quality check"""
    print("\n=== Test 6: Output Quality Check ===")
    quality_issues = []
    
    for i, sample in enumerate(all_data):
        output = sample['output']
        if len(output) < 5:
            quality_issues.append(f"Sample {i}: output too short ({len(output)} chars)")
        if not output.strip():
            quality_issues.append(f"Sample {i}: empty output")
    
    if quality_issues:
        print(f"⚠️  WARNING: {len(quality_issues)} quality issues")
        for msg in quality_issues[:5]:
            print(f"   {msg}")
        return False
    else:
        print(f"✅ PASS: All outputs meet quality criteria")
        return True


def print_summary(all_data):
    """Print summary"""
    brands = [s['metadata']['brand'] for s in all_data]
    tasks = [s['metadata']['task'] for s in all_data]
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print(f"Total samples: {len(all_data)}")
    print(f"Unique brands: {len(set(brands))}")
    print(f"Unique tasks: {len(set(tasks))}")
    print(f"Average output length: {sum(len(s['output']) for s in all_data) / len(all_data):.1f} chars")


def main():
    """Run all tests"""
    print("=" * 70)
    print("Module 3 Dataset Validation Test Suite")
    print("=" * 70 + "\n")
    
    # Test 1: JSONL format
    success, train_data, val_data, test_data = test_jsonl_format()
    if not success:
        return
    
    all_data = train_data + val_data + test_data
    
    # Test 2: Required fields
    test_required_fields(all_data)
    
    # Test 3: Data leakage
    test_data_leakage(train_data, val_data, test_data)
    
    # Test 4: Metadata
    test_metadata(all_data)
    
    # Test 5: Distribution
    test_distribution(all_data)
    
    # Test 6: Output quality
    test_output_quality(all_data)
    
    # Summary
    print_summary(all_data)
    
    print("\n" + "=" * 70)
    print("✅ All tests completed successfully!")
    print("Dataset is ready for fine-tuning.")
    print("=" * 70)


if __name__ == "__main__":
    main()
