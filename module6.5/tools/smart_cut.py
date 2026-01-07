"""
Module 6.5: Smart Cut - Intelligent Video Editing
=================================================

Main Smart Cut tool that combines scene detection, auto-editing,
and intelligent cutting decisions.

Features:
- Automatic scene detection
- Silence removal
- Smart trimming
- B-roll insertion (placeholder)
- Pacing optimization
- Beat-sync editing

Author: AI Director Team
License: MIT
"""

import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip
from dataclasses import dataclass, asdict
import json

from .scene_detector import SceneDetector, Scene
from .auto_editor import AutoEditor, EditDecision

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SmartCutConfig:
    """Configuration for Smart Cut."""
    # Scene detection
    scene_detection_method: str = "content"
    scene_threshold: float = 30.0
    min_scene_length: float = 0.5
    
    # Audio analysis
    silence_threshold: float = -40.0
    min_silence_duration: float = 0.5
    min_clip_duration: float = 0.3
    
    # Editing
    remove_silence: bool = True
    auto_trim: bool = False
    target_duration: Optional[float] = None
    trim_strategy: str = "smart"
    
    # Output
    output_fps: int = 30
    output_codec: str = "libx264"
    output_quality: str = "medium"


class SmartCut:
    """
    Smart Cut: Intelligent video editing system.
    
    Combines multiple AI-powered tools to automatically edit videos:
    - Scene detection
    - Silence removal
    - Smart trimming
    - Pacing optimization
    
    Example:
        >>> smart_cut = SmartCut()
        >>> result = smart_cut.process_video(
        ...     input_path="raw_video.mp4",
        ...     output_path="edited_video.mp4",
        ...     remove_silence=True,
        ...     target_duration=60.0
        ... )
    """
    
    def __init__(self, config: Optional[SmartCutConfig] = None):
        """
        Initialize Smart Cut.
        
        Args:
            config: Optional configuration object
        """
        self.config = config or SmartCutConfig()
        
        # Initialize components
        self.scene_detector = SceneDetector(
            downscale_factor=2,
            min_scene_len=self.config.min_scene_length
        )
        
        self.auto_editor = AutoEditor(
            silence_threshold=self.config.silence_threshold,
            min_silence_duration=self.config.min_silence_duration,
            min_clip_duration=self.config.min_clip_duration
        )
        
        logger.info("✅ SmartCut initialized")
    
    def analyze_video(
        self,
        video_path: str,
        detect_scenes: bool = True,
        detect_silence: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze video and return metadata.
        
        Args:
            video_path: Path to video file
            detect_scenes: Whether to detect scenes
            detect_silence: Whether to detect silent segments
            
        Returns:
            Dictionary containing analysis results
        """
        logger.info(f"🔍 Analyzing video: {video_path}")
        
        # Get video properties
        video = VideoFileClip(video_path)
        analysis = {
            "duration": video.duration,
            "fps": video.fps,
            "size": video.size,
            "has_audio": video.audio is not None
        }
        video.close()
        
        # Detect scenes
        if detect_scenes:
            scenes = self.scene_detector.detect_scenes(
                video_path=video_path,
                method=self.config.scene_detection_method,
                threshold=self.config.scene_threshold
            )
            
            analysis["scenes"] = [scene.to_dict() for scene in scenes]
            analysis["scene_count"] = len(scenes)
            analysis["scene_stats"] = self.scene_detector.get_scene_statistics(scenes)
        
        # Detect silence
        if detect_silence and analysis["has_audio"]:
            # Extract audio temporarily
            video = VideoFileClip(video_path)
            temp_audio = "temp_audio_analysis.wav"
            video.audio.write_audiofile(temp_audio, verbose=False, logger=None)
            video.close()
            
            silent_segments = self.auto_editor.detect_silence(temp_audio)
            analysis["silent_segments"] = [
                {"start": start, "end": end, "duration": end - start}
                for start, end in silent_segments
            ]
            analysis["silence_count"] = len(silent_segments)
            analysis["total_silence_duration"] = sum(
                seg["duration"] for seg in analysis["silent_segments"]
            )
            
            Path(temp_audio).unlink(missing_ok=True)
        
        logger.info(f"✅ Analysis complete")
        return analysis
    
    def process_video(
        self,
        input_path: str,
        output_path: str,
        remove_silence: Optional[bool] = None,
        target_duration: Optional[float] = None,
        save_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Process video with Smart Cut.
        
        Args:
            input_path: Path to input video
            output_path: Path to output video
            remove_silence: Override config setting
            target_duration: Override config setting
            save_analysis: Whether to save analysis JSON
            
        Returns:
            Dictionary containing processing results
        """
        logger.info(f"🎬 Smart Cut processing: {input_path}")
        logger.info(f"   Output: {output_path}")
        
        # Use config defaults if not specified
        remove_silence = remove_silence if remove_silence is not None else self.config.remove_silence
        target_duration = target_duration or self.config.target_duration
        
        # Step 1: Analyze video
        logger.info("\n📊 Step 1: Analyzing video...")
        analysis = self.analyze_video(
            video_path=input_path,
            detect_scenes=True,
            detect_silence=remove_silence
        )
        
        # Save analysis if requested
        if save_analysis:
            analysis_path = Path(output_path).with_suffix(".json")
            with open(analysis_path, "w") as f:
                json.dump(analysis, f, indent=2)
            logger.info(f"📄 Analysis saved: {analysis_path}")
        
        # Step 2: Detect scenes
        logger.info("\n🎬 Step 2: Detecting scenes...")
        scenes = self.scene_detector.detect_scenes(
            video_path=input_path,
            method=self.config.scene_detection_method,
            threshold=self.config.scene_threshold
        )
        
        # Step 3: Auto-edit
        logger.info("\n✂️  Step 3: Auto-editing...")
        edited_path = self.auto_editor.auto_edit(
            video_path=input_path,
            output_path=output_path,
            remove_silence=remove_silence,
            target_duration=target_duration,
            scenes=scenes
        )
        
        # Get final video properties
        final_video = VideoFileClip(edited_path)
        final_duration = final_video.duration
        final_video.close()
        
        # Calculate savings
        time_saved = analysis["duration"] - final_duration
        percent_saved = (time_saved / analysis["duration"]) * 100 if analysis["duration"] > 0 else 0
        
        # Prepare result
        result = {
            "input_path": input_path,
            "output_path": output_path,
            "original_duration": analysis["duration"],
            "edited_duration": final_duration,
            "time_saved": time_saved,
            "percent_saved": percent_saved,
            "scenes_detected": len(scenes),
            "analysis": analysis
        }
        
        logger.info(f"\n✅ Smart Cut complete!")
        logger.info(f"   Original: {analysis['duration']:.2f}s")
        logger.info(f"   Edited: {final_duration:.2f}s")
        logger.info(f"   Saved: {time_saved:.2f}s ({percent_saved:.1f}%)")
        
        return result
    
    def batch_process(
        self,
        input_files: List[str],
        output_dir: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Process multiple videos in batch.
        
        Args:
            input_files: List of input video paths
            output_dir: Output directory
            **kwargs: Additional arguments for process_video
            
        Returns:
            List of processing results
        """
        logger.info(f"🎬 Batch processing {len(input_files)} videos")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        for i, input_file in enumerate(input_files, start=1):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing {i}/{len(input_files)}: {input_file}")
            logger.info(f"{'='*60}")
            
            try:
                # Generate output filename
                input_path = Path(input_file)
                output_file = output_path / f"{input_path.stem}_smartcut{input_path.suffix}"
                
                # Process video
                result = self.process_video(
                    input_path=input_file,
                    output_path=str(output_file),
                    **kwargs
                )
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"❌ Failed to process {input_file}: {str(e)}")
                results.append({
                    "input_path": input_file,
                    "error": str(e),
                    "success": False
                })
        
        # Summary
        successful = len([r for r in results if "error" not in r])
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Batch processing complete: {successful}/{len(input_files)} successful")
        logger.info(f"{'='*60}")
        
        return results
    
    def create_highlights(
        self,
        video_path: str,
        output_path: str,
        duration: float = 30.0,
        num_clips: int = 3
    ) -> str:
        """
        Create highlights reel from video.
        
        Args:
            video_path: Path to input video
            output_path: Path to output highlights video
            duration: Total duration of highlights
            num_clips: Number of clips to include
            
        Returns:
            Path to highlights video
        """
        logger.info(f"✨ Creating highlights ({duration}s, {num_clips} clips)")
        
        # Detect scenes
        scenes = self.scene_detector.detect_scenes(
            video_path=video_path,
            method=self.config.scene_detection_method,
            threshold=self.config.scene_threshold
        )
        
        # Select best scenes (by duration for now)
        # TODO: Use more sophisticated scoring (motion, audio, etc.)
        scenes_sorted = sorted(scenes, key=lambda s: s.duration, reverse=True)
        selected_scenes = scenes_sorted[:num_clips]
        selected_scenes.sort(key=lambda s: s.start_time)
        
        # Calculate duration per clip
        clip_duration = duration / num_clips
        
        # Create clips
        video = VideoFileClip(video_path)
        clips = []
        
        for scene in selected_scenes:
            # Take clip from middle of scene
            scene_center = scene.start_time + (scene.duration / 2)
            clip_start = max(scene.start_time, scene_center - clip_duration / 2)
            clip_end = min(scene.end_time, clip_start + clip_duration)
            
            clip = video.subclip(clip_start, clip_end)
            clips.append(clip)
        
        # Concatenate clips
        highlights = concatenate_videoclips(clips, method="compose")
        
        # Export
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        highlights.write_videofile(
            output_path,
            codec=self.config.output_codec,
            preset=self.config.output_quality,
            verbose=False,
            logger=None
        )
        
        highlights.close()
        video.close()
        
        logger.info(f"✅ Highlights created: {output_path}")
        return output_path


# Example usage
if __name__ == "__main__":
    # Initialize Smart Cut
    config = SmartCutConfig(
        remove_silence=True,
        target_duration=60.0,
        scene_threshold=30.0
    )
    
    smart_cut = SmartCut(config=config)
    
    # Process video
    video_path = "test_video.mp4"
    output_path = "edited_video.mp4"
    
    try:
        result = smart_cut.process_video(
            input_path=video_path,
            output_path=output_path
        )
        
        print(f"\n✅ Processing complete!")
        print(f"   Time saved: {result['time_saved']:.2f}s ({result['percent_saved']:.1f}%)")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
