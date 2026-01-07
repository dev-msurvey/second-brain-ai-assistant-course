"""
Module 6.5: Smart Cut - Advanced Video Editing
==============================================

Intelligent video editing with AI-powered scene detection,
automatic silence removal, and smart trimming.

Components:
- SceneDetector: Detect scenes using multiple algorithms
- AutoEditor: Remove silence and optimize pacing
- SmartCut: Main intelligent editing system

Author: AI Director Team
License: MIT
"""

__version__ = "1.0.0"

from .scene_detector import SceneDetector, Scene
from .auto_editor import AutoEditor, EditDecision
from .smart_cut import SmartCut, SmartCutConfig

__all__ = [
    "SceneDetector",
    "Scene",
    "AutoEditor",
    "EditDecision",
    "SmartCut",
    "SmartCutConfig"
]
