# Quick Start Guide: Run Optimization on Google Colab

## 📋 Prerequisites

- Google account (for Colab)
- Internet connection
- ~2.5 hours of free time

## 🚀 Step-by-Step Instructions

### 1. Open Google Colab

Go to: https://colab.research.google.com

### 2. Upload Notebook

- Click **File** → **Upload notebook**
- Select: `module4.5/Module_4_5_Optimization.ipynb`
- OR use URL: https://github.com/decodingai-magazine/second-brain-ai-assistant-course/blob/feature/module4-training-v2/module4.5/Module_4_5_Optimization.ipynb

### 3. Enable GPU

- Click **Runtime** → **Change runtime type**
- Hardware accelerator: **T4 GPU**
- Click **Save**

### 4. Run All Cells

- Click **Runtime** → **Run all**
- OR press `Ctrl+F9` (Windows/Linux) / `Cmd+F9` (Mac)

### 5. Monitor Progress

The notebook will:
1. ✅ Check GPU (should show NVIDIA T4)
2. ✅ Clone repository (~30 seconds)
3. ✅ Install dependencies (~2 minutes)
4. ✅ Verify dataset (should show 185 samples)
5. ✅ Run 20 optimization trials (~2.5 hours)
   - Each trial trains model for 1 epoch
   - Progress shown trial-by-trial
6. ✅ Generate results and plots

### 6. Download Results

After completion, download:
- `optimization_results.zip` (all results packed)

Contains:
- `best_config.yaml` - Best hyperparameters found
- `optimization_results.json` - Full trial history
- `trial_history.csv` - Data for analysis
- `optimization_progress.png` - Visualization

### 7. Update Local Repository

```bash
# Extract downloaded zip
unzip optimization_results.zip

# Copy to local repo
cp -r configs/* /path/to/your/repo/module4.5/configs/

# Commit
git add module4.5/configs/
git commit -m "feat: Add real optimization results from Colab"
git push
```

## ⚡ Quick Troubleshooting

### GPU Not Available
- Make sure you selected "T4 GPU" in runtime settings
- Free tier has daily limits - try again later if quota exceeded

### Import Errors
- Should auto-resolve after installing dependencies
- If persists, restart runtime: Runtime → Restart runtime

### Out of Memory
- Reduce batch size in optimization_config.yaml
- Or reduce number of trials: `--trials 10` instead of 20

### Dataset Not Found
- Notebook should auto-download from GitHub
- Check branch is correct: feature/module4-training-v2

## 📊 Expected Results

After successful run, you should see:
- **Best Loss**: Around 0.56-0.58 (vs baseline 0.6097)
- **Improvement**: 5-10%
- **Best Config**: Likely rank=32, alpha=64, lr~1.2e-4, batch=2

## 🔗 Resources

- Colab: https://colab.research.google.com
- Repository: https://github.com/decodingai-magazine/second-brain-ai-assistant-course
- Branch: feature/module4-training-v2
- Issues: Open GitHub issue if problems occur

## ✅ Success Indicators

You'll know it worked if:
1. All 20 trials complete without errors
2. Loss values are reasonable (0.5-0.7 range)
3. `optimization_results.zip` downloads successfully
4. Plots show convergence pattern

---

**Ready to run?** Just upload the notebook to Colab and click "Run all"! 🚀
