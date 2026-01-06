# Module 3: Dataset Generation for AI Director Fine-tuning

> สร้าง training datasets จากข้อมูล brands และ campaigns เพื่อ fine-tune AI Director models

## 📋 Overview

Module นี้สร้าง instruction-response pairs สำหรับ fine-tuning AI models ให้สามารถสร้างเนื้อหา marketing ที่เหมาะสมกับแต่ละ brand

### Dataset Types

1. **Caption Generation** - สร้าง captions สำหรับ Instagram/TikTok
2. **Campaign Brief Creation** - สร้าง campaign briefs
3. **Brand Voice Adaptation** - ปรับ content ให้เข้ากับ brand voice
4. **Content Strategy** - สร้างแผนกลยุทธ์เนื้อหา

## 🚀 Quick Start

### Generate Datasets

```bash
cd module3
python scripts/generate_dataset.py
```

### Output Structure

```
module3/
├── data/
│   ├── generated/
│   │   ├── train.jsonl              # Training set (80%)
│   │   ├── val.jsonl                # Validation set (10%)
│   │   ├── test.jsonl               # Test set (10%)
│   │   ├── caption_dataset.jsonl    # Caption-specific dataset
│   │   ├── campaign_brief_dataset.jsonl
│   │   ├── brand_voice_dataset.jsonl
│   │   ├── content_strategy_dataset.jsonl
│   │   └── metadata.json            # Dataset statistics
│   └── samples/
│       └── sample_caption.jsonl     # Example format
```

## 📊 Dataset Format

### JSONL Format (JSON Lines)

Each line is a valid JSON object:

```jsonl
{
  "instruction": "เขียน caption สำหรับ CoffeeLab ใช้ tone: friendly, premium, modern",
  "input": "Brand: CoffeeLab\nTagline: Craft Your Perfect Morning\nTarget: young professionals",
  "output": "เริ่มต้นเช้าวันใหม่ด้วยกาแฟที่ใช่ ☕️ #CoffeeLab",
  "metadata": {
    "brand": "CoffeeLab",
    "task": "caption_generation",
    "platform": "instagram/tiktok",
    "quality": "good"
  }
}
```

### Fields

- **instruction**: คำสั่งที่ model ต้องทำ (task description)
- **input**: context และข้อมูล input สำหรับการสร้าง output
- **output**: ผลลัพธ์ที่ต้องการให้ model สร้าง
- **metadata**: ข้อมูลเพิ่มเติมสำหรับการติดตามและ filtering

## 🎯 Dataset Generation Strategy

### 1. Caption Generation Dataset

**Source**: `content_examples.caption_good` จาก brands.json

**Approach**:
- ใช้ good caption examples จากแต่ละ brand
- สร้าง variations ตาม context (product launch, weekend post, etc.)
- รวม brand tone, target audience ใน instruction

**Example**:
```json
{
  "instruction": "เขียน caption สำหรับ CoffeeLab ใช้ tone: friendly, premium, modern",
  "input": "Brand: CoffeeLab\nTagline: Craft Your Perfect Morning",
  "output": "เริ่มต้นเช้าวันใหม่ด้วยกาแฟที่ใช่ ☕️ #CoffeeLab"
}
```

### 2. Campaign Brief Dataset

**Source**: campaigns.json

**Approach**:
- ใช้ existing campaign briefs เป็น ground truth
- รวม objectives, key messages
- เพิ่ม brand context

**Example**:
```json
{
  "instruction": "สร้าง campaign brief สำหรับ CoffeeLab",
  "input": "Objectives: Launch new Cold Brew, Increase awareness 30%",
  "output": "Campaign: Cold Brew Launch 2025\nGoal: เปิดตัว Cold Brew..."
}
```

### 3. Brand Voice Adaptation Dataset

**Source**: Synthetic - แปลง generic messages ให้เข้ากับ brand voice

**Approach**:
- เริ่มจาก generic message
- ปรับให้เข้ากับ tone, values ของแต่ละ brand
- เพิ่ม brand-specific elements (emojis, hashtags)

**Example**:
```json
{
  "instruction": "แปลงข้อความนี้ให้เข้ากับ brand voice ของ CoffeeLab",
  "input": "Message: เรามีผลิตภัณฑ์ใหม่เปิดตัวแล้ว",
  "output": "☕️ เรามีผลิตภัณฑ์ใหม่เปิดตัวแล้ว #CraftYourMorning"
}
```

### 4. Content Strategy Dataset

**Source**: campaigns.json (timeline, content_requirements)

**Approach**:
- สร้าง strategy จาก campaign objectives
- รวม timeline phases
- ระบุ content requirements

## 📈 Dataset Statistics

**Current Dataset** (Generated: 2026-01-04):

| Dataset Type | Samples | Description |
|-------------|---------|-------------|
| Caption Generation | 15 | Instagram/TikTok captions |
| Campaign Brief | 6 | Campaign planning documents |
| Brand Voice Adaptation | 15 | Generic to branded content |
| Content Strategy | 3 | Strategic content plans |
| **Total** | **39** | All training samples |

**Data Splits**:
- Training: 31 samples (80%)
- Validation: 4 samples (10%)
- Test: 4 samples (10%)

## 🔧 Technical Details

### Dependencies

```python
# Core
import json
import random
from pathlib import Path
from typing import List, Dict, Any
from loguru import logger
```

No external ML libraries required for generation (uses rule-based synthesis)

### Input Data

- **brands.json**: 3 brands with comprehensive v2 structure
  - CoffeeLab (coffee shop)
  - FitFlow (fitness center)
  - GreenLeaf (organic food delivery)

- **campaigns.json**: 3 campaigns
  - Cold Brew Launch 2025
  - New Year Transformation
  - Farm to Table Series

### Data Quality

**Good Examples (from brands.json)**:
- Real captions from content_examples
- Verified to match brand voice
- Include appropriate emojis and hashtags

**Synthesized Examples**:
- Generated with context variations
- Follow brand guidelines
- Quality: "synthesized" in metadata

## 🎓 Key Learnings

### 1. Data Quality > Quantity

39 samples ดีกว่า 1000 samples คุณภาพต่ำ:
- ใช้ real examples จาก brands v2 data
- Synthesize แบบมี rules ชัดเจน
- Validate ทุก sample ก่อน save

### 2. Few-Shot Learning

Dataset เล็กแต่มี diversity สูง:
- 3 brands × multiple contexts
- Different task types (caption, brief, strategy)
- Rich metadata สำหรับ filtering

### 3. Instruction Format Matters

Structure instruction-input-output ให้ชัดเจน:
```
Instruction: อะไร (task)
Input: ข้อมูลอะไรบ้าง (context)
Output: ผลลัพธ์ที่ต้องการ (expected result)
```

### 4. Metadata for Debugging

เก็บ metadata ครบ:
- brand, task, context
- quality indicator (good/synthesized)
- timestamp, version

## 🔮 Next Steps (Module 4)

### Fine-tuning with Generated Datasets

1. **Choose Base Model**: 
   - Llama 3.1 8B, Mistral 7B, หรือ Qwen 7B
   - Thai language support important

2. **Fine-tuning Approach**:
   - LoRA (Low-Rank Adaptation) สำหรับ efficiency
   - Train บน train.jsonl (31 samples)
   - Validate บน val.jsonl (4 samples)

3. **Evaluation**:
   - Test บน test.jsonl (4 samples)
   - Manual review brand voice consistency
   - Compare กับ base model

4. **Deployment**:
   - Export fine-tuned model
   - Integrate กับ AI Director system
   - A/B test กับ base model

## 📚 References

### Related Files

- **Module 2**: [../module2/README.md](../module2/README.md)
  - Source data: brands.json, campaigns.json
  - ETL pipeline และ data structure

- **Module 2 Lesson Learned**: [../module2/LESSON_LEARNED.md](../module2/LESSON_LEARNED.md)
  - 7-dimensional data modeling framework
  - Data quality best practices

### HuggingFace Format

Dataset format compatible with:
- `datasets` library: `load_dataset("json", data_files="train.jsonl")`
- Direct fine-tuning with `transformers`
- Compatible with Axolotl, LLaMA Factory

## 📝 Usage Examples

### Load Dataset in Python

```python
import json

# Load JSONL
with open("data/generated/train.jsonl", 'r') as f:
    train_data = [json.loads(line) for line in f]

print(f"Training samples: {len(train_data)}")
print(f"First sample: {train_data[0]}")
```

### Load with HuggingFace Datasets

```python
from datasets import load_dataset

dataset = load_dataset(
    "json",
    data_files={
        "train": "data/generated/train.jsonl",
        "validation": "data/generated/val.jsonl",
        "test": "data/generated/test.jsonl"
    }
)

print(dataset)
# DatasetDict({
#     train: Dataset({
#         features: ['instruction', 'input', 'output', 'metadata'],
#         num_rows: 31
#     })
#     validation: Dataset({...})
#     test: Dataset({...})
# })
```

### Filter by Task Type

```python
# Load all captions
captions = [
    sample for sample in train_data 
    if sample['metadata']['task'] == 'caption_generation'
]

print(f"Caption samples: {len(captions)}")
```

## ✅ Validation Checklist

- [x] JSONL format valid (one JSON per line)
- [x] All samples have instruction, input, output
- [x] Metadata includes brand, task, quality
- [x] Train/val/test splits created (80/10/10)
- [x] Sample files created for documentation
- [x] Output statistics logged
- [x] No data leakage between splits

## 🎯 Success Criteria

Module 3 สำเร็จเมื่อ:

1. ✅ Generate datasets สำเร็จ (39 samples)
2. ✅ JSONL format ถูกต้อง
3. ✅ มี train/val/test splits
4. ✅ Dataset มี diversity (4 task types, 3 brands)
5. ✅ Documentation ครบถ้วน
6. ⏭️ Ready สำหรับ fine-tuning (Module 4)

---

**Module 3 Status**: ✅ COMPLETE

**Generated**: 2026-01-04
**Total Samples**: 39 (31 train / 4 val / 4 test)
**Next**: Module 4 - Model Fine-tuning
