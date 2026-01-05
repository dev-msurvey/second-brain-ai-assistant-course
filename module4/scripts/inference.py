#!/usr/bin/env python3
"""
Inference script for fine-tuned AI Director model.

Load fine-tuned LoRA model and generate marketing content.
"""

import torch
from pathlib import Path
from typing import Dict, Optional
from loguru import logger

from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


class AIDirectorInference:
    """Inference engine for AI Director fine-tuned model."""
    
    def __init__(
        self,
        model_path: str = "models/qwen-7b-ai-director",
        device: str = "auto",
    ):
        """
        Initialize inference engine.
        
        Args:
            model_path: Path to fine-tuned model
            device: Device to run inference on
        """
        self.model_path = Path(model_path)
        self.device = device
        
        self.model = None
        self.tokenizer = None
        
        self.load_model()
    
    def load_model(self):
        """Load fine-tuned model and tokenizer."""
        logger.info(f"Loading model from {self.model_path}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            trust_remote_code=True,
        )
        
        # Load base model + LoRA adapters
        base_model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map=self.device,
            trust_remote_code=True,
            torch_dtype=torch.bfloat16,
        )
        
        self.model = base_model
        self.model.eval()
        
        logger.success("Model loaded successfully")
    
    def format_prompt(
        self,
        instruction: str,
        input_text: str = "",
    ) -> str:
        """
        Format instruction and input as prompt.
        
        Args:
            instruction: Task instruction
            input_text: Context/input for the task
            
        Returns:
            Formatted prompt
        """
        prompt = f"""<|im_start|>system
You are an AI Director for marketing content creation. Generate on-brand content based on the instructions.<|im_end|>
<|im_start|>user
{instruction}

{input_text}<|im_end|>
<|im_start|>assistant
"""
        return prompt
    
    def generate(
        self,
        instruction: str,
        input_text: str = "",
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
        do_sample: bool = True,
    ) -> str:
        """
        Generate content based on instruction.
        
        Args:
            instruction: Task instruction
            input_text: Context/input for the task
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            do_sample: Whether to use sampling
            
        Returns:
            Generated text
        """
        # Format prompt
        prompt = self.format_prompt(instruction, input_text)
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        ).to(self.model.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=do_sample,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        generated_text = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1]:],
            skip_special_tokens=True,
        )
        
        return generated_text.strip()
    
    def generate_caption(
        self,
        brand_name: str,
        tone: str,
        context: str = "",
    ) -> str:
        """
        Generate Instagram/TikTok caption.
        
        Args:
            brand_name: Brand name
            tone: Brand tone
            context: Optional context (e.g., "product launch")
            
        Returns:
            Generated caption
        """
        if context:
            instruction = f"เขียน caption สำหรับ{context}ของ {brand_name}"
        else:
            instruction = f"เขียน caption สำหรับ {brand_name} ใช้ tone: {tone}"
        
        input_text = f"Brand: {brand_name}\nTone: {tone}"
        if context:
            input_text += f"\nContext: {context}"
        
        return self.generate(instruction, input_text, max_new_tokens=128)
    
    def generate_campaign_brief(
        self,
        brand_name: str,
        objectives: str,
        tone: str,
    ) -> str:
        """
        Generate campaign brief.
        
        Args:
            brand_name: Brand name
            objectives: Campaign objectives
            tone: Brand tone
            
        Returns:
            Generated brief
        """
        instruction = f"สร้าง campaign brief สำหรับ {brand_name}"
        input_text = f"Brand: {brand_name}\nObjectives: {objectives}\nTone: {tone}"
        
        return self.generate(instruction, input_text, max_new_tokens=256)
    
    def adapt_brand_voice(
        self,
        brand_name: str,
        tone: str,
        message: str,
    ) -> str:
        """
        Adapt generic message to brand voice.
        
        Args:
            brand_name: Brand name
            tone: Brand tone
            message: Generic message to adapt
            
        Returns:
            Brand-adapted message
        """
        instruction = f"แปลงข้อความนี้ให้เข้ากับ brand voice ของ {brand_name}"
        input_text = f"Brand: {brand_name}\nTone: {tone}\nMessage: {message}"
        
        return self.generate(instruction, input_text, max_new_tokens=128)


def demo():
    """Demo inference with fine-tuned model."""
    logger.info("=== AI Director Inference Demo ===\n")
    
    # Initialize inference
    ai_director = AIDirectorInference()
    
    # Demo 1: Caption generation
    logger.info("📝 Demo 1: Caption Generation")
    caption = ai_director.generate_caption(
        brand_name="CoffeeLab",
        tone="friendly, premium, modern",
        context="product launch",
    )
    logger.info(f"Generated caption:\n{caption}\n")
    
    # Demo 2: Brand voice adaptation
    logger.info("🎨 Demo 2: Brand Voice Adaptation")
    adapted = ai_director.adapt_brand_voice(
        brand_name="FitFlow",
        tone="energetic, motivating",
        message="เรามีโปรโมชั่นพิเศษสำหรับคุณ",
    )
    logger.info(f"Adapted message:\n{adapted}\n")
    
    # Demo 3: Campaign brief
    logger.info("📋 Demo 3: Campaign Brief")
    brief = ai_director.generate_campaign_brief(
        brand_name="GreenLeaf",
        objectives="education, trust building",
        tone="natural, caring",
    )
    logger.info(f"Generated brief:\n{brief}\n")
    
    logger.success("✅ Demo completed!")


if __name__ == "__main__":
    demo()
