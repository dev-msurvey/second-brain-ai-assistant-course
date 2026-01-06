"""
Example: Tool Calling with FunctionGemma

This example shows how to use FunctionGemma for:
- Parsing natural language to tool calls
- Multi-step workflows
- Error handling

Module 1: Dual-Model Architecture Design
"""

import sys
sys.path.append('..')

from functiongemma_executor import (
    FunctionGemmaExecutor,
    image_gen,
    voice_gen,
    video_compose,
    smart_cut
)
import json


def example_single_tool():
    """Simple single tool call"""
    print("=" * 70)
    print("🔧 EXAMPLE 1: Single Tool Call")
    print("=" * 70)
    print()
    
    # Initialize
    executor = FunctionGemmaExecutor()
    executor.register_tool(image_gen)
    print()
    
    # Test different instructions
    instructions = [
        "สร้างรูป coffee cup แบบ minimal",
        "Generate a realistic image of a modern office",
        "สร้างรูป product แบบ cinematic สำหรับโฆษณา"
    ]
    
    for i, instruction in enumerate(instructions, 1):
        print(f"\n📝 Instruction {i}: {instruction}")
        
        tool_calls = executor.parse_to_tool_calls(instruction)
        print(f"✅ Parsed: {json.dumps(tool_calls, indent=2, ensure_ascii=False)}")
        
        results = executor.execute_tool_calls(tool_calls)
        print(f"🔧 Executed: {json.dumps(results, indent=2, ensure_ascii=False)}")
    
    print()


def example_multi_tool():
    """Multiple tool calls in sequence"""
    print("=" * 70)
    print("🔧 EXAMPLE 2: Multi-Tool Workflow")
    print("=" * 70)
    print()
    
    executor = FunctionGemmaExecutor()
    executor.register_tool(image_gen)
    executor.register_tool(voice_gen)
    executor.register_tool(video_compose)
    print()
    
    # Complex instruction
    instruction = """
    สร้าง Instagram Reel สำหรับ coffee shop:
    1. สร้างรูปกาแฟสไตล์ minimal
    2. สร้างเสียงพากย์ภาษาไทยว่า 'เริ่มต้นวันใหม่กับกาแฟที่ใช่'
    3. รวมเป็นวิดีโอ 15 วินาที พร้อม fade transitions
    """
    
    print(f"📝 Complex Instruction:\n{instruction}\n")
    
    # Parse
    print("⏳ Parsing to tool calls...")
    tool_calls = executor.parse_to_tool_calls(instruction)
    
    print(f"\n✅ Parsed {len(tool_calls)} tool calls:")
    print(json.dumps(tool_calls, indent=2, ensure_ascii=False))
    print()
    
    # Execute
    print("⏳ Executing tools...")
    results = executor.execute_tool_calls(tool_calls)
    
    print(f"\n✅ Execution results:")
    for i, result in enumerate(results, 1):
        print(f"\nTool {i}: {result['tool']}")
        if result['success']:
            print(f"  ✅ Success: {result['result']}")
        else:
            print(f"  ❌ Error: {result['error']}")
    
    print()


def example_smart_cut():
    """Smart Cut tool usage"""
    print("=" * 70)
    print("✂️ EXAMPLE 3: Smart Cut Tool")
    print("=" * 70)
    print()
    
    executor = FunctionGemmaExecutor()
    executor.register_tool(smart_cut)
    print()
    
    # Different editing scenarios
    scenarios = [
        {
            "instruction": "ตัดวิดีโอ interview.mp4 ให้เหลือ 2 นาที แบบ highlights",
            "description": "Extract highlights from interview"
        },
        {
            "instruction": "ทำวิดีโอ tutorial.mp4 เป็น summary 60 วินาที",
            "description": "Summarize tutorial video"
        },
        {
            "instruction": "ตัด webinar_recording.mp4 แบบอัตโนมัติ เอาแต่ส่วนสำคัญ",
            "description": "Auto-trim webinar to key moments"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n✂️ Scenario {i}: {scenario['description']}")
        print(f"📝 Instruction: {scenario['instruction']}")
        
        tool_calls = executor.parse_to_tool_calls(scenario['instruction'])
        print(f"✅ Parsed: {json.dumps(tool_calls, indent=2, ensure_ascii=False)}")
        
        results = executor.execute_tool_calls(tool_calls)
        print(f"🔧 Result: {json.dumps(results, indent=2, ensure_ascii=False)}")
    
    print()


def example_error_handling():
    """Handle tool calling errors"""
    print("=" * 70)
    print("⚠️ EXAMPLE 4: Error Handling")
    print("=" * 70)
    print()
    
    executor = FunctionGemmaExecutor()
    executor.register_tool(image_gen)
    print()
    
    # Test cases with potential issues
    test_cases = [
        {
            "instruction": "สร้างรูป coffee",
            "expected": "Should work - valid instruction"
        },
        {
            "instruction": "ใช้ tool ที่ไม่มี",
            "expected": "Should handle missing tool gracefully"
        },
        {
            "instruction": "",
            "expected": "Should handle empty instruction"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test['expected']}")
        print(f"📝 Instruction: '{test['instruction']}'")
        
        try:
            tool_calls = executor.parse_to_tool_calls(test['instruction'])
            print(f"✅ Parsed: {json.dumps(tool_calls, indent=2, ensure_ascii=False)}")
            
            if tool_calls:
                results = executor.execute_tool_calls(tool_calls)
                print(f"🔧 Results: {json.dumps(results, indent=2, ensure_ascii=False)}")
            else:
                print("⚠️ No tool calls generated")
                
        except Exception as e:
            print(f"❌ Exception caught: {str(e)}")
    
    print()


def example_custom_tool():
    """Create and use custom tools"""
    print("=" * 70)
    print("🛠️ EXAMPLE 5: Custom Tool Definition")
    print("=" * 70)
    print()
    
    # Define custom tool
    def send_email(to: str, subject: str, body: str) -> str:
        """
        Send an email using SMTP.
        
        Args:
            to: Recipient email address
            subject: Email subject line
            body: Email body content
            
        Returns:
            Confirmation message
        """
        # Mock implementation
        return f"Email sent to {to}: {subject}"
    
    def schedule_post(platform: str, content: str, datetime: str) -> str:
        """
        Schedule a social media post.
        
        Args:
            platform: Social media platform (instagram, facebook, linkedin)
            content: Post content text
            datetime: Schedule datetime (ISO format)
            
        Returns:
            Scheduling confirmation
        """
        # Mock implementation
        return f"Post scheduled on {platform} for {datetime}"
    
    # Register custom tools
    executor = FunctionGemmaExecutor()
    executor.register_tool(send_email)
    executor.register_tool(schedule_post)
    print()
    
    # Use custom tools
    instruction = """
    Launch campaign:
    1. ส่งอีเมลถึง team@company.com เรื่อง 'Campaign Launch' 
    2. Schedule Instagram post 'New product launch!' วันที่ 2026-01-15T09:00:00
    """
    
    print(f"📝 Instruction:\n{instruction}\n")
    
    tool_calls = executor.parse_to_tool_calls(instruction)
    print(f"✅ Parsed tool calls:")
    print(json.dumps(tool_calls, indent=2, ensure_ascii=False))
    print()
    
    results = executor.execute_tool_calls(tool_calls)
    print(f"🔧 Execution results:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    print()


if __name__ == "__main__":
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "⚡ FUNCTIONGEMMA TOOL EXAMPLES" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    # Run examples
    example_single_tool()
    example_multi_tool()
    example_smart_cut()
    example_error_handling()
    example_custom_tool()
    
    print("\n🎉 All examples completed!\n")
