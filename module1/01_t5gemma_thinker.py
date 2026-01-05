"""
T5Gemma 2 - The Thinker
รับผิดชอบ: Strategy, Creative Content, Analysis

Module 1: Dual-Model Architecture Design
AI Director v3.4
"""

from transformers import AutoProcessor, AutoModelForSeq2SeqLM
import torch
from typing import Dict, List, Optional
from PIL import Image
import requests
from io import BytesIO


class T5GemmaThinker:
    """T5Gemma 2 model wrapper สำหรับ AI Director"""
    
    def __init__(
        self, 
        model_size: str = "1b-1b",  # "270m-270m", "1b-1b", "4b-4b"
        device: str = "auto"
    ):
        """
        Initialize T5Gemma 2 model
        
        Args:
            model_size: ขนาด model (1b-1b แนะนำสำหรับ Codespaces)
            device: "auto", "cpu", "cuda"
        """
        self.model_name = f"google/t5gemma-2-{model_size}"
        print(f"🔄 Loading {self.model_name}...")
        
        # Load processor และ model
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=device
        )
        
        print(f"✅ Loaded on {self.model.device}")
        print(f"📊 Model parameters: {self.count_parameters():,}")
    
    def count_parameters(self) -> int:
        """Count total parameters"""
        return sum(p.numel() for p in self.model.parameters())
    
    def generate_strategy(
        self, 
        brief: str,
        brand_context: Optional[str] = None,
        reference_image: Optional[Image.Image] = None,
        max_length: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Generate marketing strategy จาก brief (supports text + image)
        
        Args:
            brief: Marketing brief
            brand_context: Brand guidelines (จาก RAG)
            reference_image: Optional reference image (PIL.Image)
            max_length: Maximum output tokens
            temperature: Creativity level (0.0-1.0)
            
        Returns:
            Generated strategy as text
        """
        # สร้าง prompt
        if reference_image:
            prompt = f"""You are a creative director for a marketing agency.
Analyze the provided image and generate a detailed content strategy.

BRAND CONTEXT:
{brand_context if brand_context else "No specific brand guidelines."}

BRIEF:
{brief}

Based on the image and brief, generate:
1. Creative Concept (inspired by image)
2. Image Description (for SDXL)
3. Voice Script (Thai)
4. Technical Specs

STRATEGY:"""
        else:
            prompt = f"""You are a creative director for a marketing agency.
Generate a detailed content strategy based on this brief.

BRAND CONTEXT:
{brand_context if brand_context else "No specific brand guidelines."}

BRIEF:
{brief}

Generate:
1. Creative Concept
2. Image Description (for SDXL)
3. Voice Script (Thai)
4. Technical Specs

STRATEGY:"""

        # Generate (with or without image)
        if reference_image:
            inputs = self.processor(
                text=prompt, 
                images=reference_image, 
                return_tensors="pt"
            ).to(self.model.device)
        else:
            inputs = self.processor(text=prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result
    
    def analyze_image(
        self,
        image: Image.Image,
        task: str = "describe"
    ) -> str:
        """
        Analyze image for marketing purposes (NEW: Multimodal capability)
        
        Args:
            image: PIL Image to analyze
            task: "describe", "brand_analysis", "composition", "mood"
            
        Returns:
            Analysis text
        """
        prompts = {
            "describe": "<start_of_image> Describe this image in detail for a marketing brief.",
            "brand_analysis": "<start_of_image> Analyze this image from a brand identity perspective. Identify colors, mood, style, and target audience.",
            "composition": "<start_of_image> Analyze the composition, lighting, and visual hierarchy of this image for a photographer.",
            "mood": "<start_of_image> Describe the mood, emotion, and atmosphere conveyed by this image."
        }
        
        prompt = prompts.get(task, prompts["describe"])
        
        inputs = self.processor(
            text=prompt,
            images=image,
            return_tensors="pt"
        ).to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=300,
                temperature=0.7,
                do_sample=True
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result.strip()
    
    def generate_image_prompt(
        self,
        brief: str,
        style: str = "realistic",
        aspect_ratio: str = "1:1"
    ) -> str:
        """
        Generate detailed SDXL prompt
        
        Args:
            brief: Product/concept description
            style: "realistic", "minimal", "artistic", "cinematic"
            aspect_ratio: "1:1", "16:9", "9:16"
            
        Returns:
            Detailed prompt สำหรับ SDXL
        """
        prompt = f"""You are an expert photography director.
Generate a detailed prompt for Stable Diffusion XL based on this brief.

BRIEF: {brief}
STYLE: {style}
ASPECT RATIO: {aspect_ratio}

Generate a prompt that includes:
- Subject details
- Lighting setup
- Camera settings
- Mood and atmosphere
- Technical quality descriptors

SDXL PROMPT:"""

        inputs = self.processor(text=prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.8,
                do_sample=True
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result.strip()
    
    def analyze_transcript(
        self,
        transcript: str,
        target_duration: int = 120,
        style: str = "highlight"
    ) -> Dict:
        """
        Analyze video transcript และเลือก highlights
        สำหรับ Smart Cut feature
        
        Args:
            transcript: Full transcript with timestamps
            target_duration: Target video length (seconds)
            style: "highlight", "summary", "tutorial"
            
        Returns:
            Dictionary with selected segments and editing decisions
        """
        prompt = f"""You are a video editor analyzing a transcript.

TRANSCRIPT:
{transcript}

TARGET DURATION: {target_duration} seconds
STYLE: {style}

Analyze and identify:
1. Key moments to keep (with timestamps)
2. Segments to remove (silence, tangents, repetition)
3. Suggested editing flow
4. Transition recommendations

OUTPUT (JSON format):
{{
    "keep_segments": [
        {{"start": 15.0, "end": 45.0, "reason": "strong intro"}},
        ...
    ],
    "remove_reasons": {{
        "silence": 45.2,
        "tangent": 30.0,
        "repetition": 20.0
    }},
    "suggested_order": "chronological|story-driven|impact-driven",
    "transitions": ["fade", "cut", "cross-dissolve"]
}}

ANALYSIS:"""

        inputs = self.processor(text=prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=400,
                temperature=0.5,
                do_sample=True
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        # Try to parse as JSON (in real implementation, add proper parsing)
        return {"analysis": result}
    
    def generate_voice_script(
        self,
        concept: str,
        duration: int = 30,
        tone: str = "friendly",
        language: str = "Thai"
    ) -> str:
        """
        Generate voiceover script
        
        Args:
            concept: Content concept
            duration: Target duration in seconds
            tone: Voice tone (friendly, professional, excited, etc.)
            language: Script language
            
        Returns:
            Voice script text
        """
        word_count = duration * 2.5  # ~150 words per minute
        
        prompt = f"""Generate a {language} voiceover script for a video.

CONCEPT: {concept}
DURATION: {duration} seconds (~{int(word_count)} words)
TONE: {tone}
LANGUAGE: {language}

Requirements:
- Natural conversational flow
- Clear pronunciation
- Appropriate pacing
- Engaging delivery

SCRIPT:"""

        inputs = self.processor(text=prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=int(word_count * 1.5),
                temperature=0.7,
                do_sample=True
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result.strip()


def demo_t5gemma():
    """Demo script to test T5Gemma 2 (Text + Image)"""
    print("=" * 70)
    print("🧠 T5GEMMA 2 (THINKER) - MULTIMODAL DEMO")
    print("=" * 70)
    print()
    
    # Initialize
    thinker = T5GemmaThinker(model_size="1b-1b")
    print()
    
    # Test 1: Generate Strategy (text only)
    print("📝 TEST 1: Generate Marketing Strategy (Text Only)")
    print("-" * 70)
    brief = """
    Product: CoffeeLab Cold Brew Premium
    Target: Young professionals 25-35 years old
    Platform: Instagram Reel (15 seconds)
    Goal: Launch new product, create buzz
    """
    
    strategy = thinker.generate_strategy(brief)
    print(f"Strategy:\n{strategy}")
    print()
    
    # Test 2: Analyze Image (NEW: Multimodal)
    print("📝 TEST 2: Analyze Reference Image (NEW: Multimodal)")
    print("-" * 70)
    print("Loading sample image from URL...")
    
    try:
        # Load a sample product image
        image_url = "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400"
        response = requests.get(image_url, timeout=10)
        image = Image.open(BytesIO(response.content))
        
        # Analyze image
        analysis = thinker.analyze_image(image, task="brand_analysis")
        print(f"Image Analysis:\n{analysis}")
        print()
        
        # Test 3: Generate Strategy with Image
        print("📝 TEST 3: Generate Strategy with Reference Image")
        print("-" * 70)
        strategy_with_image = thinker.generate_strategy(
            brief="Create social media content based on this coffee product image",
            reference_image=image
        )
        print(f"Strategy (with image context):\n{strategy_with_image}")
        print()
        
    except Exception as e:
        print(f"⚠️  Could not load image: {e}")
        print("Skipping multimodal tests (requires internet connection)")
        print()
    
    # Test 4: Generate Image Prompt
    print("📝 TEST 4: Generate SDXL Prompt")
    print("-" * 70)
    image_brief = "Premium cold brew coffee bottle on modern desk"
    image_prompt = thinker.generate_image_prompt(image_brief, style="minimal")
    print(f"SDXL Prompt:\n{image_prompt}")
    print()
    
    # Test 5: Generate Voice Script
    print("📝 TEST 5: Generate Voice Script")
    print("-" * 70)
    concept = "Introducing new cold brew coffee - fresh, bold, energizing"
    script = thinker.generate_voice_script(concept, duration=15, tone="friendly")
    print(f"Voice Script:\n{script}")
    print()
    
    print("=" * 70)
    print("✅ T5Gemma 2 Multimodal Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    # Run demo
    demo_t5gemma()
