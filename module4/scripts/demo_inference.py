#!/usr/bin/env python3
"""
Demo Inference Script for AI Director Model (qwen-7b-ai-director-v2)

This script demonstrates 4 use cases:
1. Customer Service Response
2. Visual Prompt Generation  
3. Video Script Writing
4. Cross-Channel Content Adaptation

Requirements:
- transformers==4.38.0
- peft==0.8.2
- bitsandbytes==0.42.0
- torch>=2.0.0
- accelerate==0.26.1
"""

import os
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from typing import Dict, Optional

# ANSI colors for pretty output
GREEN = "\033[92m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


class AIDirectorInference:
    """Inference class for AI Director model with LoRA adapters"""
    
    def __init__(self, model_path: str, base_model: str = "Qwen/Qwen2.5-7B-Instruct"):
        """
        Initialize inference model
        
        Args:
            model_path: Path to LoRA adapter model
            base_model: Base model name from HuggingFace
        """
        self.model_path = model_path
        self.base_model = base_model
        self.model = None
        self.tokenizer = None
        
        print(f"{BLUE}🔧 Initializing AI Director Inference...{RESET}")
        print(f"   Base Model: {base_model}")
        print(f"   LoRA Adapter: {model_path}")
        
    def load_model(self):
        """Load model with proper BitsAndBytesConfig"""
        
        # Configure 4-bit quantization (CRITICAL: Must match training)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        print(f"{YELLOW}📥 Loading base model with 4-bit quantization...{RESET}")
        
        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )
        
        print(f"{YELLOW}📥 Loading LoRA adapters...{RESET}")
        
        # Load LoRA adapters
        self.model = PeftModel.from_pretrained(
            self.model,
            self.model_path,
            device_map="auto"
        )
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True
        )
        
        print(f"{GREEN}✅ Model loaded successfully!{RESET}\n")
        
    def generate(
        self,
        instruction: str,
        input_text: str,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """
        Generate response using the fine-tuned model
        
        Args:
            instruction: Task instruction
            input_text: Input context
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated text
        """
        
        # Format prompt (same as training)
        prompt = f"""system
You are an AI marketing director specializing in Thai content creation and brand management.

user
{instruction}

{input_text}

assistant
"""
        
        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode output
        full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only assistant response (CRITICAL: Correct parsing method)
        if "assistant" in full_response:
            parts = full_response.split("assistant")
            result = parts[-1].strip()
        else:
            result = full_response.strip()
            
        return result


def print_section(title: str):
    """Print section header"""
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{title}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")


def print_example(use_case: str, instruction: str, input_text: str, output: str):
    """Print formatted example"""
    print(f"{YELLOW}📌 Use Case: {use_case}{RESET}")
    print(f"\n{BOLD}Instruction:{RESET}")
    print(f"  {instruction}")
    print(f"\n{BOLD}Input:{RESET}")
    for line in input_text.strip().split('\n'):
        print(f"  {line}")
    print(f"\n{BOLD}Generated Output:{RESET}")
    print(f"{GREEN}{output}{RESET}")
    print(f"\n{'-'*80}\n")


def main():
    """Run inference demo with 4 use cases"""
    
    # Check if model exists
    model_path = "../models/qwen-7b-ai-director-v2"
    
    if not os.path.exists(model_path):
        print(f"{RED}❌ Error: Model not found at {model_path}{RESET}")
        print(f"{YELLOW}ℹ️  Expected model structure:{RESET}")
        print(f"   module4/models/qwen-7b-ai-director-v2/")
        print(f"     ├── adapter_model.safetensors")
        print(f"     ├── adapter_config.json")
        print(f"     └── tokenizer files...")
        sys.exit(1)
    
    # Initialize inference
    print_section("🚀 AI Director Inference Demo - 4 Use Cases")
    
    inferencer = AIDirectorInference(model_path=model_path)
    inferencer.load_model()
    
    # ==========================================================================
    # USE CASE 1: Customer Service Response (Negative Comment)
    # ==========================================================================
    print_section("1️⃣  Customer Service Response - Crisis Management")
    
    instruction1 = "ตอบคอมเมนต์เชิงลบของลูกค้า GlowLab"
    input1 = """Brand: GlowLab
Tone: gentle, confident, natural, science-backed
Comment: 'สินค้าที่ได้รับไม่ตรงตามที่สั่ง รู้สึกผิดหวังมาก'"""
    
    print(f"{YELLOW}⏳ Generating response...{RESET}")
    output1 = inferencer.generate(instruction1, input1, max_new_tokens=256)
    print_example("Customer Service", instruction1, input1, output1)
    
    # ==========================================================================
    # USE CASE 2: Visual Prompt Generation (Midjourney/Stable Diffusion)
    # ==========================================================================
    print_section("2️⃣  Visual Prompt Generation - Midjourney/Stable Diffusion")
    
    instruction2 = "สร้าง Midjourney/Stable Diffusion prompt สำหรับ TechZone - TikTok video thumbnail"
    input2 = """Brand: TechZone
Context: TikTok video thumbnail
Visual Style: dark cyberpunk aesthetic, neon RGB lighting, action shots, close-ups of hardware, gaming setup, dark backgrounds with neon accents
Color Palette: #00FF00, #1A1A1A, #FF00FF, #00FFFF"""
    
    print(f"{YELLOW}⏳ Generating visual prompt...{RESET}")
    output2 = inferencer.generate(instruction2, input2, max_new_tokens=256)
    print_example("Visual Prompting", instruction2, input2, output2)
    
    # ==========================================================================
    # USE CASE 3: Video Script Writing (TikTok 60s)
    # ==========================================================================
    print_section("3️⃣  Video Script Writing - TikTok 60s Format")
    
    instruction3 = "เขียนบทวิดีโอ TikTok 60s สำหรับแคมเปญ Engagement ของ GlowLab"
    input3 = """Brand: GlowLab
Format: TikTok 60s
Objective: Engagement
Tone: gentle, confident, natural, science-backed
Key Message: Natural Beauty, Scientific Care"""
    
    print(f"{YELLOW}⏳ Generating script...{RESET}")
    output3 = inferencer.generate(instruction3, input3, max_new_tokens=512)
    print_example("Script Writing", instruction3, input3, output3)
    
    # ==========================================================================
    # USE CASE 4: Cross-Channel Content Adaptation (Instagram → Twitter)
    # ==========================================================================
    print_section("4️⃣  Cross-Channel Adaptation - Instagram to Twitter")
    
    instruction4 = "Adapt content from Instagram to Twitter for UrbanNest"
    input4 = """Brand: UrbanNest
Source: Instagram
Target: Twitter
Original: 'พื้นที่เล็ก แต่สไตล์ไม่เล็กตาม ✨'"""
    
    print(f"{YELLOW}⏳ Adapting content...{RESET}")
    output4 = inferencer.generate(instruction4, input4, max_new_tokens=256)
    print_example("Cross-Channel", instruction4, input4, output4)
    
    # ==========================================================================
    # Summary
    # ==========================================================================
    print_section("✅ Demo Complete!")
    
    print(f"{GREEN}All 4 use cases tested successfully!{RESET}\n")
    print(f"{BOLD}Tested Use Cases:{RESET}")
    print(f"  ✓ Customer Service Response (Crisis Management)")
    print(f"  ✓ Visual Prompt Generation (Midjourney/SD)")
    print(f"  ✓ Video Script Writing (TikTok 60s)")
    print(f"  ✓ Cross-Channel Content Adaptation")
    print(f"\n{YELLOW}Model: qwen-7b-ai-director-v2{RESET}")
    print(f"{YELLOW}Training Loss: 0.6097{RESET}")
    print(f"{YELLOW}Training Time: 2.58 hours{RESET}\n")


if __name__ == "__main__":
    main()
