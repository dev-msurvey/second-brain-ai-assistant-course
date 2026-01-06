# Module 6: Quick Start Guide

> Get started with Production Tools in 5 minutes! 🚀

---

## Prerequisites

- Python 3.10+
- FFmpeg installed
- HuggingFace account (for image generation)

---

## Installation

### 1. Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Verify installation
ffmpeg -version
```

### 2. Install Python Dependencies

```bash
cd module6
pip install -r requirements.txt
```

### 3. Setup HuggingFace API Token

Get your free API token: https://huggingface.co/settings/tokens

```bash
export HF_TOKEN="your_token_here"
```

---

## Quick Tests

### Test 1: Voice Generation (5 seconds)

```bash
python examples/example_voice_generation.py
```

Expected output:
- `output/thai_male.mp3`
- `output/thai_female.mp3`
- `output/english_male.mp3`

### Test 2: Image Generation (30 seconds)

```bash
python examples/example_image_generation.py
```

Expected output:
- `output/coffee_product.png`

### Test 3: Full Pipeline (2 minutes)

```bash
python examples/example_full_pipeline.py
```

Expected output:
- `output/pipeline/coffeelab_ad_15s.mp4`

---

## Basic Usage

### Image Generation

```python
from tools.image_generator import ImageGenerator

generator = ImageGenerator(model="sdxl")

image = generator.generate(
    prompt="A premium coffee cup",
    style_preset="product",
    output_file="coffee.png"
)
```

### Voice Generation

```python
import asyncio
from tools.voice_generator import VoiceGenerator

async def main():
    generator = VoiceGenerator()
    
    await generator.generate(
        text="สวัสดีครับ",
        voice="th-TH-NiwatNeural",
        output_file="hello.mp3"
    )

asyncio.run(main())
```

### Video Composition

```python
from tools.video_composer import VideoComposer

composer = VideoComposer()

video = composer.create_ad(
    images=["img1.png"],
    audio="voice.mp3",
    title="My Ad"
)

composer.export(video, "ad.mp4")
```

---

## Troubleshooting

### Issue: ModuleNotFoundError: edge_tts

**Solution:**
```bash
pip install edge-tts==6.1.9
```

### Issue: FFmpeg not found

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# Verify
which ffmpeg
```

### Issue: HuggingFace API Error

**Solution:**
1. Check token: `echo $HF_TOKEN`
2. Get new token: https://huggingface.co/settings/tokens
3. Re-export: `export HF_TOKEN="new_token"`

---

## Next Steps

1. ✅ Complete [README.md](README.md) for full documentation
2. ✅ Try all examples in `examples/` directory
3. ✅ Run tests: `pytest tests/`
4. ✅ Integrate with Module 5 (Vector RAG)
5. ✅ Build your first AI-generated ad!

---

## Support

- 📖 Full Documentation: [README.md](README.md)
- 💬 Issues: GitHub Issues
- 📧 Contact: AI Director Team

---

**Happy Creating! 🎨🎙️🎬**
