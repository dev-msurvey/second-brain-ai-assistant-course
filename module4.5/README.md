# Module 4.5: Meta Ax Hyperparameter Optimization

**Status**: In Development  
**Version**: v1.0  
**Date**: January 5, 2026

## 🎯 Overview

Module 4.5 implements **Bayesian Hyperparameter Optimization** using **Meta Ax** to find the best training configuration for our AI Director model (Qwen2.5-7B + LoRA).

### Why Optimization?
Current training (Module 4) uses manually selected hyperparameters:
- LoRA rank: 16
- Learning rate: 2e-4
- Batch size: 1
- Alpha: 32
- **Final loss: 0.6097**

We can potentially improve this by **systematically searching** for better configurations using Bayesian optimization.

## 🔬 Meta Ax

[Meta Ax](https://ax.dev/) is Meta's platform for adaptive experimentation:
- **Bayesian Optimization**: Efficient search using probabilistic models
- **Multi-Objective**: Optimize multiple metrics simultaneously
- **Early Stopping**: Skip poor configurations quickly
- **Parallel Trials**: Run multiple experiments concurrently (if resources allow)

### Why Bayesian Optimization?
- **Sample Efficient**: Finds good parameters in 10-20 trials (vs 100s for grid search)
- **Intelligent**: Learns from previous trials to suggest promising areas
- **Handles Mixed Types**: Continuous (learning rate), discrete (LoRA rank), categorical
- **Uncertainty Aware**: Balances exploration vs exploitation

## 📊 Optimization Space

### Hyperparameters to Optimize

| Parameter | Type | Current | Search Range | Impact |
|-----------|------|---------|--------------|--------|
| `lora_rank` | Discrete | 16 | [8, 16, 32, 64] | Model capacity, VRAM |
| `lora_alpha` | Discrete | 32 | [16, 32, 64, 128] | Adaptation strength |
| `learning_rate` | Continuous | 2e-4 | [1e-5, 5e-4] | Convergence speed |
| `batch_size` | Discrete | 1 | [1, 2, 4] | Gradient quality, VRAM |

**Note**: We skip per_device_train_batch_size > 4 due to Tesla T4 16GB VRAM limit.

### Fixed Parameters
- Model: `Qwen/Qwen2.5-7B-Instruct`
- Epochs per trial: **1** (fast evaluation)
- Dataset: 148 training samples
- Gradient accumulation: Auto-adjust based on batch_size
- Optimizer: AdamW
- Warmup: 10% of steps
- Weight decay: 0.01

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd module4.5
pip install -r requirements.txt
```

### 2. Run Optimization
```bash
python ax_optimization.py \
    --trials 20 \
    --output configs/optimization_results.json
```

### 3. View Results
```bash
# Best parameters found
cat configs/best_config.yaml

# Full trial history
python -c "import json; print(json.dumps(json.load(open('configs/optimization_results.json')), indent=2))"
```

### 4. Retrain with Best Config
```bash
cd ../module4
python finetune_lora.py --config ../module4.5/configs/best_config.yaml
```

## 📁 Files

- **ax_optimization.py** - Main optimization script
- **configs/optimization_config.yaml** - Search space configuration
- **configs/best_config.yaml** - Best hyperparameters found (generated)
- **configs/optimization_results.json** - Full trial history (generated)
- **OPTIMIZATION_RESULTS.md** - Analysis and recommendations (generated)
- **requirements.txt** - Python dependencies
- **README.md** - This file

## 🔧 Usage

### Basic Usage
```python
from ax_optimization import run_optimization

# Run 20 trials
results = run_optimization(
    num_trials=20,
    model_name="Qwen/Qwen2.5-7B-Instruct",
    output_dir="configs/"
)

print(f"Best loss: {results['best_loss']:.4f}")
print(f"Best params: {results['best_params']}")
```

### Custom Search Space
```python
from ax_optimization import run_optimization

# Focus on learning rate
results = run_optimization(
    num_trials=15,
    search_space={
        "lora_rank": [16],  # Fixed
        "lora_alpha": [32],  # Fixed
        "learning_rate": [5e-5, 3e-4],  # Range
        "batch_size": [1, 2]  # Discrete
    }
)
```

### Resume Optimization
```python
# Load previous results and continue
from ax_optimization import resume_optimization

results = resume_optimization(
    checkpoint="configs/optimization_checkpoint.json",
    additional_trials=10
)
```

## 📈 Expected Results

### Target Improvements
- **Current baseline**: 0.6097 loss
- **Expected improvement**: 5-15% (loss: 0.52-0.58)
- **Best case**: 20%+ improvement (loss: < 0.50)

### Key Insights to Look For
1. **LoRA Rank vs Loss**: Does higher rank help? (capacity vs overfitting)
2. **Learning Rate Sweet Spot**: Too high → unstable, too low → slow
3. **Batch Size Impact**: Larger batch → more stable gradients, more VRAM
4. **Alpha Ratio**: Does rank/alpha ratio matter?

### Example Output
```
Trial 1/20: rank=16, alpha=32, lr=2e-4, bs=1 → loss=0.6097 (baseline)
Trial 2/20: rank=32, alpha=64, lr=1.5e-4, bs=2 → loss=0.5834 ✓ IMPROVED
Trial 3/20: rank=8, alpha=16, lr=3e-4, bs=1 → loss=0.6523 ✗ WORSE
...
Trial 20/20: rank=32, alpha=64, lr=1.2e-4, bs=2 → loss=0.5621 ✓ BEST
```

## 🧮 Evaluation Function

Each trial runs:
1. Initialize model with trial's hyperparameters
2. Train for **1 epoch** (fast evaluation)
3. Compute validation loss
4. Return loss to Ax (lower is better)
5. Ax suggests next trial based on results

**Training Time**: ~8 minutes per trial (Tesla T4)  
**Total Time**: ~2.5 hours for 20 trials

## 🎓 Advanced Features

### Multi-Objective Optimization
Optimize multiple metrics:
```python
# Optimize loss AND inference speed
from ax import MultiObjective

results = run_optimization(
    num_trials=20,
    objectives=["loss", "inference_time"],
    minimize=[True, True]  # Minimize both
)
```

### Early Stopping
Stop poor trials early:
```python
# Stop if loss > 0.7 after 10% training
from ax_optimization import EarlyStoppingCallback

results = run_optimization(
    num_trials=20,
    early_stopping=EarlyStoppingCallback(threshold=0.7, check_at=0.1)
)
```

### Constraints
Add feasibility constraints:
```python
# Ensure rank * batch_size <= 128 (VRAM limit)
results = run_optimization(
    num_trials=20,
    constraints=["lora_rank * batch_size <= 128"]
)
```

## 📊 Visualization

After optimization, generate plots:
```python
from ax.plot.trace import optimization_trace_single_method
from ax.plot.contour import plot_contour

# Loss over trials
fig = optimization_trace_single_method(ax_client=ax)
fig.write_html("optimization_trace.html")

# Parameter importance
fig = plot_contour(model=ax.generation_strategy.model, param_x="lora_rank", param_y="learning_rate")
fig.write_html("contour_plot.html")
```

## 🐛 Troubleshooting

### CUDA Out of Memory
- Reduce `batch_size` search space: `[1]` only
- Reduce max `lora_rank`: `[8, 16, 32]` instead of `[8, 16, 32, 64]`
- Enable gradient checkpointing (already enabled)

### Optimization Too Slow
- Reduce `num_trials`: 10 instead of 20
- Reduce epochs per trial: 0.5 epochs (half dataset)
- Use smaller model: Qwen2.5-3B instead of 7B

### Poor Results
- Check baseline: Make sure current config is in search space
- Increase trials: 30-50 for thorough search
- Widen search ranges
- Check data quality: Maybe dataset is the bottleneck

### Ax Errors
```bash
# If Ax installation fails
pip install ax-platform --no-deps
pip install botorch
pip install gpytorch
```

## 📚 Dependencies

```txt
ax-platform>=0.3.7
botorch>=0.9.5
gpytorch>=1.11
torch>=2.0.0
transformers>=4.40.0
peft>=0.10.0
datasets>=2.18.0
pandas>=2.0.0
pyyaml>=6.0
```

## 🔗 Resources

- [Meta Ax Documentation](https://ax.dev/)
- [Bayesian Optimization Tutorial](https://ax.dev/tutorials/gpei_hartmann_loop.html)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [Qwen2.5 Model Card](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct)

## ✅ Next Steps

1. **Run Optimization** - Find best hyperparameters
2. **Analyze Results** - Understand what works and why
3. **Retrain Model** - Use best config for full 3-epoch training
4. **Compare Performance** - Baseline (0.6097) vs optimized
5. **Document Findings** - Update TRAINING_SUMMARY.md

---

**Module 4.5: Systematic Hyperparameter Optimization with Meta Ax** 🎯
