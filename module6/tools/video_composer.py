"""
Module 6: Video Composer - MoviePy Integration
==============================================

Compose videos from images, audio, and effects using MoviePy.

Features:
- Combine images and audio
- Add text overlays
- Transitions (fade, dissolve, crossfade)
- Effects (zoom, pan, filters)
- Timeline management
- Multiple export formats
- Background music

Author: AI Director Team
License: MIT
"""

import logging
from typing import Optional, List, Dict, Any, Tuple, Union
from pathlib import Path
import numpy as np

from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
    TextClip,
    ColorClip
)
from moviepy.video.fx.all import (
    fadein,
    fadeout,
    resize,
    crop
)
from moviepy.audio.fx.all import (
    audio_fadein,
    audio_fadeout,
    volumex
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VideoComposer:
    """
    Compose videos from images, audio, and effects.
    
    Example:
        >>> composer = VideoComposer()
        >>> video = composer.compose(
        ...     images=["img1.png", "img2.png"],
        ...     audio="voiceover.mp3",
        ...     duration=15,
        ...     transitions=["fade"]
        ... )
        >>> video.write_videofile("output.mp4", fps=30)
    """
    
    TRANSITIONS = ["fade", "dissolve", "crossfade", "cut"]
    EFFECTS = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
    
    def __init__(
        self,
        default_fps: int = 30,
        default_resolution: Tuple[int, int] = (1920, 1080)
    ):
        """
        Initialize VideoComposer.
        
        Args:
            default_fps: Default frames per second
            default_resolution: Default video resolution (width, height)
        """
        self.default_fps = default_fps
        self.default_resolution = default_resolution
        logger.info(f"✅ VideoComposer initialized (FPS={default_fps}, Resolution={default_resolution})")
    
    def compose(
        self,
        images: List[str],
        audio: Optional[str] = None,
        duration: float = 5.0,
        transitions: Optional[List[str]] = None,
        text_overlays: Optional[List[Dict[str, Any]]] = None,
        effects: Optional[List[str]] = None,
        background_music: Optional[str] = None,
        background_music_volume: float = 0.3
    ) -> CompositeVideoClip:
        """
        Compose video from images and audio.
        
        Args:
            images: List of image file paths
            audio: Audio file path (voiceover)
            duration: Duration per image in seconds
            transitions: List of transitions between images
            text_overlays: List of text overlay configs
            effects: List of effects to apply
            background_music: Background music file path
            background_music_volume: Background music volume (0.0-1.0)
            
        Returns:
            CompositeVideoClip ready for export
        """
        logger.info(f"🎬 Composing video with {len(images)} images")
        
        # Create clips from images
        clips = []
        for i, image_path in enumerate(images):
            # Create image clip
            clip = ImageClip(image_path, duration=duration)
            
            # Resize to target resolution
            clip = clip.resize(self.default_resolution)
            
            # Apply effects
            if effects:
                effect = effects[i % len(effects)]
                clip = self._apply_effect(clip, effect)
            
            clips.append(clip)
        
        # Apply transitions
        if transitions:
            clips = self._apply_transitions(clips, transitions)
        
        # Concatenate clips
        video = concatenate_videoclips(clips, method="compose")
        
        # Add audio
        if audio:
            audio_clip = AudioFileClip(audio)
            video = video.set_audio(audio_clip)
            logger.info(f"🎵 Audio added: {audio}")
        
        # Add background music
        if background_music:
            bg_music = AudioFileClip(background_music)
            bg_music = bg_music.fx(volumex, background_music_volume)
            
            # Loop background music to match video duration
            if bg_music.duration < video.duration:
                loops = int(np.ceil(video.duration / bg_music.duration))
                bg_music = concatenate_videoclips([bg_music] * loops)
            
            bg_music = bg_music.set_duration(video.duration)
            
            # Mix with voiceover
            if video.audio:
                from moviepy.audio.AudioClip import CompositeAudioClip
                video = video.set_audio(CompositeAudioClip([video.audio, bg_music]))
            else:
                video = video.set_audio(bg_music)
            
            logger.info(f"🎵 Background music added: {background_music}")
        
        # Add text overlays
        if text_overlays:
            video = self._add_text_overlays(video, text_overlays)
        
        logger.info(f"✅ Video composed: {video.duration:.2f}s")
        return video
    
    def _apply_effect(self, clip: ImageClip, effect: str) -> ImageClip:
        """Apply effect to a clip."""
        if effect == "zoom_in":
            # Zoom in effect
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                zoom = 1 + (t / clip.duration) * 0.2  # 20% zoom
                h, w = frame.shape[:2]
                new_h, new_w = int(h / zoom), int(w / zoom)
                top, left = (h - new_h) // 2, (w - new_w) // 2
                cropped = frame[top:top+new_h, left:left+new_w]
                return np.array(Image.fromarray(cropped).resize((w, h)))
            
            clip = clip.fl(zoom_effect)
        
        elif effect == "zoom_out":
            # Zoom out effect
            def zoom_effect(get_frame, t):
                frame = get_frame(t)
                zoom = 1.2 - (t / clip.duration) * 0.2  # Start at 120%, zoom out to 100%
                h, w = frame.shape[:2]
                new_h, new_w = int(h / zoom), int(w / zoom)
                top, left = (h - new_h) // 2, (w - new_w) // 2
                cropped = frame[top:top+new_h, left:left+new_w]
                return np.array(Image.fromarray(cropped).resize((w, h)))
            
            clip = clip.fl(zoom_effect)
        
        elif effect == "pan_left":
            # Pan left effect
            def pan_effect(get_frame, t):
                frame = get_frame(t)
                h, w = frame.shape[:2]
                shift = int((t / clip.duration) * w * 0.1)  # Pan 10% of width
                return np.roll(frame, -shift, axis=1)
            
            clip = clip.fl(pan_effect)
        
        elif effect == "pan_right":
            # Pan right effect
            def pan_effect(get_frame, t):
                frame = get_frame(t)
                h, w = frame.shape[:2]
                shift = int((t / clip.duration) * w * 0.1)  # Pan 10% of width
                return np.roll(frame, shift, axis=1)
            
            clip = clip.fl(pan_effect)
        
        return clip
    
    def _apply_transitions(
        self,
        clips: List[ImageClip],
        transitions: List[str]
    ) -> List[ImageClip]:
        """Apply transitions between clips."""
        if len(clips) <= 1:
            return clips
        
        transition_duration = 0.5  # 0.5 seconds
        
        for i in range(len(clips)):
            # Fade in first clip
            if i == 0:
                clips[i] = clips[i].fx(fadein, transition_duration)
            
            # Fade out last clip
            if i == len(clips) - 1:
                clips[i] = clips[i].fx(fadeout, transition_duration)
            
            # Apply transition between clips
            if i > 0 and transitions:
                transition = transitions[(i-1) % len(transitions)]
                
                if transition == "fade":
                    clips[i] = clips[i].fx(fadein, transition_duration)
                    clips[i-1] = clips[i-1].fx(fadeout, transition_duration)
                
                elif transition == "crossfade":
                    # Overlap clips with crossfade
                    clips[i] = clips[i].set_start(clips[i-1].end - transition_duration)
                    clips[i] = clips[i].fx(fadein, transition_duration)
                    clips[i-1] = clips[i-1].fx(fadeout, transition_duration)
        
        return clips
    
    def _add_text_overlays(
        self,
        video: CompositeVideoClip,
        text_overlays: List[Dict[str, Any]]
    ) -> CompositeVideoClip:
        """Add text overlays to video."""
        text_clips = []
        
        for overlay in text_overlays:
            text = overlay.get("text", "")
            position = overlay.get("position", "center")
            duration = overlay.get("duration", 3.0)
            start_time = overlay.get("start_time", 0.0)
            font_size = overlay.get("font_size", 70)
            color = overlay.get("color", "white")
            font = overlay.get("font", "Arial")
            
            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=font_size,
                color=color,
                font=font,
                method='caption',
                size=(self.default_resolution[0] * 0.8, None)
            )
            
            # Set position
            if position == "center":
                txt_clip = txt_clip.set_position("center")
            elif position == "top":
                txt_clip = txt_clip.set_position(("center", 100))
            elif position == "bottom":
                txt_clip = txt_clip.set_position(("center", self.default_resolution[1] - 200))
            else:
                txt_clip = txt_clip.set_position(position)
            
            # Set timing
            txt_clip = txt_clip.set_start(start_time).set_duration(duration)
            
            # Add fade in/out
            txt_clip = txt_clip.fx(fadein, 0.3).fx(fadeout, 0.3)
            
            text_clips.append(txt_clip)
        
        # Composite video with text overlays
        video = CompositeVideoClip([video] + text_clips)
        
        logger.info(f"📝 Added {len(text_clips)} text overlays")
        return video
    
    def create_ad(
        self,
        images: List[str],
        audio: str,
        duration: float = 15.0,
        title: Optional[str] = None,
        style: str = "minimal"
    ) -> CompositeVideoClip:
        """
        Create a simple ad video.
        
        Args:
            images: Product images
            audio: Voiceover audio
            duration: Total video duration
            title: Ad title
            style: Visual style ("minimal", "dynamic", "cinematic")
            
        Returns:
            CompositeVideoClip ready for export
        """
        logger.info(f"🎬 Creating {style} ad: {title}")
        
        # Configure based on style
        if style == "minimal":
            transitions = ["fade"]
            effects = ["zoom_in"]
            text_overlays = [
                {
                    "text": title,
                    "position": "center",
                    "duration": 3.0,
                    "start_time": 0.0,
                    "font_size": 80,
                    "color": "white"
                }
            ] if title else None
        
        elif style == "dynamic":
            transitions = ["crossfade"]
            effects = ["zoom_in", "zoom_out", "pan_left"]
            text_overlays = [
                {
                    "text": title,
                    "position": "bottom",
                    "duration": 2.0,
                    "start_time": 1.0,
                    "font_size": 70,
                    "color": "yellow"
                }
            ] if title else None
        
        elif style == "cinematic":
            transitions = ["fade"]
            effects = ["pan_right"]
            text_overlays = [
                {
                    "text": title,
                    "position": ("center", 200),
                    "duration": 4.0,
                    "start_time": 0.5,
                    "font_size": 90,
                    "color": "white"
                }
            ] if title else None
        
        else:
            transitions = None
            effects = None
            text_overlays = None
        
        # Compose video
        video = self.compose(
            images=images,
            audio=audio,
            duration=duration / len(images),
            transitions=transitions,
            text_overlays=text_overlays,
            effects=effects
        )
        
        return video
    
    def export(
        self,
        video: CompositeVideoClip,
        output_file: str,
        fps: Optional[int] = None,
        codec: str = "libx264",
        audio_codec: str = "aac",
        bitrate: str = "5000k",
        preset: str = "medium"
    ) -> str:
        """
        Export video to file.
        
        Args:
            video: CompositeVideoClip to export
            output_file: Output file path
            fps: Frames per second
            codec: Video codec
            audio_codec: Audio codec
            bitrate: Video bitrate
            preset: Encoding preset (ultrafast, fast, medium, slow, veryslow)
            
        Returns:
            Path to exported video
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fps = fps or self.default_fps
        
        logger.info(f"💾 Exporting video: {output_file}")
        logger.info(f"   FPS: {fps}, Codec: {codec}, Bitrate: {bitrate}")
        
        video.write_videofile(
            output_file,
            fps=fps,
            codec=codec,
            audio_codec=audio_codec,
            bitrate=bitrate,
            preset=preset,
            threads=4
        )
        
        logger.info(f"✅ Video exported: {output_file}")
        return output_file


# Example usage
if __name__ == "__main__":
    # Initialize composer
    composer = VideoComposer()
    
    # Example 1: Simple video from images
    print("\n📹 Creating simple video...")
    
    # Note: Replace with actual image/audio files
    try:
        video = composer.compose(
            images=["image1.png", "image2.png", "image3.png"],
            audio="voiceover.mp3",
            duration=5.0,
            transitions=["fade"],
            text_overlays=[
                {
                    "text": "CoffeeLab",
                    "position": "center",
                    "duration": 3.0
                }
            ]
        )
        
        composer.export(video, "output_simple.mp4")
        print("✅ Simple video created!")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
    
    # Example 2: Ad video
    print("\n🎬 Creating ad video...")
    
    try:
        video = composer.create_ad(
            images=["product.png"],
            audio="ad_voiceover.mp3",
            duration=15.0,
            title="CoffeeLab - Premium Coffee",
            style="minimal"
        )
        
        composer.export(video, "output_ad.mp4")
        print("✅ Ad video created!")
        
    except Exception as e:
        print(f"❌ Failed: {str(e)}")
