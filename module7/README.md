# Module 7: Integration - AI Director System

Complete integration layer that connects all AI Director modules into a unified system.

## 🎯 Overview

Module 7 provides:
- **AIDirector**: Main orchestrator coordinating all modules
- **Unified API**: FastAPI REST API for all functionalities
- **Content Pipeline**: End-to-end content generation workflows
- **Batch Processing**: Process multiple content briefs efficiently

## 📦 Architecture

```
┌─────────────────────────────────────────────────────┐
│              Module 7: Integration                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐     ┌──────────────┐             │
│  │ AI Director  │────▶│ Unified API  │             │
│  │ Orchestrator │     │  (FastAPI)   │             │
│  └──────┬───────┘     └──────────────┘             │
│         │                                            │
│         ├─────▶ Module 5: Vector RAG               │
│         │       (Brand Context Retrieval)           │
│         │                                            │
│         ├─────▶ Module 6: Production Tools         │
│         │       (Image/Voice/Video Generation)      │
│         │                                            │
│         └─────▶ Module 6.5: Smart Cut              │
│                 (Video Editing)                      │
│                                                      │
└─────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd module7
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export MONGODB_URI="mongodb+srv://..."
export HF_TOKEN="hf_..."
```

### 3. Run Full Pipeline Example

```bash
python examples/example_full_pipeline.py
```

### 4. Start API Server

```bash
python -m api.main
# or
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Test API

```bash
python examples/example_api_usage.py
```

## 📚 Components

### Core: AI Director Orchestrator

Main class that coordinates all modules:

```python
from module7.core import AIDirector, DirectorConfig, Brief

# Configure
config = DirectorConfig(
    mongodb_uri="mongodb+srv://...",
    hf_token="hf_...",
    output_dir="output"
)

# Initialize
director = AIDirector(config)

# Create brief
brief = Brief(
    brand="CoffeeLab",
    product="Cold Brew",
    duration=15.0,
    platform="instagram"
)

# Generate content
result = await director.create_content(brief)
print(f"Video: {result.video_path}")
```

**Pipeline Steps:**
1. **Retrieve Brand Context** (Module 5: Vector RAG)
2. **Generate Creative Strategy** (Module 4: LLM)
3. **Generate Images** (Module 6: Image Generator)
4. **Generate Voiceover** (Module 6: Voice Generator)
5. **Compose Video** (Module 6: Video Composer)
6. **Apply Smart Editing** (Module 6.5: Smart Cut)

### API: Unified REST API

FastAPI application providing REST endpoints:

```python
# Health Check
GET /api/v1/health

# Full Pipeline
POST /api/v1/generate
{
  "brand": "CoffeeLab",
  "product": "Cold Brew",
  "duration": 15.0,
  "platform": "instagram"
}

# Vector RAG Search
POST /api/v1/rag/search
{
  "query": "CoffeeLab brand guidelines",
  "top_k": 3
}

# Image Generation
POST /api/v1/media/image
{
  "prompt": "Premium coffee product",
  "style": "product",
  "width": 1024,
  "height": 1024
}

# Voice Generation
POST /api/v1/media/voice
{
  "text": "สวัสดีครับ",
  "voice": "th-TH-NiwatNeural"
}

# Smart Cut
POST /api/v1/edit/smart-cut
{
  "video_path": "input.mp4",
  "remove_silence": true
}
```

### Pipelines: Workflow Orchestration

High-level workflows for batch processing:

```python
from module7.pipelines import ContentPipeline

pipeline = ContentPipeline(director)

# Single brief
result = await pipeline.process_brief(brief)

# Batch processing (sequential)
briefs = [brief1, brief2, brief3]
results = await pipeline.process_batch(briefs, parallel=False)

# Get statistics
stats = pipeline.get_statistics()
print(f"Average time: {stats['average_processing_time']:.2f}s")

# Export results
pipeline.export_results("batch_results.json")
```

## 📖 Examples

### Example 1: Full Pipeline

Complete content generation from brief to final video:

```bash
python examples/example_full_pipeline.py
```

Output:
```
🎬 AI DIRECTOR: Complete Pipeline Example
============================================================

✅ PIPELINE COMPLETE!
============================================================

📊 Results:
   Video: output/full_pipeline/video_final_1234567890.mp4
   Images: 2 files
   Audio: output/full_pipeline/voiceover_1234567890.mp3
   Duration: 15.0s
   Processing Time: 45.23s
```

### Example 2: API Usage

Using the REST API:

```bash
# Terminal 1: Start API server
python -m api.main

# Terminal 2: Run client examples
python examples/example_api_usage.py
```

### Example 3: Batch Production

Process multiple briefs:

```bash
python examples/example_batch_production.py
```

Output:
```
📦 AI DIRECTOR: Batch Production Example
============================================================

📊 Statistics:
   Total Briefs: 5
   Successful: 5
   Total Time: 225.45s
   Average Time: 45.09s per brief
   Total Videos: 5
   Total Images: 10
```

## 🔧 Configuration

### DirectorConfig Options

```python
config = DirectorConfig(
    # Module 5: Vector RAG
    mongodb_uri="mongodb+srv://...",
    mongodb_database="ai_director",
    mongodb_collection="brand_vectors",
    retrieval_method="hybrid",  # "vector", "bm25", "hybrid"
    top_k=3,
    
    # Module 6: Production Tools
    hf_token="hf_...",
    image_model="sdxl",  # "sdxl", "flux"
    voice_language="thai",
    video_fps=30,
    
    # Module 6.5: Smart Cut
    scene_detection_method="content",
    remove_silence=True,
    
    # General
    output_dir="output",
    temp_dir="temp",
    cache_enabled=False
)
```

## 📊 Performance

### Single Brief Processing

| Step | Time | Module |
|------|------|--------|
| Brand Context Retrieval | ~2s | Module 5 |
| Strategy Generation | ~5s | Module 4 |
| Image Generation (2 images) | ~20s | Module 6 |
| Voice Generation | ~5s | Module 6 |
| Video Composition | ~8s | Module 6 |
| Smart Editing | ~5s | Module 6.5 |
| **Total** | **~45s** | - |

### Batch Processing

- **Sequential**: 45s × N briefs
- **Parallel**: ~45s (theoretical, resource-dependent)

## 🧪 Testing

### Run Integration Tests

```bash
pytest tests/ -v
```

### Manual Testing Checklist

- [ ] AIDirector initialization
- [ ] Vector RAG retrieval
- [ ] Image generation
- [ ] Voice generation
- [ ] Video composition
- [ ] Smart editing
- [ ] Full pipeline (single brief)
- [ ] Batch processing (multiple briefs)
- [ ] API endpoints
- [ ] Error handling
- [ ] Resource cleanup

## 🐛 Troubleshooting

### Module Import Errors

```bash
# Add modules to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/workspaces/second-brain-ai-assistant-course"
```

### MongoDB Connection Issues

```bash
# Verify connection
python -c "from pymongo import MongoClient; client = MongoClient('$MONGODB_URI'); print(client.admin.command('ping'))"
```

### HuggingFace API Issues

```bash
# Verify token
python -c "from huggingface_hub import HfApi; api = HfApi(token='$HF_TOKEN'); print(api.whoami())"
```

### Missing Dependencies

```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

## 📁 Directory Structure

```
module7/
├── README.md                 # This file
├── QUICKSTART.md             # Quick start guide
├── requirements.txt          # All dependencies
├── core/                     # Core integration logic
│   ├── __init__.py
│   └── ai_director.py        # Main orchestrator (600+ lines)
├── api/                      # Unified REST API
│   ├── __init__.py
│   └── main.py               # FastAPI app (500+ lines)
├── pipelines/                # Workflow orchestration
│   ├── __init__.py
│   └── content_generation.py # Content pipeline (300+ lines)
├── examples/                 # Usage examples
│   ├── example_full_pipeline.py      # Complete pipeline
│   ├── example_api_usage.py          # API client
│   └── example_batch_production.py   # Batch processing
├── configs/                  # Configuration files
├── tests/                    # Integration tests
└── tools/                    # Utility scripts
```

## 🔗 Integration with Other Modules

### Module 5: Vector RAG

```python
# Used for brand context retrieval
rag = director._get_rag_system()
context = rag.retrieve(query="brand guidelines")
```

### Module 6: Production Tools

```python
# Image generation
image_gen = director._get_image_generator()
image = image_gen.generate(prompt="product photo")

# Voice generation
voice_gen = director._get_voice_generator()
audio = await voice_gen.generate(text="script")

# Video composition
video_comp = director._get_video_composer()
video = video_comp.create_ad(images=[...], audio="audio.mp3")
```

### Module 6.5: Smart Cut

```python
# Video editing
smart_cut = director._get_smart_cut()
edited = smart_cut.process_video(input_path="video.mp4")
```

## 🎓 Key Concepts

### Lazy Loading

Modules are loaded only when needed to save resources:

```python
# Module loaded on first access
rag = director._get_rag_system()  # Loads Module 5

# Subsequent calls use cached instance
rag = director._get_rag_system()  # Returns cached
```

### Error Handling

Graceful degradation when modules unavailable:

```python
rag = director._get_rag_system()
if rag is None:
    logger.warning("RAG unavailable, using fallback")
    return default_context
```

### Metadata Tracking

Complete provenance for every output:

```python
output = await director.create_content(brief)
metadata = output.metadata
# Contains: brief, strategy, context, timing, etc.
```

## 💡 Best Practices

1. **Environment Variables**: Always use env vars for secrets
2. **Resource Management**: Use lazy loading for optional modules
3. **Error Handling**: Implement fallbacks for each module
4. **Logging**: Log all steps for debugging
5. **Cleanup**: Clear temp files after processing
6. **Batch Size**: Limit parallel batches to avoid OOM
7. **Timeouts**: Set appropriate timeouts for API calls

## 📝 License

MIT License - See LICENSE file for details

## 👥 Authors

AI Director Team

## 🙏 Acknowledgments

- Module 5: Vector RAG Team
- Module 6: Production Tools Team
- Module 6.5: Smart Cut Team
- FastAPI Community
- HuggingFace Team

---

**Status**: ✅ Integration Complete  
**Version**: 1.0.0  
**Last Updated**: 2024
