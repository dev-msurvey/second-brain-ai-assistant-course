"""
FunctionGemma - The Executor
รับผิดชอบ: Tool Calling, Structured Output, Action Execution

Module 1: Dual-Model Architecture Design
AI Director v3.4
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re
from typing import Dict, List, Callable, Any, Optional


class FunctionGemmaExecutor:
    """FunctionGemma model wrapper สำหรับ AI Director"""
    
    def __init__(
        self,
        model_name: str = "google/functiongemma-270m-it",
        device: str = "auto"
    ):
        """
        Initialize FunctionGemma model
        
        Args:
            model_name: Model identifier
            device: "auto", "cpu", "cuda"
        """
        self.model_name = model_name
        print(f"🔄 Loading {self.model_name}...")
        
        # Load tokenizer และ model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=device
        )
        
        print(f"✅ Loaded on {self.model.device}")
        print(f"📊 Model parameters: {self.count_parameters():,}")
        
        # Tool registry
        self.tools: Dict[str, Callable] = {}
    
    def count_parameters(self) -> int:
        """Count total parameters"""
        return sum(p.numel() for p in self.model.parameters())
    
    def register_tool(self, func: Callable) -> None:
        """
        Register a tool function
        
        Args:
            func: Function to register (must have docstring with Args/Returns)
        """
        self.tools[func.__name__] = func
        print(f"✅ Registered tool: {func.__name__}")
    
    def parse_to_tool_calls(
        self,
        instruction: str,
        max_new_tokens: int = 200
    ) -> List[Dict[str, Any]]:
        """
        Parse natural language instruction to tool calls
        
        Args:
            instruction: Natural language instruction
            max_new_tokens: Maximum tokens to generate
            
        Returns:
            List of tool call dictionaries
        """
        if not self.tools:
            raise ValueError("No tools registered. Use register_tool() first.")
        
        # Apply chat template with tools
        messages = [{"role": "user", "content": instruction}]
        formatted = self.tokenizer.apply_chat_template(
            messages,
            tools=list(self.tools.values()),
            add_generation_prompt=True,
            tokenize=False
        )
        
        # Generate
        inputs = self.tokenizer(formatted, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.1,  # Low temperature for precision
                do_sample=False
            )
        
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
        
        # Parse function calls from output
        tool_calls = self._extract_function_calls(result)
        
        return tool_calls
    
    def _extract_function_calls(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract function calls from FunctionGemma output
        
        Format: <start_function_call>call:function_name{param:<escape>value<escape>}<end_function_call>
        """
        tool_calls = []
        
        # Find all function call blocks
        pattern = r'<start_function_call>call:(\w+)\{([^}]+)\}<end_function_call>'
        matches = re.findall(pattern, text)
        
        for func_name, params_str in matches:
            # Parse parameters
            params = {}
            param_pattern = r'(\w+):<escape>([^<]+)<escape>'
            param_matches = re.findall(param_pattern, params_str)
            
            for param_name, param_value in param_matches:
                params[param_name] = param_value
            
            tool_calls.append({
                "tool": func_name,
                "params": params
            })
        
        return tool_calls
    
    def execute_tool_calls(
        self,
        tool_calls: List[Dict[str, Any]]
    ) -> List[Any]:
        """
        Execute parsed tool calls
        
        Args:
            tool_calls: List of tool call dicts from parse_to_tool_calls()
            
        Returns:
            List of results from each tool call
        """
        results = []
        
        for call in tool_calls:
            tool_name = call["tool"]
            params = call["params"]
            
            if tool_name not in self.tools:
                results.append({
                    "error": f"Tool '{tool_name}' not found",
                    "call": call
                })
                continue
            
            try:
                # Execute tool
                result = self.tools[tool_name](**params)
                results.append({
                    "success": True,
                    "tool": tool_name,
                    "params": params,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "success": False,
                    "tool": tool_name,
                    "params": params,
                    "error": str(e)
                })
        
        return results


# Example tool definitions
def image_gen(prompt: str, style: str = "realistic", aspect_ratio: str = "1:1") -> str:
    """
    Generate an image from text prompt using SDXL.
    
    Args:
        prompt: Description of the image to generate
        style: Visual style (realistic, minimal, artistic, cinematic)
        aspect_ratio: Image ratio (1:1, 16:9, 9:16)
        
    Returns:
        Path to generated image file
    """
    # Mock implementation
    return f"generated_image_{style}_{aspect_ratio}.png"


def voice_gen(text: str, voice: str = "th-TH-NiwatNeural", rate: str = "+0%") -> str:
    """
    Generate voiceover from text using Edge-TTS.
    
    Args:
        text: Text to convert to speech
        voice: Voice ID (th-TH-NiwatNeural, th-TH-PremwadeeNeural)
        rate: Speech rate adjustment (-50% to +100%)
        
    Returns:
        Path to generated audio file
    """
    # Mock implementation
    return f"voiceover_{voice}.mp3"


def video_compose(
    images: str,  # JSON string of image paths
    audio: str,
    duration: int = 15,
    transitions: str = "fade"
) -> str:
    """
    Compose video from images and audio using MoviePy.
    
    Args:
        images: JSON string list of image file paths
        audio: Audio file path
        duration: Video duration in seconds
        transitions: Transition style (fade, cut, dissolve)
        
    Returns:
        Path to composed video file
    """
    # Mock implementation
    return f"final_video_{duration}s.mp4"


def smart_cut(
    video_path: str,
    mode: str = "auto",
    target_duration: int = 120
) -> str:
    """
    Automatically trim and cut video using AI analysis.
    
    Args:
        video_path: Path to input video file
        mode: Cutting mode (auto, highlights, summary)
        target_duration: Target video length in seconds
        
    Returns:
        Path to edited video file
    """
    # Mock implementation
    return f"edited_{mode}_{target_duration}s.mp4"


def demo_functiongemma():
    """Demo script to test FunctionGemma"""
    print("=" * 70)
    print("⚡ FUNCTIONGEMMA (EXECUTOR) - DEMO")
    print("=" * 70)
    print()
    
    # Initialize
    executor = FunctionGemmaExecutor()
    print()
    
    # Register tools
    print("📦 Registering tools...")
    executor.register_tool(image_gen)
    executor.register_tool(voice_gen)
    executor.register_tool(video_compose)
    executor.register_tool(smart_cut)
    print()
    
    # Test 1: Simple tool call
    print("📝 TEST 1: Single Tool Call")
    print("-" * 70)
    instruction1 = "สร้างรูปกาแฟแบบ minimal style"
    print(f"Instruction: {instruction1}")
    
    tool_calls = executor.parse_to_tool_calls(instruction1)
    print(f"Parsed calls: {json.dumps(tool_calls, indent=2, ensure_ascii=False)}")
    
    results = executor.execute_tool_calls(tool_calls)
    print(f"Results: {json.dumps(results, indent=2, ensure_ascii=False)}")
    print()
    
    # Test 2: Multiple tool calls
    print("📝 TEST 2: Multiple Tool Calls")
    print("-" * 70)
    instruction2 = """สร้าง Instagram Reel:
    1. สร้างรูปกาแฟสไตล์ minimal
    2. สร้างเสียงพากย์ภาษาไทยว่า 'Cold Brew Premium จาก CoffeeLab'
    3. รวมเป็นวิดีโอ 15 วินาที"""
    print(f"Instruction: {instruction2}")
    
    tool_calls = executor.parse_to_tool_calls(instruction2)
    print(f"Parsed calls: {json.dumps(tool_calls, indent=2, ensure_ascii=False)}")
    
    results = executor.execute_tool_calls(tool_calls)
    print(f"Results: {json.dumps(results, indent=2, ensure_ascii=False)}")
    print()
    
    # Test 3: Smart Cut
    print("📝 TEST 3: Smart Cut Tool")
    print("-" * 70)
    instruction3 = "ตัดวิดีโอ interview.mp4 ให้เหลือ 2 นาที แบบ highlights"
    print(f"Instruction: {instruction3}")
    
    tool_calls = executor.parse_to_tool_calls(instruction3)
    print(f"Parsed calls: {json.dumps(tool_calls, indent=2, ensure_ascii=False)}")
    
    results = executor.execute_tool_calls(tool_calls)
    print(f"Results: {json.dumps(results, indent=2, ensure_ascii=False)}")
    print()
    
    print("=" * 70)
    print("✅ FunctionGemma Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    # Run demo
    demo_functiongemma()
