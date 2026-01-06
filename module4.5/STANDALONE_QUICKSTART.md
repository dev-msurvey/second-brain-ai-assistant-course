# 🚀 Module 4.5 Standalone Notebook - Quick Start Guide

## 📋 What is This?

**Standalone Colab Notebook** for Meta Ax hyperparameter optimization that:
- ✅ **No repo cloning needed** - All code embedded
- ✅ **Works immediately** - Just upload dataset to Google Drive
- ✅ **Self-contained** - Everything in one file
- ✅ **GPU-optimized** - Uses free T4 GPU from Colab

---

## 🎯 Quick Start (3 Steps)

### Step 1: Prepare Dataset

Upload these files to your Google Drive:
```
MyDrive/ai_director_dataset/
├── train_v2.jsonl
├── val_v2.jsonl
└── test_v2.jsonl
```

**Where to get dataset?**
- From: `module3/data/generated/` in this repo
- Or download from: [Add your dataset link]

### Step 2: Open in Colab

1. Upload `Module_4_5_Optimization_Standalone.ipynb` to Colab
2. Or open directly: [Add Colab link]

### Step 3: Enable GPU

```
Runtime → Change runtime type → Hardware accelerator → T4 GPU → Save
```

### Step 4: Run All Cells

```
Runtime → Run all (Ctrl+F9)
```

**That's it!** 🎉

---

## ⏱️ Expected Timeline

| Phase | Time | Description |
|-------|------|-------------|
| Setup | 2 min | Install packages, mount Drive |
| Test Trial 1 | ~8 min | First trial (slower due to model download) |
| Trial 2-20 | ~7 min each | Subsequent trials |
| **Total** | **~2.5 hours** | For 20 trials |

**Quick Test Option**: Change to 3 trials (~25 minutes)

---

## 📊 What Gets Optimized?

**Search Space:**
- LoRA rank: [8, 16, 32, 64]
- LoRA alpha: [16, 32, 64, 128]  
- Learning rate: [1e-5, 5e-4] (log scale)
- Batch size: [1, 2, 4]

**Baseline to Beat:**
- Loss: 0.6097
- Config: rank=16, alpha=32, lr=2e-4, bs=1

**Goal:** Find config with lower loss (5-10% improvement expected)

---

## 📁 Output Files

All results saved to Google Drive:

```
MyDrive/ai_director_optimization_results/
├── optimization_results.json      # Full results
├── best_config.yaml               # Best hyperparameters
├── trial_history.csv              # All trials
└── optimization_plot.png          # Visualization
```

Plus downloadable ZIP at the end.

---

## 🆚 vs Original Notebook

| Feature | Original | Standalone |
|---------|----------|------------|
| Repo clone | ✅ Required | ❌ Not needed |
| GitHub access | ✅ Required | ❌ Not needed |
| Code location | External files | Embedded |
| Dataset source | Clone from repo | Upload to Drive |
| Complexity | Medium | Simple |
| Setup time | 10 min | 2 min |
| **Best for** | Development | Quick experiments |

---

## 🐛 Troubleshooting

### Error: "No GPU found"
**Solution**: Runtime → Change runtime type → T4 GPU

### Error: "Dataset files not found"
**Solution**: 
1. Check path in Cell 3: `/content/drive/MyDrive/ai_director_dataset`
2. Verify files: `train_v2.jsonl`, `val_v2.jsonl`, `test_v2.jsonl`
3. Upload dataset to correct location

### Error: "CUDA out of memory"
**Solution**: 
1. Restart runtime: Runtime → Restart runtime
2. Reduce batch size in config (change values to [1, 2])
3. Or use fewer trials first

### Trial takes too long (>15 min)
**Solution**:
1. Check GPU is enabled: `!nvidia-smi`
2. Verify using T4 (not CPU)
3. If persistent, try factory reset runtime

### 🔄 Colab Disconnected Mid-Training?
**✅ No Problem! Checkpoint System Included**

**What happens:**
- Notebook auto-saves checkpoint after EVERY trial to Google Drive
- Checkpoint includes: completed trials, parameters, results

**How to resume:**
1. Reconnect to Colab
2. Re-run cells 1-7 (setup + config)
3. Run cell 8 (check checkpoint) - will show progress
4. Run cell 9 (optimizer) - **automatically resumes from last completed trial!**

**Example:**
```
📁 Checkpoint found!
Completed trials: 12/20
Last updated: 2026-01-05T15:30:00

✅ Will resume from trial 13
```

**To start over completely:**
- Run the "Delete Checkpoint" cell before running optimizer

**Checkpoint location:**
`/content/drive/MyDrive/ai_director_optimization_checkpoint.json`

---

## 🎓 Understanding the Results

### Optimization Trace Plot
- **Blue line**: Each trial's validation loss
- **Red dashed line**: Baseline (0.6097)
- **Look for**: Points below red line = improvement!

### Best Config
Example output:
```yaml
model: Qwen/Qwen2.5-7B-Instruct
lora_rank: 32
lora_alpha: 64
learning_rate: 0.00012
batch_size: 2
best_loss: 0.5621
improvement: +7.8%
```

**What this means:**
- Found config that beats baseline by 7.8%
- Use these hyperparameters for full training
- Expected final loss: ~0.52-0.54 (after 3 epochs)

---

## 🔥 Next Steps After Optimization

### 1. Use Best Config
Copy best hyperparameters to your training script:
```python
config = FineTuningConfig(
    lora_r=32,           # From best config
    lora_alpha=64,       # From best config
    learning_rate=1.2e-4,# From best config
    per_device_train_batch_size=2,  # From best config
    num_train_epochs=3,  # Full training (not 1)
)
```

### 2. Full Training
Train for 3+ epochs with best config (~2.5 hours)

### 3. Evaluate
Test on held-out test set

### 4. Deploy
Use optimized model in production (Module 7-8)

---

## 💡 Tips

**For Quick Testing:**
- Set `num_trials=3` in Cell 7 (~25 minutes)
- Verify everything works before full run

**For Best Results:**
- Use 20 trials (default)
- Don't interrupt mid-optimization
- Keep Colab tab active (prevents disconnect)

**To Avoid Colab Timeout:**
- ✅ **Checkpoint system included** - auto-saves after each trial!
- If disconnected, just reconnect and re-run - resumes automatically
- Keep browser tab active anyway (helps prevent disconnect)
- Use Colab Pro (longer runtime, less likely to disconnect)
- Can pause and resume anytime

**Managing Long Runs:**
- Split into sessions: Run 10 trials, stop, resume later
- Checkpoint survives runtime restarts
- Check progress anytime by running checkpoint check cell

---

## 📚 Learn More

**Bayesian Optimization:**
- Paper: https://arxiv.org/abs/1807.02811
- Meta Ax: https://ax.dev/

**LoRA Fine-tuning:**
- Paper: https://arxiv.org/abs/2106.09685
- HuggingFace PEFT: https://huggingface.co/docs/peft

**Full Course:**
- See: `course_ai-assistant_v3.4.md`

---

## ✅ Success Checklist

Before running:
- [ ] GPU enabled (T4)
- [ ] Dataset uploaded to Drive
- [ ] Drive path updated in Cell 3
- [ ] Packages installed (Cell 2)

After completion:
- [ ] Results saved to Drive
- [ ] Best config downloaded
- [ ] Improvement > 0% (beat baseline)
- [ ] Ready for full training

---

## 🆘 Need Help?

**Common Issues:**
1. GPU not enabled → See "Troubleshooting" above
2. Dataset not found → Check Drive path
3. Out of memory → Reduce batch size
4. Slow trials → Verify GPU active

**Still stuck?**
- Check cell outputs for error messages
- Restart runtime and try again
- Use 3 trials first to debug

---

**Happy Optimizing! 🚀**

*Module 4.5: Hyperparameter Optimization*  
*AI Director v3.4 - One-Man Marketing Agency*
