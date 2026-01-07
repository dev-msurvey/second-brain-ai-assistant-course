"""
Module 7: Unified API
=====================

FastAPI application providing unified interface for all AI Director modules.

Endpoints:
- POST /api/v1/generate - Full content generation pipeline
- POST /api/v1/rag/search - Vector search
- POST /api/v1/media/image - Generate image
- POST /api/v1/media/voice - Generate voice
- POST /api/v1/media/video - Compose video
- POST /api/v1/edit/smart-cut - Smart video editing
- GET /api/v1/health - Health check
- GET /api/v1/metrics - Prometheus metrics

Author: AI Director Team
License: MIT
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
import logging
import os
from pathlib import Path
import sys

# Add module paths
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from ai_director import AIDirector, DirectorConfig, Brief

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="AI Director API",
    description="Unified API for AI Director content generation system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global director instance
director: Optional[AIDirector] = None


# Request/Response Models
class BriefRequest(BaseModel):
    """Content brief request."""
    brand: str = Field(..., description="Brand name")
    product: str = Field(..., description="Product name")
    duration: float = Field(..., gt=0, le=300, description="Duration in seconds")
    platform: str = Field(..., description="Platform (instagram, youtube, tiktok)")
    language: str = Field(default="thai", description="Content language")
    tone: str = Field(default="professional", description="Content tone")
    additional_notes: Optional[str] = Field(None, description="Additional notes")


class RAGSearchRequest(BaseModel):
    """RAG search request."""
    query: str = Field(..., description="Search query")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of results")
    method: str = Field(default="hybrid", description="Retrieval method")


class ImageGenerationRequest(BaseModel):
    """Image generation request."""
    prompt: str = Field(..., description="Image prompt")
    style: str = Field(default="product", description="Style preset")
    width: int = Field(default=1024, ge=512, le=2048, description="Image width")
    height: int = Field(default=1024, ge=512, le=2048, description="Image height")


class VoiceGenerationRequest(BaseModel):
    """Voice generation request."""
    text: str = Field(..., description="Text to speak")
    voice: str = Field(default="th-TH-NiwatNeural", description="Voice ID")
    rate: str = Field(default="+0%", description="Speech rate")


class SmartCutRequest(BaseModel):
    """Smart cut request."""
    video_path: str = Field(..., description="Input video path")
    remove_silence: bool = Field(default=True, description="Remove silent parts")
    target_duration: Optional[float] = Field(None, description="Target duration")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    modules: Dict[str, bool]


class ContentResponse(BaseModel):
    """Content generation response."""
    video_path: str
    images: List[str]
    audio_path: str
    duration: float
    processing_time: float
    metadata: Dict[str, Any]


# Startup/Shutdown
@app.on_event("startup")
async def startup_event():
    """Initialize AI Director on startup."""
    global director
    
    logger.info("🚀 Starting AI Director API...")
    
    config = DirectorConfig(
        mongodb_uri=os.getenv("MONGODB_URI"),
        hf_token=os.getenv("HF_TOKEN"),
        output_dir=os.getenv("OUTPUT_DIR", "output"),
        temp_dir=os.getenv("TEMP_DIR", "temp"),
        image_model=os.getenv("IMAGE_MODEL", "sdxl"),
        video_fps=int(os.getenv("VIDEO_FPS", "30"))
    )
    
    director = AIDirector(config)
    
    logger.info("✅ AI Director API started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("👋 Shutting down AI Director API...")


# Health Check
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns system status and module availability.
    """
    if director is None:
        raise HTTPException(status_code=503, detail="Director not initialized")
    
    modules = {
        "vector_rag": director._get_rag_system() is not None,
        "image_generator": director._get_image_generator() is not None,
        "voice_generator": director._get_voice_generator() is not None,
        "video_composer": director._get_video_composer() is not None,
        "smart_cut": director._get_smart_cut() is not None
    }
    
    return HealthResponse(
        status="healthy" if any(modules.values()) else "degraded",
        version="1.0.0",
        modules=modules
    )


# Content Generation
@app.post("/api/v1/generate", response_model=ContentResponse)
async def generate_content(
    brief_request: BriefRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate complete content from brief.
    
    Full pipeline: brief → strategy → images → voice → video → editing
    
    Args:
        brief_request: Content brief
        
    Returns:
        Content output with video, images, audio
    """
    if director is None:
        raise HTTPException(status_code=503, detail="Director not initialized")
    
    try:
        # Create brief
        brief = Brief(
            brand=brief_request.brand,
            product=brief_request.product,
            duration=brief_request.duration,
            platform=brief_request.platform,
            language=brief_request.language,
            tone=brief_request.tone,
            additional_notes=brief_request.additional_notes
        )
        
        # Generate content
        result = await director.create_content(brief)
        
        return ContentResponse(
            video_path=result.video_path,
            images=result.images,
            audio_path=result.audio_path,
            duration=result.duration,
            processing_time=result.metadata["processing_time"],
            metadata=result.metadata
        )
        
    except Exception as e:
        logger.error(f"❌ Content generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Vector RAG
@app.post("/api/v1/rag/search")
async def search_rag(request: RAGSearchRequest):
    """
    Search brand context using Vector RAG.
    
    Args:
        request: Search request
        
    Returns:
        Search results
    """
    if director is None:
        raise HTTPException(status_code=503, detail="Director not initialized")
    
    try:
        rag = director._get_rag_system()
        
        if rag is None:
            raise HTTPException(status_code=503, detail="RAG system not available")
        
        results = rag.retrieve(query=request.query, top_k=request.top_k)
        
        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"❌ RAG search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Image Generation
@app.post("/api/v1/media/image")
async def generate_image(request: ImageGenerationRequest):
    """
    Generate image from prompt.
    
    Args:
        request: Image generation request
        
    Returns:
        Image file path
    """
    if director is None:
        raise HTTPException(status_code=503, detail="Director not initialized")
    
    try:
        image_gen = director._get_image_generator()
        
        if image_gen is None:
            raise HTTPException(status_code=503, detail="Image generator not available")
        
        output_file = Path(director.config.output_dir) / f"image_{int(time.time())}.png"
        
        image = image_gen.generate(
            prompt=request.prompt,
            style_preset=request.style,
            width=request.width,
            height=request.height,
            output_file=str(output_file)
        )
        
        return {
            "image_path": str(output_file),
            "prompt": request.prompt,
            "size": f"{request.width}x{request.height}"
        }
        
    except Exception as e:
        logger.error(f"❌ Image generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Voice Generation
@app.post("/api/v1/media/voice")
async def generate_voice(request: VoiceGenerationRequest):
    """
    Generate voice from text.
    
    Args:
        request: Voice generation request
        
    Returns:
        Audio file path
    """
    if director is None:
        raise HTTPException(status_code=503, detail="Director not initialized")
    
    try:
        voice_gen = director._get_voice_generator()
        
        if voice_gen is None:
            raise HTTPException(status_code=503, detail="Voice generator not available")
        
        output_file = Path(director.config.output_dir) / f"voice_{int(time.time())}.mp3"
        
        await voice_gen.generate(
            text=request.text,
            voice=request.voice,
            rate=request.rate,
            output_file=str(output_file)
        )
        
        return {
            "audio_path": str(output_file),
            "text": request.text,
            "voice": request.voice
        }
        
    except Exception as e:
        logger.error(f"❌ Voice generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Smart Cut
@app.post("/api/v1/edit/smart-cut")
async def smart_cut_video(request: SmartCutRequest):
    """
    Apply smart editing to video.
    
    Args:
        request: Smart cut request
        
    Returns:
        Edited video path
    """
    if director is None:
        raise HTTPException(status_code=503, detail="Director not initialized")
    
    try:
        smart_cut = director._get_smart_cut()
        
        if smart_cut is None:
            raise HTTPException(status_code=503, detail="Smart Cut not available")
        
        # Validate input file
        if not Path(request.video_path).exists():
            raise HTTPException(status_code=404, detail="Input video not found")
        
        output_file = Path(director.config.output_dir) / f"edited_{int(time.time())}.mp4"
        
        result = smart_cut.process_video(
            input_path=request.video_path,
            output_path=str(output_file),
            remove_silence=request.remove_silence,
            target_duration=request.target_duration
        )
        
        return {
            "video_path": str(output_file),
            "original_duration": result["original_duration"],
            "final_duration": result["final_duration"],
            "time_saved": result["time_saved"]
        }
        
    except Exception as e:
        logger.error(f"❌ Smart cut failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Download File
@app.get("/api/v1/download/{file_type}/{filename}")
async def download_file(file_type: str, filename: str):
    """
    Download generated file.
    
    Args:
        file_type: File type (video, image, audio)
        filename: File name
        
    Returns:
        File download
    """
    if director is None:
        raise HTTPException(status_code=503, detail="Director not initialized")
    
    file_path = Path(director.config.output_dir) / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=filename)


# Metrics (placeholder for Prometheus)
@app.get("/api/v1/metrics")
async def metrics():
    """
    Get system metrics (Prometheus format).
    
    Returns:
        Metrics in Prometheus format
    """
    # TODO: Implement Prometheus metrics
    return {
        "message": "Metrics endpoint - Prometheus integration pending"
    }


# Run server
if __name__ == "__main__":
    import time
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
