"""
Example: Scene Detection
========================

Demonstrates scene detection using different methods.

Usage:
    python examples/example_scene_detection.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.scene_detector import SceneDetector


def example_content_detection():
    """Example 1: Content-based scene detection."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Content-Based Scene Detection")
    print("="*60)
    
    detector = SceneDetector()
    
    video_path = "test_video.mp4"  # Replace with your video
    
    try:
        scenes = detector.detect_scenes(
            video_path=video_path,
            method="content",
            threshold=30.0
        )
        
        print(f"\n✅ Detected {len(scenes)} scenes")
        
        # Print first 10 scenes
        for scene in scenes[:10]:
            print(f"  Scene {scene.scene_number}: "
                  f"{scene.start_time:.2f}s - {scene.end_time:.2f}s "
                  f"({scene.duration:.2f}s, {scene.frame_count} frames)")
        
        # Get statistics
        stats = detector.get_scene_statistics(scenes)
        
        print(f"\n📊 Statistics:")
        print(f"  Total scenes: {stats['total_scenes']}")
        print(f"  Avg duration: {stats['avg_scene_duration']:.2f}s")
        print(f"  Min duration: {stats['min_scene_duration']:.2f}s")
        print(f"  Max duration: {stats['max_scene_duration']:.2f}s")
        print(f"  Total duration: {stats['total_duration']:.2f}s")
        
    except FileNotFoundError:
        print(f"❌ Error: Video file not found: {video_path}")
        print("   Please provide a test video file.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_threshold_detection():
    """Example 2: Threshold-based scene detection."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Threshold-Based Scene Detection")
    print("="*60)
    
    detector = SceneDetector()
    
    video_path = "test_video.mp4"
    
    try:
        scenes = detector.detect_scenes(
            video_path=video_path,
            method="threshold",
            threshold=12.0  # Lower threshold for fades
        )
        
        print(f"\n✅ Detected {len(scenes)} scenes (with fades)")
        
        for scene in scenes[:5]:
            print(f"  Scene {scene.scene_number}: "
                  f"{scene.start_time:.2f}s - {scene.end_time:.2f}s")
        
    except FileNotFoundError:
        print(f"❌ Video not found. Using example data...")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_adaptive_detection():
    """Example 3: Adaptive scene detection."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Adaptive Scene Detection")
    print("="*60)
    
    detector = SceneDetector()
    
    video_path = "test_video.mp4"
    
    try:
        scenes = detector.detect_scenes(
            video_path=video_path,
            method="adaptive",
            threshold=3.0  # Adaptive threshold
        )
        
        print(f"\n✅ Detected {len(scenes)} scenes (adaptive)")
        
        # Show scene transitions
        print("\n📊 Scene Transitions:")
        for i, scene in enumerate(scenes[:5]):
            if i > 0:
                gap = scene.start_time - scenes[i-1].end_time
                print(f"  Gap between scenes {i} and {i+1}: {gap:.3f}s")
        
    except FileNotFoundError:
        print(f"❌ Video not found.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_opencv_detection():
    """Example 4: OpenCV-based scene detection."""
    print("\n" + "="*60)
    print("EXAMPLE 4: OpenCV Scene Detection")
    print("="*60)
    
    detector = SceneDetector()
    
    video_path = "test_video.mp4"
    
    try:
        scenes = detector.detect_scenes_opencv(
            video_path=video_path,
            threshold=30.0,
            method="histogram"
        )
        
        print(f"\n✅ Detected {len(scenes)} scenes (OpenCV)")
        
        for scene in scenes[:5]:
            print(f"  Scene {scene.scene_number}: "
                  f"{scene.start_time:.2f}s - {scene.end_time:.2f}s")
        
    except FileNotFoundError:
        print(f"❌ Video not found.")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("MODULE 6.5: SCENE DETECTION EXAMPLES")
    print("="*60)
    
    try:
        example_content_detection()
        # example_threshold_detection()  # Uncomment to run
        # example_adaptive_detection()   # Uncomment to run
        # example_opencv_detection()     # Uncomment to run
        
        print("\n" + "="*60)
        print("✅ EXAMPLES COMPLETED!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
