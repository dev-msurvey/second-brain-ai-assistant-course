"""
Example: Smart Cut Complete Workflow
====================================

Demonstrates complete Smart Cut workflow from analysis to editing.

Usage:
    python examples/example_smart_cut.py
"""

import sys
from pathlib import Path
import json

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.smart_cut import SmartCut, SmartCutConfig


def example_analyze_video():
    """Example 1: Analyze video without editing."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Video Analysis")
    print("="*60)
    
    smart_cut = SmartCut()
    
    video_path = "test_video.mp4"
    
    try:
        analysis = smart_cut.analyze_video(
            video_path=video_path,
            detect_scenes=True,
            detect_silence=True
        )
        
        print(f"\n📊 Video Analysis:")
        print(f"  Duration: {analysis['duration']:.2f}s")
        print(f"  FPS: {analysis['fps']}")
        print(f"  Resolution: {analysis['size']}")
        print(f"  Has audio: {analysis['has_audio']}")
        print(f"  Scenes: {analysis.get('scene_count', 0)}")
        
        if 'silent_segments' in analysis:
            print(f"  Silent segments: {analysis['silence_count']}")
            print(f"  Total silence: {analysis['total_silence_duration']:.2f}s")
        
    except FileNotFoundError:
        print(f"❌ Video not found: {video_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_remove_silence():
    """Example 2: Remove silence only."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Remove Silence")
    print("="*60)
    
    config = SmartCutConfig(
        remove_silence=True,
        target_duration=None  # Don't trim
    )
    
    smart_cut = SmartCut(config=config)
    
    try:
        result = smart_cut.process_video(
            input_path="test_video.mp4",
            output_path="output/no_silence.mp4"
        )
        
        print(f"\n✅ Silence removed!")
        print(f"  Original: {result['original_duration']:.2f}s")
        print(f"  Edited: {result['edited_duration']:.2f}s")
        print(f"  Saved: {result['time_saved']:.2f}s "
              f"({result['percent_saved']:.1f}%)")
        
    except FileNotFoundError:
        print("❌ Video not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_trim_to_duration():
    """Example 3: Trim to target duration."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Trim to Duration")
    print("="*60)
    
    config = SmartCutConfig(
        remove_silence=False,
        target_duration=60.0  # 1 minute
    )
    
    smart_cut = SmartCut(config=config)
    
    try:
        result = smart_cut.process_video(
            input_path="test_video.mp4",
            output_path="output/trimmed_60s.mp4"
        )
        
        print(f"\n✅ Video trimmed!")
        print(f"  Target: 60.0s")
        print(f"  Result: {result['edited_duration']:.2f}s")
        print(f"  Scenes used: {result['scenes_detected']}")
        
    except FileNotFoundError:
        print("❌ Video not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_complete_smart_cut():
    """Example 4: Complete Smart Cut (silence + trim)."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Complete Smart Cut")
    print("="*60)
    
    config = SmartCutConfig(
        remove_silence=True,
        target_duration=45.0,  # 45 seconds
        scene_threshold=30.0,
        silence_threshold=-40.0
    )
    
    smart_cut = SmartCut(config=config)
    
    try:
        result = smart_cut.process_video(
            input_path="test_video.mp4",
            output_path="output/smart_cut_45s.mp4",
            save_analysis=True  # Save JSON analysis
        )
        
        print(f"\n✅ Smart Cut complete!")
        print(f"  Original: {result['original_duration']:.2f}s")
        print(f"  Edited: {result['edited_duration']:.2f}s")
        print(f"  Target: 45.0s")
        print(f"  Time saved: {result['time_saved']:.2f}s")
        print(f"  Efficiency: {result['percent_saved']:.1f}%")
        print(f"  Scenes: {result['scenes_detected']}")
        print(f"\n📄 Analysis saved: output/smart_cut_45s.json")
        
    except FileNotFoundError:
        print("❌ Video not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_create_highlights():
    """Example 5: Create highlight reel."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Create Highlights")
    print("="*60)
    
    smart_cut = SmartCut()
    
    try:
        highlights = smart_cut.create_highlights(
            video_path="test_video.mp4",
            output_path="output/highlights_30s.mp4",
            duration=30.0,  # 30 second highlight
            num_clips=3     # Best 3 clips
        )
        
        print(f"\n✅ Highlights created!")
        print(f"  Duration: 30s")
        print(f"  Clips: 3")
        print(f"  Output: {highlights}")
        
    except FileNotFoundError:
        print("❌ Video not found")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_batch_processing():
    """Example 6: Batch process multiple videos."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Batch Processing")
    print("="*60)
    
    smart_cut = SmartCut()
    
    input_files = [
        "video1.mp4",
        "video2.mp4",
        "video3.mp4"
    ]
    
    try:
        results = smart_cut.batch_process(
            input_files=input_files,
            output_dir="output/batch/",
            remove_silence=True,
            target_duration=60.0
        )
        
        print(f"\n✅ Batch processing complete!")
        print(f"  Processed: {len(results)} videos")
        
        for i, result in enumerate(results, start=1):
            if 'error' not in result:
                print(f"\n  Video {i}:")
                print(f"    Saved: {result['time_saved']:.2f}s")
            else:
                print(f"\n  Video {i}: ❌ {result['error']}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Run all examples."""
    # Create output directory
    Path("output").mkdir(exist_ok=True)
    Path("output/batch").mkdir(exist_ok=True)
    
    print("\n" + "="*60)
    print("MODULE 6.5: SMART CUT EXAMPLES")
    print("="*60)
    
    try:
        example_analyze_video()
        # example_remove_silence()        # Uncomment to run
        # example_trim_to_duration()      # Uncomment to run
        # example_complete_smart_cut()    # Uncomment to run
        # example_create_highlights()     # Uncomment to run
        # example_batch_processing()      # Uncomment to run
        
        print("\n" + "="*60)
        print("✅ EXAMPLES COMPLETED!")
        print("="*60)
        print("\nNote: Some examples require a test video file.")
        print("Replace 'test_video.mp4' with your own video.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
