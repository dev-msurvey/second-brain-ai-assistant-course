# AI Director Model - Training Summary (V2)

**Model:** qwen-7b-ai-director-v2  
**Base Model:** Qwen/Qwen2.5-7B-Instruct  
**Training Method:** LoRA (Low-Rank Adaptation) with 4-bit Quantization (QLoRA)  
**Training Date:** January 4, 2026  
**Training Platform:** Google Colab Free Tier (Tesla T4 GPU)

---

## 📊 Training Configuration

### Model Architecture
- **Base Model:** Qwen/Qwen2.5-7B-Instruct (7.62B parameters)
- **Fine-tuning Method:** LoRA (Low-Rank Adaptation)
- **Quantization:** 4-bit (QLoRA with BitsAndBytesConfig)

### LoRA Configuration
```python
lora_config = {
    "r": 16,                    # Rank
    "lora_alpha": 32,           # Alpha parameter
    "lora_dropout": 0.05,       # Dropout rate
    "target_modules": [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ]
}
```

### Training Parameters
- **Trainable Parameters:** 40,370,176 (0.92% of base model)
- **Total Parameters:** 4,393,342,464
- **Epochs:** 3
- **Batch Size:** 1
- **Gradient Accumulation Steps:** 4 (effective batch size = 4)
- **Learning Rate:** 2e-4
- **Optimizer:** paged_adamw_8bit
- **Max Sequence Length:** 1024 tokens
- **Warmup Steps:** 10

---

## 📁 Dataset V2

### Summary
- **Total Samples:** 185
- **Training Set:** 148 samples (80%)
- **Validation Set:** 18 samples (9.7%)
- **Test Set:** 19 samples (10.3%)

### Use Case Distribution
1. **Video Scripts:** 60 samples (32.4%)
2. **Visual Prompts:** 52 samples (28.1%)
3. **Cross-Channel Marketing:** 51 samples (27.6%)
4. **Customer Service:** 16 samples (8.6%)
5. **Crisis Management:** 6 samples (3.2%)

### Brand Coverage
8 brands total:
- CoffeeLab (premium coffee)
- FitFlow (fitness & wellness)
- GreenLeaf (organic products)
- TechZone (gaming gear)
- UrbanNest (interior design)
- PetPals (pet care)
- GlowLab (beauty & skincare)
- EduKid (educational toys)

---

## 🎯 Training Results

### Performance Metrics
- **Final Training Loss:** 0.6097
- **Training Time:** 2 hours 34 minutes (9,281 seconds)
- **GPU:** Tesla T4 (14.74 GB VRAM used)
- **Training Start:** 2026-01-04 14:32:34 UTC
- **Training End:** 2026-01-04 17:08:15 UTC

### Checkpoints Saved
- `checkpoint-100` - Intermediate checkpoint
- `checkpoint-111` - Final checkpoint (best model)

---

## 💾 Output Files

### Model Directory: `trained_models/qwen-7b-ai-director-v2/`

Total Size: **666 MB**

Files:
```
adapter_model.safetensors    154 MB  (LoRA weights)
adapter_config.json          1.1 KB  (LoRA configuration)
training_args.bin            5.8 KB  (Training arguments)
tokenizer.json               11 MB   (Tokenizer)
vocab.json                   2.6 MB  (Vocabulary)
merges.txt                   1.6 MB  (BPE merges)
special_tokens_map.json      449 B
added_tokens.json            2 B
tokenizer_config.json        7.1 KB
chat_template.jinja          2.5 KB
README.md                    5.1 KB
checkpoint-100/              (intermediate)
checkpoint-111/              (final)
```

---

## 🚀 New Capabilities (V2)

### 1. Customer Service Response
Generate empathetic responses to customer comments (positive, negative, neutral).

**Example:**
```
Input: "สินค้าที่ได้รับไม่ตรงตามที่สั่ง รู้สึกผิดหวังมาก"
Output: "ขอบคุณที่แจ้งให้ทราบค่ะ เรารู้สึกเสียใจจริงๆ ที่ทำให้คุณผิดหวัง 
รบกวนส่งรูปสินค้าที่ได้รับมาทาง DM ได้ไหมค่ะ เราจะดำเนินการแก้ไขให้ทันทีเลยค่ะ 🙏"
```

### 2. Visual Prompt Generation
Create detailed prompts for AI image generation (Midjourney, Stable Diffusion).

**Example:**
```
Input: Brand: TechZone, Context: Gaming setup, Style: Cyberpunk
Output: "dark cyberpunk aesthetic, neon RGB lighting, gaming setup, 
professional photography, edgy, tech-savvy, commercial quality --ar 16:9"
```

### 3. Video Script Writing
Write structured scripts for TikTok/YouTube (15s, 30s, 60s formats).

**Example:**
```
Input: Brand: GlowLab, Format: TikTok 60s, Objective: Engagement
Output: "[00-10s] Hook | [10-30s] Story | [30-50s] Product | [50-60s] CTA"
```

### 4. Cross-Channel Content Adaptation
Adapt content between platforms (Instagram → Twitter, TikTok → LinkedIn, etc.).

**Example:**
```
Input: Instagram post → Twitter
Output: Optimized for Twitter audience with appropriate tone and format
```

---

## ⚠️ Issues Encountered & Solutions

### Issue 1: Model Folder Not Found
**Problem:** Model files uploaded as .zip but not extracted  
**Solution:** Auto-extract ZIP files before loading
```python
if os.path.exists(zip_file) and not os.path.exists(model_folder):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(base_path)
```

### Issue 2: KeyError When Loading LoRA Adapters
**Problem:** Missing BitsAndBytesConfig during inference  
**Solution:** Use same quantization config as training
```python
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
```

### Issue 3: Output Contains Prompt Structure
**Problem:** Generated text includes system/user/assistant markers  
**Solution:** Parse output with string split instead of special tokens
```python
if "assistant" in full_response:
    result = full_response.split("assistant")[-1].strip()
```

### Issue 4: Path Errors in Google Colab
**Problem:** Relative paths don't work in Colab  
**Solution:** Always use absolute paths
```python
BASE_PATH = "/content/drive/MyDrive/ai-director-colab"
```

---

## 📝 Next Steps

- [ ] Test inference with new examples
- [ ] Evaluate on held-out test set (19 samples)
- [ ] Calculate quality metrics (BLEU, ROUGE, F1)
- [ ] Conduct human evaluation
- [ ] Compare with base model performance
- [ ] Deploy as API (FastAPI/Gradio)
- [ ] Integrate with RAG system (Module 5)

---

## 🎓 Key Learnings

### What Worked Well
1. **QLoRA Training:** 4-bit quantization enabled training 7B model on free Colab
2. **Low Loss:** Final loss of 0.6097 indicates good convergence
3. **Fast Training:** 2.58 hours is practical for iteration
4. **Small Footprint:** Only 154 MB for LoRA adapters

### Challenges Faced
1. **Path Management:** Needed absolute paths in Colab
2. **File Handling:** ZIP extraction not automatic
3. **Output Parsing:** Special tokens can be stripped unexpectedly
4. **Memory:** Required careful quantization to fit in T4 VRAM

### Recommendations
1. Always document issues in TROUBLESHOOTING.md
2. Create improved notebooks for next training session
3. Test inference immediately after training
4. Keep test set completely separate
5. Version control everything except model weights

---

## 📚 Related Files

- `AI_Director_FineTuning_Colab.ipynb` - Training notebook (with all fixes)
- `README.md` - Module 4 overview
- `EVALUATION_RESULTS.md` - Test set evaluation
- `scripts/finetune_lora.py` - Training script
- `scripts/demo_inference.py` - Inference demo
- `scripts/evaluate_test_set.py` - Test evaluation

---

**Training completed successfully on January 4, 2026! 🎉**
