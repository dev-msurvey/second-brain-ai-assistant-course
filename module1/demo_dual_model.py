"""
Simple Dual-Model Demo - FLAN-T5 + FunctionGemma
Demonstrates Thinker + Executor Architecture

Module 1: Dual-Model Architecture Design
AI Director v3.4
"""

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import torch
import json
from typing import Dict, List, Any


class SimpleThinker:
    """FLAN-T5 for content generation"""
    
    def __init__(self):
        print("🧠 Loading Thinker: google/flan-t5-base...")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            "google/flan-t5-base",
            torch_dtype=torch.float32
        )
        self.device = "cpu"
        self.model.to(self.device)
        print(f"✅ Thinker loaded ({self.model.num_parameters():,} parameters)")
    
    def think(self, task: str) -> str:
        """Generate strategy/plan"""
        prompt = f"Generate a creative strategy for: {task}"
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7
        )
        
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)


class SimpleExecutor:
    """FunctionGemma for tool calling"""
    
    def __init__(self):
        print("⚡ Loading Executor: google/functiongemma-270m-it...")
        self.tokenizer = AutoTokenizer.from_pretrained("google/functiongemma-270m-it")
        self.model = AutoModelForCausalLM.from_pretrained(
            "google/functiongemma-270m-it",
            torch_dtype=torch.float32
        )
        self.device = "cpu"
        self.model.to(self.device)
        print(f"✅ Executor loaded ({self.model.num_parameters():,} parameters)")
        
        self.tools = {
            "image_gen": self.mock_image_gen,
            "voice_gen": self.mock_voice_gen,
            "video_compose": self.mock_video_compose
        }
    
    def mock_image_gen(self, prompt: str, aspect_ratio: str = "16:9") -> str:
        return f"🖼️  Generated image: {prompt[:50]}... [{aspect_ratio}]"
    
    def mock_voice_gen(self, text: str, voice: str = "thai_female") -> str:
        return f"🎤 Generated voice: '{text[:50]}...' [{voice}]"
    
    def mock_video_compose(self, images: List[str], audio: str, duration: int) -> str:
        return f"🎬 Composed video: {len(images)} frames + audio [{duration}s]"
    
    def execute(self, instruction: str) -> List[Dict[str, Any]]:
        """Parse instruction and execute tools"""
        # Simple keyword-based tool calling (production would use model generation)
        results = []
        
        if "image" in instruction.lower() or "รูป" in instruction:
            result = self.mock_image_gen(instruction)
            results.append({"tool": "image_gen", "output": result})
        
        if "voice" in instruction.lower() or "เสียง" in instruction:
            result = self.mock_voice_gen(instruction)
            results.append({"tool": "voice_gen", "output": result})
        
        if "video" in instruction.lower() or "วิดีโอ" in instruction:
            result = self.mock_video_compose(["frame1", "frame2"], "audio.mp3", 15)
            results.append({"tool": "video_compose", "output": result})
        
        return results


class DualModelAgent:
    """Complete Agent: Thinker + Executor"""
    
    def __init__(self):
        print("\n" + "="*70)
        print("🎬 INITIALIZING DUAL-MODEL AI DIRECTOR")
        print("="*70 + "\n")
        
        self.thinker = SimpleThinker()
        print()
        self.executor = SimpleExecutor()
        
        print("\n" + "="*70)
        print("✅ AGENT READY!")
        print("="*70)
    
    def process(self, brief: str) -> Dict[str, Any]:
        """
        Complete workflow:
        1. Thinker generates strategy
        2. Executor calls tools to execute
        """
        print(f"\n\n📋 BRIEF: {brief}\n")
        
        # Step 1: Think
        print("🧠 THINKER: Generating strategy...")
        strategy = self.thinker.think(brief)
        print(f"💡 Strategy: {strategy}\n")
        
        # Step 2: Execute
        print("⚡ EXECUTOR: Calling tools...")
        tool_results = self.executor.execute(brief)
        
        for result in tool_results:
            print(f"  • {result['output']}")
        
        return {
            "brief": brief,
            "strategy": strategy,
            "executions": tool_results,
            "status": "completed"
        }


def demo():
    """Run demonstration"""
    print("\n")
    print("╔" + "═"*68 + "╗")
    print("║" + " "*15 + "🎬 DUAL-MODEL ARCHITECTURE DEMO" + " "*23 + "║")
    print("║" + " "*20 + "Thinker + Executor System" + " "*23 + "║")
    print("╚" + "═"*68 + "╝")
    
    # Initialize agent
    agent = DualModelAgent()
    
    # Test cases
    test_cases = [
        "สร้าง Instagram Reel สำหรับกาแฟ Cold Brew พร้อมเสียงพากย์",
        "Create a promotional video with modern visuals and voiceover",
        "สร้างรูปภาพและเสียงสำหรับโฆษณา 15 วินาที"
    ]
    
    for i, brief in enumerate(test_cases, 1):
        print("\n" + "="*70)
        print(f"TEST CASE {i}/{len(test_cases)}")
        print("="*70)
        
        result = agent.process(brief)
        
        print("\n📊 RESULT:")
        print(f"  Status: {result['status']}")
        print(f"  Tools executed: {len(result['executions'])}")
    
    print("\n" + "="*70)
    print("✅ DEMO COMPLETE!")
    print("="*70)
    print("\nKey Learnings:")
    print("  • Thinker (FLAN-T5): Generates creative strategies")
    print("  • Executor (FunctionGemma): Executes tools")
    print("  • Together: Complete AI Director workflow")
    print()


if __name__ == "__main__":
    demo()
