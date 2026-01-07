"""
Module 6.5: Auto Editor
=======================

Automatic video editing based on detected scenes and audio analysis.

Features:
- Remove silence/pauses
- Cut dead space
- Auto-trim scenes
- Beat-sync editing
- Pacing optimization

Author: AI Director Team
License: MIT
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.all import speedx
import librosa
from dataclasses import dataclass

from .scene_detector import Scene

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class EditDecision:
    """Represents an editing decision."""
    action: str  # "keep", "cut", "trim", "speed"
    start_time: float
    end_time: float
    speed_factor: float = 1.0
    reason: str = ""


class AutoEditor:
    """
    Automatically edit videos based on content analysis.
    
    Features:
    - Remove silences and pauses
    - Cut dead space
    - Optimize pacing
    - Beat-sync editing
    - Scene trimming
    
    Example:
        >>> editor = AutoEditor()
        >>> edited_video = editor.auto_edit(
        ...     video_path="raw_video.mp4",
        ...     remove_silence=True,
        ...     target_duration=60.0
        ... )
    """
    
    def __init__(
        self,
        silence_threshold: float = -40.0,  # dB
        min_silence_duration: float = 0.5,  # seconds
        min_clip_duration: float = 0.3      # seconds
    ):
        """
        Initialize AutoEditor.
        
        Args:
            silence_threshold: Audio threshold in dB for silence detection
            min_silence_duration: Minimum silence duration to remove
            min_clip_duration: Minimum clip length to keep
        """
        self.silence_threshold = silence_threshold
        self.min_silence_duration = min_silence_duration
        self.min_clip_duration = min_clip_duration
        logger.info("✅ AutoEditor initialized")
    
    def detect_silence(
        self,
        audio_path: str,
        threshold: Optional[float] = None
    ) -> List[Tuple[float, float]]:
        """
        Detect silent segments in audio.
        
        Args:
            audio_path: Path to audio file
            threshold: Silence threshold in dB (uses default if None)
            
        Returns:
            List of (start_time, end_time) tuples for silent segments
        """
        threshold = threshold or self.silence_threshold
        
        logger.info(f"🔇 Detecting silence: {audio_path}")
        
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate RMS energy
        hop_length = 512
        frame_length = 2048
        rms = librosa.feature.rms(
            y=y,
            frame_length=frame_length,
            hop_length=hop_length
        )[0]
        
        # Convert to dB
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        
        # Find silent frames
        silent_frames = rms_db < threshold
        
        # Convert frames to time
        times = librosa.frames_to_time(
            np.arange(len(rms_db)),
            sr=sr,
            hop_length=hop_length
        )
        
        # Find continuous silent segments
        silent_segments = []
        in_silence = False
        silence_start = 0.0
        
        for i, (is_silent, time) in enumerate(zip(silent_frames, times)):
            if is_silent and not in_silence:
                # Start of silence
                silence_start = time
                in_silence = True
            elif not is_silent and in_silence:
                # End of silence
                silence_end = time
                duration = silence_end - silence_start
                
                # Only keep if longer than minimum
                if duration >= self.min_silence_duration:
                    silent_segments.append((silence_start, silence_end))
                
                in_silence = False
        
        # Handle case where audio ends in silence
        if in_silence:
            duration = times[-1] - silence_start
            if duration >= self.min_silence_duration:
                silent_segments.append((silence_start, times[-1]))
        
        logger.info(f"✅ Found {len(silent_segments)} silent segments")
        return silent_segments
    
    def remove_silence(
        self,
        video_path: str,
        output_path: str,
        padding: float = 0.1
    ) -> str:
        """
        Remove silent segments from video.
        
        Args:
            video_path: Path to input video
            output_path: Path to output video
            padding: Seconds to keep before/after speech
            
        Returns:
            Path to edited video
        """
        logger.info(f"✂️  Removing silence from: {video_path}")
        
        # Load video
        video = VideoFileClip(video_path)
        
        # Extract audio temporarily
        temp_audio = "temp_audio.wav"
        video.audio.write_audiofile(temp_audio, verbose=False, logger=None)
        
        # Detect silence
        silent_segments = self.detect_silence(temp_audio)
        
        # Create list of clips to keep (non-silent parts)
        clips = []
        current_time = 0.0
        
        for silence_start, silence_end in silent_segments:
            # Add clip before silence (with padding)
            clip_start = current_time
            clip_end = max(current_time, silence_start - padding)
            
            if clip_end - clip_start >= self.min_clip_duration:
                clips.append(video.subclip(clip_start, clip_end))
            
            current_time = silence_end + padding
        
        # Add final clip after last silence
        if current_time < video.duration:
            clips.append(video.subclip(current_time, video.duration))
        
        # Concatenate clips
        if clips:
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Export
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            final_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )
            
            logger.info(f"✅ Edited video saved: {output_path}")
            logger.info(f"   Original: {video.duration:.2f}s → Edited: {final_video.duration:.2f}s")
            
            # Cleanup
            final_video.close()
        else:
            logger.warning("⚠️  No clips to keep!")
        
        video.close()
        Path(temp_audio).unlink(missing_ok=True)
        
        return output_path
    
    def trim_to_duration(
        self,
        video_path: str,
        target_duration: float,
        scenes: Optional[List[Scene]] = None,
        strategy: str = "smart"
    ) -> List[EditDecision]:
        """
        Create edit decisions to trim video to target duration.
        
        Args:
            video_path: Path to video file
            target_duration: Target duration in seconds
            scenes: Optional list of scenes for smart editing
            strategy: Trimming strategy ("smart", "end", "proportional")
            
        Returns:
            List of edit decisions
        """
        logger.info(f"✂️  Planning trim to {target_duration}s using '{strategy}' strategy")
        
        video = VideoFileClip(video_path)
        current_duration = video.duration
        video.close()
        
        if current_duration <= target_duration:
            logger.info("✅ Video already within target duration")
            return [EditDecision(
                action="keep",
                start_time=0.0,
                end_time=current_duration,
                reason="Already within target"
            )]
        
        time_to_cut = current_duration - target_duration
        logger.info(f"   Need to cut {time_to_cut:.2f}s")
        
        decisions = []
        
        if strategy == "end":
            # Simple: cut from end
            decisions.append(EditDecision(
                action="keep",
                start_time=0.0,
                end_time=target_duration,
                reason="Keep from start to target"
            ))
        
        elif strategy == "proportional" and scenes:
            # Cut proportionally from each scene
            cut_per_scene = time_to_cut / len(scenes)
            
            for scene in scenes:
                new_duration = max(
                    self.min_clip_duration,
                    scene.duration - cut_per_scene
                )
                
                decisions.append(EditDecision(
                    action="trim",
                    start_time=scene.start_time,
                    end_time=scene.start_time + new_duration,
                    reason=f"Proportional trim ({cut_per_scene:.2f}s)"
                ))
        
        elif strategy == "smart" and scenes:
            # Smart: keep important scenes, cut less important ones
            # Score scenes by duration (longer = more important for now)
            scene_scores = [(s, s.duration) for s in scenes]
            scene_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Keep scenes until we reach target
            kept_duration = 0.0
            for scene, score in scene_scores:
                if kept_duration + scene.duration <= target_duration:
                    decisions.append(EditDecision(
                        action="keep",
                        start_time=scene.start_time,
                        end_time=scene.end_time,
                        reason=f"High importance (score={score:.2f})"
                    ))
                    kept_duration += scene.duration
                else:
                    remaining = target_duration - kept_duration
                    if remaining >= self.min_clip_duration:
                        decisions.append(EditDecision(
                            action="trim",
                            start_time=scene.start_time,
                            end_time=scene.start_time + remaining,
                            reason="Partial keep to reach target"
                        ))
                    break
            
            # Sort decisions by time
            decisions.sort(key=lambda d: d.start_time)
        
        else:
            # Fallback: simple end cut
            decisions.append(EditDecision(
                action="keep",
                start_time=0.0,
                end_time=target_duration,
                reason="Fallback: simple cut"
            ))
        
        logger.info(f"✅ Created {len(decisions)} edit decisions")
        return decisions
    
    def apply_edit_decisions(
        self,
        video_path: str,
        decisions: List[EditDecision],
        output_path: str
    ) -> str:
        """
        Apply edit decisions to video.
        
        Args:
            video_path: Path to input video
            decisions: List of edit decisions
            output_path: Path to output video
            
        Returns:
            Path to edited video
        """
        logger.info(f"✂️  Applying {len(decisions)} edit decisions")
        
        video = VideoFileClip(video_path)
        clips = []
        
        for decision in decisions:
            if decision.action in ["keep", "trim"]:
                clip = video.subclip(decision.start_time, decision.end_time)
                
                # Apply speed if specified
                if decision.speed_factor != 1.0:
                    clip = clip.fx(speedx, decision.speed_factor)
                
                clips.append(clip)
        
        if clips:
            # Concatenate all clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Export
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            final_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )
            
            logger.info(f"✅ Edited video saved: {output_path}")
            logger.info(f"   Duration: {final_video.duration:.2f}s")
            
            final_video.close()
        
        video.close()
        return output_path
    
    def auto_edit(
        self,
        video_path: str,
        output_path: str,
        remove_silence: bool = True,
        target_duration: Optional[float] = None,
        scenes: Optional[List[Scene]] = None
    ) -> str:
        """
        Automatically edit video with all available optimizations.
        
        Args:
            video_path: Path to input video
            output_path: Path to output video
            remove_silence: Whether to remove silent segments
            target_duration: Optional target duration
            scenes: Optional pre-detected scenes
            
        Returns:
            Path to edited video
        """
        logger.info(f"🎬 Auto-editing: {video_path}")
        
        temp_file = "temp_edit.mp4"
        current_file = video_path
        
        # Step 1: Remove silence if requested
        if remove_silence:
            logger.info("Step 1: Removing silence...")
            current_file = self.remove_silence(
                video_path=current_file,
                output_path=temp_file
            )
        
        # Step 2: Trim to target duration if specified
        if target_duration:
            logger.info(f"Step 2: Trimming to {target_duration}s...")
            decisions = self.trim_to_duration(
                video_path=current_file,
                target_duration=target_duration,
                scenes=scenes,
                strategy="smart" if scenes else "end"
            )
            
            current_file = self.apply_edit_decisions(
                video_path=current_file,
                decisions=decisions,
                output_path=output_path
            )
        else:
            # No trimming needed, just rename temp file
            if remove_silence:
                Path(temp_file).rename(output_path)
                current_file = output_path
        
        # Cleanup
        if Path(temp_file).exists() and temp_file != current_file:
            Path(temp_file).unlink()
        
        logger.info(f"✅ Auto-edit complete: {output_path}")
        return output_path


# Example usage
if __name__ == "__main__":
    editor = AutoEditor()
    
    # Example: Remove silence
    video_path = "test_video.mp4"
    output_path = "edited_video.mp4"
    
    try:
        edited = editor.auto_edit(
            video_path=video_path,
            output_path=output_path,
            remove_silence=True,
            target_duration=60.0
        )
        print(f"✅ Edited video: {edited}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
