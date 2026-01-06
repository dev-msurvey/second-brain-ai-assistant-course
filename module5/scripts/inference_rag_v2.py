#!/usr/bin/env python3
"""
Enhanced RAG Inference using Module 5 Vector Search (Module 4 + Module 5 Integration)

Upgrade from Module 4:
- Module 4: Simple dictionary lookup (brands.json)
- Module 5: Vector search with parent-child retrieval

Benefits of Vector Search RAG:
✅ Semantic search (not just exact brand name match)
✅ Better context retrieval (finds relevant information)
✅ Scalable to unlimited brands
✅ Handles typos and variations
✅ Retrieves most relevant chunks automatically

Architecture:
Input → Vector Search (MongoDB Atlas) → Parent-Child Retrieval → Fine-tuned Model → Output
"""

import sys
import os
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from loguru import logger

# Add Module 5 to path
module5_path = Path(__file__).parent.parent.parent / "module5" / "src"
sys.path.insert(0, str(module5_path))

from module5.parent_child_retriever import ProductionRAG


@dataclass
class GenerationConfig:
    """Generation parameters for fine-tuned model"""
    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    do_sample: bool = True
    repetition_penalty: float = 1.1


class AIDirectorRAGInferenceV2:
    """
    AI Director with Enhanced Vector RAG (Module 5)
    
    Combines:
    - Module 4: Fine-tuned Qwen model (skills)
    - Module 5: Vector search RAG (knowledge)
    """
    
    def __init__(
        self,
        base_model_name: str = "Qwen/Qwen2.5-1.5B-Instruct",
        adapter_path: Optional[str] = None,
        use_vector_rag: bool = True,
        device: str = "auto"
    ):
        """
        Args:
            base_model_name: Base model (Qwen 1.5B or 7B)
            adapter_path: Path to fine-tuned LoRA adapter
            use_vector_rag: Use Module 5 vector RAG (True) or Module 4 dict lookup (False)
            device: Device for inference
        """
        self.base_model_name = base_model_name
        self.adapter_path = adapter_path
        self.use_vector_rag = use_vector_rag
        
        # Setup device
        if device == "auto":
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
        
        logger.info(f"🚀 Initializing AI Director RAG Inference V2")
        logger.info(f"   Base model: {base_model_name}")
        logger.info(f"   Adapter: {adapter_path}")
        logger.info(f"   RAG type: {'Vector Search (Module 5)' if use_vector_rag else 'Dictionary (Module 4)'}")
        logger.info(f"   Device: {self.device}")
        
        # Load model
        self._load_model()
        
        # Initialize RAG
        if use_vector_rag:
            logger.info("📚 Initializing Vector RAG (Module 5)...")
            self.rag = ProductionRAG(embedder_type="sentence-transformers")
        else:
            logger.warning("⚠️ Vector RAG disabled, using fallback (no retrieval)")
            self.rag = None
    
    def _load_model(self):
        """Load base model and adapter"""
        logger.info("⏳ Loading model...")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_name,
            trust_remote_code=True
        )
        
        # Load base model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map=self.device,
            trust_remote_code=True
        )
        
        # Load adapter if provided
        if self.adapter_path and os.path.exists(self.adapter_path):
            logger.info(f"⏳ Loading LoRA adapter from {self.adapter_path}...")
            self.model = PeftModel.from_pretrained(self.model, self.adapter_path)
            self.model = self.model.merge_and_unload()
            logger.info("✅ Adapter loaded and merged")
        else:
            logger.warning("⚠️ No adapter loaded, using base model only")
        
        self.model.eval()
        logger.info("✅ Model loaded successfully")
    
    def retrieve_brand_context(
        self,
        brand_name: Optional[str] = None,
        instruction: Optional[str] = None,
        k: int = 2
    ) -> str:
        """
        Retrieve brand context using Vector RAG
        
        Args:
            brand_name: Brand name to filter
            instruction: User instruction (for semantic search)
            k: Number of results
            
        Returns:
            Brand context string
        """
        if not self.rag:
            return "[No RAG context available]"
        
        # Create search query
        if instruction and brand_name:
            query = f"{instruction} for brand {brand_name}"
        elif brand_name:
            query = f"information about {brand_name}"
        elif instruction:
            query = instruction
        else:
            query = "brand information"
        
        # Retrieve using vector search
        results = self.rag.retrieve(
            query=query,
            brand_name=brand_name,
            k=k
        )
        
        if not results:
            return f"[No context found for query: {query}]"
        
        # Combine results
        context = "\n\n".join(results)
        return context
    
    def format_prompt(
        self,
        instruction: str,
        brand_context: str,
        input_text: Optional[str] = None
    ) -> str:
        """
        Format prompt with instruction, brand context, and optional input
        
        Args:
            instruction: Task instruction
            brand_context: Retrieved brand information
            input_text: Optional additional input
            
        Returns:
            Formatted prompt
        """
        # Qwen chat template format
        messages = [
            {
                "role": "system",
                "content": "You are an AI marketing assistant specialized in creating brand content. Use the provided brand context to generate appropriate content."
            }
        ]
        
        # Build user message
        user_message = f"{instruction}\n\n## Brand Context:\n{brand_context}"
        
        if input_text:
            user_message += f"\n\n## Additional Input:\n{input_text}"
        
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Apply chat template
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        return prompt
    
    def generate(
        self,
        instruction: str,
        brand_name: Optional[str] = None,
        input_text: Optional[str] = None,
        config: Optional[GenerationConfig] = None
    ) -> str:
        """
        Generate content with RAG-enhanced inference
        
        Args:
            instruction: Task instruction (e.g., "Create Instagram caption")
            brand_name: Brand name (optional, for filtering)
            input_text: Additional input (optional)
            config: Generation config (optional)
            
        Returns:
            Generated text
        """
        if config is None:
            config = GenerationConfig()
        
        # 1. Retrieve brand context
        logger.info(f"🔍 Retrieving context for: {brand_name or 'generic'}")
        brand_context = self.retrieve_brand_context(
            brand_name=brand_name,
            instruction=instruction,
            k=2
        )
        
        # 2. Format prompt
        prompt = self.format_prompt(instruction, brand_context, input_text)
        
        # 3. Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # 4. Generate
        logger.info(f"⚙️ Generating with {self.base_model_name}...")
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=config.max_new_tokens,
                temperature=config.temperature,
                top_p=config.top_p,
                top_k=config.top_k,
                do_sample=config.do_sample,
                repetition_penalty=config.repetition_penalty,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # 5. Decode
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the assistant's response (remove prompt)
        if "<|im_start|>assistant" in generated_text:
            response = generated_text.split("<|im_start|>assistant")[-1].strip()
        else:
            # Fallback: remove input prompt
            response = generated_text[len(prompt):].strip()
        
        logger.info(f"✅ Generated {len(response)} characters")
        
        return response
    
    def close(self):
        """Clean up resources"""
        if self.rag:
            self.rag.close()
        logger.info("👋 Resources cleaned up")


def demo_comparison():
    """
    Demo comparing Module 4 (dict) vs Module 5 (vector search)
    """
    print("\n" + "="*80)
    print("🔬 DEMO: Module 4 vs Module 5 RAG Comparison")
    print("="*80)
    
    # Initialize with vector RAG
    inferencer = AIDirectorRAGInferenceV2(
        base_model_name="Qwen/Qwen2.5-1.5B-Instruct",
        adapter_path=None,  # Set path if you have fine-tuned adapter
        use_vector_rag=True
    )
    
    # Test cases
    test_cases = [
        {
            "instruction": "Create an Instagram caption for a new product launch",
            "brand_name": None,  # Semantic search will find relevant brand
            "description": "Generic search (no brand specified)"
        },
        {
            "instruction": "Write a professional LinkedIn post about sustainability",
            "brand_name": None,
            "description": "Topic-based search"
        }
    ]
    
    # Also get actual brand names for specific tests
    try:
        from module5.mongodb_vector import MongoDBVectorStore
        store = MongoDBVectorStore()
        brands = store.collection.distinct("brand_name", {"doc_type": "parent"})
        store.close()
        
        if brands:
            test_cases.append({
                "instruction": "Create social media content",
                "brand_name": brands[0],
                "description": f"Brand-specific search ({brands[0]})"
            })
    except:
        pass
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}: {test['description']}")
        print('='*80)
        print(f"Instruction: {test['instruction']}")
        if test['brand_name']:
            print(f"Brand: {test['brand_name']}")
        
        try:
            output = inferencer.generate(
                instruction=test['instruction'],
                brand_name=test['brand_name']
            )
            
            print(f"\n📝 Generated Output:")
            print("-" * 80)
            print(output)
            print("-" * 80)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    inferencer.close()
    print("\n" + "="*80)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Director RAG Inference V2 (Module 5)")
    parser.add_argument("--model", default="Qwen/Qwen2.5-1.5B-Instruct", help="Base model")
    parser.add_argument("--adapter", help="Path to fine-tuned adapter")
    parser.add_argument("--instruction", default="Create an Instagram caption", help="Task instruction")
    parser.add_argument("--brand", help="Brand name")
    parser.add_argument("--demo", action="store_true", help="Run comparison demo")
    
    args = parser.parse_args()
    
    if args.demo:
        demo_comparison()
    else:
        # Single generation
        inferencer = AIDirectorRAGInferenceV2(
            base_model_name=args.model,
            adapter_path=args.adapter,
            use_vector_rag=True
        )
        
        try:
            output = inferencer.generate(
                instruction=args.instruction,
                brand_name=args.brand
            )
            
            print("\n" + "="*80)
            print("📝 Generated Content:")
            print("="*80)
            print(output)
            print("="*80 + "\n")
            
        finally:
            inferencer.close()


if __name__ == "__main__":
    main()
