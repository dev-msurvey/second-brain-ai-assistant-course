"""
Module 4 LLM Integration for AI Director
Connects fine-tuned Gemma model to generate creative strategies
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


class LLMCreativeEngine:
    """
    Integration with Module 4 fine-tuned LLM for creative strategy generation.
    Falls back to templates if model not available.
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.model_path = self._find_model_path()
        
        # Try to load model
        self._lazy_load_model()
    
    def _find_model_path(self) -> Optional[Path]:
        """Find the fine-tuned model from Module 4."""
        possible_paths = [
            # Local trained model
            Path("/workspaces/second-brain-ai-assistant-course/models_me/ai-director-colab/trained_models/lora_model"),
            Path("/workspaces/second-brain-ai-assistant-course/module4/models/lora_model"),
            
            # Colab saved model
            Path("/workspaces/second-brain-ai-assistant-course/ai-director-colab/trained_models/lora_model"),
            
            # Alternative locations
            Path("./models/lora_model"),
            Path("../module4/models/lora_model"),
        ]
        
        for path in possible_paths:
            if path.exists():
                logger.info(f"✅ Found model at: {path}")
                return path
        
        logger.warning("⚠️  No fine-tuned model found, will use template fallback")
        return None
    
    def _lazy_load_model(self):
        """Lazy load the model to avoid startup delays."""
        if self.model_loaded or not self.model_path:
            return
        
        try:
            # Try importing transformers
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            logger.info(f"Loading model from {self.model_path}...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(str(self.model_path))
            self.model = AutoModelForCausalLM.from_pretrained(
                str(self.model_path),
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            self.model_loaded = True
            logger.info("✅ Model loaded successfully")
            
        except ImportError:
            logger.warning("⚠️  transformers not installed, using template fallback")
            logger.info("Install with: pip install transformers torch")
        except Exception as e:
            logger.warning(f"⚠️  Failed to load model: {e}")
            logger.info("Using template-based fallback")
    
    def generate_strategy(
        self,
        product: str,
        brand: str,
        tone: str,
        platform: str,
        duration: int,
        language: str,
        brand_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate creative strategy using fine-tuned LLM.
        Falls back to template if model not available.
        """
        
        # Try LLM generation if model loaded
        if self.model_loaded and self.model and self.tokenizer:
            try:
                return self._generate_with_llm(
                    product, brand, tone, platform, duration, language, brand_context
                )
            except Exception as e:
                logger.warning(f"⚠️  LLM generation failed: {e}, using fallback")
        
        # Fallback to template
        return self._generate_template_strategy(
            product, brand, tone, platform, duration, language, brand_context
        )
    
    def _generate_with_llm(
        self,
        product: str,
        brand: str,
        tone: str,
        platform: str,
        duration: int,
        language: str,
        brand_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate strategy using the fine-tuned LLM."""
        
        # Construct prompt based on Module 4 training format
        prompt = self._build_llm_prompt(
            product, brand, tone, platform, duration, language, brand_context
        )
        
        logger.info(f"🤖 Generating creative strategy with LLM...")
        
        # Generate with model
        import torch
        
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        
        if torch.cuda.is_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=1024,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode output
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Parse the generated strategy
        strategy = self._parse_llm_output(generated_text, duration)
        
        logger.info(f"✅ Generated strategy with {len(strategy['visual_scenes'])} scenes")
        
        return strategy
    
    def _build_llm_prompt(
        self,
        product: str,
        brand: str,
        tone: str,
        platform: str,
        duration: int,
        language: str,
        brand_context: Optional[str] = None
    ) -> str:
        """Build prompt for LLM based on Module 4 training format."""
        
        # Base prompt structure matching training data
        prompt = f"""Create a professional advertising campaign strategy:

Product: {product}
Brand: {brand}
Tone: {tone}
Platform: {platform}
Duration: {duration} seconds
Language: {language}
"""
        
        if brand_context:
            prompt += f"\nBrand Context:\n{brand_context}\n"
        
        prompt += """
Generate a comprehensive creative strategy with:
1. Core Message (1-2 sentences)
2. Visual Scenes (detailed image prompts for AI generation)
3. Script Outline (narrative structure)
4. Call to Action

Visual Scenes should be detailed, cinematic prompts optimized for AI image generation.
Use professional photography and cinematography terminology.
"""
        
        return prompt
    
    def _parse_llm_output(self, generated_text: str, duration: int) -> Dict[str, Any]:
        """Parse LLM output into strategy structure."""
        
        try:
            # Simple parsing - in production, use more robust parsing
            lines = generated_text.split('\n')
            
            strategy = {
                'core_message': '',
                'visual_scenes': [],
                'script_outline': [],
                'call_to_action': ''
            }
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Detect sections
                lower_line = line.lower()
                if 'core message' in lower_line or 'message:' in lower_line:
                    current_section = 'core_message'
                    continue
                elif 'visual scene' in lower_line or 'scene' in lower_line:
                    current_section = 'visual_scenes'
                    continue
                elif 'script' in lower_line or 'outline' in lower_line:
                    current_section = 'script_outline'
                    continue
                elif 'call to action' in lower_line or 'cta' in lower_line:
                    current_section = 'call_to_action'
                    continue
                
                # Add content to current section
                if current_section == 'core_message' and not strategy['core_message']:
                    strategy['core_message'] = line
                elif current_section == 'visual_scenes':
                    if line.startswith(('-', '*', '•')) or line[0].isdigit():
                        # Remove bullet/number prefix
                        scene = line.lstrip('-*•0123456789. ')
                        if len(scene) > 20:  # Valid scene description
                            strategy['visual_scenes'].append(scene)
                elif current_section == 'script_outline':
                    if line.startswith(('-', '*', '•')) or line[0].isdigit():
                        outline = line.lstrip('-*•0123456789. ')
                        if len(outline) > 10:
                            strategy['script_outline'].append(outline)
                elif current_section == 'call_to_action' and not strategy['call_to_action']:
                    strategy['call_to_action'] = line
            
            # Ensure we have minimum content
            if not strategy['visual_scenes']:
                # Calculate scenes needed (1 per 30-60 seconds)
                num_scenes = max(3, min(10, duration // 45))
                strategy['visual_scenes'] = [
                    f"Professional commercial scene {i+1}" 
                    for i in range(num_scenes)
                ]
            
            if not strategy['core_message']:
                strategy['core_message'] = "Engaging brand story"
            
            if not strategy['call_to_action']:
                strategy['call_to_action'] = "Take action today"
            
            return strategy
            
        except Exception as e:
            logger.error(f"Failed to parse LLM output: {e}")
            # Return minimal valid strategy
            num_scenes = max(3, min(10, duration // 45))
            return {
                'core_message': 'Premium quality',
                'visual_scenes': [f"Scene {i+1}" for i in range(num_scenes)],
                'script_outline': ['Introduction', 'Features', 'Benefits', 'Conclusion'],
                'call_to_action': 'Learn more'
            }
    
    def _generate_template_strategy(
        self,
        product: str,
        brand: str,
        tone: str,
        platform: str,
        duration: int,
        language: str,
        brand_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """Fallback template-based strategy generation."""
        
        logger.info("📝 Using template-based strategy generation (fallback)")
        
        # Calculate number of scenes (1 per 30-60 seconds)
        num_scenes = max(3, min(10, duration // 45))
        
        # Enhanced template prompts
        try:
            from prompt_templates import generate_visual_scenes
            visual_scenes = generate_visual_scenes(
                product=product,
                brand=brand,
                tone=tone,
                platform=platform,
                duration=duration,
                language=language
            )
        except Exception as e:
            logger.warning(f"Prompt templates failed: {e}")
            # Ultra-basic fallback
            visual_scenes = [
                f"Professional commercial shot of {product}, cinematic lighting, 8k, high quality",
                f"Close-up detail of {product}, studio photography, elegant composition",
                f"Lifestyle scene featuring {product}, premium environment, editorial style"
            ]
        
        # Template script outline
        if language.lower() in ['th', 'thai', 'ไทย']:
            script_outline = [
                f"เปิดฉากด้วยภาพที่โดดเด่นของ {product}",
                f"แสดงคุณสมบัติเด่นและความพิเศษ",
                f"เชื่อมโยงกับไลฟ์สไตล์และความต้องการของลูกค้า",
                f"สร้างความประทับใจและความน่าเชื่อถือ",
                f"ปิดท้ายด้วย call to action ที่ชัดเจน"
            ]
            core_message = f"ค้นพบความเป็นเลิศกับ {product} จาก {brand}"
            cta = f"สัมผัดประสบการณ์พิเศษกับ {brand} วันนี้"
            
            # CRITICAL: Generate comprehensive 30-minute advertising voiceover script
            # This is actual ad narration (NOT image prompts!)
            # Target: ~30,000 characters for 30-minute duration
            voiceover_script = self._generate_extended_thai_script(
                product=product,
                brand=brand,
                tone=tone,
                duration=duration
            )
            
        else:
            script_outline = [
                f"Opening with striking visual of {product}",
                f"Showcase key features and benefits",
                f"Connect to customer lifestyle and needs",
                f"Build trust and emotional connection",
                f"Clear call to action"
            ]
            core_message = f"Discover excellence with {product} from {brand}"
            cta = f"Experience {brand} today"
            
            # English voiceover script
            voiceover_script = f"""Imagine a future...
            
Where you never get stuck in traffic again. Where every journey is effortless.

Introducing {product} from {brand}

Advanced technology that lets you truly fly.
Clean energy. Fuel efficient. Environmentally friendly.

{product} isn't just a vehicle.
It's the future of transportation, available today.

Engineered for maximum safety.
Simple to use. Ready to fly.

Experience freedom in travel like never before.

{product} - The future of transportation starts here.

{brand} - Leading you to a new world."""
        
        return {
            'core_message': core_message,
            'visual_scenes': visual_scenes,
            'script_outline': script_outline,
            'voiceover_script': voiceover_script,  # ✅ Actual advertising copy
            'call_to_action': cta,
            'generation_method': 'template_fallback'
        }
    
    def _generate_extended_thai_script(
        self,
        product: str,
        brand: str,
        tone: str,
        duration: int
    ) -> str:

            # CRITICAL: Generate comprehensive 30-minute advertising voiceover script
            # This is actual ad narration (NOT image prompts!)
            voiceover_script = self._generate_extended_thai_script(
                product=product,
                brand=brand,
                tone=tone,
                duration=duration
            )
            
        else:
            script_outline = [
                f"Opening with striking visual of {product}",
                f"Showcase key features and benefits",
                f"Connect to customer lifestyle and needs",
                f"Build trust and emotional connection",
                f"Clear call to action"
            ]
            core_message = f"Discover excellence with {product} from {brand}"
            cta = f"Experience {brand} today"
            voiceover_script = f"Introducing {product}. Experience innovation."
        
        return {
            "core_message": core_message,
            "visual_scenes": visual_scenes,
            "script_outline": script_outline,
            "voiceover_script": voiceover_script,
            "call_to_action": cta,
            "generation_method": "template_fallback"
        }


เพราะตอนนี้ {product} จาก {brand} มาถึงแล้ว

นี่ไม่ใช่เรื่องในภาพยนตร์ไซไฟอีกต่อไป
นี่คืออนาคตที่กำลังเกิดขึ้นจริง ณ ตอนนี้

{product} คือการปฏิวัติวงการที่จะเปลี่ยนวิถีชีวิตของคุณไปตลอดกาล""")
        
        # Section 2: Benefits
        script_sections.append(f"""ด้วย {product} คุณจะได้รับประสบการณ์ที่แตกต่าง
คุณภาพที่เหนือกว่า เทคโนโลยีที่ล้ำสมัย
และความพึงพอใจที่แท้จริง

{brand} มุ่งมั่นในการส่งมอบความเป็นเลิศ
ที่คุณสามารถเชื่อถือได้

สัมผัสความแตกต่างกับ {product} วันนี้""")
        
        # Combine sections
        full_script = "\n\n".join(script_sections)
        
        # Extend if needed
        while len(full_script) < target_chars * 0.95:
            extension = f"""

{product} พร้อมมอบประสบการณ์ที่ดีที่สุดให้คุณ
ด้วยคุณภาพที่เหนือชั้น บริการที่ประทับใจ
และนวัตกรรมที่ทันสมัย

{brand} ผู้นำที่คุณวางใจ
มุ่งมั่นสร้างสรรค์เพื่อคุณภาพชีวิตที่ดีกว่า

ติดต่อเราวันนี้ เพื่อเริ่มต้นประสบการณ์ใหม่กับ {product}"""
            
            full_script += extension
        
        logger.info(f"Generated {len(full_script):,} character advertising script (target: {target_chars:,})")
        
        return full_script


# Singleton instance
_llm_engine = None

