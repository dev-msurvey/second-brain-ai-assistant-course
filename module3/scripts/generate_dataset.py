#!/usr/bin/env python3
"""
Dataset Generator for AI Director Fine-tuning

This script generates training datasets from brand and campaign data
for fine-tuning AI Director models to create on-brand marketing content.
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from loguru import logger


class MarketingDatasetGenerator:
    """Generate training datasets for AI Director fine-tuning."""
    
    def __init__(
        self,
        brands_path: str = "../module2/data/raw/brands.json",
        campaigns_path: str = "../module2/data/raw/campaigns.json",
        output_dir: str = "data/generated"
    ):
        """
        Initialize dataset generator.
        
        Args:
            brands_path: Path to brands JSON file
            campaigns_path: Path to campaigns JSON file
            output_dir: Directory to save generated datasets
        """
        self.brands_path = Path(brands_path)
        self.campaigns_path = Path(campaigns_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.brands = []
        self.campaigns = []
        
    def load_data(self):
        """Load brands and campaigns data from JSON files."""
        logger.info(f"Loading brands from {self.brands_path}")
        with open(self.brands_path, 'r', encoding='utf-8') as f:
            self.brands = json.load(f)
        logger.info(f"Loaded {len(self.brands)} brands")
        
        logger.info(f"Loading campaigns from {self.campaigns_path}")
        with open(self.campaigns_path, 'r', encoding='utf-8') as f:
            self.campaigns = json.load(f)
        logger.info(f"Loaded {len(self.campaigns)} campaigns")
        
    def generate_caption_dataset(self) -> List[Dict[str, Any]]:
        """
        Generate Instagram/TikTok caption dataset.
        
        Uses content_examples from brands to create instruction-response pairs.
        
        Returns:
            List of training samples
        """
        dataset = []
        
        for brand in self.brands:
            brand_name = brand["name"]
            tone = brand["tone"]
            tagline = brand.get("tagline", "")
            target_audience = brand.get("target_audience", {})
            content_examples = brand.get("content_examples", {})
            
            # Good caption examples
            good_captions = content_examples.get("caption_good", [])
            for caption in good_captions:
                sample = {
                    "instruction": f"เขียน caption สำหรับ {brand_name} ใช้ tone: {tone}",
                    "input": f"Brand: {brand_name}\nTagline: {tagline}\nTarget: {target_audience.get('demographics', '')}",
                    "output": caption,
                    "metadata": {
                        "brand": brand_name,
                        "task": "caption_generation",
                        "platform": "instagram/tiktok",
                        "quality": "good"
                    }
                }
                dataset.append(sample)
            
            # Generate variations with different contexts
            if good_captions:
                base_caption = good_captions[0]
                
                # Variation 1: Product launch
                sample = {
                    "instruction": f"เขียน caption สำหรับการเปิดตัวผลิตภัณฑ์ใหม่ของ {brand_name}",
                    "input": f"Brand: {brand_name}\nTone: {tone}\nContext: Product launch announcement",
                    "output": f"🎉 เปิดตัว! {base_caption}",
                    "metadata": {
                        "brand": brand_name,
                        "task": "caption_generation",
                        "context": "product_launch",
                        "quality": "synthesized"
                    }
                }
                dataset.append(sample)
                
                # Variation 2: Weekend post
                sample = {
                    "instruction": f"เขียน caption สำหรับโพสต์วันหยุดสุดสัปดาห์ของ {brand_name}",
                    "input": f"Brand: {brand_name}\nTone: {tone}\nContext: Weekend casual post",
                    "output": f"สุขสันต์วันหยุด! {base_caption}",
                    "metadata": {
                        "brand": brand_name,
                        "task": "caption_generation",
                        "context": "weekend_post",
                        "quality": "synthesized"
                    }
                }
                dataset.append(sample)
                
        logger.info(f"Generated {len(dataset)} caption training samples")
        return dataset
    
    def generate_campaign_brief_dataset(self) -> List[Dict[str, Any]]:
        """
        Generate campaign brief creation dataset.
        
        Uses campaigns data to create instruction-response pairs.
        
        Returns:
            List of training samples
        """
        dataset = []
        
        for campaign in self.campaigns:
            brand_name = campaign["brand_name"]
            campaign_name = campaign["campaign_name"]
            brief = campaign["brief"]
            objectives = campaign.get("objectives", [])
            key_messages = campaign.get("key_messages", [])
            
            # Find corresponding brand
            brand = next((b for b in self.brands if b["name"] == brand_name), None)
            if not brand:
                continue
                
            tone = brand["tone"]
            
            # Basic brief generation
            sample = {
                "instruction": f"สร้าง campaign brief สำหรับ {brand_name}",
                "input": f"Brand: {brand_name}\nObjectives: {', '.join(objectives)}\nTone: {tone}",
                "output": brief,
                "metadata": {
                    "brand": brand_name,
                    "task": "brief_generation",
                    "campaign": campaign_name
                }
            }
            dataset.append(sample)
            
            # Key messages generation
            if key_messages:
                sample = {
                    "instruction": f"สร้าง key messages สำหรับ campaign {campaign_name} ของ {brand_name}",
                    "input": f"Brand: {brand_name}\nCampaign: {campaign_name}\nBrief: {brief[:200]}...",
                    "output": "\n".join([f"• {msg}" for msg in key_messages]),
                    "metadata": {
                        "brand": brand_name,
                        "task": "key_messages_generation",
                        "campaign": campaign_name
                    }
                }
                dataset.append(sample)
                
        logger.info(f"Generated {len(dataset)} campaign brief training samples")
        return dataset
    
    def generate_brand_voice_dataset(self) -> List[Dict[str, Any]]:
        """
        Generate brand voice adaptation dataset.
        
        Teaches model to adapt content to different brand voices.
        
        Returns:
            List of training samples
        """
        dataset = []
        
        # Generic message that needs brand voice adaptation
        generic_messages = [
            "เรามีผลิตภัณฑ์ใหม่เปิดตัวแล้ว มาลองกันเลย",
            "ขอบคุณที่ให้การสนับสนุนเสมอมา",
            "วันนี้เป็นวันพิเศษ มาร่วมฉลองกับเรา",
            "คุณภาพคือสิ่งที่เราให้ความสำคัญ",
            "เราพร้อมบริการคุณทุกวัน"
        ]
        
        for brand in self.brands:
            brand_name = brand["name"]
            tone = brand["tone"]
            brand_values = brand.get("brand_values", [])
            tagline = brand.get("tagline", "")
            
            for generic_msg in generic_messages:
                # Create brand-specific version
                brand_voice_msg = self._adapt_to_brand_voice(
                    generic_msg, 
                    brand_name, 
                    tone, 
                    brand_values
                )
                
                sample = {
                    "instruction": f"แปลงข้อความนี้ให้เข้ากับ brand voice ของ {brand_name}",
                    "input": f"Brand: {brand_name}\nTone: {tone}\nMessage: {generic_msg}",
                    "output": brand_voice_msg,
                    "metadata": {
                        "brand": brand_name,
                        "task": "brand_voice_adaptation",
                        "source_type": "generic_to_branded"
                    }
                }
                dataset.append(sample)
                
        logger.info(f"Generated {len(dataset)} brand voice training samples")
        return dataset
    
    def _adapt_to_brand_voice(
        self, 
        message: str, 
        brand_name: str, 
        tone: str, 
        values: List[str]
    ) -> str:
        """Helper to adapt generic message to brand voice."""
        # Simple adaptation rules (in production, use LLM)
        if "CoffeeLab" in brand_name:
            return f"☕️ {message} #CraftYourMorning"
        elif "FitFlow" in brand_name:
            return f"💪 {message} เริ่มต้นการเปลี่ยนแปลงวันนี้!"
        elif "GreenLeaf" in brand_name:
            return f"🌿 {message} เพื่อโลกที่ยั่งยืน"
        else:
            return message
    
    def generate_content_strategy_dataset(self) -> List[Dict[str, Any]]:
        """
        Generate content strategy dataset.
        
        Teaches model to create content strategies based on campaign objectives.
        
        Returns:
            List of training samples
        """
        dataset = []
        
        for campaign in self.campaigns:
            brand_name = campaign["brand_name"]
            campaign_name = campaign["campaign_name"]
            objectives = campaign.get("objectives", [])
            timeline = campaign.get("timeline", {})
            content_req = campaign.get("content_requirements", {})
            
            # Find corresponding brand
            brand = next((b for b in self.brands if b["name"] == brand_name), None)
            if not brand:
                continue
            
            # Generate strategy based on objectives and timeline
            strategy = self._create_content_strategy(
                brand_name,
                campaign_name,
                objectives,
                timeline,
                content_req
            )
            
            sample = {
                "instruction": f"สร้าง content strategy สำหรับ campaign {campaign_name}",
                "input": f"Brand: {brand_name}\nObjectives: {', '.join(objectives)}\nDuration: {timeline.get('start_date', '')} to {timeline.get('end_date', '')}",
                "output": strategy,
                "metadata": {
                    "brand": brand_name,
                    "task": "strategy_generation",
                    "campaign": campaign_name
                }
            }
            dataset.append(sample)
            
        logger.info(f"Generated {len(dataset)} content strategy training samples")
        return dataset
    
    def _create_content_strategy(
        self,
        brand_name: str,
        campaign_name: str,
        objectives: List[str],
        timeline: Dict,
        content_req: Dict
    ) -> str:
        """Helper to create content strategy text."""
        phases = timeline.get("phases", [])
        
        strategy = f"Content Strategy สำหรับ {campaign_name}:\n\n"
        strategy += f"วัตถุประสงค์:\n"
        for obj in objectives:
            strategy += f"• {obj}\n"
        
        strategy += f"\nแผนการสร้างเนื้อหา:\n"
        if phases:
            for phase in phases:
                strategy += f"• {phase.get('phase', '')}: {phase.get('content', '')} ({phase.get('dates', '')})\n"
        
        if content_req:
            strategy += f"\nความต้องการ Content:\n"
            strategy += f"• รูปภาพ: {content_req.get('image_count', 0)} ชิ้น\n"
            strategy += f"• วิดีโอ: {content_req.get('video_count', 0)} ชิ้น\n"
            strategy += f"• Formats: {', '.join(content_req.get('formats', []))}\n"
        
        return strategy.strip()
    
    def generate_all_datasets(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate all dataset types.
        
        Returns:
            Dictionary with all generated datasets
        """
        logger.info("Starting dataset generation...")
        
        self.load_data()
        
        datasets = {
            "caption": self.generate_caption_dataset(),
            "campaign_brief": self.generate_campaign_brief_dataset(),
            "brand_voice": self.generate_brand_voice_dataset(),
            "content_strategy": self.generate_content_strategy_dataset()
        }
        
        # Calculate total samples
        total_samples = sum(len(d) for d in datasets.values())
        logger.info(f"Generated {total_samples} total training samples")
        
        return datasets
    
    def save_dataset(
        self, 
        dataset: List[Dict[str, Any]], 
        filename: str,
        format: str = "jsonl"
    ):
        """
        Save dataset to file.
        
        Args:
            dataset: List of training samples
            filename: Output filename
            format: Output format (jsonl or json)
        """
        output_path = self.output_dir / f"{filename}.{format}"
        
        logger.info(f"Saving {len(dataset)} samples to {output_path}")
        
        if format == "jsonl":
            with open(output_path, 'w', encoding='utf-8') as f:
                for sample in dataset:
                    f.write(json.dumps(sample, ensure_ascii=False) + '\n')
        else:  # json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, ensure_ascii=False, indent=2)
        
        logger.success(f"Dataset saved to {output_path}")
    
    def create_combined_dataset(self, datasets: Dict[str, List[Dict[str, Any]]]):
        """
        Combine all datasets into train/val/test splits.
        
        Args:
            datasets: Dictionary of all datasets
        """
        # Combine all samples
        all_samples = []
        for dataset_type, samples in datasets.items():
            all_samples.extend(samples)
        
        # Shuffle
        random.shuffle(all_samples)
        
        # Split train/val/test (80/10/10)
        n = len(all_samples)
        train_end = int(n * 0.8)
        val_end = int(n * 0.9)
        
        train_set = all_samples[:train_end]
        val_set = all_samples[train_end:val_end]
        test_set = all_samples[val_end:]
        
        # Save splits
        self.save_dataset(train_set, "train", "jsonl")
        self.save_dataset(val_set, "val", "jsonl")
        self.save_dataset(test_set, "test", "jsonl")
        
        # Save combined for analysis
        combined = {
            "train": train_set,
            "val": val_set,
            "test": test_set,
            "metadata": {
                "total_samples": n,
                "train_samples": len(train_set),
                "val_samples": len(val_set),
                "test_samples": len(test_set),
                "generated_at": datetime.now().isoformat(),
                "dataset_types": list(datasets.keys())
            }
        }
        
        self.save_dataset([combined["metadata"]], "metadata", "json")
        
        logger.success(f"Combined dataset created:")
        logger.info(f"  Train: {len(train_set)} samples")
        logger.info(f"  Val: {len(val_set)} samples")
        logger.info(f"  Test: {len(test_set)} samples")


def main():
    """Main function to run dataset generation."""
    logger.info("=== AI Director Dataset Generator ===")
    
    generator = MarketingDatasetGenerator()
    
    # Generate all dataset types
    datasets = generator.generate_all_datasets()
    
    # Save individual datasets
    for dataset_type, samples in datasets.items():
        generator.save_dataset(samples, f"{dataset_type}_dataset", "jsonl")
    
    # Create combined train/val/test splits
    generator.create_combined_dataset(datasets)
    
    logger.success("Dataset generation complete! ✅")
    logger.info(f"Output directory: {generator.output_dir}")


if __name__ == "__main__":
    main()
