# Module 6.5: Quick Start Guide

> Get started with Smart Cut in 5 minutes! ✂️

---

## Prerequisites

- Python 3.10+
- FFmpeg installed
- Module 6 (Production Tools) installed

---

## Installation

### 1. Install FFmpeg

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Verify
ffmpeg -version
```

### 2. Install Python Dependencies

```bash
cd module6.5
pip install -r requirements.txt
```

---

## Quick Tests

### Test 1: Scene Detection (10 seconds)

```python
from module6_5.tools import SceneDetector

detector = SceneDetector()
scenes = detector.detect_scenes("test_video.mp4")

print(f"Found {len(scenes)} scenes")
```

### Test 2: Remove Silence (30 seconds)

```python
from module6_5.tools import AutoEditor

editor = AutoEditor()
edited = editor.remove_silence(
    video_path="test_video.mp4",
    output_path="no_silence.mp4"
)
```

### Test 3: Smart Cut (1 minute)

```python
from module6_5.tools import SmartCut

smart_cut = SmartCut()
result = smart_cut.process_video(
    input_path="test_video.mp4",
    output_path="edited.mp4",
    remove_silence=True,
    target_duration=60.0
)

print(f"Saved {result['time_saved']:.2f}s!")
```

---

## Basic Usage

### Scene Detection

```python
from module6_5.tools import SceneDetector

detector = SceneDetector()

# Detect scenes
scenes = detector.detect_scenes(
    video_path="video.mp4",
    method="content",  # or "threshold", "adaptive"
    threshold=30.0
)

# Print results
for scene in scenes:
    print(f"Scene {scene.scene_number}: "
          f"{scene.start_time:.2f}s - {scene.end_time:.2f}s")
```

### Remove Silence

```python
from module6_5.tools import AutoEditor

editor = AutoEditor()

edited = editor.remove_silence(
    video_path="raw.mp4",
    output_path="no_silence.mp4",
    padding=0.1  # Keep 0.1s before/after speech
)
```

### Complete Smart Cut

```python
from module6_5.tools import SmartCut, SmartCutConfig

# Configure
config = SmartCutConfig(
    remove_silence=True,
    target_duration=60.0,
    scene_threshold=30.0
)

# Process
smart_cut = SmartCut(config=config)
result = smart_cut.process_video(
    input_path="raw_video.mp4",
    output_path="edited_video.mp4"
)

print(f"✅ Saved {result['time_saved']:.2f}s "
      f"({result['percent_saved']:.1f}%)")
```

---

## Troubleshooting

### Issue: ModuleNotFoundError: scenedetect

**Solution:**
```bash
pip install scenedetect[opencv]==0.6.3
```

### Issue: FFmpeg not found

**Solution:**
```bash
sudo apt-get install ffmpeg
which ffmpeg
```

### Issue: Scene detection too sensitive

**Solution:**
```python
# Increase threshold (higher = less sensitive)
scenes = detector.detect_scenes(
    video_path="video.mp4",
    threshold=50.0  # Default: 30.0
)
```

---

## Next Steps

1. ✅ Read [README.md](README.md) for full documentation
2. ✅ Try examples in `examples/` directory
3. ✅ Run tests: `pytest tests/`
4. ✅ Integrate with Module 6 (Production Tools)
5. ✅ Build your AI Director pipeline!

---

**Happy Editing! ✂️🎬**
