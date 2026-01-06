"""
T5Gemma 2 Demo - Working Version
Uses alternative approach for Module 1 learning

Module 1: Dual-Model Architecture Design
"""

print("=" * 70)
print("🧠 T5GEMMA 2 (THINKER) - DEMO")
print("=" * 70)
print()

print("⚠️  Note: T5Gemma 2 requires latest transformers version.")
print("For this demo, we'll use google/flan-t5-base as demonstration.")
print("The architecture and workflow are identical.")
print()

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# Use FLAN-T5 as demo (same architecture as T5Gemma)
model_name = "google/flan-t5-base"
print(f"🔄 Loading {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

print(f"✅ Model loaded successfully!")
print(f"📊 Parameters: {sum(p.numel() for p in model.parameters()):,}")
print()

# Test 1: Generate Strategy
print("📝 TEST 1: Generate Marketing Strategy")
print("-" * 70)

brief = """Create a marketing strategy for CoffeeLab Cold Brew.
Target: Young professionals 25-35 years old
Platform: Instagram Reel (15 seconds)
Goal: Product launch awareness
"""

prompt = f"""You are a creative director. Generate a brief content strategy.

BRIEF:
{brief}

STRATEGY:"""

print(f"Input:\n{brief}\n")

inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.7,
        do_sample=True,
        top_p=0.9
    )

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"✅ Generated Strategy:\n{result}\n")

# Test 2: Generate Image Prompt
print("📝 TEST 2: Generate Image Prompt")
print("-" * 70)

image_brief = "Premium cold brew coffee bottle on modern desk with morning light"
prompt = f"Generate a detailed photography prompt: {image_brief}"

inputs = tokenizer(prompt, return_tensors="pt", max_length=128, truncation=True)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Image Brief: {image_brief}")
print(f"✅ SDXL Prompt:\n{result}\n")

# Test 3: Generate Voice Script  
print("📝 TEST 3: Generate Voice Script")
print("-" * 70)

concept = "Introducing CoffeeLab Cold Brew - fresh, bold, energizing"
prompt = f"Write a 15-second Thai voiceover script: {concept}"

inputs = tokenizer(prompt, return_tensors="pt", max_length=128, truncation=True)

with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Concept: {concept}")
print(f"✅ Voice Script:\n{result}\n")

print("=" * 70)
print("✅ T5 (Thinker) Demo Complete!")
print()
print("💡 Key Takeaways:")
print("   • T5 architecture is encoder-decoder")
print("   • Good for creative/strategic tasks")
print("   • Generates natural language output")
print("   • T5Gemma 2 has same architecture + multimodal")
print("=" * 70)
