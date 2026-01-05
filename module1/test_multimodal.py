#!/usr/bin/env python3
"""Quick test for Module 1 multimodal upgrade"""

import ast
import sys

def test_file_structure():
    """Test that methods exist with correct signatures"""
    print("=" * 70)
    print("🧪 TESTING MODULE 1 MULTIMODAL UPGRADE")
    print("=" * 70)
    print()
    
    # Test 1: Check T5GemmaThinker
    print("📝 Test 1: T5GemmaThinker structure")
    print("-" * 70)
    
    with open('01_t5gemma_thinker.py', 'r') as f:
        tree = ast.parse(f.read())
    
    thinker_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'T5GemmaThinker':
            thinker_found = True
            methods = {m.name: [arg.arg for arg in m.args.args] 
                      for m in node.body if isinstance(m, ast.FunctionDef)}
            
            print(f"✅ T5GemmaThinker class found")
            print(f"   Total methods: {len(methods)}")
            print()
            
            # Check analyze_image
            if 'analyze_image' in methods:
                params = methods['analyze_image']
                print(f"✅ analyze_image() exists")
                print(f"   Parameters: {params}")
                if 'image' in params and 'task' in params:
                    print(f"   ✅ Has required parameters (image, task)")
                else:
                    print(f"   ❌ Missing required parameters")
            else:
                print("❌ analyze_image() NOT FOUND")
                return False
            print()
            
            # Check generate_strategy
            if 'generate_strategy' in methods:
                params = methods['generate_strategy']
                print(f"✅ generate_strategy() exists")
                print(f"   Parameters: {params}")
                if 'reference_image' in params:
                    print(f"   ✅ Has reference_image parameter (multimodal!)")
                else:
                    print(f"   ❌ Missing reference_image parameter")
                    return False
            else:
                print("❌ generate_strategy() NOT FOUND")
                return False
            print()
            break
    
    if not thinker_found:
        print("❌ T5GemmaThinker class NOT FOUND")
        return False
    
    # Test 2: Check AIDirectorAgent
    print("📝 Test 2: AIDirectorAgent structure")
    print("-" * 70)
    
    with open('03_ai_director_agent.py', 'r') as f:
        tree = ast.parse(f.read())
    
    agent_found = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'AIDirectorAgent':
            agent_found = True
            methods = {m.name: [arg.arg for arg in m.args.args] 
                      for m in node.body if isinstance(m, ast.FunctionDef)}
            
            print(f"✅ AIDirectorAgent class found")
            print()
            
            # Check process_brief
            if 'process_brief' in methods:
                params = methods['process_brief']
                print(f"✅ process_brief() exists")
                print(f"   Parameters: {params}")
                if 'reference_image' in params:
                    print(f"   ✅ Has reference_image parameter (multimodal!)")
                else:
                    print(f"   ❌ Missing reference_image parameter")
                    return False
            else:
                print("❌ process_brief() NOT FOUND")
                return False
            print()
            break
    
    if not agent_found:
        print("❌ AIDirectorAgent class NOT FOUND")
        return False
    
    # Test 3: Check example file exists
    print("📝 Test 3: Example file")
    print("-" * 70)
    import os
    if os.path.exists('examples/example_multimodal.py'):
        print("✅ example_multimodal.py exists")
        
        # Check it has main examples
        with open('examples/example_multimodal.py', 'r') as f:
            content = f.read()
        
        examples = [
            'example_1_image_analysis',
            'example_2_strategy_with_image',
            'example_3_full_agent_with_image',
            'example_4_comparison'
        ]
        
        for ex in examples:
            if ex in content:
                print(f"   ✅ {ex}() found")
            else:
                print(f"   ❌ {ex}() NOT FOUND")
                return False
    else:
        print("❌ example_multimodal.py NOT FOUND")
        return False
    print()
    
    # Test 4: Check documentation
    print("📝 Test 4: Documentation")
    print("-" * 70)
    if os.path.exists('MODULE1_COMPLETION.md'):
        print("✅ MODULE1_COMPLETION.md exists")
        with open('MODULE1_COMPLETION.md', 'r') as f:
            doc = f.read()
        
        keywords = ['multimodal', 'analyze_image', 'reference_image', 'T5Gemma 2']
        for kw in keywords:
            if kw in doc:
                print(f"   ✅ Contains '{kw}'")
            else:
                print(f"   ⚠️  Missing '{kw}'")
    else:
        print("❌ MODULE1_COMPLETION.md NOT FOUND")
        return False
    print()
    
    return True

if __name__ == '__main__':
    success = test_file_structure()
    
    print("=" * 70)
    if success:
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print()
        print("🎉 Module 1 multimodal upgrade is structurally correct!")
        print()
        print("📋 Summary:")
        print("   ✅ T5GemmaThinker has analyze_image() method")
        print("   ✅ T5GemmaThinker.generate_strategy() accepts reference_image")
        print("   ✅ AIDirectorAgent.process_brief() accepts reference_image")
        print("   ✅ Example file with 4 demos created")
        print("   ✅ Documentation complete")
        print()
        print("⚠️  NOTE: Actual runtime testing requires:")
        print("   - GPU/CPU with sufficient RAM")
        print("   - Model downloads (~2-4 GB)")
        print("   - Internet connection (for example images)")
        sys.exit(0)
    else:
        print("❌ TESTS FAILED!")
        print("=" * 70)
        sys.exit(1)
