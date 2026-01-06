"""
Test Suite for Module 1
Tests T5Gemma, FunctionGemma, and AI Director Agent

Module 1: Dual-Model Architecture Design
AI Director v3.4
"""

import sys
from typing import Dict, Any
import json


class TestRunner:
    """Simple test runner for Module 1"""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.tests_total = 0
    
    def run_test(self, test_name: str, test_func) -> bool:
        """Run a single test"""
        self.tests_total += 1
        print(f"\n{'='*70}")
        print(f"TEST {self.tests_total}: {test_name}")
        print(f"{'='*70}")
        
        try:
            test_func()
            print(f"✅ PASSED: {test_name}")
            self.tests_passed += 1
            return True
        except Exception as e:
            print(f"❌ FAILED: {test_name}")
            print(f"Error: {str(e)}")
            self.tests_failed += 1
            return False
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n\n{'='*70}")
        print("📊 TEST SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests: {self.tests_total}")
        print(f"✅ Passed: {self.tests_passed}")
        print(f"❌ Failed: {self.tests_failed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_total*100):.1f}%")
        print(f"{'='*70}\n")


def test_t5gemma_load():
    """Test 1: T5Gemma 2 loads successfully"""
    from t5gemma_thinker import T5GemmaThinker
    
    thinker = T5GemmaThinker(model_size="1b-1b")
    assert thinker.model is not None, "Model failed to load"
    assert thinker.processor is not None, "Processor failed to load"
    print("✓ T5Gemma 2 loaded successfully")
    print(f"✓ Parameters: {thinker.count_parameters():,}")


def test_t5gemma_generate():
    """Test 2: T5Gemma 2 can generate text"""
    from t5gemma_thinker import T5GemmaThinker
    
    thinker = T5GemmaThinker(model_size="1b-1b")
    
    brief = "Create a coffee ad for Instagram"
    strategy = thinker.generate_strategy(brief, max_length=100)
    
    assert isinstance(strategy, str), "Strategy should be string"
    assert len(strategy) > 0, "Strategy should not be empty"
    print(f"✓ Generated strategy ({len(strategy)} chars)")
    print(f"Preview: {strategy[:100]}...")


def test_functiongemma_load():
    """Test 3: FunctionGemma loads successfully"""
    from functiongemma_executor import FunctionGemmaExecutor
    
    executor = FunctionGemmaExecutor()
    assert executor.model is not None, "Model failed to load"
    assert executor.tokenizer is not None, "Tokenizer failed to load"
    print("✓ FunctionGemma loaded successfully")
    print(f"✓ Parameters: {executor.count_parameters():,}")


def test_functiongemma_tools():
    """Test 4: FunctionGemma can register and parse tools"""
    from functiongemma_executor import FunctionGemmaExecutor, image_gen, voice_gen
    
    executor = FunctionGemmaExecutor()
    executor.register_tool(image_gen)
    executor.register_tool(voice_gen)
    
    assert len(executor.tools) == 2, "Should have 2 tools registered"
    print("✓ Tools registered successfully")
    
    instruction = "สร้างรูปกาแฟ และเสียงพากย์"
    tool_calls = executor.parse_to_tool_calls(instruction, max_new_tokens=150)
    
    assert isinstance(tool_calls, list), "Tool calls should be a list"
    print(f"✓ Parsed {len(tool_calls)} tool call(s)")
    print(f"Calls: {json.dumps(tool_calls, indent=2, ensure_ascii=False)}")


def test_ai_director_init():
    """Test 5: AI Director Agent initializes successfully"""
    from ai_director_agent import AIDirectorAgent
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    assert agent.thinker is not None, "Thinker should be initialized"
    assert agent.executor is not None, "Executor should be initialized"
    assert len(agent.executor.tools) > 0, "Tools should be registered"
    print("✓ AI Director initialized successfully")
    print(f"✓ Tools available: {list(agent.executor.tools.keys())}")


def test_ai_director_brief():
    """Test 6: AI Director can process a brief"""
    from ai_director_agent import AIDirectorAgent
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    brief = """
    Product: Coffee
    Platform: Instagram
    Duration: 15s
    """
    
    result = agent.process_brief(brief)
    
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "strategy" in result, "Should have strategy"
    assert "tool_calls" in result, "Should have tool_calls"
    assert "results" in result, "Should have results"
    assert "duration_seconds" in result, "Should have duration"
    
    print("✓ Brief processed successfully")
    print(f"✓ Processing time: {result['duration_seconds']:.2f}s")
    print(f"✓ Tool calls: {len(result['tool_calls'])}")
    print(f"✓ Results: {len(result['results'])}")


def test_dual_model_integration():
    """Test 7: Dual-model integration works end-to-end"""
    from ai_director_agent import AIDirectorAgent
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    # Test complete workflow
    brief = "Create Instagram ad for coffee"
    result = agent.process_brief(brief)
    
    # Verify Thinker output
    assert len(result["strategy"]) > 0, "Thinker should generate strategy"
    
    # Verify Executor output
    assert isinstance(result["tool_calls"], list), "Executor should parse to list"
    
    # Verify execution
    assert isinstance(result["results"], list), "Should have execution results"
    
    print("✓ End-to-end workflow successful")
    print(f"✓ Thinker → Executor → Tools: WORKING")


def test_smart_cut_workflow():
    """Test 8: Smart Cut workflow works"""
    from ai_director_agent import AIDirectorAgent
    
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
    
    result = agent.process_video_edit(
        video_path="test_video.mp4",
        requirements="Extract highlights",
        target_duration=120
    )
    
    assert isinstance(result, dict), "Result should be a dictionary"
    assert "analysis" in result, "Should have transcript analysis"
    assert "tool_calls" in result, "Should have tool calls"
    assert "results" in result, "Should have results"
    
    print("✓ Smart Cut workflow successful")
    print(f"✓ Processing time: {result['duration_seconds']:.2f}s")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "🧪 MODULE 1 TEST SUITE" + " " * 25 + "║")
    print("║" + " " * 15 + "AI Director v3.4 - Dual-Model Test" + " " * 18 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    runner = TestRunner()
    
    # Run all tests
    runner.run_test("T5Gemma 2 Load", test_t5gemma_load)
    runner.run_test("T5Gemma 2 Generation", test_t5gemma_generate)
    runner.run_test("FunctionGemma Load", test_functiongemma_load)
    runner.run_test("FunctionGemma Tool Calling", test_functiongemma_tools)
    runner.run_test("AI Director Initialization", test_ai_director_init)
    runner.run_test("AI Director Brief Processing", test_ai_director_brief)
    runner.run_test("Dual-Model Integration", test_dual_model_integration)
    runner.run_test("Smart Cut Workflow", test_smart_cut_workflow)
    
    # Print summary
    runner.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if runner.tests_failed == 0 else 1)


if __name__ == "__main__":
    main()
