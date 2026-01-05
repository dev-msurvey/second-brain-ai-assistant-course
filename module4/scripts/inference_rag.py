#!/usr/bin/env python3
"""
RAG-Enhanced Inference Script for AI Director (Module 4)

แนวคิด: Fine-tuning สอน "ทักษะ" (Skill) + RAG ป้อน "ความรู้" (Knowledge)
- Fine-tuned model: เรียนรู้วิธีเขียน caption, brief, tone adaptation
- RAG: ดึงข้อมูลแบรนด์จาก brands.json มาใส่ใน prompt

ข้อดี:
✅ รองรับแบรนด์ใหม่ได้ทันทีโดยไม่ต้อง retrain
✅ ข้อมูลอัปเดตแบบ real-time (แก้ brands.json ได้เลย)
✅ ป้องกัน hallucination (โมเดลไม่ต้องจำ brand details)
✅ Scalable สำหรับระบบ production

Architecture:
Input (User) → RAG Retrieval (brands.json) → Enriched Prompt → Fine-tuned Model → Output
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from loguru import logger


@dataclass
class BrandContext:
    """Brand information retrieved from RAG"""
    name: str
    description: str
    tone: List[str]
    target_audience: str
    core_values: List[str]
    visual_style: Optional[str] = None
    
    def to_prompt_string(self) -> str:
        """แปลงเป็น string ที่ใส่ใน prompt ได้"""
        tone_str = ", ".join(self.tone)
        values_str = ", ".join(self.core_values)
        
        result = f"""Brand: {self.name}
Description: {self.description}
Tone: {tone_str}
Target Audience: {self.target_audience}
Core Values: {values_str}"""
        
        if self.visual_style:
            result += f"\nVisual Style: {self.visual_style}"
        
        return result


class BrandRAG:
    """
    Retrieval-Augmented Generation for Brand Context
    
    ดึงข้อมูลแบรนด์จาก brands_v2.json แทนการให้โมเดลจำ
    """
    
    def __init__(self, brands_json_path: str):
        self.brands_json_path = Path(brands_json_path)
        self.brands_db: Dict[str, Dict] = {}
        self._load_brands()
    
    def _load_brands(self):
        """โหลดข้อมูลแบรนด์จาก JSON"""
        if not self.brands_json_path.exists():
            logger.warning(f"❌ ไม่พบไฟล์ {self.brands_json_path}")
            return
        
        with open(self.brands_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # สมมติว่า structure คือ {"brands": [...]}
        brands_list = data.get("brands", [])
        
        for brand in brands_list:
            brand_name = brand.get("name", "")
            self.brands_db[brand_name.lower()] = brand
        
        logger.info(f"✅ โหลดแบรนด์ {len(self.brands_db)} แบรนด์จาก RAG: {list(self.brands_db.keys())}")
    
    def retrieve(self, brand_name: str) -> Optional[BrandContext]:
        """
        ดึงข้อมูลแบรนด์จาก database
        
        Args:
            brand_name: ชื่อแบรนด์ (เช่น "CoffeeLab", "TechZone")
        
        Returns:
            BrandContext ถ้าเจอ, None ถ้าไม่เจอ
        """
        brand_key = brand_name.lower()
        
        if brand_key not in self.brands_db:
            logger.warning(f"⚠️  ไม่พบแบรนด์ '{brand_name}' ใน RAG database")
            return None
        
        brand_data = self.brands_db[brand_key]
        
        return BrandContext(
            name=brand_data.get("name", brand_name),
            description=brand_data.get("description", ""),
            tone=brand_data.get("tone", []),
            target_audience=brand_data.get("target_audience", ""),
            core_values=brand_data.get("core_values", []),
            visual_style=brand_data.get("visual_style")
        )
    
    def list_available_brands(self) -> List[str]:
        """แสดงรายชื่อแบรนด์ที่มีใน database"""
        return list(self.brands_db.keys())


class AIDirectorRAGInference:
    """
    AI Director Inference Engine with RAG Support
    
    ใช้ RAG ดึงข้อมูลแบรนด์มาใส่ใน prompt → ส่งให้ fine-tuned model ประมวลผล
    """
    
    def __init__(
        self,
        base_model_path: str = "Qwen/Qwen2.5-7B-Instruct",
        lora_adapter_path: Optional[str] = None,
        brands_json_path: str = "../../module2/data/raw/brands_v2.json",
        device: str = "auto"
    ):
        self.device = device
        self.tokenizer = None
        self.model = None
        self.rag = BrandRAG(brands_json_path)
        
        logger.info("🔧 กำลังโหลด tokenizer และโมเดล...")
        self._load_model(base_model_path, lora_adapter_path)
    
    def _load_model(self, base_model_path: str, lora_adapter_path: Optional[str]):
        """โหลด base model + LoRA adapter (ถ้ามี)"""
        
        # โหลด tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_path,
            trust_remote_code=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # โหลด base model
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16,
            device_map=self.device,
            trust_remote_code=True
        )
        
        # โหลด LoRA adapter (ถ้า fine-tune แล้ว)
        if lora_adapter_path and os.path.exists(lora_adapter_path):
            logger.info(f"🎯 กำลังโหลด LoRA adapter จาก {lora_adapter_path}")
            self.model = PeftModel.from_pretrained(self.model, lora_adapter_path)
            self.model = self.model.merge_and_unload()  # Merge เพื่อ inference เร็วขึ้น
            logger.info("✅ โหลด fine-tuned model สำเร็จ (ทักษะพร้อมใช้)")
        else:
            logger.warning("⚠️  ใช้ base model (ยังไม่ได้ fine-tune)")
        
        self.model.eval()
    
    def generate(
        self,
        instruction: str,
        brand_name: Optional[str] = None,
        additional_context: Optional[str] = None,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9
    ) -> str:
        """
        Generate content with RAG support
        
        Args:
            instruction: คำสั่งที่ต้องการ (เช่น "เขียน caption สำหรับโพสต์วันหยุด")
            brand_name: ชื่อแบรนด์ (จะดึงข้อมูลจาก RAG อัตโนมัติ)
            additional_context: Context เพิ่มเติม (เช่น "Product launch")
            max_new_tokens: ความยาว output
            temperature: ความสร้างสรรค์ (0.0-1.0)
            top_p: nucleus sampling
        
        Returns:
            Generated text
        """
        
        # 1. ดึงข้อมูลแบรนด์จาก RAG (ถ้ามี brand_name)
        brand_context = None
        if brand_name:
            brand_context = self.rag.retrieve(brand_name)
            
            if brand_context:
                logger.info(f"✅ RAG: ดึงข้อมูล {brand_name} สำเร็จ")
            else:
                logger.warning(f"⚠️  RAG: ไม่พบ {brand_name} - จะใช้ base model เท่านั้น")
        
        # 2. สร้าง enriched prompt (instruction + RAG context)
        input_text = self._build_input(brand_context, additional_context)
        
        # 3. Format ตาม Qwen2.5 chat template
        messages = [
            {"role": "system", "content": "You are an expert AI Creative Director specializing in Thai marketing content."},
            {"role": "user", "content": f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}"}
        ]
        
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # 4. Generate
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        # 5. Decode output
        generated = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # ตัดส่วน prompt ออก (เอาแค่ response)
        response = self._extract_response(generated, prompt)
        
        return response
    
    def _build_input(
        self,
        brand_context: Optional[BrandContext],
        additional_context: Optional[str]
    ) -> str:
        """สร้าง input text จาก RAG context"""
        
        parts = []
        
        # Brand context จาก RAG
        if brand_context:
            parts.append(brand_context.to_prompt_string())
        
        # Additional context (เช่น product info)
        if additional_context:
            parts.append(f"Context: {additional_context}")
        
        return "\n".join(parts) if parts else ""
    
    def _extract_response(self, generated_text: str, prompt: str) -> str:
        """ตัด prompt ออกจาก generated text"""
        if prompt in generated_text:
            response = generated_text[len(prompt):].strip()
        else:
            # Fallback: หา <|im_start|>assistant (Qwen format)
            if "<|im_start|>assistant" in generated_text:
                response = generated_text.split("<|im_start|>assistant")[-1]
                response = response.replace("<|im_end|>", "").strip()
            else:
                response = generated_text
        
        return response
    
    # ========== Helper Methods for Common Tasks ==========
    
    def generate_caption(
        self,
        brand_name: str,
        context: str = "General post"
    ) -> str:
        """
        Generate Instagram/TikTok caption
        
        ตัวอย่าง:
        >>> inference.generate_caption("TechZone", "Gaming mouse launch")
        """
        instruction = f"เขียน caption สำหรับโพสต์ {context}"
        return self.generate(instruction, brand_name=brand_name)
    
    def generate_campaign_brief(
        self,
        brand_name: str,
        campaign_objective: str
    ) -> str:
        """
        Generate campaign brief
        
        ตัวอย่าง:
        >>> inference.generate_campaign_brief("TechZone", "Product launch for new gaming series")
        """
        instruction = "สร้าง campaign brief"
        additional_context = f"Campaign Objective: {campaign_objective}"
        return self.generate(instruction, brand_name=brand_name, additional_context=additional_context)
    
    def adapt_brand_voice(
        self,
        brand_name: str,
        generic_message: str
    ) -> str:
        """
        Adapt generic message to brand voice
        
        ตัวอย่าง:
        >>> inference.adapt_brand_voice("TechZone", "มาลองผลิตภัณฑ์ใหม่กันเถอะ")
        """
        instruction = f"แปลงข้อความนี้ให้เข้ากับ brand voice: {generic_message}"
        return self.generate(instruction, brand_name=brand_name)


def demo_comparison():
    """
    Demo: เปรียบเทียบ 3 แนวทาง
    1. Base model (ไม่ fine-tune, ไม่ใช้ RAG)
    2. Fine-tuned only (ไม่ใช้ RAG - เสี่ยง hallucinate ถ้าแบรนด์ใหม่)
    3. Fine-tuned + RAG (แนะนำที่สุด)
    """
    
    print("\n" + "="*70)
    print("🎯 DEMO: RAG-Enhanced Inference for New Brand")
    print("="*70)
    
    # สมมติเราสร้างแบรนด์ใหม่ชื่อ "TechZone" (ไม่มีใน train.jsonl)
    new_brand = {
        "name": "TechZone",
        "description": "ร้านอุปกรณ์เกมมิ่งและไอทีครบวงจร",
        "tone": ["ล้ำสมัย", "รวดเร็ว", "เท่"],
        "target_audience": "Gamers วัยรุ่น-วัยทำงาน 18-35 ปี",
        "core_values": ["Performance First", "Cutting Edge Tech", "Gamer Community"]
    }
    
    print(f"\n📦 แบรนด์ใหม่: {new_brand['name']}")
    print(f"   (แบรนด์นี้ไม่เคยเจอใน train.jsonl เลย)")
    print(f"   Tone: {', '.join(new_brand['tone'])}")
    
    print("\n" + "-"*70)
    print("📝 Task: เขียน caption ประกาศขาย Gaming Mouse")
    print("-"*70)
    
    # NOTE: ใน demo จริง คุณต้องแก้ brands.json ให้มี TechZone ก่อน
    # หรือจะ mock ข้อมูลก็ได้
    
    print("""
┌─────────────────────────────────────────────────────────────────┐
│ แนวทาง 1: Base Model (ไม่ fine-tune, ไม่ RAG)                   │
│ ผลลัพธ์: ได้ caption ทั่วไป ไม่มี brand voice เฉพาะ            │
└─────────────────────────────────────────────────────────────────┘

"ลองใช้เมาส์เกมมิ่งตัวใหม่ของเราสิ! 🖱️"

❌ ปัญหา: ไม่มี tone, ไม่มี hashtag, ดูไม่มี brand identity

┌─────────────────────────────────────────────────────────────────┐
│ แนวทาง 2: Fine-tuned Only (ไม่ใช้ RAG)                         │
│ ผลลัพธ์: เสี่ยง hallucinate เพราะไม่รู้จัก TechZone             │
└─────────────────────────────────────────────────────────────────┘

"เติมพลังเช้าวันใหม่กับเมาส์ Gaming Mouse จาก TechZone ☕"

❌ ปัญหา: ใช้ tone ของ CoffeeLab (เติมพลังเช้า) มาปนกับ TechZone
         เพราะโมเดลจำได้แค่ว่า "caption ที่ดีต้องมีคำพวกนี้"

┌─────────────────────────────────────────────────────────────────┐
│ แนวทาง 3: Fine-tuned + RAG (✅ แนะนำ)                           │
│ ผลลัพธ์: RAG ดึงข้อมูล TechZone มาใส่ใน prompt                 │
└─────────────────────────────────────────────────────────────────┘

"🎮 Level Up Your Game! Gaming Mouse ตัวใหม่
สเปกเทพ ตอบสนองเร็วทันใจ
สำหรับ Gamers ตัวจริง 🔥
#TechZone #PerformanceFirst #GamingGear"

✅ สมบูรณ์แบบ:
   • ใช้ tone ที่ถูกต้อง (ล้ำสมัย, รวดเร็ว, เท่)
   • มี emoji ที่เหมาะกับแบรนด์ (🎮🔥 ไม่ใช่ ☕)
   • Core values ถูกสอดแทรก (Performance First)
   • Hashtag เฉพาะแบรนด์
""")
    
    print("\n" + "="*70)
    print("💡 สรุป:")
    print("="*70)
    print("""
✅ Fine-tuning → สอน "ทักษะ" (รู้วิธีเขียน format, tone, structure)
✅ RAG → ป้อน "ความรู้" (ข้อมูลแบรนด์แบบ real-time จาก brands.json)

ผลลัพธ์: รองรับแบรนด์ใหม่ได้ไม่จำกัดโดยไม่ต้อง retrain! 🚀
    """)


def demo_live_inference():
    """
    Demo: ใช้งานจริง (ต้องมี fine-tuned model และ brands.json ที่มี TechZone)
    
    วิธีเพิ่มแบรนด์ใหม่:
    1. แก้ไข ../../module2/data/raw/brands_v2.json เพิ่ม TechZone
    2. ไม่ต้อง retrain model
    3. Run script นี้ได้เลย!
    """
    
    print("\n" + "="*70)
    print("🚀 LIVE DEMO: ทดสอบกับแบรนด์ใหม่จริงๆ")
    print("="*70)
    
    # สมมติว่าคุณ fine-tune เสร็จแล้ว และเพิ่ม TechZone ใน brands.json แล้ว
    lora_adapter_path = "../models/qwen-7b-ai-director"
    
    if not os.path.exists(lora_adapter_path):
        print(f"\n❌ ยังไม่พบ fine-tuned model ที่ {lora_adapter_path}")
        print("   → ต้องรัน finetune_lora.py ก่อนครับ")
        return
    
    # สร้าง inference engine พร้อม RAG
    inference = AIDirectorRAGInference(
        lora_adapter_path=lora_adapter_path,
        brands_json_path="../../module2/data/raw/brands_v2.json"
    )
    
    print("\n📋 แบรนด์ที่มีใน RAG database:")
    available_brands = inference.rag.list_available_brands()
    print(f"   {', '.join(available_brands)}")
    
    # ทดสอบกับแบรนด์ใหม่
    print("\n" + "-"*70)
    print("Test 1: Generate Caption สำหรับแบรนด์ใหม่ 'TechZone'")
    print("-"*70)
    
    try:
        caption = inference.generate_caption(
            brand_name="TechZone",
            context="Gaming mouse launch"
        )
        print(f"\n📝 Output:\n{caption}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   → ตรวจสอบว่ามี 'TechZone' ใน brands_v2.json หรือยัง")
    
    # ทดสอบกับแบรนด์เก่า
    print("\n" + "-"*70)
    print("Test 2: Generate Caption สำหรับแบรนด์เดิม 'CoffeeLab'")
    print("-"*70)
    
    caption = inference.generate_caption(
        brand_name="CoffeeLab",
        context="Weekend special promotion"
    )
    print(f"\n📝 Output:\n{caption}")


if __name__ == "__main__":
    # เรียก demo แบบ conceptual ก่อน (ไม่ต้องใช้ GPU)
    demo_comparison()
    
    # ถ้าต้องการทดสอบจริง ให้ uncomment บรรทัดนี้
    # (ต้องมี GPU และ fine-tuned model พร้อม)
    # demo_live_inference()
