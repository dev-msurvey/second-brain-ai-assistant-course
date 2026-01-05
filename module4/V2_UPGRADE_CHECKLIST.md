# ✅ V2 Upgrade Checklist

## การอัปเกรด AI Director สู่ V2 เสร็จสมบูรณ์!

### 📦 Data Files Created

- [x] **brands_v2.json** (8 brands, 490 lines)
  - Location: `module2/data/raw/brands_v2.json`
  - Content: 3 original + 5 new brands
  - Enhanced: customer_service_guidelines

- [x] **campaigns_v2.json** (4 campaigns)
  - Location: `module2/data/raw/campaigns_v2.json`
  - Content: 4 campaigns covering all use cases

- [x] **train_v2.jsonl** (148 samples)
  - Location: `module3/data/generated/train_v2.jsonl`
  - Content: 80% of total dataset

- [x] **val_v2.jsonl** (18 samples)
  - Location: `module3/data/generated/val_v2.jsonl`
  - Content: 10% of total dataset

- [x] **test_v2.jsonl** (19 samples)
  - Location: `module3/data/generated/test_v2.jsonl`
  - Content: 10% of total dataset

---

### 🔧 Scripts Updated

- [x] **finetune_lora.py**
  - ✓ train.jsonl → train_v2.jsonl
  - ✓ val.jsonl → val_v2.jsonl
  - ✓ test.jsonl → test_v2.jsonl

- [x] **inference_rag.py**
  - ✓ brands.json → brands_v2.json
  - ✓ Updated default paths
  - ✓ Fixed all comments

- [x] **augment_training_data.py**
  - ✓ train.jsonl → train_v2.jsonl
  - ✓ Output: train_v2_augmented.jsonl

- [x] **test_ood_inputs.py**
  - ✓ train.jsonl → train_v2.jsonl

- [x] **demo_rag_concept.py**
  - ✓ brands.json → brands_v2.json

---

### 📊 Dataset Statistics

```
Total Samples: 185 (was 71)
├── Train:      148 samples (80%)
├── Validation:  18 samples (10%)
└── Test:        19 samples (10%)

Growth: +161% from V1
```

**Use Case Breakdown:**
- 📞 Customer Service: 22 samples (11.9%)
- 🎨 Visual Prompts: 52 samples (28.1%)
- 🎬 Scripts: 60 samples (32.4%)
- 🔄 Cross-Channel: 51 samples (27.6%)

**Brand Coverage:**
- CoffeeLab, FitFlow, GreenLeaf (original)
- TechZone, UrbanNest, PetPals, GlowLab, EduKid (new)

---

### 🎯 New Capabilities

- [x] **Customer Service & Crisis Management**
  - Negative/positive/neutral responses
  - Brand-appropriate tone
  - Crisis escalation protocols

- [x] **Visual Prompt Engineering**
  - Stable Diffusion prompts
  - Midjourney style guides
  - Technical photography specs

- [x] **Script Writing with Timestamps**
  - 15s/30s/60s formats
  - Timestamp-based editing
  - Audio + Visual cues

- [x] **Cross-Channel Adaptation**
  - Instagram → LinkedIn, TikTok, etc.
  - Platform-specific optimization
  - Tone adjustments

---

### 📝 Documentation

- [x] **README_V2.md**
  - Location: `module3/data/generated/README_V2.md`
  - Content: Complete V2 documentation
  - 400+ lines of detailed information

---

### ⏭️ Next Steps (Pending)

- [ ] **Fine-tune Model** (requires GPU)
  ```bash
  cd module4/scripts
  python finetune_lora.py
  ```
  - Expected time: 3-4 hours on T4
  - Output: models/qwen-7b-ai-director-v2/

- [ ] **Test New Use Cases**
  - Customer service responses
  - Visual prompt generation
  - Timestamp scripts
  - Cross-platform content

- [ ] **Evaluate Performance**
  - Run inference on test_v2.jsonl
  - Calculate metrics (loss, perplexity)
  - Manual quality review

- [ ] **Update Main README**
  - Document V2 capabilities
  - Add usage examples
  - Update architecture diagrams

- [ ] **Create LESSON_LEARNED.md**
  - Module 4 insights
  - Best practices
  - Challenges & solutions

---

### �� Quick Start

```bash
# 1. Verify files
ls -lh module2/data/raw/*_v2.json
ls -lh module3/data/generated/*_v2.jsonl

# 2. Test data loading
cd module4/scripts
python -c "
from datasets import load_dataset
ds = load_dataset('json', data_files={'train': '../module3/data/generated/train_v2.jsonl'})
print(f'Loaded {len(ds[\"train\"])} samples')
"

# 3. Test RAG
python -c "
import json
with open('../../module2/data/raw/brands_v2.json') as f:
    brands = json.load(f)
print(f'Loaded {len(brands[\"brands\"])} brands')
"

# 4. Ready for fine-tuning!
# Transfer to Google Colab and run:
python finetune_lora.py
```

---

### 📈 Key Improvements

| Metric | V1 | V2 | Change |
|--------|----|----|--------|
| Total Samples | 71 | 185 | +161% |
| Brands | 3 | 8 | +167% |
| Use Cases | 2 | 6 | +200% |
| Training Time | ~2h | ~4h | +100% |

---

### 🎉 Status: COMPLETE

All scripts updated and ready for fine-tuning!

**Date Completed:** January 4, 2026  
**Version:** 2.0  
**Next Milestone:** Fine-tune model on GPU
