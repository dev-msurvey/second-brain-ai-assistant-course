# Module 6.5: Smart Cut - Advanced Video Editing

> **"Intelligent Video Editing with AI"**  
> Automatic scene detection, silence removal, and smart trimming

**Status**: ✅ Complete  
**Duration**: ~3 hours  
**Difficulty**: ⭐⭐⭐⭐

---

## 📋 Overview

Module 6.5 adds intelligent video editing capabilities to the AI Director system:
- **Scene Detection**: Automatically detect scene changes
- **Silence Removal**: Remove pauses and dead space
- **Smart Trimming**: Intelligently cut videos to target duration
- **Auto-Editing**: Optimize pacing and flow
- **Highlights Creation**: Generate highlight reels

---

## 🎯 Learning Objectives

After completing Module 6.5, you will be able to:
- ✅ Detect scenes using content-based analysis
- ✅ Remove silent segments from videos
- ✅ Automatically trim videos to specific durations
- ✅ Create highlight reels
- ✅ Batch process multiple videos
- ✅ Analyze video content programmatically

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                MODULE 6.5 ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   INPUT VIDEO                                                │
│       │                                                      │
│       ▼                                                      │
│   ┌──────────────────────┐                                  │
│   │  Scene Detector      │                                  │
│   │  - Content-based     │                                  │
│   │  - Threshold-based   │                                  │
│   │  - Adaptive          │                                  │
│   └──────────┬───────────┘                                  │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────┐                                  │
│   │  Audio Analyzer      │                                  │
│   │  - Silence detection │                                  │
│   │  - RMS energy        │                                  │
│   │  - Voice activity    │                                  │
│   └──────────┬───────────┘                                  │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────┐                                  │
│   │  Smart Cut Engine    │                                  │
│   │  - Edit decisions    │                                  │
│   │  - Trim strategy     │                                  │
│   │  - Pacing optimize   │                                  │
│   └──────────┬───────────┘                                  │
│              │                                               │
│              ▼                                               │
│   ┌──────────────────────┐                                  │
│   │  Auto Editor         │                                  │
│   │  - Apply cuts        │                                  │
│   │  - Concatenate       │                                  │
│   │  - Export            │                                  │
│   └──────────┬───────────┘                                  │
│              │                                               │
│              ▼                                               │
│   [EDITED VIDEO]                                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 1. Scene Detection

**Methods:**
- **Content-based**: Detects changes in frame content
- **Threshold-based**: Detects fades and cuts based on brightness
- **Adaptive**: Combines multiple detection methods

**API:**
```python
from module6_5.tools import SceneDetector

detector = SceneDetector()
scenes = detector.detect_scenes(
    video_path="video.mp4",
    method="content",
    threshold=30.0
)

# Print detected scenes
for scene in scenes:
    print(f"Scene {scene.scene_number}: "
          f"{scene.start_time:.2f}s - {scene.end_time:.2f}s")
```

### 2. Silence Removal

**Capabilities:**
- Detect silent segments using RMS energy
- Configurable silence threshold
- Padding before/after speech
- Minimum clip duration

**API:**
```python
from module6_5.tools import AutoEditor

editor = AutoEditor(
    silence_threshold=-40.0,  # dB
    min_silence_duration=0.5  # seconds
)

edited_video = editor.remove_silence(
    video_path="input.mp4",
    output_path="output.mp4",
    padding=0.1  # seconds
)
```

### 3. Smart Trimming

**Strategies:**
- **Smart**: Keep most important scenes
- **End**: Simple cut from end
- **Proportional**: Cut equally from all scenes

**API:**
```python
editor = AutoEditor()

decisions = editor.trim_to_duration(
    video_path="video.mp4",
    target_duration=60.0,  # 1 minute
    scenes=scenes,
    strategy="smart"
)

edited = editor.apply_edit_decisions(
    video_path="video.mp4",
    decisions=decisions,
    output_path="trimmed.mp4"
)
```

### 4. Complete Smart Cut

**All-in-one Processing:**
```python
from module6_5.tools import SmartCut, SmartCutConfig

config = SmartCutConfig(
    remove_silence=True,
    target_duration=60.0,
    scene_threshold=30.0
)

smart_cut = SmartCut(config=config)

result = smart_cut.process_video(
    input_path="raw_video.mp4",
    output_path="edited_video.mp4"
)

print(f"Time saved: {result['time_saved']:.2f}s")
print(f"Percent saved: {result['percent_saved']:.1f}%")
```

### 5. Highlights Creation

**Automatic Highlight Reels:**
```python
smart_cut = SmartCut()

highlights = smart_cut.create_highlights(
    video_path="full_video.mp4",
    output_path="highlights.mp4",
    duration=30.0,  # 30 second highlight reel
    num_clips=3     # 3 best clips
)
```

---

## 📦 Installation

### Prerequisites

```bash
# System dependencies
sudo apt-get install ffmpeg

# Python dependencies
cd module6.5
pip install -r requirements.txt
```

### Dependencies

- **scenedetect**: Scene detection
- **opencv-python**: Video processing
- **moviepy**: Video editing
- **librosa**: Audio analysis
- **numpy/scipy**: Numerical computing

---

## 🚀 Quick Start

### Example 1: Detect Scenes

```python
from module6_5.tools import SceneDetector

detector = SceneDetector()

scenes = detector.detect_scenes(
    video_path="video.mp4",
    method="content",
    threshold=30.0
)

print(f"Found {len(scenes)} scenes")
for scene in scenes:
    print(f"  Scene {scene.scene_number}: "
          f"{scene.start_time:.2f}s - {scene.end_time:.2f}s "
          f"({scene.duration:.2f}s)")
```

### Example 2: Remove Silence

```python
from module6_5.tools import AutoEditor

editor = AutoEditor()

edited = editor.remove_silence(
    video_path="raw_video.mp4",
    output_path="no_silence.mp4"
)

print(f"Silence removed: {edited}")
```

### Example 3: Smart Cut

```python
from module6_5.tools import SmartCut

smart_cut = SmartCut()

result = smart_cut.process_video(
    input_path="raw_video.mp4",
    output_path="edited_video.mp4",
    remove_silence=True,
    target_duration=60.0
)

print(f"✅ Saved {result['time_saved']:.2f}s "
      f"({result['percent_saved']:.1f}%)")
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test scene detection
pytest tests/test_scene_detector.py -v

# Test auto editor
pytest tests/test_auto_editor.py -v

# With coverage
pytest tests/ --cov=tools --cov-report=html
```

---

## 📊 Performance

| Operation | Avg Time | Accuracy | Method |
|-----------|----------|----------|--------|
| Scene Detection (1min) | ~5s | High | PySceneDetect |
| Silence Detection | ~2s | High | Librosa RMS |
| Trim to Duration | ~1s | High | Smart algorithm |
| Full Smart Cut | ~30-60s | High | Combined |

**Hardware:**
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB recommended
- GPU: Not required

---

## 💰 Zero-Cost Components

All tools are **100% free** and open-source:

- **PySceneDetect**: Free, open-source
- **OpenCV**: Free, open-source
- **MoviePy**: Free, open-source
- **Librosa**: Free, open-source

**Total Cost: $0.00/month** ✅

---

## 📚 Configuration

All settings configurable via `SmartCutConfig`:

```python
from module6_5.tools import SmartCutConfig

config = SmartCutConfig(
    # Scene detection
    scene_detection_method="content",
    scene_threshold=30.0,
    min_scene_length=0.5,
    
    # Audio analysis
    silence_threshold=-40.0,
    min_silence_duration=0.5,
    min_clip_duration=0.3,
    
    # Editing
    remove_silence=True,
    target_duration=None,
    trim_strategy="smart",
    
    # Output
    output_fps=30,
    output_codec="libx264"
)
```

Or use YAML config file:

```yaml
# configs/smart_cut_config.yaml
scene_detection_method: "content"
scene_threshold: 30.0
remove_silence: true
target_duration: 60.0
```

---

## 🎯 Use Cases

### 1. Interview Editing
- Remove long pauses
- Cut dead space
- Trim to specific duration

### 2. Tutorial Videos
- Remove mistakes and retakes
- Keep only important segments
- Optimize pacing

### 3. Podcast Editing
- Remove silence between speakers
- Cut intro/outro music precisely
- Trim to episode length

### 4. Social Media Content
- Create short highlights
- Trim to platform limits (60s, 90s)
- Auto-generate clips

---

## 🔧 Advanced Features

### Batch Processing

```python
smart_cut = SmartCut()

results = smart_cut.batch_process(
    input_files=[
        "video1.mp4",
        "video2.mp4",
        "video3.mp4"
    ],
    output_dir="edited_videos/",
    remove_silence=True,
    target_duration=60.0
)
```

### Custom Edit Decisions

```python
from module6_5.tools import AutoEditor, EditDecision

editor = AutoEditor()

# Create custom edit decisions
decisions = [
    EditDecision(
        action="keep",
        start_time=0.0,
        end_time=30.0,
        reason="Intro"
    ),
    EditDecision(
        action="trim",
        start_time=30.0,
        end_time=45.0,
        speed_factor=1.5,  # Speed up 1.5x
        reason="Slow segment"
    )
]

# Apply decisions
edited = editor.apply_edit_decisions(
    video_path="video.mp4",
    decisions=decisions,
    output_path="custom_edit.mp4"
)
```

### Scene Statistics

```python
detector = SceneDetector()
scenes = detector.detect_scenes("video.mp4")

stats = detector.get_scene_statistics(scenes)

print(f"Total scenes: {stats['total_scenes']}")
print(f"Average duration: {stats['avg_scene_duration']:.2f}s")
print(f"Shortest scene: {stats['min_scene_duration']:.2f}s")
print(f"Longest scene: {stats['max_scene_duration']:.2f}s")
```

---

## 🐛 Troubleshooting

### Issue: Scene detection too sensitive

**Solution**: Increase threshold
```python
scenes = detector.detect_scenes(
    video_path="video.mp4",
    threshold=50.0  # Higher = less sensitive
)
```

### Issue: Too much silence removed

**Solution**: Lower silence threshold or increase minimum duration
```python
editor = AutoEditor(
    silence_threshold=-50.0,  # Lower = more silence kept
    min_silence_duration=1.0   # Only remove longer silences
)
```

### Issue: FFmpeg not found

**Solution**: Install FFmpeg
```bash
sudo apt-get install ffmpeg
```

---

## 📖 API Reference

### SceneDetector

```python
SceneDetector(
    downscale_factor: int = 1,
    min_scene_len: float = 0.5
)

detect_scenes(
    video_path: str,
    method: str = "content",
    threshold: float = 30.0,
    save_stats: bool = False
) -> List[Scene]

get_scene_statistics(scenes: List[Scene]) -> Dict[str, Any]
```

### AutoEditor

```python
AutoEditor(
    silence_threshold: float = -40.0,
    min_silence_duration: float = 0.5,
    min_clip_duration: float = 0.3
)

remove_silence(
    video_path: str,
    output_path: str,
    padding: float = 0.1
) -> str

trim_to_duration(
    video_path: str,
    target_duration: float,
    strategy: str = "smart"
) -> List[EditDecision]

auto_edit(
    video_path: str,
    output_path: str,
    remove_silence: bool = True,
    target_duration: Optional[float] = None
) -> str
```

### SmartCut

```python
SmartCut(config: Optional[SmartCutConfig] = None)

analyze_video(
    video_path: str,
    detect_scenes: bool = True,
    detect_silence: bool = True
) -> Dict[str, Any]

process_video(
    input_path: str,
    output_path: str,
    remove_silence: Optional[bool] = None,
    target_duration: Optional[float] = None
) -> Dict[str, Any]

create_highlights(
    video_path: str,
    output_path: str,
    duration: float = 30.0,
    num_clips: int = 3
) -> str

batch_process(
    input_files: List[str],
    output_dir: str,
    **kwargs
) -> List[Dict[str, Any]]
```

---

## 🎯 Next Steps

After completing Module 6.5:
1. ✅ Integrate with Module 6 (Production Tools)
2. ✅ Connect to Module 5 (Vector RAG) for content-aware editing
3. ✅ Add B-roll management system
4. ✅ Implement beat-sync editing
5. ✅ Build complete AI Director pipeline

---

## 📖 Additional Resources

- [PySceneDetect Documentation](https://pyscenedetect.readthedocs.io/)
- [MoviePy User Guide](https://zulko.github.io/moviepy/)
- [Librosa Tutorial](https://librosa.org/doc/latest/tutorial.html)
- [OpenCV Video Processing](https://docs.opencv.org/master/d7/d9e/tutorial_video_write.html)

---

**Module 6.5 Status**: ✅ Complete  
**Integration Ready**: Yes

**Happy Editing! ✂️🎬**
