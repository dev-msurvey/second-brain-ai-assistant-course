#!/usr/bin/env python3
"""
Data Augmentation Script for Module 4

เพิ่มแบรนด์สมมติ (Synthetic Brands) หลากหลายอุตสาหกรรม
เข้าไปใน train.jsonl เพื่อป้องกัน Overfitting

ปัญหาเดิม:
- มีแค่ 3 แบรนด์: CoffeeLab (กาแฟ), FitFlow (ฟิตเนส), GreenLeaf (ผัก)
- โมเดลเสี่ยง hallucinate เมื่อเจอแบรนด์ใหม่

วิธีแก้:
- สร้างแบรนด์สมมติ 6-8 แบรนด์ หลากหลายอุตสาหกรรม
- เพิ่ม 30-50 samples ลง train.jsonl
- โมเดลจะเรียนรู้ว่า "Brand tone แตกต่างกันตามอุตสาหกรรม"
"""

import json
import random
from pathlib import Path
from typing import List, Dict


# ========== Synthetic Brand Definitions ==========

SYNTHETIC_BRANDS = [
    {
        "name": "PetPals",
        "industry": "Pet Care",
        "description": "อาหารและสินค้าสัตว์เลี้ยงคุณภาพพรีเมี่ยม",
        "tone": ["น่ารัก", "อบอุ่น", "เป็นกันเอง"],
        "target_audience": "เจ้าของสัตว์เลี้ยง 25-45 ปี",
        "core_values": ["Love Your Pets", "Premium Quality", "Happy Tails"],
        "emoji_style": ["🐶", "🐱", "❤️", "🎾", "🦴"],
        "hashtags": ["#PetPals", "#HappyPets", "ตัวเก่งของแม่"]
    },
    {
        "name": "SpeedyLoans",
        "industry": "Finance/Banking",
        "description": "สินเชื่อด่วน อนุมัติไว ใช้เทคโนโลยี AI",
        "tone": ["น่าเชื่อถือ", "มืออาชีพ", "รวดเร็ว"],
        "target_audience": "ผู้ประกอบการ วัยทำงาน 30-55 ปี",
        "core_values": ["Fast Approval", "Transparent", "Customer First"],
        "emoji_style": ["💰", "⚡", "📊", "✅", "🏦"],
        "hashtags": ["#SpeedyLoans", "#FastApproval", "#SmartFinance"]
    },
    {
        "name": "LuxStay",
        "industry": "Hotel/Hospitality",
        "description": "โรงแรมบูติก ห้องพัก luxury ท่ามกลางธรรมชาติ",
        "tone": ["หรูหรา", "สงบ", "exclusive"],
        "target_audience": "นักท่องเที่ยวระดับ high-end 35-60 ปี",
        "core_values": ["Luxury Experience", "Nature Harmony", "Exclusive Service"],
        "emoji_style": ["🏨", "✨", "🌿", "🛁", "🍷"],
        "hashtags": ["#LuxStay", "#LuxuryEscape", "#PrivateRetreat"]
    },
    {
        "name": "EduKid",
        "industry": "Education/Children",
        "description": "แอปเกมการศึกษาสำหรับเด็ก เรียนรู้ผ่านการเล่น",
        "tone": ["สนุกสนาน", "ให้กำลังใจ", "เป็นมิตร"],
        "target_audience": "พ่อแม่ที่มีลูกอายุ 3-12 ปี",
        "core_values": ["Learn Through Play", "Safe Content", "Child Development"],
        "emoji_style": ["🎓", "🎮", "🌈", "🧩", "⭐"],
        "hashtags": ["#EduKid", "#PlayToLearn", "#SmartKids"]
    },
    {
        "name": "UrbanRide",
        "industry": "Transportation",
        "description": "บริการ e-scooter และ e-bike สำหรับคนเมือง",
        "tone": ["ทันสมัย", "eco-friendly", "สะดวกสบาย"],
        "target_audience": "คนทำงานในเมืองใหญ่ 20-40 ปี",
        "core_values": ["Green Mobility", "Urban Convenience", "Affordable"],
        "emoji_style": ["🛴", "🌱", "🌆", "⚡", "🚴"],
        "hashtags": ["#UrbanRide", "#EcoCommute", "#CityMobility"]
    },
    {
        "name": "HealthHub",
        "industry": "Healthcare/Telemedicine",
        "description": "แพลตฟอร์มปรึกษาหมอออนไลน์ 24/7",
        "tone": ["เป็นมิตร", "มืออาชีพ", "ให้ความมั่นใจ"],
        "target_audience": "ทุกช่วงวัย โดยเฉพาะผู้สูงอายุ",
        "core_values": ["Accessible Healthcare", "Expert Care", "Always Available"],
        "emoji_style": ["🏥", "👨‍⚕️", "💊", "📱", "❤️"],
        "hashtags": ["#HealthHub", "#OnlineDoctor", "#CareAnywhere"]
    },
    {
        "name": "FoodieBox",
        "industry": "Food Delivery/Subscription",
        "description": "กล่องอาหารพร้อมทำ ส่งถึงบ้าน มีสูตรใหม่ทุกสัปดาห์",
        "tone": ["อร่อย", "สนุก", "ครีเอทีฟ"],
        "target_audience": "คนทำงาน millennial 25-40 ปี",
        "core_values": ["Fresh Ingredients", "Easy Cooking", "New Experiences"],
        "emoji_style": ["🍱", "🍜", "👨‍🍳", "📦", "✨"],
        "hashtags": ["#FoodieBox", "#HomeCooking", "#WeeklyRecipes"]
    },
    {
        "name": "GlowLab",
        "industry": "Cosmetics/Skincare",
        "description": "เครื่องสำอางไทย ใช้สารสกัดธรรมชาติ",
        "tone": ["นุ่มนวล", "มั่นใจ", "natural beauty"],
        "target_audience": "ผู้หญิงวัยทำงาน 20-45 ปี",
        "core_values": ["Natural Ingredients", "Gentle Care", "Thai Beauty Wisdom"],
        "emoji_style": ["✨", "🌸", "💄", "🧴", "💆‍♀️"],
        "hashtags": ["#GlowLab", "#NaturalGlow", "#ThaiBeauty"]
    }
]


# ========== Template Generators ==========

def generate_caption_sample(brand: Dict) -> Dict:
    """สร้าง caption generation sample"""
    
    contexts = ["Product launch", "Weekend post", "Customer testimonial", "Behind the scenes"]
    context = random.choice(contexts)
    
    # สร้าง output ตาม brand tone
    emoji = random.choice(brand["emoji_style"])
    hashtag = random.choice(brand["hashtags"])
    
    if "น่ารัก" in brand["tone"]:
        output = f"{emoji} รักษ์สัตว์เลี้ยง ด้วยใจ ที่ {brand['name']} {hashtag}"
    elif "น่าเชื่อถือ" in brand["tone"]:
        output = f"{emoji} {brand['core_values'][0]} กับ {brand['name']} - {brand['description'][:30]}... {hashtag}"
    elif "หรูหรา" in brand["tone"]:
        output = f"{emoji} Experience {brand['core_values'][0]} at {brand['name']} {hashtag}"
    elif "สนุกสนาน" in brand["tone"]:
        output = f"{emoji} มาสนุกกันเถอะ! ที่ {brand['name']} {hashtag}"
    elif "ทันสมัย" in brand["tone"]:
        output = f"{emoji} {brand['core_values'][0]} - {brand['name']} พร้อมแล้วสำหรับคุณ {hashtag}"
    else:
        output = f"{emoji} ค้นพบ {brand['name']} {hashtag}"
    
    return {
        "instruction": f"เขียน caption สำหรับโพสต์ {context} ของ {brand['name']}",
        "input": f"Brand: {brand['name']}\nTone: {', '.join(brand['tone'])}\nContext: {context}",
        "output": output,
        "metadata": {
            "brand": brand["name"],
            "task": "caption_generation",
            "context": context.lower().replace(" ", "_"),
            "quality": "synthetic"
        }
    }


def generate_brand_voice_sample(brand: Dict) -> Dict:
    """สร้าง brand voice adaptation sample"""
    
    generic_messages = [
        "ลองผลิตภัณฑ์ใหม่กันเถอะ",
        "มาร่วมฉลองกับเรา",
        "สนใจติดต่อเราได้เลย",
        "วันนี้เป็นวันพิเศษ"
    ]
    
    generic_msg = random.choice(generic_messages)
    emoji = random.choice(brand["emoji_style"])
    tone_keyword = brand["tone"][0]
    
    # Adapt ตาม brand voice
    adapted = f"{emoji} {generic_msg} {tone_keyword}กับ {brand['name']}"
    
    return {
        "instruction": f"แปลงข้อความนี้ให้เข้ากับ brand voice ของ {brand['name']}",
        "input": f"Brand: {brand['name']}\nTone: {', '.join(brand['tone'])}\nMessage: {generic_msg}",
        "output": adapted,
        "metadata": {
            "brand": brand["name"],
            "task": "brand_voice_adaptation",
            "source_type": "generic_to_branded",
            "quality": "synthetic"
        }
    }


def generate_key_messages_sample(brand: Dict) -> Dict:
    """สร้าง key messages generation sample"""
    
    values = brand["core_values"]
    
    key_messages = "\n".join([f"• {value}" for value in values[:3]])
    
    return {
        "instruction": f"สร้าง key messages สำหรับแคมเปญของ {brand['name']}",
        "input": f"Brand: {brand['name']}\nIndustry: {brand['industry']}\nDescription: {brand['description']}\nCore Values: {', '.join(values)}",
        "output": key_messages,
        "metadata": {
            "brand": brand["name"],
            "task": "key_messages_generation",
            "quality": "synthetic"
        }
    }


# ========== Main Augmentation Logic ==========

def augment_training_data(
    input_train_path: str = "../module3/data/generated/train_v2.jsonl",
    output_train_path: str = "../module3/data/generated/train_v2_augmented.jsonl",
    samples_per_brand: int = 5
) -> None:
    """
    เพิ่ม synthetic brand samples ลงใน train_v2.jsonl
    
    Args:
        input_train_path: Path ของ train_v2.jsonl เดิม
        output_train_path: Path ของ train_v2.jsonl ใหม่ที่มี synthetic data
        samples_per_brand: จำนวน samples ที่จะสร้างต่อแบรนด์ (default: 5)
    """
    
    print("\n" + "="*80)
    print("🔧 Data Augmentation: เพิ่มแบรนด์สมมติเพื่อป้องกัน Overfitting")
    print("="*80)
    
    # 1. โหลด train.jsonl เดิม
    input_path = Path(input_train_path)
    
    if not input_path.exists():
        print(f"❌ ไม่พบไฟล์ {input_train_path}")
        return
    
    original_samples = []
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            original_samples.append(json.loads(line))
    
    print(f"\n📊 สถิติข้อมูลเดิม:")
    print(f"   • จำนวน samples: {len(original_samples)}")
    
    # นับแบรนด์
    original_brands = {}
    for sample in original_samples:
        brand = sample.get("metadata", {}).get("brand", "Unknown")
        original_brands[brand] = original_brands.get(brand, 0) + 1
    
    print(f"   • แบรนด์เดิม: {list(original_brands.keys())}")
    for brand, count in original_brands.items():
        print(f"     - {brand}: {count} samples")
    
    # 2. สร้าง synthetic samples
    print(f"\n🎨 กำลังสร้างแบรนด์สมมติ {len(SYNTHETIC_BRANDS)} แบรนด์...")
    
    synthetic_samples = []
    
    for brand in SYNTHETIC_BRANDS:
        print(f"\n   • {brand['name']} ({brand['industry']})")
        print(f"     Tone: {', '.join(brand['tone'])}")
        
        brand_samples = []
        
        # สร้าง samples แบบหลากหลาย
        for _ in range(samples_per_brand):
            task_type = random.choice(["caption", "voice", "key_messages"])
            
            if task_type == "caption":
                sample = generate_caption_sample(brand)
            elif task_type == "voice":
                sample = generate_brand_voice_sample(brand)
            else:
                sample = generate_key_messages_sample(brand)
            
            brand_samples.append(sample)
        
        synthetic_samples.extend(brand_samples)
        print(f"     ✅ สร้าง {len(brand_samples)} samples")
    
    # 3. รวมข้อมูลเดิม + synthetic
    all_samples = original_samples + synthetic_samples
    
    # Shuffle เพื่อไม่ให้แบรนด์เดียวกันติดกัน
    random.shuffle(all_samples)
    
    # 4. บันทึกเป็น train_augmented.jsonl
    output_path = Path(output_train_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    
    print(f"\n✅ บันทึกไฟล์ใหม่: {output_path}")
    
    # 5. สรุปสถิติ
    print(f"\n📊 สถิติข้อมูลใหม่:")
    print(f"   • จำนวน samples รวม: {len(all_samples)}")
    print(f"     - เดิม: {len(original_samples)}")
    print(f"     - เพิ่ม: {len(synthetic_samples)}")
    
    # นับแบรนด์ใหม่
    all_brands = {}
    for sample in all_samples:
        brand = sample.get("metadata", {}).get("brand", "Unknown")
        all_brands[brand] = all_brands.get(brand, 0) + 1
    
    print(f"\n   • แบรนด์ทั้งหมด ({len(all_brands)} brands):")
    for brand, count in sorted(all_brands.items(), key=lambda x: x[1], reverse=True):
        status = "เดิม" if brand in original_brands else "ใหม่"
        print(f"     - {brand}: {count} samples ({status})")
    
    print("\n" + "="*80)
    print("💡 ขั้นตอนถัดไป:")
    print("="*80)
    print(f"""
1. ✅ สร้าง train_augmented.jsonl แล้ว ({len(all_samples)} samples)

2. ⏭️  แก้ไข finetune_lora.py ให้ใช้ไฟล์ใหม่:
   
   เดิม:  train_dataset = load_dataset("json", data_files="{{"train": "train.jsonl"}}")
   ใหม่:  train_dataset = load_dataset("json", data_files="{{"train": "train_augmented.jsonl"}}")

3. ⏭️  Fine-tune ด้วยข้อมูลใหม่บน Colab
   → python finetune_lora.py

4. ✅ ผลลัพธ์ที่คาดหวัง:
   • โมเดลจะเห็นความหลากหลายของแบรนด์ ({len(all_brands)} brands)
   • เรียนรู้ว่า Tone แตกต่างกันตามอุตสาหกรรม
   • ลดความเสี่ยง hallucination เมื่อเจอแบรนด์ใหม่
   • เมื่อใช้ RAG ร่วมด้วย = สมบูรณ์แบบ! 🚀
""")


def show_sample_preview(n_samples: int = 3):
    """แสดงตัวอย่าง synthetic samples ที่จะถูกสร้าง"""
    
    print("\n" + "="*80)
    print("👀 Preview: ตัวอย่าง Synthetic Samples")
    print("="*80)
    
    for i, brand in enumerate(SYNTHETIC_BRANDS[:n_samples]):
        print(f"\n{'─'*80}")
        print(f"แบรนด์ {i+1}: {brand['name']} ({brand['industry']})")
        print(f"Tone: {', '.join(brand['tone'])}")
        print(f"{'─'*80}")
        
        # Caption sample
        caption_sample = generate_caption_sample(brand)
        print(f"\n1️⃣  Caption Generation:")
        print(f"   Instruction: {caption_sample['instruction']}")
        print(f"   Output: {caption_sample['output']}")
        
        # Brand voice sample
        voice_sample = generate_brand_voice_sample(brand)
        print(f"\n2️⃣  Brand Voice Adaptation:")
        print(f"   Instruction: {voice_sample['instruction']}")
        print(f"   Output: {voice_sample['output']}")
        
        # Key messages sample
        key_sample = generate_key_messages_sample(brand)
        print(f"\n3️⃣  Key Messages:")
        print(f"   Output:\n{key_sample['output']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        # แสดง preview อย่างเดียว (ไม่สร้างไฟล์)
        show_sample_preview(n_samples=8)
    else:
        # สร้างข้อมูลจริง
        augment_training_data(
            input_train_path="../module3/data/generated/train_v2.jsonl",
            output_train_path="../module3/data/generated/train_v2_augmented.jsonl",
            samples_per_brand=5  # สร้าง 5 samples ต่อแบรนด์ = 8 brands × 5 = 40 samples เพิ่ม
        )
