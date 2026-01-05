#!/usr/bin/env python3
"""
LoRA Fine-tuning Script for AI Director

Fine-tunes a base LLM (Qwen2.5-7B) using LoRA on marketing content generation tasks.
Optimized for small datasets (39 samples) with high quality.
"""

import json
import torch
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass, field
from loguru import logger

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType,
)
from datasets import load_dataset, Dataset
import bitsandbytes as bnb


@dataclass
class FineTuningConfig:
    """Configuration for fine-tuning."""
    
    # Model
    base_model: str = "Qwen/Qwen2.5-7B-Instruct"  # Thai support ดี
    max_seq_length: int = 1024  # Short content ไม่ต้องยาว
    
    # LoRA parameters
    lora_r: int = 16  # Rank
    lora_alpha: int = 32  # Alpha (usually 2x of r)
    lora_dropout: float = 0.05
    target_modules: List[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ])
    
    # Training parameters
    num_train_epochs: int = 3  # Few epochs สำหรับ small dataset
    per_device_train_batch_size: int = 1
    gradient_accumulation_steps: int = 4  # Effective batch_size = 4
    learning_rate: float = 2e-4
    warmup_steps: int = 10
    logging_steps: int = 1
    save_steps: int = 50
    eval_steps: int = 50
    
    # Optimization
    load_in_4bit: bool = True  # Use 4-bit quantization (QLoRA)
    use_gradient_checkpointing: bool = True
    optim: str = "paged_adamw_8bit"
    
    # Paths
    dataset_path: str = "../module3/data/generated"
    output_dir: str = "models/qwen-7b-ai-director"
    logs_dir: str = "logs"


class AIDirectorFineTuner:
    """Fine-tune LLM for AI Director marketing content generation."""
    
    def __init__(self, config: FineTuningConfig):
        """
        Initialize fine-tuner.
        
        Args:
            config: Fine-tuning configuration
        """
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.logs_dir = Path(config.logs_dir)
        
        # Create directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logger.add(
            self.logs_dir / "finetune_{time}.log",
            rotation="500 MB",
            retention="10 days",
            level="INFO",
        )
        
        self.model = None
        self.tokenizer = None
        self.dataset = None
        
    def check_gpu(self):
        """Check GPU availability."""
        if not torch.cuda.is_available():
            logger.error("No GPU found! Fine-tuning requires CUDA GPU.")
            raise RuntimeError("CUDA GPU required for fine-tuning")
        
        gpu_name = torch.cuda.get_device_properties(0).name
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        logger.info(f"GPU: {gpu_name}")
        logger.info(f"GPU Memory: {gpu_memory:.2f} GB")
        
        if gpu_memory < 8:
            logger.warning("GPU memory < 8GB. Consider using Colab with T4/L4 GPU")
    
    def load_tokenizer(self):
        """Load tokenizer."""
        logger.info(f"Loading tokenizer: {self.config.base_model}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.base_model,
            trust_remote_code=True,
            padding_side="right",  # For training
        )
        
        # Set pad token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        
        logger.success(f"Tokenizer loaded. Vocab size: {len(self.tokenizer)}")
    
    def load_model(self):
        """Load base model with 4-bit quantization."""
        logger.info(f"Loading model: {self.config.base_model}")
        
        # 4-bit quantization config
        if self.config.load_in_4bit:
            from transformers import BitsAndBytesConfig
            
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.bfloat16,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.base_model,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.bfloat16,
            )
        
        # Prepare for k-bit training
        self.model = prepare_model_for_kbit_training(self.model)
        
        logger.success("Model loaded successfully")
        
        # Print model info
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        all_params = sum(p.numel() for p in self.model.parameters())
        logger.info(f"Trainable params: {trainable_params:,} / {all_params:,} ({100 * trainable_params / all_params:.2f}%)")
    
    def setup_lora(self):
        """Setup LoRA adapters."""
        logger.info("Setting up LoRA adapters...")
        
        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=self.config.target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type=TaskType.CAUSAL_LM,
        )
        
        self.model = get_peft_model(self.model, lora_config)
        
        logger.success("LoRA adapters configured")
        
        # Print trainable parameters
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        all_params = sum(p.numel() for p in self.model.parameters())
        logger.info(f"LoRA trainable params: {trainable_params:,} / {all_params:,} ({100 * trainable_params / all_params:.2f}%)")
    
    def load_datasets(self):
        """Load training datasets."""
        logger.info(f"Loading datasets from {self.config.dataset_path}")
        
        dataset_path = Path(self.config.dataset_path)
        
        self.dataset = load_dataset(
            "json",
            data_files={
                "train": str(dataset_path / "train_v2.jsonl"),
                "validation": str(dataset_path / "val_v2.jsonl"),
                "test": str(dataset_path / "test_v2.jsonl"),
            }
        )
        
        logger.info(f"Train samples: {len(self.dataset['train'])}")
        logger.info(f"Validation samples: {len(self.dataset['validation'])}")
        logger.info(f"Test samples: {len(self.dataset['test'])}")
        
        # Show sample
        sample = self.dataset['train'][0]
        logger.info(f"Sample instruction: {sample['instruction'][:80]}...")
        logger.info(f"Sample output: {sample['output'][:80]}...")
    
    def format_instruction(self, sample: Dict) -> str:
        """
        Format sample as instruction-following prompt.
        
        Uses Alpaca format similar to Module 3 dataset.
        """
        instruction = sample["instruction"]
        input_text = sample["input"]
        output_text = sample["output"]
        
        # Qwen2.5 chat format
        prompt = f"""<|im_start|>system
You are an AI Director for marketing content creation. Generate on-brand content based on the instructions.<|im_end|>
<|im_start|>user
{instruction}

{input_text}<|im_end|>
<|im_start|>assistant
{output_text}<|im_end|>"""
        
        return prompt
    
    def tokenize_dataset(self):
        """Tokenize datasets."""
        logger.info("Tokenizing datasets...")
        
        def tokenize_function(examples):
            # Format prompts
            texts = [self.format_instruction(ex) for ex in examples]
            
            # Tokenize
            tokenized = self.tokenizer(
                texts,
                truncation=True,
                max_length=self.config.max_seq_length,
                padding="max_length",
                return_tensors=None,
            )
            
            # Labels = input_ids for causal LM
            tokenized["labels"] = tokenized["input_ids"].copy()
            
            return tokenized
        
        # Convert to list of dicts format
        def to_dict_format(dataset):
            return [
                {
                    "instruction": ex["instruction"],
                    "input": ex["input"],
                    "output": ex["output"],
                }
                for ex in dataset
            ]
        
        # Tokenize all splits
        self.dataset["train"] = self.dataset["train"].map(
            lambda batch: tokenize_function([batch]),
            batched=False,
            desc="Tokenizing train",
        )
        
        self.dataset["validation"] = self.dataset["validation"].map(
            lambda batch: tokenize_function([batch]),
            batched=False,
            desc="Tokenizing validation",
        )
        
        logger.success("Datasets tokenized")
        
        # Show tokenized sample
        sample = self.dataset["train"][0]
        logger.info(f"Tokenized length: {len(sample['input_ids'])} tokens")
    
    def train(self):
        """Train the model."""
        logger.info("=== Starting Training ===")
        
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            num_train_epochs=self.config.num_train_epochs,
            per_device_train_batch_size=self.config.per_device_train_batch_size,
            per_device_eval_batch_size=self.config.per_device_train_batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            learning_rate=self.config.learning_rate,
            warmup_steps=self.config.warmup_steps,
            logging_steps=self.config.logging_steps,
            save_steps=self.config.save_steps,
            eval_steps=self.config.eval_steps,
            evaluation_strategy="steps",
            save_strategy="steps",
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            optim=self.config.optim,
            fp16=False,
            bf16=torch.cuda.is_bf16_supported(),
            gradient_checkpointing=self.config.use_gradient_checkpointing,
            logging_dir=str(self.logs_dir),
            report_to=["tensorboard"],
            push_to_hub=False,
            save_total_limit=2,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,  # Causal LM, not masked LM
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=self.dataset["train"],
            eval_dataset=self.dataset["validation"],
            data_collator=data_collator,
        )
        
        # Train
        logger.info("Starting training loop...")
        train_result = trainer.train()
        
        logger.success("Training completed!")
        logger.info(f"Train loss: {train_result.metrics['train_loss']:.4f}")
        logger.info(f"Train runtime: {train_result.metrics['train_runtime']:.2f}s")
        
        # Save final model
        trainer.save_model()
        self.tokenizer.save_pretrained(self.output_dir)
        
        logger.success(f"Model saved to {self.output_dir}")
        
        return train_result
    
    def evaluate(self):
        """Evaluate on test set."""
        logger.info("=== Evaluating on Test Set ===")
        
        training_args = TrainingArguments(
            output_dir=str(self.output_dir),
            per_device_eval_batch_size=1,
            fp16=False,
            bf16=torch.cuda.is_bf16_supported(),
        )
        
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )
        
        trainer = Trainer(
            model=self.model,
            args=training_args,
            eval_dataset=self.dataset["test"],
            data_collator=data_collator,
        )
        
        eval_results = trainer.evaluate()
        
        logger.info(f"Test loss: {eval_results['eval_loss']:.4f}")
        logger.info(f"Test perplexity: {torch.exp(torch.tensor(eval_results['eval_loss'])):.2f}")
        
        # Save evaluation results
        results_path = self.output_dir / "eval_results.json"
        with open(results_path, 'w') as f:
            json.dump(eval_results, f, indent=2)
        
        logger.success(f"Evaluation results saved to {results_path}")
        
        return eval_results
    
    def run(self):
        """Run complete fine-tuning pipeline."""
        logger.info("=" * 70)
        logger.info("AI Director LoRA Fine-tuning Pipeline")
        logger.info("=" * 70)
        
        # Check GPU
        self.check_gpu()
        
        # Load components
        self.load_tokenizer()
        self.load_model()
        self.setup_lora()
        
        # Load and prepare data
        self.load_datasets()
        self.tokenize_dataset()
        
        # Train
        train_result = self.train()
        
        # Evaluate
        eval_results = self.evaluate()
        
        logger.info("=" * 70)
        logger.success("✅ Fine-tuning pipeline completed!")
        logger.info(f"Model saved to: {self.output_dir}")
        logger.info("=" * 70)
        
        return {
            "train_result": train_result,
            "eval_results": eval_results,
        }


def main():
    """Main function to run fine-tuning."""
    config = FineTuningConfig()
    
    finetuner = AIDirectorFineTuner(config)
    results = finetuner.run()
    
    logger.info("Done! 🎉")


if __name__ == "__main__":
    main()
