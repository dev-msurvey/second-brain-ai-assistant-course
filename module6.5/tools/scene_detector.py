"""
Module 6.5: Scene Detector
===========================

Automatic scene detection using PySceneDetect and OpenCV.

Features:
- Content-based scene detection
- Threshold-based detection
- Adaptive detection
- Shot boundary detection
- Scene statistics and analysis

Author: AI Director Team
License: MIT
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import cv2
from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector, ThresholdDetector, AdaptiveDetector
from scenedetect.stats_manager import StatsManager
from dataclasses import dataclass
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Scene:
    """Represents a detected scene."""
    scene_number: int
    start_frame: int
    end_frame: int
    start_time: float  # seconds
    end_time: float    # seconds
    duration: float    # seconds
    frame_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scene to dictionary."""
        return {
            "scene_number": self.scene_number,
            "start_frame": self.start_frame,
            "end_frame": self.end_frame,
            "start_time": round(self.start_time, 3),
            "end_time": round(self.end_time, 3),
            "duration": round(self.duration, 3),
            "frame_count": self.frame_count
        }


class SceneDetector:
    """
    Detect scenes in video using multiple detection methods.
    
    Methods:
    - Content-based: Detects scene changes based on frame content
    - Threshold-based: Detects fades and cuts based on brightness
    - Adaptive: Combines multiple detection methods
    
    Example:
        >>> detector = SceneDetector()
        >>> scenes = detector.detect_scenes(
        ...     video_path="video.mp4",
        ...     method="content",
        ...     threshold=30.0
        ... )
        >>> print(f"Found {len(scenes)} scenes")
    """
    
    METHODS = ["content", "threshold", "adaptive"]
    
    def __init__(
        self,
        downscale_factor: int = 1,
        min_scene_len: float = 0.5
    ):
        """
        Initialize SceneDetector.
        
        Args:
            downscale_factor: Factor to downscale video for faster processing
            min_scene_len: Minimum scene length in seconds
        """
        self.downscale_factor = downscale_factor
        self.min_scene_len = min_scene_len
        logger.info(f"✅ SceneDetector initialized (downscale={downscale_factor})")
    
    def detect_scenes(
        self,
        video_path: str,
        method: str = "content",
        threshold: float = 30.0,
        save_stats: bool = False,
        stats_file: Optional[str] = None
    ) -> List[Scene]:
        """
        Detect scenes in video.
        
        Args:
            video_path: Path to video file
            method: Detection method ("content", "threshold", "adaptive")
            threshold: Detection sensitivity threshold
            save_stats: Whether to save detection statistics
            stats_file: Path to save stats (CSV format)
            
        Returns:
            List of detected scenes
        """
        logger.info(f"🎬 Detecting scenes: {video_path}")
        logger.info(f"   Method: {method}, Threshold: {threshold}")
        
        # Validate method
        if method not in self.METHODS:
            raise ValueError(f"Invalid method. Choose from: {self.METHODS}")
        
        # Create video manager
        video_manager = VideoManager([video_path])
        stats_manager = StatsManager() if save_stats else None
        scene_manager = SceneManager(stats_manager)
        
        # Add detector based on method
        if method == "content":
            detector = ContentDetector(threshold=threshold)
        elif method == "threshold":
            detector = ThresholdDetector(threshold=threshold, min_scene_len=self.min_scene_len)
        else:  # adaptive
            detector = AdaptiveDetector(adaptive_threshold=threshold)
        
        scene_manager.add_detector(detector)
        
        # Start video manager
        video_manager.set_downscale_factor(self.downscale_factor)
        video_manager.start()
        
        # Detect scenes
        scene_manager.detect_scenes(video=video_manager)
        
        # Get scene list
        scene_list = scene_manager.get_scene_list()
        
        # Get video properties
        fps = video_manager.get_framerate()
        
        # Convert to Scene objects
        scenes = []
        for i, (start_time, end_time) in enumerate(scene_list, start=1):
            start_frame = start_time.get_frames()
            end_frame = end_time.get_frames()
            start_sec = start_time.get_seconds()
            end_sec = end_time.get_seconds()
            
            scene = Scene(
                scene_number=i,
                start_frame=start_frame,
                end_frame=end_frame,
                start_time=start_sec,
                end_time=end_sec,
                duration=end_sec - start_sec,
                frame_count=end_frame - start_frame
            )
            scenes.append(scene)
        
        logger.info(f"✅ Detected {len(scenes)} scenes")
        
        # Save stats if requested
        if save_stats and stats_file and stats_manager:
            stats_manager.save_to_csv(csv_file=stats_file)
            logger.info(f"📊 Stats saved to: {stats_file}")
        
        # Release video manager
        video_manager.release()
        
        return scenes
    
    def detect_scenes_opencv(
        self,
        video_path: str,
        threshold: float = 30.0,
        method: str = "histogram"
    ) -> List[Scene]:
        """
        Detect scenes using OpenCV (alternative method).
        
        Args:
            video_path: Path to video file
            threshold: Detection threshold
            method: Comparison method ("histogram", "mse", "ssim")
            
        Returns:
            List of detected scenes
        """
        logger.info(f"🎬 Detecting scenes (OpenCV): {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        scene_boundaries = [0]  # Start with first frame
        prev_frame = None
        frame_idx = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale for comparison
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            if prev_frame is not None:
                # Calculate difference
                if method == "histogram":
                    diff = self._compare_histograms(prev_frame, gray)
                elif method == "mse":
                    diff = self._calculate_mse(prev_frame, gray)
                else:  # ssim
                    diff = 1.0 - self._calculate_ssim(prev_frame, gray)
                
                # Check if difference exceeds threshold
                if diff > threshold:
                    scene_boundaries.append(frame_idx)
                    logger.debug(f"Scene boundary at frame {frame_idx} (diff={diff:.2f})")
            
            prev_frame = gray
            frame_idx += 1
        
        scene_boundaries.append(total_frames)  # End with last frame
        cap.release()
        
        # Convert boundaries to scenes
        scenes = []
        for i in range(len(scene_boundaries) - 1):
            start_frame = scene_boundaries[i]
            end_frame = scene_boundaries[i + 1]
            start_time = start_frame / fps
            end_time = end_frame / fps
            
            scene = Scene(
                scene_number=i + 1,
                start_frame=start_frame,
                end_frame=end_frame,
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                frame_count=end_frame - start_frame
            )
            scenes.append(scene)
        
        logger.info(f"✅ Detected {len(scenes)} scenes")
        return scenes
    
    def _compare_histograms(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Compare two images using histogram correlation."""
        hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
        
        # Normalize histograms
        cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        
        # Calculate correlation (higher = more similar)
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        
        # Return inverse (higher = more different)
        return 1.0 - correlation
    
    def _calculate_mse(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate Mean Squared Error between two images."""
        err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        err /= float(img1.shape[0] * img1.shape[1])
        return err / 1000.0  # Normalize
    
    def _calculate_ssim(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """Calculate Structural Similarity Index (simplified version)."""
        # Simple SSIM approximation
        mean1 = np.mean(img1)
        mean2 = np.mean(img2)
        std1 = np.std(img1)
        std2 = np.std(img2)
        
        cov = np.mean((img1 - mean1) * (img2 - mean2))
        
        c1 = (0.01 * 255) ** 2
        c2 = (0.03 * 255) ** 2
        
        numerator = (2 * mean1 * mean2 + c1) * (2 * cov + c2)
        denominator = (mean1 ** 2 + mean2 ** 2 + c1) * (std1 ** 2 + std2 ** 2 + c2)
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def get_scene_statistics(self, scenes: List[Scene]) -> Dict[str, Any]:
        """
        Calculate statistics for detected scenes.
        
        Args:
            scenes: List of scenes
            
        Returns:
            Dictionary of statistics
        """
        if not scenes:
            return {}
        
        durations = [s.duration for s in scenes]
        frame_counts = [s.frame_count for s in scenes]
        
        stats = {
            "total_scenes": len(scenes),
            "total_duration": sum(durations),
            "avg_scene_duration": np.mean(durations),
            "median_scene_duration": np.median(durations),
            "min_scene_duration": min(durations),
            "max_scene_duration": max(durations),
            "std_scene_duration": np.std(durations),
            "avg_frames_per_scene": np.mean(frame_counts),
            "total_frames": sum(frame_counts)
        }
        
        return stats


# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = SceneDetector(downscale_factor=2)
    
    # Detect scenes
    video_path = "test_video.mp4"
    
    try:
        # Method 1: Content-based detection
        print("\n🎬 Method 1: Content-based detection")
        scenes = detector.detect_scenes(
            video_path=video_path,
            method="content",
            threshold=30.0
        )
        
        # Print results
        print(f"\n📊 Found {len(scenes)} scenes:")
        for scene in scenes[:5]:  # Show first 5
            print(f"  Scene {scene.scene_number}: "
                  f"{scene.start_time:.2f}s - {scene.end_time:.2f}s "
                  f"({scene.duration:.2f}s)")
        
        # Get statistics
        stats = detector.get_scene_statistics(scenes)
        print(f"\n📈 Statistics:")
        print(f"  Average scene duration: {stats['avg_scene_duration']:.2f}s")
        print(f"  Total duration: {stats['total_duration']:.2f}s")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
