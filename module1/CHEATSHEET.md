# Module 1 Cheat Sheet
# AI Director v3.4 - Quick Reference

## 🚀 Quick Commands

```bash
# Setup
cd module1
bash setup.sh

# Run individual components
python 01_t5gemma_thinker.py
python 02_functiongemma_executor.py
python 03_ai_director_agent.py

# Run tests
python 04_test_module1.py

# Run examples
python examples/example_strategy.py
python examples/example_tool_calling.py
python examples/example_smart_cut.py
```

## 🧠 T5Gemma 2 (Thinker) Usage

```python
from t5gemma_thinker import T5GemmaThinker

# Initialize
thinker = T5GemmaThinker(model_size="1b-1b")

# Generate strategy
strategy = thinker.generate_strategy(
    brief="Create coffee ad for Instagram",
    brand_context="Premium, minimal style",
    max_length=500,
    temperature=0.7
)

# Generate image prompt
prompt = thinker.generate_image_prompt(
    brief="Coffee cup on desk",
    style="minimal",
    aspect_ratio="1:1"
)

# Generate voice script
script = thinker.generate_voice_script(
    concept="New product launch",
    duration=15,
    tone="friendly",
    language="Thai"
)

# Analyze transcript (Smart Cut)
analysis = thinker.analyze_transcript(
    transcript="[00:00] Hello...",
    target_duration=120,
    style="highlight"
)
```

## ⚡ FunctionGemma (Executor) Usage

```python
from functiongemma_executor import (
    FunctionGemmaExecutor,
    image_gen,
    voice_gen,
    video_compose
)

# Initialize
executor = FunctionGemmaExecutor()

# Register tools
executor.register_tool(image_gen)
executor.register_tool(voice_gen)
executor.register_tool(video_compose)

# Parse instruction to tool calls
instruction = "สร้างรูปกาแฟและเสียงพากย์"
tool_calls = executor.parse_to_tool_calls(instruction)

# Execute tool calls
results = executor.execute_tool_calls(tool_calls)
```

## 🎬 AI Director Agent Usage

```python
from ai_director_agent import AIDirectorAgent

# Initialize
agent = AIDirectorAgent(thinker_size="1b-1b")

# Process marketing brief
result = agent.process_brief(
    brief="Create Instagram ad for coffee",
    brand_context="Premium brand"
)

# Process video edit (Smart Cut)
result = agent.process_video_edit(
    video_path="interview.mp4",
    requirements="Extract highlights",
    target_duration=120
)
```

## 🔧 Tool Definitions

### Built-in Tools

```python
# Image Generation
image_gen(prompt, style="realistic", aspect_ratio="1:1")

# Voice Generation
voice_gen(text, voice="th-TH-NiwatNeural", rate="+0%")

# Video Composition
video_compose(images, audio, duration=15, transitions="fade")

# Smart Cut
smart_cut(video_path, mode="auto", target_duration=120)
```

### Custom Tool Template

```python
def my_custom_tool(param1: str, param2: int = 10) -> str:
    """
    Description of what this tool does.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
        
    Returns:
        Description of return value
    """
    # Implementation
    return "result"

# Register
executor.register_tool(my_custom_tool)
```

## 📊 Model Sizes & Requirements

| Model | Size | VRAM | Speed | Use Case |
|-------|------|------|-------|----------|
| T5Gemma 2-270M | ~370M | ~1GB | Fast | Testing |
| T5Gemma 2-1B | ~1.7B | ~4GB | Medium | Recommended |
| T5Gemma 2-4B | ~7B | ~16GB | Slow | Best quality |
| FunctionGemma | 270M | ~550MB | Very fast | Always use |

## 🎯 Decision Tree

```
Task Type Decision:
├─ Creative/Strategic?
│  ├─ Generate content → T5Gemma 2
│  ├─ Write scripts → T5Gemma 2
│  ├─ Analyze video → T5Gemma 2
│  └─ Make decisions → T5Gemma 2
│
├─ Execution/Tools?
│  ├─ Parse to JSON → FunctionGemma
│  ├─ Call APIs → FunctionGemma
│  └─ Orchestrate → FunctionGemma
│
└─ Both?
   └─ Use AI Director Agent (Both models)
```

## ⚙️ Common Configurations

### Low Memory (< 4GB RAM)
```python
# Use smallest models
thinker = T5GemmaThinker(model_size="270m-270m")
executor = FunctionGemmaExecutor()  # Always 270M
```

### Balanced (4-8GB RAM)
```python
# Recommended for Codespaces
thinker = T5GemmaThinker(model_size="1b-1b")
executor = FunctionGemmaExecutor()
```

### High Quality (16GB+ RAM)
```python
# Best quality, slower
thinker = T5GemmaThinker(model_size="4b-4b")
executor = FunctionGemmaExecutor()
```

## 🐛 Troubleshooting

### Model Loading Issues
```python
# Force CPU if CUDA fails
thinker = T5GemmaThinker(model_size="1b-1b", device="cpu")

# Use float32 if float16 fails
import torch
torch.set_default_dtype(torch.float32)
```

### Out of Memory
```python
# Reduce batch size / max tokens
strategy = thinker.generate_strategy(brief, max_length=200)

# Clear cache
import torch
torch.cuda.empty_cache()
```

### Slow Inference
```python
# Use smaller model
thinker = T5GemmaThinker(model_size="270m-270m")

# Reduce output length
tool_calls = executor.parse_to_tool_calls(instruction, max_new_tokens=100)
```

## 📈 Performance Benchmarks

Typical performance on 2-core Codespaces:

| Task | T5Gemma 1B | FunctionGemma |
|------|-----------|---------------|
| Load time | ~10-15s | ~5-8s |
| Strategy generation | ~15-25s | - |
| Tool parsing | - | ~1-2s |
| Complete workflow | ~20-30s | - |

## ✅ Completion Checklist

- [ ] All dependencies installed
- [ ] T5Gemma 2 loads successfully
- [ ] FunctionGemma loads successfully
- [ ] Can generate strategy
- [ ] Can parse tool calls
- [ ] AI Director Agent works end-to-end
- [ ] All tests pass
- [ ] Understand dual-model architecture

## 🔗 Resources

- [T5Gemma 2 Docs](https://huggingface.co/google/t5gemma-2-1b-1b)
- [FunctionGemma Docs](https://huggingface.co/google/functiongemma-270m-it)
- [Course Documentation](../course_ai-assistant_v3.4.2.md)
- [Module README](README.md)

## 📞 Need Help?

1. Check error messages carefully
2. Review README.md for detailed explanations
3. Run test suite: `python 04_test_module1.py`
4. Try examples in `examples/` directory
5. Check model documentation links above

---

**Module 1 Version:** v3.4  
**Last Updated:** January 2026
