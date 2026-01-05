"""
AI Director Agent - Complete Dual-Model System
Combines T5Gemma 2 (Thinker) + FunctionGemma (Executor)

Module 1: Dual-Model Architecture Design
AI Director v3.4
"""

from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# Import our components
import sys
import importlib.util
from pathlib import Path

# Dynamic import for numbered modules
def import_module_by_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

module_dir = Path(__file__).parent
thinker_mod = import_module_by_path("t5gemma_thinker", module_dir / "01_t5gemma_thinker.py")
executor_mod = import_module_by_path("functiongemma_executor", module_dir / "02_functiongemma_executor.py")

T5GemmaThinker = thinker_mod.T5GemmaThinker
FunctionGemmaExecutor = executor_mod.FunctionGemmaExecutor
image_gen = executor_mod.image_gen
voice_gen = executor_mod.voice_gen
video_compose = executor_mod.video_compose
smart_cut = executor_mod.smart_cut


class AIDirectorAgent:
    """
    Complete AI Director using Dual-Model Architecture
    
    Workflow:
    1. User gives brief
    2. T5Gemma 2 (Thinker) generates strategy and content
    3. FunctionGemma (Executor) parses strategy to tool calls
    4. Tools execute and produce outputs
    5. Return final results
    """
    
    def __init__(
        self,
        thinker_size: str = "1b-1b",
        device: str = "auto",
        verbose: bool = True
    ):
        """
        Initialize AI Director with both models
        
        Args:
            thinker_size: T5Gemma 2 model size
            device: Device for models
            verbose: Print progress messages
        """
        self.verbose = verbose
        
        if self.verbose:
            print("=" * 70)
            print("🎬 INITIALIZING AI DIRECTOR v3.4")
            print("=" * 70)
            print()
        
        # Load Thinker (T5Gemma 2)
        if self.verbose:
            print("🧠 Loading Thinker (T5Gemma 2)...")
        self.thinker = T5GemmaThinker(model_size=thinker_size, device=device)
        print()
        
        # Load Executor (FunctionGemma)
        if self.verbose:
            print("⚡ Loading Executor (FunctionGemma)...")
        self.executor = FunctionGemmaExecutor(device=device)
        print()
        
        # Register tools
        if self.verbose:
            print("📦 Registering production tools...")
        self.executor.register_tool(image_gen)
        self.executor.register_tool(voice_gen)
        self.executor.register_tool(video_compose)
        self.executor.register_tool(smart_cut)
        print()
        
        if self.verbose:
            print("=" * 70)
            print("✅ AI DIRECTOR READY!")
            print("=" * 70)
            print()
    
    def process_brief(
        self,
        brief: str,
        brand_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main workflow: Process marketing brief end-to-end
        
        Args:
            brief: Marketing brief from user
            brand_context: Optional brand guidelines
            
        Returns:
            Complete result with strategy, tool calls, and outputs
        """
        start_time = datetime.now()
        
        if self.verbose:
            print("\n" + "=" * 70)
            print("🎬 PROCESSING BRIEF")
            print("=" * 70)
            print(f"\n📝 Brief:\n{brief}\n")
        
        # STEP 1: THINKER - Generate Strategy
        if self.verbose:
            print("-" * 70)
            print("STEP 1: 🧠 THINKER - Generating Strategy...")
            print("-" * 70)
        
        strategy = self.thinker.generate_strategy(
            brief=brief,
            brand_context=brand_context
        )
        
        if self.verbose:
            print(f"\n✅ Strategy Generated:\n{strategy}\n")
        
        # STEP 2: EXECUTOR - Parse to Tool Calls
        if self.verbose:
            print("-" * 70)
            print("STEP 2: ⚡ EXECUTOR - Parsing to Tool Calls...")
            print("-" * 70)
        
        tool_calls = self.executor.parse_to_tool_calls(strategy)
        
        if self.verbose:
            print(f"\n✅ Tool Calls Parsed:")
            print(json.dumps(tool_calls, indent=2, ensure_ascii=False))
            print()
        
        # STEP 3: EXECUTION - Run Tools
        if self.verbose:
            print("-" * 70)
            print("STEP 3: 🔧 EXECUTION - Running Tools...")
            print("-" * 70)
        
        results = self.executor.execute_tool_calls(tool_calls)
        
        if self.verbose:
            print(f"\n✅ Tools Executed:")
            print(json.dumps(results, indent=2, ensure_ascii=False))
            print()
        
        # Calculate duration
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if self.verbose:
            print("=" * 70)
            print(f"✅ PROCESSING COMPLETE! (⏱️ {duration:.2f}s)")
            print("=" * 70)
        
        return {
            "brief": brief,
            "brand_context": brand_context,
            "strategy": strategy,
            "tool_calls": tool_calls,
            "results": results,
            "duration_seconds": duration,
            "timestamp": start_time.isoformat()
        }
    
    def process_video_edit(
        self,
        video_path: str,
        requirements: str,
        target_duration: int = 120
    ) -> Dict[str, Any]:
        """
        Smart Cut workflow: Analyze and edit video
        
        Args:
            video_path: Path to video file
            requirements: Editing requirements
            target_duration: Target duration in seconds
            
        Returns:
            Editing results
        """
        start_time = datetime.now()
        
        if self.verbose:
            print("\n" + "=" * 70)
            print("✂️ SMART CUT WORKFLOW")
            print("=" * 70)
            print(f"\n📹 Video: {video_path}")
            print(f"📝 Requirements: {requirements}\n")
        
        # STEP 1: Mock transcript (in real version, use Whisper)
        mock_transcript = """
        [00:15] สวัสดีครับ วันนี้เราจะมาพูดถึง CoffeeLab
        [00:45] กาแฟของเราทำจากเมล็ดคุณภาพ
        [01:20] ... (silence) ...
        [02:15] ตอนนี้เรามีโปรโมชั่นพิเศษ
        [03:00] สั่งได้ที่ coffeelabthailand.com
        """
        
        # STEP 2: THINKER - Analyze transcript
        if self.verbose:
            print("-" * 70)
            print("STEP 1: 🧠 THINKER - Analyzing Transcript...")
            print("-" * 70)
        
        analysis = self.thinker.analyze_transcript(
            transcript=mock_transcript,
            target_duration=target_duration,
            style="highlight"
        )
        
        if self.verbose:
            print(f"\n✅ Analysis Complete:")
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
            print()
        
        # STEP 3: EXECUTOR - Parse to cut commands
        if self.verbose:
            print("-" * 70)
            print("STEP 2: ⚡ EXECUTOR - Generating Cut Commands...")
            print("-" * 70)
        
        cut_instruction = f"""ใช้ smart_cut ตัดวิดีโอ {video_path} 
        ตามการวิเคราะห์: {json.dumps(analysis)}
        target duration: {target_duration} วินาที"""
        
        tool_calls = self.executor.parse_to_tool_calls(cut_instruction)
        
        if self.verbose:
            print(f"\n✅ Cut Commands:")
            print(json.dumps(tool_calls, indent=2, ensure_ascii=False))
            print()
        
        # STEP 4: Execute
        if self.verbose:
            print("-" * 70)
            print("STEP 3: ✂️ EXECUTION - Cutting Video...")
            print("-" * 70)
        
        results = self.executor.execute_tool_calls(tool_calls)
        
        if self.verbose:
            print(f"\n✅ Video Edited:")
            print(json.dumps(results, indent=2, ensure_ascii=False))
            print()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        if self.verbose:
            print("=" * 70)
            print(f"✅ SMART CUT COMPLETE! (⏱️ {duration:.2f}s)")
            print("=" * 70)
        
        return {
            "video_path": video_path,
            "requirements": requirements,
            "target_duration": target_duration,
            "transcript": mock_transcript,
            "analysis": analysis,
            "tool_calls": tool_calls,
            "results": results,
            "duration_seconds": duration,
            "timestamp": start_time.isoformat()
        }


def demo_ai_director():
    """Demo the complete AI Director system"""
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "🎬 AI DIRECTOR v3.4 - DEMO" + " " * 26 + "║")
    print("║" + " " * 15 + "Dual-Model Architecture" + " " * 29 + "║")
    print("╚" + "═" * 68 + "╝")
    print("\n")
    
    # Initialize agent
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=True)
    
    # Demo 1: Create Marketing Content
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 20 + "DEMO 1: Marketing Campaign" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")
    
    brief1 = """
    Product: CoffeeLab Cold Brew Premium
    Platform: Instagram Reel
    Duration: 15 seconds
    Target Audience: Young professionals 25-35
    Goal: Product launch, create awareness
    Style: Modern, minimal, premium
    """
    
    result1 = agent.process_brief(brief1)
    
    # Demo 2: Smart Cut Video
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 23 + "DEMO 2: Smart Cut Video" + " " * 22 + "║")
    print("╚" + "═" * 68 + "╝")
    
    result2 = agent.process_video_edit(
        video_path="interview_coffeeleb_founder.mp4",
        requirements="เลือกแต่ไฮไลท์เกี่ยวกับผลิตภัณฑ์และวิสัยทัศน์แบรนด์",
        target_duration=120
    )
    
    # Summary
    print("\n\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 26 + "📊 DEMO SUMMARY" + " " * 27 + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print(f"✅ Demo 1 completed in {result1['duration_seconds']:.2f}s")
    print(f"   - Strategy generated: ✓")
    print(f"   - Tool calls parsed: {len(result1['tool_calls'])}")
    print(f"   - Tools executed: {len(result1['results'])}")
    print()
    print(f"✅ Demo 2 completed in {result2['duration_seconds']:.2f}s")
    print(f"   - Transcript analyzed: ✓")
    print(f"   - Cuts identified: ✓")
    print(f"   - Video edited: ✓")
    print()
    print("=" * 70)
    print("🎉 ALL DEMOS COMPLETE!")
    print("=" * 70)


if __name__ == "__main__":
    # Run demos
    demo_ai_director()
