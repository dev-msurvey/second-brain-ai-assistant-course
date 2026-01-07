# Module 7: Quick Start Guide

Get started with AI Director Integration in 5 minutes!

## ⚡ Installation (2 minutes)

```bash
# 1. Navigate to Module 7
cd module7

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/"
export HF_TOKEN="hf_your_token_here"
```

## 🎬 Run Your First Pipeline (3 minutes)

### Option 1: Python Script

Create `test_director.py`:

```python
import asyncio
import os
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "core"))
from ai_director import AIDirector, DirectorConfig, Brief

async def main():
    # Configure
    config = DirectorConfig(
        mongodb_uri=os.getenv("MONGODB_URI"),
        hf_token=os.getenv("HF_TOKEN"),
        output_dir="output/test"
    )
    
    # Initialize
    director = AIDirector(config)
    
    # Create brief
    brief = Brief(
        brand="TestBrand",
        product="Test Product",
        duration=10.0,
        platform="instagram"
    )
    
    # Generate!
    result = await director.create_content(brief)
    print(f"✅ Video: {result.video_path}")

asyncio.run(main())
```

Run:
```bash
python test_director.py
```

### Option 2: Use Example Scripts

```bash
# Full pipeline
python examples/example_full_pipeline.py

# API server
python -m api.main

# Batch processing
python examples/example_batch_production.py
```

## 📝 Simple Examples

### Example 1: Generate Content

```python
from module7.core import AIDirector, DirectorConfig, Brief

# Setup
config = DirectorConfig(output_dir="output")
director = AIDirector(config)

# Brief
brief = Brief(
    brand="CoffeeLab",
    product="Cold Brew",
    duration=15.0,
    platform="instagram"
)

# Generate
result = await director.create_content(brief)
```

### Example 2: Use API

```bash
# Start server
python -m api.main

# In another terminal:
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "CoffeeLab",
    "product": "Cold Brew",
    "duration": 15.0,
    "platform": "instagram"
  }'
```

### Example 3: Batch Processing

```python
from module7.pipelines import ContentPipeline

pipeline = ContentPipeline(director)

briefs = [brief1, brief2, brief3]
results = await pipeline.process_batch(briefs)

print(f"Generated {len(results)} videos")
```

## 🎯 What's Next?

1. **Customize Configuration**: Edit `DirectorConfig` parameters
2. **Try Different Platforms**: instagram, youtube, tiktok
3. **Batch Processing**: Process multiple briefs
4. **API Integration**: Build your own client
5. **Add Custom Modules**: Extend the pipeline

## 📚 More Resources

- [Full README](README.md) - Complete documentation
- [API Reference](api/main.py) - API endpoints
- [Examples](examples/) - More examples

## 🐛 Issues?

Check [README.md#troubleshooting](README.md#troubleshooting) for common issues.

---

**Ready in 5 minutes! 🚀**
