# Module 6: Production Tools Setup

> **"Building the Hands of AI Director"**  
> Image Generation, Voice Generation, and Video Composition

**Status**: 🚧 In Development  
**Duration**: ~4 hours  
**Difficulty**: ⭐⭐⭐

---

## 📋 Overview

Module 6 implements the production tools that transform AI Director's creative ideas into actual content:
- **Image Generation**: Create visuals from text prompts
- **Voice Generation**: Text-to-speech with Thai support
- **Video Composition**: Combine images, audio, and effects

---

## 🎯 Learning Objectives

After completing Module 6, you will be able to:
- ✅ Generate images using HuggingFace Inference API (SDXL/Flux)
- ✅ Create voiceovers with Edge-TTS (Thai and English)
- ✅ Compose videos with MoviePy
- ✅ Integrate all tools into AI Director pipeline
- ✅ Handle production workflows end-to-end

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   MODULE 6 ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   USER BRIEF                                                 │
│       │                                                      │
│       ▼                                                      │
│   ┌──────────────────────┐                                  │
│   │ Module 5: Vector RAG │  ← Retrieve brand context       │
│   └──────────┬───────────┘                                  │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────┐                                  │
│   │ Module 4: LLM        │  ← Generate creative strategy   │
│   └──────────┬───────────┘                                  │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────────────────────────┐              │
│   │         MODULE 6: PRODUCTION TOOLS       │              │
│   ├──────────────────────────────────────────┤              │
│   │                                          │              │
│   │  ┌────────────────┐  ┌────────────────┐ │              │
│   │  │ Image Gen      │  │ Voice Gen      │ │              │
│   │  │ (SDXL/Flux)    │  │ (Edge-TTS)     │ │              │
│   │  └────────┬───────┘  └────────┬───────┘ │              │
│   │           │                    │         │              │
│   │           └──────────┬─────────┘         │              │
│   │                      ▼                   │              │
│   │           ┌────────────────┐             │              │
│   │           │ Video Composer │             │              │
│   │           │   (MoviePy)    │             │              │
│   │           └────────┬───────┘             │              │
│   │                    │                     │              │
│   └────────────────────┼─────────────────────┘              │
│                        │                                    │
│                        ▼                                    │
│               [Final Content]                               │
│            (Images, Audio, Video)                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 1. Image Generation Tool

**Capabilities:**
- SDXL 1.0 base model support
- Flux model support (dev/schnell)
- Negative prompts
- Configurable parameters (steps, guidance, size)
- Batch generation
- Style presets

**API:**
```python
from module6.tools.image_generator import ImageGenerator

generator = ImageGenerator(model="sdxl")

# Generate single image
image = generator.generate(
    prompt="A premium coffee cup on marble surface, soft morning light",
    negative_prompt="blurry, low quality",
    width=1024,
    height=1024
)

# Generate batch
images = generator.generate_batch(prompts_list, batch_size=4)
```

### 2. Voice Generation Tool

**Capabilities:**
- Thai voices (th-TH-NiwatNeural, th-TH-PremwadeeNeural)
- English voices (multiple)
- Adjustable rate, pitch, volume
- Subtitle generation (.srt, .vtt)
- Batch processing
- Word-level timestamps

**API:**
```python
from module6.tools.voice_generator import VoiceGenerator

generator = VoiceGenerator()

# Generate Thai voiceover
audio = await generator.generate(
    text="สวัสดีครับ วันนี้เรามาแนะนำกาแฟ Cold Brew",
    voice="th-TH-NiwatNeural",
    rate="+0%",
    output_file="voiceover.mp3"
)

# With subtitles
audio, srt = await generator.generate_with_subtitles(
    text=script,
    voice="th-TH-NiwatNeural"
)
```

### 3. Video Composition Tool

**Capabilities:**
- Combine images and audio
- Add text overlays
- Transitions (fade, dissolve, wipe)
- Effects (zoom, pan, filters)
- Timeline management
- Export multiple formats
- Background music

**API:**
```python
from module6.tools.video_composer import VideoComposer

composer = VideoComposer()

# Create video from assets
video = composer.compose(
    images=["img1.png", "img2.png"],
    audio="voiceover.mp3",
    duration=15,
    transitions=["fade"],
    text_overlays=[
        {"text": "CoffeeLab", "position": "center", "duration": 3}
    ]
)

video.export("final_ad.mp4", fps=30)
```

---

## 📦 Installation

### Prerequisites

```bash
# System dependencies
sudo apt-get install ffmpeg

# Python dependencies
pip install -r requirements.txt
```

### Environment Variables

```bash
# HuggingFace API (for image generation)
export HF_TOKEN="your_huggingface_token"

# Optional: Custom model endpoints
export IMAGE_GEN_MODEL="stabilityai/stable-diffusion-xl-base-1.0"
```

---

## 🚀 Quick Start

### 1. Image Generation Example

```python
from module6.tools.image_generator import ImageGenerator

# Initialize
generator = ImageGenerator()

# Generate product image
image = generator.generate(
    prompt="Premium coffee cup on marble surface, professional photography, 4K",
    negative_prompt="blurry, low quality, watermark",
    width=1080,
    height=1080
)

image.save("product_image.png")
print("✅ Image generated successfully!")
```

### 2. Voice Generation Example

```python
import asyncio
from module6.tools.voice_generator import VoiceGenerator

async def main():
    generator = VoiceGenerator()
    
    # Generate Thai voiceover
    await generator.generate(
        text="เริ่มต้นเช้าวันใหม่ด้วยกาแฟ Cold Brew Premium จาก CoffeeLab",
        voice="th-TH-NiwatNeural",
        output_file="voiceover.mp3"
    )
    
    print("✅ Voice generated successfully!")

asyncio.run(main())
```

### 3. Video Composition Example

```python
from module6.tools.video_composer import VideoComposer

# Initialize
composer = VideoComposer()

# Create simple video ad
video = composer.create_ad(
    images=["product.png"],
    audio="voiceover.mp3",
    duration=15,
    title="CoffeeLab - Premium Coffee",
    style="minimal"
)

video.write_videofile("ad_15s.mp4", fps=30)
print("✅ Video created successfully!")
```

---

## 🧪 Testing

```bash
# Test image generation
python tests/test_image_generator.py

# Test voice generation
python tests/test_voice_generator.py

# Test video composition
python tests/test_video_composer.py

# Run all tests
pytest tests/
```

---

## 📊 Performance

| Tool | Avg Time | Quality | Cost |
|------|----------|---------|------|
| Image Gen (SDXL) | ~10s | High | Free* |
| Voice Gen (Edge-TTS) | ~2s | High | Free |
| Video Compose | ~5-30s | High | Free |

*Free tier limits apply for HuggingFace Inference API

---

## 💰 Zero-Cost Strategy

All tools in Module 6 follow the zero-cost philosophy:

- **Image Generation**: HuggingFace Inference API (free tier)
- **Voice Generation**: Edge-TTS (unlimited, free)
- **Video Composition**: MoviePy (open-source)
- **Storage**: Local filesystem
- **Processing**: Local CPU/GPU

**Total Monthly Cost: $0.00** ✅

---

## 📚 Examples

See the `examples/` directory for complete workflows:

- `example_image_generation.py` - Image generation with different models
- `example_voice_generation.py` - Multi-language voice generation
- `example_video_composition.py` - Complete video ad creation
- `example_full_pipeline.py` - End-to-end AI Director workflow

---

## 🔧 Configuration

All tools are configurable via YAML files in `configs/`:

- `image_config.yaml` - Image generation settings
- `voice_config.yaml` - Voice generation settings
- `video_config.yaml` - Video composition settings

---

## 🐛 Troubleshooting

### Issue: HuggingFace API Rate Limit

**Solution**: Use local models or upgrade to Pro tier

```python
# Use local Stable Diffusion instead
generator = ImageGenerator(model="local", model_path="./models/sdxl")
```

### Issue: Edge-TTS Connection Error

**Solution**: Check internet connection, retry with exponential backoff

```python
generator = VoiceGenerator(retry_attempts=3, retry_delay=2)
```

### Issue: FFmpeg Not Found

**Solution**: Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Check installation
ffmpeg -version
```

---

## 🎯 Next Steps

After completing Module 6:
1. ✅ Integrate with Module 5 (RAG) for context-aware generation
2. ✅ Connect to Module 4 (LLM) for creative direction
3. ✅ Proceed to Module 6.5 (Smart Cut) for video editing
4. ✅ Build complete AI Director pipeline

---

## 📖 Additional Resources

- [HuggingFace Inference API](https://huggingface.co/docs/api-inference)
- [Edge-TTS Documentation](https://github.com/rany2/edge-tts)
- [MoviePy User Guide](https://zulko.github.io/moviepy/)
- [SDXL Model Card](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)

---

**Module 6 Status**: 🚧 In Development  
**Estimated Completion**: January 2026

**Happy Creating! 🎨🎙️🎬**
