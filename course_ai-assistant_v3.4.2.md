# 🎓 Self-Paced Course: Building Your AI Director (v3.4)

**Project Theme:** The AI Director — One-Man Marketing Agency  
**Based on:** `decodingai-magazine/second-brain-ai-assistant-course`  
**Instructor:** GitHub Copilot (Directed by You)  
**Platform:** GitHub Codespaces (Learning) & Google Colab (Training)  
**Last Updated:** January 2026

---

## 🎬 AI Director Concept

> **"One Brain (Director), Many Hands (Tools)"**  
> ไม่ใช่แค่ Chatbot ถาม-ตอบ แต่คือ **Head of Marketing** ที่คุมการผลิตทั้งหมด

### What is AI Director?

```
┌─────────────────────────────────────────────────────────────────┐
│                    🧠 AI DIRECTOR ARCHITECTURE v3.4             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌──────────────────┐                         │
│                    │   AI DIRECTOR    │                         │
│                    │  ┌────────────┐  │                         │
│                    │  │  T5Gemma 2 │  │  ← Multimodal Brain     │
│                    │  │  (4B-4B)   │  │    (Text + Image)       │
│                    │  └────────────┘  │                         │
│                    │        +         │                         │
│                    │  ┌────────────┐  │                         │
│                    │  │ Function   │  │  ← Tool Orchestrator    │
│                    │  │   Gemma    │  │    (270M, On-device)    │
│                    │  └────────────┘  │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         │                   │                   │               │
│         ▼                   ▼                   ▼               │
│   ┌───────────┐      ┌───────────┐      ┌───────────┐          │
│   │ STRATEGY  │      │  CONTENT  │      │PRODUCTION │          │
│   ├───────────┤      ├───────────┤      ├───────────┤          │
│   │• Campaign │      │• Script   │      │• Image Gen│          │
│   │• Audience │      │• Prompts  │      │• Voice Gen│          │
│   └───────────┘      └───────────┘      │• Video    │          │
│                                          │  Compose  │          │
│                                          │• Smart Cut│          │
│                                          └───────────┘          │
│                                                                  │
│   ════════════════════════════════════════════════════════      │
│   AI Director: รับโจทย์ → วางแผน → สร้าง/ตัดต่อ → ส่งมอบ          │
│   ════════════════════════════════════════════════════════      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💰 Zero Cost Strategy Edition

> **"ห้ามเสียเงินแม้แต่บาทเดียว"** - เรียนจบได้โดยไม่ต้องผูกบัตรเครดิต

---

## 🆕 What's New in v3.4

| ปรับปรุง | รายละเอียด |
|---------|-----------|
| 📚 **Comprehensive Documentation** | เพิ่มเอกสารอ้างอิงครบทุก component |
| 🔗 **Official Links** | Links ไปยัง official documentation |
| 📖 **Tutorials & Examples** | ตัวอย่าง notebooks และ tutorials |
| 🇹🇭 **Thai Language Guide** | Best practices สำหรับภาษาไทย |
| 🎯 **Quick Reference** | สรุป API, parameters, best practices |

### v3.4 vs v3.3 Comparison

| Feature | v3.3 | v3.4 |
|---------|------|------|
| Smart Cut | ✅ | ✅ |
| Documentation | Basic | **Comprehensive** |
| Official Links | ❌ | ✅ **NEW** |
| Example Notebooks | ❌ | ✅ **NEW** |
| Thai Language Guide | ❌ | ✅ **NEW** |
| Troubleshooting | ❌ | ✅ **NEW** |

---

## ✅ Zero Cost Stack (Updated v3.4)

| ส่วนประกอบ | ใช้ตัวนี้ (ฟรี 100%) | หมายเหตุ |
|-----------|---------------------|---------|
| **Compute** | GitHub Codespaces (2-core) | 120 ชม./เดือน |
| **Database** | MongoDB Atlas (M0) | Singapore, 512MB |
| **Vector DB** | ChromaDB (Local) | เก็บใน Codespace |
| **GPU (Train)** | Google Colab (Free T4) | Save ลง Drive |
| **LLM API** | Gemini 1.5 Flash | Google AI Studio |
| **Thinker Model** | T5Gemma 2 (1B-1B) | HF Inference API |
| **Executor Model** | FunctionGemma (270M) | Run locally |
| **Optimization** | Meta Ax | Bayesian hyperparameter tuning |
| **Image Gen** | HF Inference API | SDXL/Flux |
| **Voice Gen** | Edge-TTS | Microsoft Edge voices |
| **Video Compose** | MoviePy | Python library |
| **Smart Cut** | FFmpeg + Whisper | ตัดต่ออัจฉริยะ |
| **Transcription** | Whisper (tiny/base) | รัน CPU ได้ |

---

## 📅 Course Syllabus

### 🗺️ Learning Path

```
┌─────────────────────────────────────────────────────────────────┐
│                 AI DIRECTOR LEARNING PATH v3.4                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   FOUNDATION                                                     │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                    │
│   │Module 1 │───▶│Module 2 │───▶│Module 3 │                    │
│   │Dual-Arch│    │  ETL    │    │Dataset+ │                    │
│   │ Design  │    │         │    │Prompts  │                    │
│   └─────────┘    └─────────┘    └─────────┘                    │
│                                       │                         │
│   CORE                                ▼                         │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐                    │
│   │Module 4 │───▶│Mod. 4.5 │───▶│Module 5 │                    │
│   │Fine-tune│    │ Meta Ax │    │  RAG    │                    │
│   └─────────┘    └─────────┘    └─────────┘                    │
│                                       │                         │
│   PRODUCTION                          ▼                         │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    │
│   │Module 6 │───▶│Mod. 6.5 │───▶│Module 7 │───▶│Module 8 │    │
│   │ Tools   │    │Smart Cut│    │  Agent  │    │ Deploy  │    │
│   │ Setup   │    │         │    │         │    │         │    │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘    │
│                                       │                         │
│                              ┌────────▼────────┐                │
│                              │  FINAL PROJECT  │                │
│                              │  Full Pipeline  │                │
│                              └─────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

# 📚 COMPREHENSIVE DOCUMENTATION & REFERENCES

> **v3.4 เพิ่มเอกสารอ้างอิงครบทุก component พร้อม links และ tutorials**

---

## 🧠 Models & AI Documentation

### T5Gemma 2 (Thinker Model)

**Overview:**
T5Gemma 2 เป็น encoder-decoder model จาก Google ที่รองรับ multimodal (text + image) และ long context (128K tokens) ใน 140+ ภาษา

**Available Sizes:**

| Model | Total Params | VRAM | Model ID |
|-------|--------------|------|----------|
| 270M-270M | ~370M | ~1GB | `google/t5gemma-2-270m-270m` |
| 1B-1B | ~1.7B | ~4GB | `google/t5gemma-2-1b-1b` |
| 4B-4B | ~7B | ~16GB | `google/t5gemma-2-4b-4b` |

**Key Features:**
- Multimodal: รับ text + image input
- Long Context: 128K token window
- Multilingual: 140+ languages รวมภาษาไทย
- Tied embeddings: ลด parameters
- Merged attention: รวม self + cross attention

**Official Documentation:**

| Resource | Link |
|----------|------|
| 📄 Model Card (270M) | https://huggingface.co/google/t5gemma-2-270m-270m |
| 📄 Model Card (1B) | https://huggingface.co/google/t5gemma-2-1b-1b |
| 📄 Model Card (4B) | https://huggingface.co/google/t5gemma-2-4b-4b |
| 📖 HF Transformers Doc | https://huggingface.co/docs/transformers/model_doc/t5gemma2 |
| 📰 Google Blog | https://blog.google/technology/developers/t5gemma-2/ |
| 📦 HF Collection | https://huggingface.co/collections/google/t5gemma-2 |
| 📝 ArXiv Paper | Search "T5Gemma 2: Seeing, Reading, and Understanding Longer" |

**Quick Start Code:**

```python
from transformers import AutoProcessor, AutoModelForSeq2SeqLM
import requests
from PIL import Image

# Load model and processor
processor = AutoProcessor.from_pretrained("google/t5gemma-2-1b-1b")
model = AutoModelForSeq2SeqLM.from_pretrained("google/t5gemma-2-1b-1b")

# Text-only example
text = "Translate to Thai: Hello, how are you?"
inputs = processor(text=text, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(processor.decode(outputs[0]))

# Multimodal example (text + image)
url = "https://example.com/image.jpg"
image = Image.open(requests.get(url, stream=True).raw)
prompt = "<start_of_image> Describe this image in detail"
inputs = processor(text=prompt, images=image, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
print(processor.decode(outputs[0]))
```

---

### FunctionGemma (Executor Model)

**Overview:**
FunctionGemma เป็น 270M model จาก Google ที่ออกแบบมาเฉพาะสำหรับ function/tool calling รันได้บน edge devices

**Key Features:**
- **Tiny but Powerful:** 270M params, รัน CPU ได้
- **Tool Calling Expert:** Natural language → JSON
- **Fine-tune Friendly:** 58% → 85% accuracy after fine-tuning
- **On-device Ready:** 550MB RAM

**Official Documentation:**

| Resource | Link |
|----------|------|
| 📄 Model Card | https://huggingface.co/google/functiongemma-270m-it |
| 📄 Unsloth GGUF | https://huggingface.co/unsloth/functiongemma-270m-it-GGUF |
| 📰 Google Blog | https://blog.google/technology/developers/functiongemma/ |
| 📖 Unsloth Guide | https://docs.unsloth.ai/models/functiongemma |
| 🎮 Ollama | https://ollama.com/library/functiongemma |
| 📖 LM Studio Guide | https://lmstudio.ai/blog/functiongemma-unsloth |

**Fine-Tuning Notebooks (Unsloth):**

| Notebook | Description |
|----------|-------------|
| [Reason Before Tool Calling](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/FunctionGemma_(270M)-Reasoning.ipynb) | Fine-tune to "think" before calling |
| [Mobile Actions](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/FunctionGemma_(270M)-MobileActions.ipynb) | Android system actions |
| [Multi-Turn Tool Calling](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/FunctionGemma_(270M)-MultiTurn.ipynb) | Chain tool calls |
| [LM Studio Export](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/FunctionGemma_(270M)-LMStudio.ipynb) | Fine-tune + export to GGUF |

**Tool Definition Format:**

```python
def get_weather(city: str) -> str:
    """
    Get the current weather for a city.
    
    Args:
        city: The name of the city
        
    Returns:
        A string describing the weather
    """
    return json.dumps({'city': city, 'temperature': 22, 'unit': 'celsius'})

# Apply chat template
tokenizer.apply_chat_template(
    [{"role": "user", "content": "What's the weather in Bangkok?"}],
    tools=[get_weather],
    add_generation_prompt=True,
    tokenize=False,
)
```

**Output Format:**

```
<start_function_call>call:get_weather{city:<escape>Bangkok<escape>}<end_function_call>
```

---

### Gemini API (Dataset Generation)

**Overview:**
Gemini API ใช้สำหรับ generate training datasets และ fallback inference

**Free Tier Limits (Dec 2025):**

| Model | RPM | TPM | RPD |
|-------|-----|-----|-----|
| Gemini 2.5 Pro | 2 | 250K | 50 |
| Gemini 2.5 Flash | 10 | 250K | 500 |
| Gemini 2.5 Flash-Lite | 15 | 250K | 1,000 |

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 API Homepage | https://ai.google.dev/gemini-api/docs |
| 🚀 Quickstart | https://ai.google.dev/gemini-api/docs/quickstart |
| 📋 Models List | https://ai.google.dev/gemini-api/docs/models |
| 💰 Pricing | https://ai.google.dev/pricing |
| 🔑 Get API Key | https://aistudio.google.com/apikey |

**Quick Start Code:**

```python
from google import genai

# Initialize client (API key from environment)
client = genai.Client()

# Simple generation
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain AI Director concept in Thai"
)
print(response.text)

# With system instruction
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Generate a marketing brief for coffee shop",
    config={
        "system_instruction": "You are a Thai marketing expert.",
        "temperature": 0.7,
        "max_output_tokens": 1000
    }
)
```

---

### Meta Ax (Hyperparameter Optimization)

**Overview:**
Ax เป็น open-source Bayesian optimization platform จาก Meta สำหรับ hyperparameter tuning

**Key Features:**
- **Bayesian Optimization:** ใช้ Gaussian Process
- **Multi-objective:** Optimize หลาย metrics พร้อมกัน
- **Built on BoTorch:** PyTorch-based
- **Production Ready:** ใช้ที่ Meta scale

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 Ax Website | https://ax.dev/ |
| 📦 GitHub | https://github.com/facebook/Ax |
| 📖 Tutorials | https://ax.dev/tutorials/ |
| 📄 BoTorch | https://botorch.org/docs/introduction/ |
| 📰 Meta Blog | https://engineering.fb.com/2025/11/18/open-source/efficient-optimization-ax-open-platform-adaptive-experimentation/ |

**Installation:**

```bash
pip install ax-platform botorch
```

**Quick Start Code:**

```python
from ax import Client, RangeParameterConfig

# Initialize client
client = Client()

# Define search space
client.configure_experiment(
    parameters=[
        RangeParameterConfig(name="learning_rate", bounds=(1e-5, 1e-3), parameter_type="float"),
        RangeParameterConfig(name="batch_size", bounds=(4, 32), parameter_type="int"),
        RangeParameterConfig(name="lora_r", bounds=(4, 32), parameter_type="int"),
        RangeParameterConfig(name="epochs", bounds=(1, 5), parameter_type="int"),
    ],
)

# Define objective (minimize loss)
client.configure_optimization(objective="-1 * eval_loss")

# Run optimization loop
for _ in range(20):
    for trial_index, parameters in client.get_next_trials(max_trials=1).items():
        # Train model with these parameters
        eval_loss = train_model(
            learning_rate=parameters["learning_rate"],
            batch_size=parameters["batch_size"],
            lora_r=parameters["lora_r"],
            epochs=parameters["epochs"]
        )
        
        # Report result
        client.complete_trial(
            trial_index=trial_index,
            raw_data={"eval_loss": eval_loss}
        )

# Get best parameters
best_params = client.get_best_parameterization()
print(f"Best parameters: {best_params}")
```

**Multi-Objective Example:**

```python
from ax.service.ax_client import AxClient
from ax.service.utils.instantiation import ObjectiveProperties

ax_client = AxClient()
ax_client.create_experiment(
    parameters=[
        {"name": "learning_rate", "type": "range", "bounds": [1e-5, 1e-3]},
        {"name": "lora_r", "type": "range", "bounds": [4, 32]},
    ],
    objectives={
        "eval_loss": ObjectiveProperties(minimize=True),
        "inference_speed": ObjectiveProperties(minimize=False),
        "memory_usage": ObjectiveProperties(minimize=True),
    },
)
```

---

### LoRA/PEFT (Efficient Fine-Tuning)

**Overview:**
LoRA (Low-Rank Adaptation) เป็นเทคนิค parameter-efficient fine-tuning ที่ train เฉพาะ small adapter weights

**Key Benefits:**
- **Memory Efficient:** ลด trainable params ~90%
- **Fast Training:** เร็วกว่า full fine-tuning มาก
- **Small Checkpoints:** Adapter weights ~10-50MB
- **No Inference Latency:** Merge weights ได้

**Official Documentation:**

| Resource | Link |
|----------|------|
| 📦 PEFT GitHub | https://github.com/huggingface/peft |
| 📖 PEFT Docs | https://huggingface.co/docs/peft |
| 📖 LoRA Guide | https://huggingface.co/docs/peft/main/en/conceptual_guides/lora |
| 📖 Transformers PEFT | https://huggingface.co/docs/transformers/en/peft |
| 📰 PEFT Blog | https://huggingface.co/blog/peft |
| 📖 Smol Course | https://huggingface.co/learn/smol-course/en/unit1/3a |

**Key Parameters:**

| Parameter | Description | Recommended |
|-----------|-------------|-------------|
| `r` | Rank of update matrices | 8-16 |
| `lora_alpha` | Scaling factor | 16-32 |
| `target_modules` | Which layers to adapt | `q_proj, k_proj, v_proj, o_proj` |
| `lora_dropout` | Dropout for LoRA layers | 0.05-0.1 |
| `bias` | Whether to train bias | `none` |

**Quick Start Code:**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType

# Load base model
model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b")
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b")

# Configure LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 4,194,304 || all params: 2,506,172,416 || trainable%: 0.1673

# Train with HuggingFace Trainer
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./lora_model",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4,
    fp16=True,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)
trainer.train()

# Save adapter only (~50MB)
model.save_pretrained("./lora_adapter")

# Load and merge for inference
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b")
model = PeftModel.from_pretrained(base_model, "./lora_adapter")
model = model.merge_and_unload()  # Merge weights
```

**QLoRA (4-bit) for Low VRAM:**

```python
from transformers import BitsAndBytesConfig
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2-2b",
    quantization_config=bnb_config,
    device_map="auto",
)

# Apply LoRA on quantized model
model = get_peft_model(model, lora_config)
```

---

## 🗄️ Data & Storage Documentation

### MongoDB Atlas (Free Tier)

**Overview:**
MongoDB Atlas M0 ให้ cloud database ฟรี 512MB สำหรับเก็บ brand data, campaigns, transcripts

**Free Tier Specs:**
- Storage: 512MB
- Connections: 100 max
- RAM: Shared
- vCPU: Shared
- Regions: AWS, GCP, Azure

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 MongoDB Atlas | https://www.mongodb.com/atlas |
| 📖 Getting Started | https://www.mongodb.com/docs/atlas/getting-started/ |
| 📖 Deploy Free Cluster | https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/ |
| 📖 M0 Limits | https://www.mongodb.com/docs/atlas/reference/free-shared-limitations/ |
| 📖 PyMongo Docs | https://pymongo.readthedocs.io/ |

**Setup Steps:**

1. สร้าง account ที่ https://www.mongodb.com/cloud/atlas
2. Create Free Cluster (M0)
3. เลือก Region: Singapore (ap-southeast-1)
4. Whitelist IP: 0.0.0.0/0 (for development)
5. Create Database User
6. Get Connection String

**Quick Start Code:**

```python
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://user:password@cluster.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["ai_director"]

# Collections
brands = db["brands"]
campaigns = db["campaigns"]
transcripts = db["transcripts"]

# Insert brand data
brand_data = {
    "name": "CoffeeLab",
    "tone": "friendly, premium, modern",
    "colors": ["#8B4513", "#F5F5DC", "#2C1810"],
    "target_audience": "young professionals 25-35",
    "created_at": datetime.now()
}
brands.insert_one(brand_data)

# Query
brand = brands.find_one({"name": "CoffeeLab"})
print(brand)
```

**Schema Design for AI Director:**

```python
# Brand Schema
{
    "_id": ObjectId,
    "name": str,
    "description": str,
    "tone": str,
    "colors": [str],
    "fonts": [str],
    "target_audience": str,
    "brand_values": [str],
    "created_at": datetime,
    "updated_at": datetime
}

# Campaign Schema
{
    "_id": ObjectId,
    "brand_id": ObjectId,
    "name": str,
    "brief": str,
    "generated_prompts": [str],
    "assets": [{
        "type": "image|video|audio",
        "url": str,
        "metadata": dict
    }],
    "status": "draft|active|completed",
    "created_at": datetime
}

# Transcript Schema
{
    "_id": ObjectId,
    "video_id": str,
    "filename": str,
    "duration": float,
    "language": str,
    "segments": [{
        "start": float,
        "end": float,
        "text": str,
        "words": [{
            "word": str,
            "start": float,
            "end": float,
            "confidence": float
        }]
    }],
    "silence_regions": [{
        "start": float,
        "end": float,
        "duration": float
    }],
    "created_at": datetime
}
```

---

### ChromaDB (Vector Database)

**Overview:**
ChromaDB เป็น open-source vector database สำหรับ RAG ใช้เก็บ embeddings ของ brand knowledge และ prompt templates

**Key Features:**
- In-memory หรือ persistent storage
- Built-in embedding functions
- Metadata filtering
- Python-native

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 ChromaDB | https://www.trychroma.com/ |
| 📦 GitHub | https://github.com/chroma-core/chroma |
| 📖 Documentation | https://docs.trychroma.com/ |
| 📖 LangChain Integration | https://python.langchain.com/docs/integrations/vectorstores/chroma |
| 📖 Real Python Tutorial | https://realpython.com/chromadb-vector-database/ |

**Installation:**

```bash
pip install chromadb
```

**Quick Start Code:**

```python
import chromadb
from chromadb.utils import embedding_functions

# Create persistent client
client = chromadb.PersistentClient(path="./chroma_db")

# Use sentence-transformers for embeddings
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Create collection
collection = client.get_or_create_collection(
    name="brand_knowledge",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)

# Add documents
collection.add(
    documents=[
        "CoffeeLab เป็นแบรนด์กาแฟพรีเมียม สำหรับคนรุ่นใหม่",
        "โทนสีหลักคือน้ำตาลเข้ม และครีม ให้ความรู้สึกอบอุ่น",
        "Target คือ young professionals อายุ 25-35 ปี",
    ],
    metadatas=[
        {"category": "brand", "type": "description"},
        {"category": "brand", "type": "colors"},
        {"category": "brand", "type": "audience"},
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Query
results = collection.query(
    query_texts=["ใครคือกลุ่มเป้าหมายของ CoffeeLab"],
    n_results=2,
    where={"category": "brand"}
)
print(results)
```

**RAG Pattern:**

```python
class BrandKnowledgeRAG:
    def __init__(self, collection):
        self.collection = collection
    
    def get_context(self, query: str, n_results: int = 3) -> str:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        context = "\n".join(results["documents"][0])
        return context
    
    def generate_with_context(self, query: str, llm) -> str:
        context = self.get_context(query)
        
        prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {query}

Answer:"""
        
        return llm.generate(prompt)
```

---

### Hugging Face Datasets

**Overview:**
ใช้สำหรับ prepare และ format training datasets

**Official Documentation:**

| Resource | Link |
|----------|------|
| 📦 GitHub | https://github.com/huggingface/datasets |
| 📖 Documentation | https://huggingface.co/docs/datasets |
| 📖 Loading Datasets | https://huggingface.co/docs/datasets/loading |
| 📖 Process Data | https://huggingface.co/docs/datasets/process |

**Quick Start Code:**

```python
from datasets import Dataset, DatasetDict

# Create dataset from dict
train_data = {
    "instruction": [
        "สร้าง prompt สำหรับโฆษณากาแฟ",
        "วิเคราะห์ target audience",
    ],
    "input": [
        "แบรนด์: CoffeeLab, สไตล์: minimal",
        "สินค้า: Cold Brew Premium",
    ],
    "output": [
        "A minimalist coffee cup on marble surface...",
        "กลุ่มเป้าหมาย: คนทำงานออฟฟิศ อายุ 25-35...",
    ],
}

dataset = Dataset.from_dict(train_data)

# Split dataset
dataset = dataset.train_test_split(test_size=0.1)

# Save to disk
dataset.save_to_disk("./ai_director_dataset")

# Load from disk
loaded_dataset = DatasetDict.load_from_disk("./ai_director_dataset")
```

---

## 🎨 Production Tools Documentation

### Image Generation (HF Inference API)

**Overview:**
ใช้ Hugging Face Inference API สำหรับ generate images ด้วย SDXL/Flux

**Official Documentation:**

| Resource | Link |
|----------|------|
| 📖 Inference API | https://huggingface.co/docs/api-inference |
| 📖 SDXL Model | https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 |
| 📖 Flux Models | https://huggingface.co/black-forest-labs |

**Quick Start Code:**

```python
import requests
import io
from PIL import Image

HF_TOKEN = "your_token_here"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

def generate_image(prompt: str, negative_prompt: str = "") -> Image.Image:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "negative_prompt": negative_prompt,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        return image
    else:
        raise Exception(f"Error: {response.status_code}")

# Usage
image = generate_image(
    prompt="A premium coffee cup on marble surface, soft morning light, minimal style, 4K",
    negative_prompt="blurry, low quality, watermark"
)
image.save("coffee_ad.png")
```

---

### Edge-TTS (Voice Generation)

**Overview:**
Edge-TTS ใช้ Microsoft Edge's TTS service สำหรับสร้างเสียงพากย์ ฟรี 100%

**Key Features:**
- Neural voices คุณภาพสูง
- รองรับหลายภาษา รวมภาษาไทย
- ปรับ rate, pitch, volume ได้
- สร้าง subtitles (.srt/.vtt) ได้

**Official Documentation:**

| Resource | Link |
|----------|------|
| 📦 PyPI | https://pypi.org/project/edge-tts/ |
| 📦 GitHub | https://github.com/rany2/edge-tts |

**Thai Voices:**

| Voice | Gender | Style |
|-------|--------|-------|
| `th-TH-PremwadeeNeural` | Female | Friendly, Positive |
| `th-TH-NiwatNeural` | Male | Friendly, Positive |

**Installation:**

```bash
pip install edge-tts
```

**Quick Start Code:**

```python
import edge_tts
import asyncio

async def generate_voice(text: str, voice: str, output_file: str):
    """Generate voice from text using Edge TTS"""
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate="+0%",      # -50% to +100%
        volume="+0%",    # -50% to +100%
        pitch="+0Hz"     # -50Hz to +50Hz
    )
    
    await communicate.save(output_file)
    print(f"Saved to {output_file}")

# Usage
text = "สวัสดีครับ วันนี้เรามาแนะนำกาแฟ Cold Brew ใหม่ล่าสุดจาก CoffeeLab"
asyncio.run(generate_voice(
    text=text,
    voice="th-TH-NiwatNeural",
    output_file="voiceover.mp3"
))

# Generate with subtitles
async def generate_with_subtitles(text: str, voice: str, audio_file: str, subtitle_file: str):
    communicate = edge_tts.Communicate(text, voice)
    
    submaker = edge_tts.SubMaker()
    
    with open(audio_file, "wb") as audio:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
    
    with open(subtitle_file, "w", encoding="utf-8") as srt:
        srt.write(submaker.generate_srt())

asyncio.run(generate_with_subtitles(
    text=text,
    voice="th-TH-NiwatNeural",
    audio_file="voiceover.mp3",
    subtitle_file="voiceover.srt"
))
```

**List Available Voices:**

```bash
edge-tts --list-voices | grep th-TH
```

---

### MoviePy (Video Composition)

**Overview:**
MoviePy เป็น Python library สำหรับ video editing: cuts, concatenations, text overlays, compositing

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 Documentation | https://zulko.github.io/moviepy/ |
| 📦 GitHub | https://github.com/Zulko/moviepy |
| 📦 PyPI | https://pypi.org/project/moviepy/ |
| 📖 User Guide | https://zulko.github.io/moviepy/user_guide/index.html |

**Installation:**

```bash
pip install moviepy

# Also need FFmpeg (usually auto-installed)
# Ubuntu: sudo apt-get install ffmpeg
# Mac: brew install ffmpeg
```

**Quick Start Code:**

```python
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# Load video
clip = VideoFileClip("raw_video.mp4")

# Basic operations
clip = clip.subclipped(10, 30)  # Cut from 10s to 30s
clip = clip.with_volume_scaled(0.8)  # Reduce volume to 80%
clip = clip.resized(width=1080)  # Resize

# Add text overlay
txt_clip = TextClip(
    text="CoffeeLab - Premium Coffee",
    font="Arial.ttf",
    font_size=70,
    color='white',
    bg_color='black',
    size=(1080, None)
)
txt_clip = txt_clip.with_position('center').with_duration(5)

# Composite
final = CompositeVideoClip([clip, txt_clip])

# Add audio
audio = AudioFileClip("voiceover.mp3")
final = final.with_audio(audio)

# Export
final.write_videofile(
    "output.mp4",
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

# Concatenate multiple clips
clips = [
    VideoFileClip("intro.mp4"),
    VideoFileClip("content.mp4"),
    VideoFileClip("outro.mp4"),
]
final = concatenate_videoclips(clips, method="compose")
final.write_videofile("full_video.mp4")
```

**Common Operations:**

```python
# Fade in/out
clip = clip.with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])

# Speed up/slow down
clip = clip.with_speed_scaled(1.5)  # 1.5x speed

# Crop
clip = clip.cropped(x1=100, y1=100, x2=800, y2=600)

# Rotate
clip = clip.rotated(90)

# Mirror
clip = clip.with_effects([vfx.MirrorX()])
```

---

### Pillow (Image Processing)

**Overview:**
Pillow เป็น Python library สำหรับ image processing

**Official Documentation:**

| Resource | Link |
|----------|------|
| 📖 Documentation | https://pillow.readthedocs.io/ |
| 📦 GitHub | https://github.com/python-pillow/Pillow |
| 📦 PyPI | https://pypi.org/project/pillow/ |

**Quick Start Code:**

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Open image
img = Image.open("input.jpg")

# Resize
img = img.resize((1080, 1080))

# Add text
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("Arial.ttf", 60)
draw.text((100, 100), "CoffeeLab", fill="white", font=font)

# Apply filter
img = img.filter(ImageFilter.GaussianBlur(radius=2))

# Save
img.save("output.jpg", quality=95)
```

---

## ☁️ Infrastructure Documentation

### GitHub Codespaces

**Overview:**
GitHub Codespaces ให้ cloud development environment ฟรี 120 ชม./เดือน

**Free Tier Limits:**
- 120 core-hours/month
- 15GB storage/month
- 2-core, 8GB RAM default

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 Codespaces | https://github.com/features/codespaces |
| 📖 Quickstart | https://docs.github.com/en/codespaces/getting-started/quickstart |
| 📖 Billing | https://docs.github.com/en/billing/managing-billing-for-github-codespaces |

**Tips:**
1. ใช้ 2-core machine (ประหยัด hours)
2. Stop codespace เมื่อไม่ใช้
3. Set auto-stop timeout (30 mins)
4. ใช้ `.devcontainer.json` สำหรับ setup

**devcontainer.json Example:**

```json
{
  "name": "AI Director",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "pip install -r requirements.txt",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "GitHub.copilot"
      ]
    }
  }
}
```

---

### Google Colab

**Overview:**
Google Colab ให้ free GPU (T4) สำหรับ training

**Free Tier:**
- GPU: Tesla T4 (15GB VRAM)
- Runtime: ~12 hours max
- Storage: Save to Google Drive

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 Colab | https://colab.research.google.com/ |
| 📖 FAQ | https://research.google.com/colaboratory/faq.html |

**Tips:**

```python
# Check GPU
!nvidia-smi

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Save model to Drive
model.save_pretrained('/content/drive/MyDrive/models/ai_director')

# Install packages
!pip install transformers peft accelerate bitsandbytes

# Keep session alive (run in separate cell)
import time
while True:
    time.sleep(60)
```

---

### Hugging Face Spaces (Deployment)

**Overview:**
HF Spaces ให้ free hosting สำหรับ Gradio apps

**Free Tier:**
- CPU: 2 vCPU
- RAM: 16GB
- Storage: Ephemeral
- Auto-sleep: After inactivity

**Official Documentation:**

| Resource | Link |
|----------|------|
| 🏠 Spaces | https://huggingface.co/spaces |
| 📖 Gradio Spaces | https://huggingface.co/docs/hub/en/spaces-sdks-gradio |
| 📖 Using HF Integrations | https://www.gradio.app/guides/using-hugging-face-integrations |

**Quick Deploy:**

1. Create new Space at https://huggingface.co/new-space
2. Select Gradio SDK
3. Create `app.py` and `requirements.txt`
4. Push files

**app.py Example:**

```python
import gradio as gr
from transformers import pipeline

# Load model
pipe = pipeline("text-generation", model="your-model")

def generate(prompt):
    result = pipe(prompt, max_length=200)
    return result[0]["generated_text"]

# Create interface
demo = gr.Interface(
    fn=generate,
    inputs=gr.Textbox(label="Brief", lines=5),
    outputs=gr.Textbox(label="Output", lines=10),
    title="AI Director",
    description="Generate marketing content"
)

if __name__ == "__main__":
    demo.launch()
```

**requirements.txt:**

```
gradio
transformers
torch
```

---

## 📖 Tutorials & Example Notebooks

### End-to-End RAG Examples

| Notebook | Description | Link |
|----------|-------------|------|
| RAG with ChromaDB | Basic RAG implementation | [DataCamp Tutorial](https://www.datacamp.com/tutorial/chromadb-tutorial-step-by-step-guide) |
| RAG with Ollama | Local LLM RAG | [Medium Article](https://medium.com/@arunpatidar26/rag-chromadb-ollama-python-guide-for-beginners-30857499d0a0) |
| LlamaIndex + ChromaDB | Production RAG | [Dev.to Tutorial](https://dev.to/sophyia/how-to-build-a-rag-solution-with-llama-index-chromadb-and-ollama-20lb) |
| LangChain + Chroma | LangChain integration | [LangChain Docs](https://docs.langchain.com/oss/python/integrations/vectorstores/chroma) |

### LoRA Fine-Tuning Notebooks

| Notebook | Description | Link |
|----------|-------------|------|
| Fine-tune LLM with PEFT | Comprehensive guide | [HF Blog](https://huggingface.co/blog/dvgodoy/fine-tuning-llm-hugging-face) |
| QLoRA on T4 | Free Colab training | [Phil Schmid](https://www.philschmid.de/fine-tune-llms-in-2025) |
| FunctionGemma Fine-tune | Tool calling | [Unsloth Notebooks](https://docs.unsloth.ai/models/functiongemma) |
| Gemma 3 Fine-tune | Vision + Text | [Unsloth Guide](https://docs.unsloth.ai/models/gemma-3-how-to-run-and-fine-tune) |
| DreamBooth LoRA | Stable Diffusion | [PEFT Guide](https://huggingface.co/docs/peft/main/en/task_guides/dreambooth_lora) |

### Multi-Modal Prompting Guides

| Resource | Description | Link |
|----------|-------------|------|
| T5Gemma 2 Usage | Image + Text prompting | [HF Model Card](https://huggingface.co/google/t5gemma-2-1b-1b) |
| PaliGemma Guide | Vision-Language | [Google AI](https://ai.google.dev/gemma/docs/paligemma) |
| Gemini Multimodal | API examples | [Google AI Docs](https://ai.google.dev/gemini-api/docs/vision) |

---

## 🇹🇭 Thai Language Best Practices

### Recommended Models for Thai

| Task | Model | Notes |
|------|-------|-------|
| **Text Generation** | Qwen 2.5-7B | Strong Thai support |
| **Embeddings** | paraphrase-multilingual-MiniLM-L12-v2 | Good for Thai RAG |
| **TTS** | th-TH-NiwatNeural / th-TH-PremwadeeNeural | Edge-TTS voices |
| **Transcription** | Whisper (base/small) | Decent Thai accuracy |
| **Translation** | Helsinki-NLP/opus-mt-th-en | Thai ↔ English |

### Thai Text Processing Tips

```python
# Thai word segmentation
from pythainlp.tokenize import word_tokenize

text = "สวัสดีครับวันนี้อากาศดีมาก"
tokens = word_tokenize(text, engine="newmm")
print(tokens)  # ['สวัสดี', 'ครับ', 'วันนี้', 'อากาศ', 'ดี', 'มาก']

# Thai sentence segmentation
from pythainlp.tokenize import sent_tokenize

text = "วันนี้อากาศดีมาก ไปเที่ยวกันเถอะ"
sentences = sent_tokenize(text)

# Thai spell check
from pythainlp.spell import spell

misspelled = "สวัดดี"
corrections = spell(misspelled)
```

### Prompt Engineering for Thai

```python
# Good: Be specific about language
prompt = """
คุณเป็นผู้เชี่ยวชาญด้านการตลาดในประเทศไทย
ช่วยเขียน copy โฆษณาสำหรับแบรนด์กาแฟ CoffeeLab
กลุ่มเป้าหมาย: คนทำงานออฟฟิศ อายุ 25-35 ปี
โทนเสียง: เป็นกันเอง แต่ดูพรีเมียม
ความยาว: 100-150 คำ
"""

# Include examples (few-shot)
prompt = """
ตัวอย่าง copy โฆษณาที่ดี:
- "เริ่มต้นเช้าวันใหม่ด้วยกาแฟที่ใช่ CoffeeLab Cold Brew"
- "ทุกหยดคือความพิถีพิถัน จาก bean ถึง cup"

เขียน copy โฆษณาใหม่สำหรับโปรโมชั่น...
"""
```

---

## 🔧 Troubleshooting Guide

### Common Issues

#### 1. CUDA Out of Memory

```python
# Solution 1: Use 4-bit quantization
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModel.from_pretrained("...", quantization_config=bnb_config)

# Solution 2: Reduce batch size
training_args = TrainingArguments(per_device_train_batch_size=2)

# Solution 3: Gradient checkpointing
model.gradient_checkpointing_enable()
```

#### 2. Colab Session Disconnect

```python
# Keep session alive
import time
from IPython.display import display, Javascript

def keep_alive():
    display(Javascript('function Click(){document.querySelector("colab-connect-button").click()}setInterval(Click, 60000)'))

keep_alive()
```

#### 3. MongoDB Connection Issues

```python
# Check connection
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("Connected!")
except ConnectionFailure:
    print("Failed to connect. Check:")
    print("1. IP whitelist (0.0.0.0/0 for dev)")
    print("2. Username/password")
    print("3. Network connectivity")
```

#### 4. Edge-TTS Rate Limiting

```python
# Add delay between requests
import asyncio

async def generate_batch(texts, voice, output_dir):
    for i, text in enumerate(texts):
        await generate_voice(text, voice, f"{output_dir}/audio_{i}.mp3")
        await asyncio.sleep(1)  # 1 second delay
```

#### 5. FFmpeg Not Found

```bash
# Ubuntu/Codespaces
sudo apt-get update && sudo apt-get install -y ffmpeg

# Mac
brew install ffmpeg

# Check installation
ffmpeg -version
```

---

## 📊 Quick Reference Cards

### API Keys Required

| Service | Get Key At | Env Variable |
|---------|------------|--------------|
| Hugging Face | https://huggingface.co/settings/tokens | `HF_TOKEN` |
| Google Gemini | https://aistudio.google.com/apikey | `GEMINI_API_KEY` |
| MongoDB Atlas | Atlas Dashboard | `MONGO_URI` |

### Model Loading Cheatsheet

```python
# T5Gemma 2
from transformers import AutoProcessor, AutoModelForSeq2SeqLM
processor = AutoProcessor.from_pretrained("google/t5gemma-2-1b-1b")
model = AutoModelForSeq2SeqLM.from_pretrained("google/t5gemma-2-1b-1b")

# FunctionGemma (with Unsloth)
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained("unsloth/functiongemma-270m-it")

# With LoRA
from peft import PeftModel, LoraConfig, get_peft_model
lora_config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
model = get_peft_model(model, lora_config)

# 4-bit Quantization
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
model = AutoModel.from_pretrained("...", quantization_config=bnb_config)
```

### Common pip Installs

```bash
# Core
pip install transformers torch accelerate

# Fine-tuning
pip install peft bitsandbytes trl datasets

# Optimization
pip install ax-platform botorch

# Vector DB
pip install chromadb pymongo

# Production Tools
pip install edge-tts moviepy pillow

# Smart Cut
pip install openai-whisper ffmpeg-python pydub

# Deployment
pip install gradio
```

---

## 🎯 Success Metrics

| Metric | Target |
|--------|--------|
| Strategy generation (T5Gemma 2) | < 30s |
| Tool calling (FunctionGemma) | < 1s per call |
| Tool calling accuracy | ≥ 85% |
| Prompt quality | 1000+ chars |
| Total pipeline | < 5 min |
| Transcription speed | < 0.5x realtime |
| Auto trim | < 1 min per 10 min video |
| **Cost** | **$0.00** |

---

## 📚 Additional Resources

### Official Documentation Hub

| Category | Links |
|----------|-------|
| **Models** | [T5Gemma 2](https://huggingface.co/collections/google/t5gemma-2) • [FunctionGemma](https://huggingface.co/google/functiongemma-270m-it) • [Gemini API](https://ai.google.dev/) |
| **Training** | [PEFT](https://huggingface.co/docs/peft) • [Unsloth](https://docs.unsloth.ai/) • [Meta Ax](https://ax.dev/) |
| **Data** | [MongoDB Atlas](https://www.mongodb.com/docs/atlas/) • [ChromaDB](https://docs.trychroma.com/) • [HF Datasets](https://huggingface.co/docs/datasets) |
| **Production** | [MoviePy](https://zulko.github.io/moviepy/) • [Edge-TTS](https://github.com/rany2/edge-tts) • [Whisper](https://github.com/openai/whisper) |
| **Deploy** | [HF Spaces](https://huggingface.co/docs/hub/spaces) • [Gradio](https://www.gradio.app/) |

### Community Resources

| Resource | Link |
|----------|------|
| Hugging Face Forum | https://discuss.huggingface.co/ |
| Unsloth Discord | https://discord.gg/unsloth |
| MoviePy Reddit | https://www.reddit.com/r/moviepy/ |

---

**🎬 AI Director v3.4 - Complete Documentation Edition**

**New in v3.4:**
- 📚 Comprehensive documentation for all components
- 🔗 Official links to documentation
- 📖 Tutorial notebooks and examples
- 🇹🇭 Thai language best practices
- 🔧 Troubleshooting guide
- 📊 Quick reference cards

**Zero Cost Stack ยังคงเดิม: $0.00**

**Happy Directing! 🚀**
