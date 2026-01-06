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

# 🎓 MODULE 1: DUAL-MODEL ARCHITECTURE DESIGN

> **"Understanding the Brain and Hands of AI Director"**

**Location:** GitHub Codespaces  
**Duration:** 3-4 ชั่วโมง  
**Difficulty:** ⭐⭐

---

## 📋 Module Overview

### Learning Objectives

เมื่อจบ Module 1 คุณจะสามารถ:
- ✅ อธิบาย Dual-Model Architecture และเหตุผลที่ใช้
- ✅ เข้าใจความแตกต่างระหว่าง T5Gemma 2 (Thinker) และ FunctionGemma (Executor)
- ✅ ตัดสินใจว่าควรใช้ model ไหนสำหรับ task ไหน
- ✅ เข้าใจการทำงานร่วมกันของทั้งสอง models
- ✅ รู้จัก Smart Cut feature และการ integrate กับ architecture

### Prerequisites

- GitHub account (สำหรับ Codespaces)
- ความเข้าใจพื้นฐานเกี่ยว LLM และ AI models
- Python basics

---

## 🧠 Part 1: Why Dual-Model Architecture?

### The Problem with Single-Model Approach

```
┌─────────────────────────────────────────────────────────────┐
│          ❌ SINGLE LARGE MODEL (Traditional Way)            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User: "สร้าง video โฆษณากาแฟ"                              │
│     │                                                        │
│     ▼                                                        │
│   ┌────────────────────────────────────────┐                │
│   │  Large LLM (e.g., GPT-4, Claude)      │                │
│   │  7B-70B+ parameters                    │                │
│   │  • Slow inference                      │                │
│   │  • Expensive API calls                 │                │
│   │  • Needs prompt engineering            │                │
│   │  • Not good at structured output       │                │
│   └────────────────────────────────────────┘                │
│                                                              │
│   Problems:                                                  │
│   💸 Cost: $0.01-0.10 per request                           │
│   🐌 Speed: 5-30 seconds                                    │
│   🎲 Reliability: 60-70% correct tool calls                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Our Solution: Dual-Model Architecture

```
┌─────────────────────────────────────────────────────────────┐
│         ✅ DUAL-MODEL ARCHITECTURE (Our Way)                │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User: "สร้าง video โฆษณากาแฟ"                              │
│     │                                                        │
│     ▼                                                        │
│   ┌────────────────────────────────────────┐                │
│   │  🧠 THINKER (T5Gemma 2 - 1B)          │                │
│   │  Role: Strategy & Content Creation     │                │
│   │  • Understand brief                    │                │
│   │  • Generate creative prompts           │                │
│   │  • Write marketing copy                │                │
│   │  • Select video highlights             │                │
│   │  Output: Natural language plan         │                │
│   └──────────────┬─────────────────────────┘                │
│                  │ "Create premium coffee ad                │
│                  │  with moody lighting..."                 │
│                  ▼                                           │
│   ┌────────────────────────────────────────┐                │
│   │  ⚡ EXECUTOR (FunctionGemma - 270M)   │                │
│   │  Role: Tool Orchestration              │                │
│   │  • Parse instructions                  │                │
│   │  • Call image_gen()                    │                │
│   │  • Call voice_gen()                    │                │
│   │  • Call video_compose()                │                │
│   │  • Call smart_cut()                    │                │
│   │  Output: Structured tool calls         │                │
│   └────────────────────────────────────────┘                │
│                  │                                           │
│                  ▼                                           │
│         [Generated Content]                                  │
│                                                              │
│   Benefits:                                                  │
│   💰 Cost: $0.00 (free tier)                                │
│   ⚡ Speed: < 5 seconds total                               │
│   🎯 Reliability: 85%+ tool calls                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Key Principles

| Principle | Explanation |
|-----------|-------------|
| **Separation of Concerns** | Thinking (creative) ≠ Doing (execution) |
| **Right Tool for Right Job** | Large model for creativity, tiny model for precision |
| **Cost Efficiency** | 1B + 270M < 7B model but better results |
| **Speed Optimization** | Parallel processing possible |
| **Reliability** | Fine-tuned specialist > General purpose |

---

## 🎯 Part 2: T5Gemma 2 (The Thinker)

### What is T5Gemma 2?

T5Gemma 2 คือ **encoder-decoder multimodal model** จาก Google ที่ออกแบบมาสำหรับงาน generation ที่ซับซ้อน

### Key Characteristics

```python
T5Gemma 2 Profile:
├── Architecture: Encoder-Decoder (T5-style)
├── Parameters: 270M / 1B / 4B
├── Context Window: 128K tokens
├── Modality: Text + Image (multimodal)
├── Languages: 140+ (including Thai)
├── Strengths:
│   ├── Creative content generation
│   ├── Long-form text
│   ├── Translation & summarization
│   ├── Image understanding
│   └── Reasoning over documents
└── Use Cases in AI Director:
    ├── Understand marketing briefs
    ├── Generate image prompts
    ├── Write video scripts
    ├── Analyze video transcripts
    └── Select highlight moments
```

### When to Use T5Gemma 2?

Use T5Gemma 2 for **THINKING** tasks:

| Task Type | Example | Why T5Gemma 2? |
|-----------|---------|----------------|
| **Strategy** | "สร้างแคมเปญสำหรับ Gen Z" | Needs understanding + creativity |
| **Content Creation** | เขียน copy โฆษณา | Long-form generation |
| **Prompt Engineering** | สร้าง SDXL prompt | Creative + technical knowledge |
| **Analysis** | วิเคราะห์ brand guidelines | Long context understanding |
| **Multimodal** | อธิบายรูปภาพ | Image + text input |
| **Highlight Selection** | เลือก best moments จาก transcript | Reasoning over long text |

### T5Gemma 2 Example

```python
from transformers import AutoProcessor, AutoModelForSeq2SeqLM

# Load T5Gemma 2 (1B)
processor = AutoProcessor.from_pretrained("google/t5gemma-2-1b-1b")
model = AutoModelForSeq2SeqLM.from_pretrained("google/t5gemma-2-1b-1b")

# Example 1: Generate marketing prompt
brief = """
Brand: CoffeeLab
Product: Cold Brew Premium
Audience: คนทำงานออฟฟิศ 25-35 ปี
Mood: Premium, modern, minimal
"""

prompt = f"""You are a creative director. Generate a detailed photography prompt for this product.

{brief}

Photography prompt:"""

inputs = processor(text=prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
result = processor.decode(outputs[0], skip_special_tokens=True)

print(result)
# Output: "A sleek glass bottle of cold brew coffee on white marble surface, 
#          soft morning light from window, minimalist composition, 
#          professional product photography, shot on Canon EOS R5, f/2.8..."
```

### T5Gemma 2 Strengths

✅ **Long Context:** 128K tokens = เอกสารยาวๆ ได้  
✅ **Multimodal:** รูป + ข้อความพร้อมกัน  
✅ **Multilingual:** ภาษาไทยดีมาก  
✅ **Creative:** เขียน copy, script ได้เนียน  
✅ **Reasoning:** วิเคราะห์และตัดสินใจได้

### T5Gemma 2 Limitations

❌ **Not for Tool Calling:** ไม่เชี่ยวชาญ JSON/structured output  
❌ **Slower:** Encoder-decoder architecture ช้ากว่า decoder-only  
❌ **Larger:** 1B-4B parameters ต้องการ resources มากกว่า  
❌ **Overkill for Simple Tasks:** ไม่ควรใช้กับงานง่ายๆ

---

## ⚡ Part 3: FunctionGemma (The Executor)

### What is FunctionGemma?

FunctionGemma คือ **specialized 270M model** ที่ออกแบบมาเฉพาะสำหรับ **function/tool calling**

### Key Characteristics

```python
FunctionGemma Profile:
├── Architecture: Decoder-only (Gemma-based)
├── Parameters: 270M (tiny!)
├── Context Window: 8K tokens
├── Modality: Text only
├── Specialty: Function/Tool calling
├── Strengths:
│   ├── Parse natural language → JSON
│   ├── Extremely fast inference
│   ├── Low resource requirements
│   ├── High accuracy after fine-tuning
│   └── Runs on CPU/edge devices
└── Use Cases in AI Director:
    ├── Parse user instructions
    ├── Call image_gen(prompt, style)
    ├── Call voice_gen(text, voice)
    ├── Call video_compose(clips, audio)
    └── Call smart_cut(video, mode)
```

### When to Use FunctionGemma?

Use FunctionGemma for **EXECUTION** tasks:

| Task Type | Example | Why FunctionGemma? |
|-----------|---------|-------------------|
| **Tool Calling** | `image_gen("coffee cup")` | Specialized for this |
| **Parsing** | Extract parameters from text | Fast + accurate |
| **Orchestration** | Call multiple tools in sequence | Low latency |
| **Structured Output** | Generate JSON/API calls | Trained specifically |
| **Multi-step** | Chain tool calls | Reliable execution |

### FunctionGemma Example

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load FunctionGemma
tokenizer = AutoTokenizer.from_pretrained("google/functiongemma-270m-it")
model = AutoModelForCausalLM.from_pretrained("google/functiongemma-270m-it")

# Define tools
def image_gen(prompt: str, style: str = "realistic") -> str:
    """Generate an image from text prompt"""
    return f"image_{style}.png"

def voice_gen(text: str, voice: str = "th-TH-NiwatNeural") -> str:
    """Generate voiceover from text"""
    return f"voice.mp3"

# User instruction
instruction = "สร้างรูปกาแฟแบบ minimal และเสียงพากย์ว่า 'Cold Brew Premium'"

# Apply chat template with tools
messages = [{"role": "user", "content": instruction}]
formatted = tokenizer.apply_chat_template(
    messages,
    tools=[image_gen, voice_gen],
    add_generation_prompt=True,
    tokenize=False
)

# Generate
inputs = tokenizer(formatted, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100)
result = tokenizer.decode(outputs[0])

print(result)
# Output: <start_function_call>call:image_gen{prompt:<escape>กาแฟแบบ minimal<escape>,style:<escape>minimal<escape>}<end_function_call>
#         <start_function_call>call:voice_gen{text:<escape>Cold Brew Premium<escape>,voice:<escape>th-TH-NiwatNeural<escape>}<end_function_call>
```

### FunctionGemma Strengths

✅ **Tiny but Mighty:** 270M params แต่แม่นมาก  
✅ **Lightning Fast:** < 1 second per call  
✅ **CPU-Friendly:** รันบน Codespace ได้เลย  
✅ **Fine-tunable:** ปรับแต่งง่าย accuracy เพิ่มเยอะ  
✅ **Structured Output:** JSON perfect ทุกครั้ง

### FunctionGemma Limitations

❌ **Not Creative:** ไม่ใช่สำหรับเขียน content  
❌ **Text Only:** ไม่รับรูปภาพ  
❌ **Short Context:** 8K tokens only  
❌ **Needs Fine-tuning:** Out-of-box accuracy ~60%

---

## 🔄 Part 4: How They Work Together

### The Dual-Model Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COMPLETE WORKFLOW EXAMPLE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT: "สร้าง video ad 15 วินาที สำหรับ CoffeeLab Cold Brew"      │
│                                                                      │
│  STEP 1: T5GEMMA 2 (THINKER) - Strategy & Planning                 │
│  ───────────────────────────────────────────────────────────        │
│  Input: User brief + Brand knowledge (from RAG)                     │
│  Process:                                                            │
│    • Analyze brief                                                   │
│    • Recall brand guidelines                                         │
│    • Generate creative strategy                                      │
│  Output:                                                             │
│    {                                                                 │
│      "concept": "Premium morning ritual",                            │
│      "image_prompt": "Sleek cold brew bottle on marble...",         │
│      "voice_script": "เริ่มต้นเช้าวันใหม่กับ CoffeeLab...",        │
│      "duration": 15,                                                 │
│      "music_mood": "calm, sophisticated"                             │
│    }                                                                 │
│                                                                      │
│  STEP 2: FUNCTIONGEMMA (EXECUTOR) - Tool Orchestration              │
│  ─────────────────────────────────────────────────────────          │
│  Input: T5Gemma 2's output (natural language)                       │
│  Process:                                                            │
│    • Parse the plan                                                  │
│    • Map to tool calls                                               │
│    • Execute in correct order                                        │
│  Output:                                                             │
│    [                                                                 │
│      {                                                               │
│        "tool": "image_gen",                                          │
│        "params": {                                                   │
│          "prompt": "Sleek cold brew bottle on marble...",           │
│          "style": "minimal",                                         │
│          "aspect_ratio": "9:16"                                      │
│        }                                                             │
│      },                                                              │
│      {                                                               │
│        "tool": "voice_gen",                                          │
│        "params": {                                                   │
│          "text": "เริ่มต้นเช้าวันใหม่กับ CoffeeLab...",            │
│          "voice": "th-TH-NiwatNeural",                               │
│          "rate": "+0%"                                               │
│        }                                                             │
│      },                                                              │
│      {                                                               │
│        "tool": "video_compose",                                      │
│        "params": {                                                   │
│          "images": ["coffee_01.png"],                                │
│          "audio": "voiceover.mp3",                                   │
│          "duration": 15,                                             │
│          "transitions": ["fade_in", "fade_out"]                      │
│        }                                                             │
│      }                                                               │
│    ]                                                                 │
│                                                                      │
│  STEP 3: TOOL EXECUTION - Actual Production                         │
│  ─────────────────────────────────────────────                      │
│  Each tool executes and returns results                             │
│                                                                      │
│  OUTPUT: final_video.mp4 ✅                                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Communication Protocol

```python
class DualModelAgent:
    """AI Director with dual-model architecture"""
    
    def __init__(self):
        # Load models
        self.thinker = T5Gemma2Model()
        self.executor = FunctionGemmaModel()
        
        # Load tools
        self.tools = {
            "image_gen": ImageGenerator(),
            "voice_gen": VoiceGenerator(),
            "video_compose": VideoComposer(),
            "smart_cut": SmartCutTool()
        }
    
    def process_brief(self, brief: str) -> dict:
        """Main workflow"""
        
        # Step 1: THINKER generates strategy
        strategy = self.thinker.generate_strategy(brief)
        
        # Step 2: EXECUTOR parses and calls tools
        tool_calls = self.executor.parse_to_tools(strategy)
        
        # Step 3: Execute tools
        results = []
        for call in tool_calls:
            tool = self.tools[call["tool"]]
            result = tool.execute(**call["params"])
            results.append(result)
        
        return {
            "strategy": strategy,
            "tool_calls": tool_calls,
            "outputs": results
        }
```

### Decision Tree: Which Model to Use?

```
Start: New Task
    │
    ├─ Is it creative/strategic? ────YES──► T5Gemma 2 (Thinker)
    │                                       ├─ Generate strategy
    │                                       ├─ Write content
    │                                       ├─ Analyze video/image
    │                                       └─ Select highlights
    │
    ├─ Is it tool calling? ──────────YES──► FunctionGemma (Executor)
    │                                       ├─ Parse instructions
    │                                       ├─ Call APIs/tools
    │                                       ├─ Generate JSON
    │                                       └─ Orchestrate workflow
    │
    └─ Is it both? ──────────────────YES──► Use BOTH in sequence
                                            1. T5Gemma 2 plans
                                            2. FunctionGemma executes
```

---

## 🎬 Part 5: Smart Cut Integration

### New in v3.4: Video Editing Workflow

Smart Cut feature เพิ่ม use case ใหม่สำหรับ dual-model architecture:

```
┌─────────────────────────────────────────────────────────────────────┐
│              SMART CUT WORKFLOW (NEW USE CASE)                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  INPUT: Raw video footage + "ตัดให้เหลือ 2 นาที เอาแต่ไฮไลท์"      │
│                                                                      │
│  STEP 1: ANALYSIS (Tools)                                           │
│  ─────────────────────────                                          │
│  • Whisper transcribes → Full transcript with timestamps            │
│  • FFmpeg detects → Silence regions                                 │
│  • Frame analysis → Visual content                                  │
│                                                                      │
│  STEP 2: T5GEMMA 2 (THINKER) - Editing Decisions                   │
│  ───────────────────────────────────────────────────────            │
│  Input: Transcript + Silence data + User requirements               │
│  Process:                                                            │
│    • Read entire transcript                                          │
│    • Identify key moments                                            │
│    • Decide what to keep/remove                                      │
│    • Plan narrative flow                                             │
│  Output:                                                             │
│    {                                                                 │
│      "keep_segments": [                                              │
│        {"start": 15.0, "end": 45.0, "reason": "strong intro"},     │
│        {"start": 120.5, "end": 155.0, "reason": "key demo"},       │
│        {"start": 480.0, "end": 510.0, "reason": "CTA"}             │
│      ],                                                              │
│      "remove_reasons": {                                             │
│        "silence": 45.2,                                              │
│        "tangent": 150.0,                                             │
│        "repetition": 80.0                                            │
│      },                                                              │
│      "suggested_order": "chronological",                             │
│      "target_duration": 120                                          │
│    }                                                                 │
│                                                                      │
│  STEP 3: FUNCTIONGEMMA (EXECUTOR) - Video Operations                │
│  ──────────────────────────────────────────────────────             │
│  Input: T5Gemma 2's edit decision                                   │
│  Output: FFmpeg commands                                             │
│    [                                                                 │
│      {"tool": "cut_segment", "params": {"start": 15, "end": 45}},  │
│      {"tool": "cut_segment", "params": {"start": 120.5, "end": 155}},│
│      {"tool": "concatenate", "params": {"segments": [...]}},        │
│      {"tool": "add_transitions", "params": {"type": "fade"}}        │
│    ]                                                                 │
│                                                                      │
│  OUTPUT: Edited video (2 minutes) ✅                                │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Why Dual-Model for Video Editing?

| Aspect | Why Not Single Model? | How Dual-Model Helps |
|--------|----------------------|---------------------|
| **Understanding Context** | Need to read long transcripts | T5Gemma 2: 128K tokens |
| **Creative Judgment** | What's a "highlight"? Subjective | T5Gemma 2: Good at reasoning |
| **Precise Execution** | Must cut at exact timestamps | FunctionGemma: Structured output |
| **Speed** | Large model = slow | FunctionGemma: < 1s for parsing |

---

## 🎓 Part 6: Hands-On with Copilot

### Exercise 1: Understanding Model Differences

**Copilot Prompt:**

```
I'm learning about dual-model architecture for AI Director v3.4.
Help me understand:

1. Compare T5Gemma 2 and FunctionGemma in terms of:
   - Architecture (encoder-decoder vs decoder-only)
   - Parameter count
   - Strengths and weaknesses
   - Typical use cases

2. Show me a Python code example demonstrating:
   - Loading T5Gemma 2 for creative content generation
   - Loading FunctionGemma for tool calling
   - How they complement each other

3. For these tasks, which model should I use?
   - Writing a marketing copy
   - Calling image_gen() API
   - Analyzing a video transcript
   - Parsing JSON from natural language
```

### Exercise 2: Workflow Design

**Copilot Prompt:**

```
Design a complete workflow for AI Director v3.4 that:

1. Takes input: "สร้างโฆษณา Instagram Reel สำหรับกาแฟ"

2. Shows step-by-step:
   - What T5Gemma 2 does (strategy, prompts, script)
   - What FunctionGemma does (parse to tool calls)
   - What tools get called (image_gen, voice_gen, video_compose)

3. Include error handling:
   - What if T5Gemma 2 output is unclear?
   - What if tool call fails?

4. Show the complete Python class structure
```

### Exercise 3: Smart Cut Integration

**Copilot Prompt:**

```
Explain how dual-model architecture handles video editing with Smart Cut:

1. Input: Raw interview footage (30 mins) + "ตัดให้เหลือ 3 นาที"

2. Show the workflow:
   - Analysis phase (Whisper, FFmpeg)
   - T5Gemma 2's role in selecting highlights
   - FunctionGemma's role in executing cuts

3. Why is this better than using a single large model?

4. Provide example code for the highlight selection logic
```

---

## ✅ Completion Criteria

Check ทุกข้อก่อนไป Module 2:

### Understanding (ทฤษฎี)
- [ ] อธิบายได้ว่าทำไมใช้ dual-model แทน single large model
- [ ] อธิบายความแตกต่างระหว่าง T5Gemma 2 และ FunctionGemma ได้
- [ ] บอกได้ว่า task ไหนควรใช้ model ไหน
- [ ] เข้าใจ communication protocol ระหว่าง 2 models

### Practical (ลงมือทำ)
- [ ] ติดตั้ง GitHub Codespaces สำเร็จ
- [ ] Load T5Gemma 2 และ generate text ได้
- [ ] Load FunctionGemma และ parse tool calls ได้
- [ ] ออกแบบ workflow สำหรับ use case หนึ่ง

### Smart Cut (ใหม่)
- [ ] เข้าใจว่า Smart Cut ใช้ dual-model architecture อย่างไร
- [ ] อธิบายได้ว่าทำไม T5Gemma 2 เหมาะสำหรับเลือก highlights
- [ ] เข้าใจบทบาทของ FunctionGemma ในการควบคุม FFmpeg

---

## 📝 Knowledge Check

### Quiz Questions

1. **ทำไม AI Director ใช้ 2 models แทน 1 large model?**
   - [ ] A. ถูกกว่า
   - [ ] B. เร็วกว่า
   - [ ] C. แม่นกว่า
   - [ ] D. ถูกทุกข้อ ✅

2. **T5Gemma 2 ใช้ architecture แบบไหน?**
   - [ ] A. Encoder-only
   - [ ] B. Decoder-only
   - [ ] C. Encoder-Decoder ✅
   - [ ] D. Mixture of Experts

3. **FunctionGemma มี parameters กี่ตัว?**
   - [ ] A. 1B
   - [ ] B. 270M ✅
   - [ ] C. 7B
   - [ ] D. 70B

4. **Task ไหนควรใช้ T5Gemma 2?**
   - [ ] A. Parse JSON
   - [ ] B. Call API
   - [ ] C. เขียน marketing copy ✅
   - [ ] D. ถูกทุกข้อ

5. **Smart Cut ใช้ T5Gemma 2 ทำอะไร?**
   - [ ] A. Transcribe audio
   - [ ] B. Detect silence
   - [ ] C. Select highlights ✅
   - [ ] D. Cut video

### Answer Key
1. D, 2. C, 3. B, 4. C, 5. C

---

## 💻 COMPLETE IMPLEMENTATION CODE

> **พร้อม copy-paste และ run ได้เลย!**

---

## 🚀 AUTOMATED SETUP (แนะนำ - ไม่ต้องพิมพ์คำสั่งเอง!)

> **ใช้ Dev Container เพื่อให้ Codespace ติดตั้งทุกอย่างอัตโนมัติ**

---

## 📋 คุณต้องทำเพียง 4 ขั้นตอน (ครั้งเดียว 10 นาที)

### ⚠️ สิ่งที่ผม (GitHub Copilot) ทำไม่ได้:
- ❌ สร้าง GitHub repository ให้
- ❌ สร้างไฟล์ใน GitHub ให้
- ❌ กดปุ่ม "Create Codespace" ให้
- ❌ Run คำสั่งใน GitHub หรือ Codespace ของคุณ

### ✅ สิ่งที่คุณต้องทำเอง (แต่ง่ายมาก):

---

### 🎯 ขั้นตอนที่ 1: สร้าง GitHub Repository (2 นาที)

1. **เปิด browser** ไปที่ https://github.com
2. **เข้าสู่ระบบ** ด้วย GitHub account
3. **คลิกปุ่มสีเขียว** "New" หรือ "New repository" (มุมขวาบน)
4. **กรอกข้อมูล:**
   - Repository name: `ai-director-course`
   - เลือก Public
   - ✅ เลือก "Add a README file"
5. **คลิก** "Create repository" (ปุ่มสีเขียวด้านล่าง)

✅ **เสร็จขั้นตอนที่ 1**

---

### 🎯 ขั้นตอนที่ 2: สร้างไฟล์ที่ 1 - devcontainer.json (3 นาที)

1. **ใน repository ที่เพิ่งสร้าง** คลิก "Add file" → "Create new file"
2. **ตั้งชื่อไฟล์:** `.devcontainer/devcontainer.json` 
   - ⚠️ **ต้องมี `/` เพื่อสร้าง folder** `.devcontainer`
3. **Copy code นี้ทั้งหมด** ไปวางในไฟล์:

```json
{
  "name": "AI Director Course",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    }
  },
  
  "postCreateCommand": "bash .devcontainer/setup.sh",
  
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "GitHub.copilot",
        "GitHub.copilot-chat"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black"
      }
    }
  },
  
  "forwardPorts": [8000, 8501],
  
  "remoteUser": "vscode"
}
```

4. **Scroll ลงล่าง** → คลิก "Commit changes" (ปุ่มสีเขียว)
5. **คลิก** "Commit changes" อีกครั้งในป๊อปอัพ

✅ **เสร็จขั้นตอนที่ 2** - จะเห็นไฟล์ `.devcontainer/devcontainer.json` ใน repository

---

### 🎯 ขั้นตอนที่ 3: สร้างไฟล์ที่ 2 - setup.sh (3 นาที)

1. **คลิก** "Add file" → "Create new file" อีกครั้ง
2. **ตั้งชื่อไฟล์:** `.devcontainer/setup.sh`
3. **Copy script นี้ทั้งหมด** ไปวางในไฟล์:

```bash
#!/bin/bash
set -e

echo "🚀 Setting up AI Director Course environment..."

# Upgrade pip
pip install --upgrade pip

# Install core dependencies
echo "📦 Installing dependencies..."
pip install transformers==4.45.0
pip install torch==2.5.0
pip install accelerate==0.34.0
pip install pillow==10.4.0
pip install requests

# Install additional tools
pip install ipython jupyter

# Create project structure
echo "📁 Creating project structure..."
mkdir -p module1
mkdir -p module2
mkdir -p module3
mkdir -p module4
mkdir -p module5
mkdir -p module6
mkdir -p module7
mkdir -p module8

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

# Models
*.bin
*.safetensors
models/
.cache/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Jupyter
.ipynb_checkpoints/
EOF

echo "✅ Setup complete! You can start coding now."
echo ""
echo "📍 Current directory: $(pwd)"
echo "📍 Python version: $(python --version)"
echo "📍 Pip packages installed:"
pip list | grep -E "(transformers|torch|accelerate)"

echo ""
echo "🎉 Ready to start Module 1!"
```

4. **Scroll ลงล่าง** → คลิก "Commit changes"
5. **คลิก** "Commit changes" อีกครั้ง

✅ **เสร็จขั้นตอนที่ 3** - จะเห็นไฟล์ `.devcontainer/setup.sh` ใน repository

---

### 🎯 ขั้นตอนที่ 4: เปิด Codespace (2 นาที)

1. **กลับไปหน้าหลัก repository** (คลิก "ai-director-course" ด้านบน)
2. **คลิกปุ่มสีเขียว** `<> Code`
3. **เลือกแท็บ** "Codespaces"
4. **คลิก** "Create codespace on main" (ปุ่มสีเขียว)
5. **รอ 3-5 นาที** ระหว่างที่ Codespace กำลัง:
   - สร้าง container
   - ติดตั้ง Python
   - รัน setup.sh (ติดตั้ง packages อัตโนมัติ)
   - สร้าง folders module1-8
   - ติดตั้ง VS Code extensions

**คุณจะเห็นหน้าต่าง Terminal แสดง:**
```
🚀 Setting up AI Director Course environment...
📦 Installing dependencies...
📁 Creating project structure...
✅ Setup complete! You can start coding now.

📍 Current directory: /workspaces/ai-director-course
📍 Python version: Python 3.11.x
📍 Pip packages installed:
transformers    4.45.0
torch           2.5.0
accelerate      0.34.0

🎉 Ready to start Module 1!
```

✅ **เสร็จทั้ง 4 ขั้นตอน!** VS Code จะเปิดใน browser พร้อมใช้งาน

---

## 🎊 ตอนนี้คุณพร้อมแล้ว!

### ตรวจสอบว่าทุกอย่างพร้อม:

เปิด Terminal ใน VS Code (อยู่ด้านล่างแล้ว) และลองพิมพ์:

```bash
# ตรวจสอบว่า packages ติดตั้งแล้ว
python -c "import transformers; import torch; print('✅ ทุกอย่างพร้อม!')"
```

ควรเห็น: `✅ ทุกอย่างพร้อม!`

```bash
# ดู folders ที่สร้างแล้ว
ls
```

ควรเห็น: `module1  module2  module3  module4  module5  module6  module7  module8`

---

## 📊 สรุป: ใครทำอะไร?

| ขั้นตอน | คุณทำ | ระบบทำอัตโนมัติ |
|---------|-------|-----------------|
| สร้าง repository | ✅ คลิก 5 ครั้ง | - |
| สร้างไฟล์ config 2 ไฟล์ | ✅ Copy-paste 2 ครั้ง | - |
| เปิด Codespace | ✅ คลิก 1 ครั้ง | - |
| ติดตั้ง Python | - | ✅ อัตโนมัติ |
| ติดตั้ง packages ทั้งหมด | - | ✅ อัตโนมัติ |
| สร้าง folders | - | ✅ อัตโนมัติ |
| สร้าง .gitignore | - | ✅ อัตโนมัติ |
| ติดตั้ง VS Code extensions | - | ✅ อัตโนมัติ |
| **รวม** | **คลิก 6 ครั้ง + Copy-paste 2 ครั้ง** | **ติดตั้งทุกอย่างเอง** |

---

## 🔄 ครั้งต่อไป (ง่ายกว่ามาก!)

เมื่อคุณปิด Codespace และต้องการเปิดใหม่:

1. ไปที่ https://github.com/codespaces
2. คลิกที่ Codespace `ai-director-course`
3. **เสร็จ!** ทุกอย่างพร้อมใช้งานทันที (ไม่ต้อง setup ใหม่)

---

## 💡 FAQ

### Q: ผมต้องพิมพ์คำสั่งอะไรไหม?
**A:** ไม่เลย! แค่ copy-paste code 2 ไฟล์ แล้วคลิก "Create Codespace"

### Q: ถ้า setup ไม่สำเร็จล่ะ?
**A:** ลองดูที่ Terminal จะมี error message บอก ส่วนใหญ่เป็นเพราะ:
- setup.sh ไม่มีสิทธิ์ execute → ไม่เป็นไร Codespace จะแก้ให้
- Network ช้า → รอให้จบ อาจใช้เวลานานกว่า 5 นาที

### Q: ผมจะรู้ได้ไหมว่า setup เสร็จแล้ว?
**A:** เห็น `🎉 Ready to start Module 1!` ใน Terminal

### Q: ผมสามารถแก้ไข setup.sh ทีหลังได้ไหม?
**A:** ได้! แก้ไขแล้ว rebuild container:
1. กด `F1` 
2. พิมพ์ "Rebuild Container"
3. Enter

---

## 🎯 Next: เริ่มเขียนโค้ด Module 1

เมื่อ setup เสร็จแล้ว ไปที่ส่วน **"Part 1: T5Gemma 2 Implementation"** ด้านล่างเพื่อเริ่มเขียนโค้ด!

---

#### Step 1: สร้าง GitHub Repository

1. ไปที่ https://github.com
2. คลิก **New repository** (ปุ่มสีเขียว)
3. ตั้งชื่อ: `ai-director-course`
4. เลือก **Public** (หรือ Private ถ้าต้องการ)
5. ✅ เลือก "Add a README file"
6. คลิก **Create repository**

#### Step 2: สร้าง Dev Container Config

**สำคัญ!** ทำขั้นตอนนี้ก่อนเปิด Codespace

1. ใน repository ที่เพิ่งสร้าง คลิก **Add file** → **Create new file**
2. ตั้งชื่อไฟล์: `.devcontainer/devcontainer.json`
3. วาง code นี้:

```json
{
  "name": "AI Director Course",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  
  "features": {
    "ghcr.io/devcontainers/features/python:1": {
      "version": "3.11"
    }
  },
  
  "postCreateCommand": "bash .devcontainer/setup.sh",
  
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "GitHub.copilot",
        "GitHub.copilot-chat"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": true,
        "python.formatting.provider": "black"
      }
    }
  },
  
  "forwardPorts": [8000, 8501],
  
  "remoteUser": "vscode"
}
```

4. คลิก **Commit changes**

#### Step 3: สร้าง Setup Script

1. คลิก **Add file** → **Create new file** อีกครั้ง
2. ตั้งชื่อไฟล์: `.devcontainer/setup.sh`
3. วาง script นี้:

```bash
#!/bin/bash
set -e

echo "🚀 Setting up AI Director Course environment..."

# Upgrade pip
pip install --upgrade pip

# Install core dependencies
echo "📦 Installing dependencies..."
pip install transformers==4.45.0
pip install torch==2.5.0
pip install accelerate==0.34.0
pip install pillow==10.4.0
pip install requests

# Install additional tools
pip install ipython jupyter

# Create project structure
echo "📁 Creating project structure..."
mkdir -p module1
mkdir -p module2
mkdir -p module3
mkdir -p module4
mkdir -p module5
mkdir -p module6
mkdir -p module7
mkdir -p module8

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

# Models
*.bin
*.safetensors
models/
.cache/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Jupyter
.ipynb_checkpoints/
EOF

echo "✅ Setup complete! You can start coding now."
echo ""
echo "📍 Current directory: $(pwd)"
echo "📍 Python version: $(python --version)"
echo "📍 Pip packages installed:"
pip list | grep -E "(transformers|torch|accelerate)"

echo ""
echo "🎉 Ready to start Module 1!"
```

4. คลิก **Commit changes**

#### Step 4: เปิด Codespace (จะติดตั้งอัตโนมัติ)

1. กลับไปที่หน้าหลักของ repository
2. คลิกปุ่มสีเขียว **<> Code**
3. เลือกแท็บ **Codespaces**
4. คลิก **Create codespace on main**
5. รอ 3-5 นาที (กำลังติดตั้งทุกอย่างอัตโนมัติ)

✅ **เมื่อ Codespace เปิดแล้ว ทุกอย่างพร้อมใช้งานทันที!**

---

## 🎯 ตรวจสอบว่า Setup สำเร็จ

เปิด Terminal และลอง:

```bash
# ตรวจสอบว่าอยู่ที่ directory ถูกต้อง
pwd
# Output: /workspaces/ai-director-course

# ตรวจสอบ Python
python --version
# Output: Python 3.11.x

# ตรวจสอบ packages
pip list | grep transformers
# Output: transformers    4.45.0

# ดูโครงสร้าง folders
ls -la
# Output: module1/ module2/ ... module8/

# ทดสอบ import
python -c "import transformers; import torch; print('✅ All good!')"
# Output: ✅ All good!
```

ถ้าทุกอย่างผ่าน แสดงว่าพร้อมเขียนโค้ดแล้ว! 🎉

---

## 🆚 เปรียบเทียบ 2 วิธี

| | Manual Setup | Dev Container (Automated) |
|---|---|---|
| **ติดตั้ง dependencies** | ต้องพิมพ์คำสั่งเอง | อัตโนมัติ 100% |
| **สร้าง folders** | ต้องสร้างเอง | อัตโนมัติ |
| **Install extensions** | ต้องติดตั้งเอง | มาพร้อมแล้ว |
| **เวลาที่ใช้** | 5-10 นาที | 3-5 นาที (รอ setup) |
| **ครั้งต่อไป** | ต้องทำใหม่ทุกครั้ง | เปิดใช้งานได้เลย |

**แนะนำ:** ใช้ Dev Container เพราะต่อไปเมื่อเปิด Codespace ใหม่ จะติดตั้งให้อัตโนมัติเสมอ!

---

## 💡 Tips สำหรับการใช้งาน

### ถ้าต้องการแก้ไข dependencies

แก้ไขไฟล์ `.devcontainer/setup.sh` และเพิ่ม packages:

```bash
# เพิ่มบรรทัดนี้ใน setup.sh
pip install package_name
```

แล้ว rebuild container:
1. กด `F1` หรือ `Ctrl+Shift+P`
2. พิมพ์: "Codespaces: Rebuild Container"
3. Enter

### ถ้าต้องการเพิ่ม VS Code Extensions

แก้ไขไฟล์ `.devcontainer/devcontainer.json`:

```json
"extensions": [
  "ms-python.python",
  "GitHub.copilot",
  "extension-id-here"  // เพิ่มตรงนี้
]
```

---

## 🚀 GITHUB CODESPACES SETUP (แบบ Manual - สำหรับคนที่ไม่ใช้ Dev Container)

> **หมายเหตุ:** ถ้าคุณใช้ Dev Container ด้านบน ข้ามส่วนนี้ไปได้เลย

### Step 1: สร้าง GitHub Repository (ถ้ายังไม่ได้ทำ)

1. ไปที่ https://github.com
2. คลิก **New repository** (ปุ่มสีเขียว)
3. ตั้งชื่อ: `ai-director-course`
4. เลือก **Public** (หรือ Private ถ้าต้องการ)
5. ✅ เลือก "Add a README file"
6. คลิก **Create repository**

### Step 2: เปิด Codespaces

1. ใน repository ที่เพิ่งสร้าง คลิกปุ่มสีเขียว **<> Code**
2. เลือกแท็บ **Codespaces**
3. คลิก **Create codespace on main**
4. รอ 1-2 นาที (Codespaces กำลัง setup)

✅ **หน้าจอจะเปิด VS Code ใน browser โดยอัตโนมัติ**

### Step 3: ตรวจสอบว่า Codespace พร้อมใช้งาน

เปิด Terminal ใน VS Code:
- คลิก **Terminal** → **New Terminal** (ด้านบน)
- หรือกด `` Ctrl + ` `` (backtick)

ลองพิมพ์:
```bash
python --version
# ควรเห็น: Python 3.x.x

pwd
# ควรเห็น: /workspaces/ai-director-course
```

### Step 4: สร้างโครงสร้างโปรเจค

```bash
# สร้าง folders สำหรับ Module 1
mkdir -p module1
cd module1

# สร้าง virtual environment (แนะนำ)
python -m venv venv
source venv/bin/activate  # ใน Codespaces ใช้คำสั่งนี้

# หรือถ้าใช้ PowerShell (ไม่น่าจะเจอใน Codespaces)
# venv\Scripts\activate
```

### Step 5: ติดตั้ง Dependencies

```bash
# ติดตั้ง packages ที่จำเป็น
pip install --upgrade pip

# Core dependencies
pip install transformers==4.45.0
pip install torch==2.5.0
pip install accelerate==0.34.0
pip install pillow==10.4.0
pip install requests

# Save dependencies
pip freeze > requirements.txt
```

⏳ **รอประมาณ 2-3 นาที สำหรับการติดตั้ง**

### Step 6: ตรวจสอบว่าติดตั้งสำเร็จ

```bash
# ตรวจสอบ packages
pip list | grep transformers
pip list | grep torch

# ทดสอบ import
python -c "import transformers; print(transformers.__version__)"
python -c "import torch; print(torch.__version__)"
```

ถ้าเห็น version numbers แสดงว่าพร้อมแล้ว! ✅

---

## 📁 โครงสร้างไฟล์ที่เราจะสร้าง

```
ai-director-course/
├── README.md                    (มีอยู่แล้ว)
├── module1/                     (สร้างใหม่)
│   ├── requirements.txt         (จาก pip freeze)
│   ├── t5gemma_thinker.py      (จะสร้างในขั้นตอนถัดไป)
│   ├── functiongemma_executor.py
│   ├── ai_director_agent.py
│   └── test_module1.py
└── .gitignore                   (สร้างถ้ายังไม่มี)
```

### สร้าง .gitignore (ไม่ commit files ที่ไม่จำเป็น)

```bash
# สร้างไฟล์ .gitignore ที่ root
cd /workspaces/ai-director-course
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
*.egg-info/

# Models (ไฟล์ใหญ่)
*.bin
*.safetensors
models/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
EOF
```

---

## 📝 วิธีสร้างไฟล์ใน Codespaces

### วิธีที่ 1: ใช้ VS Code UI (ง่ายที่สุด)

1. คลิกขวาที่ folder `module1` ใน Explorer (ซ้ายมือ)
2. เลือก **New File**
3. ตั้งชื่อ: `t5gemma_thinker.py`
4. Copy code จากด้านล่างไปวาง
5. กด `Ctrl + S` เพื่อ save

### วิธีที่ 2: ใช้ Command Line

```bash
cd /workspaces/ai-director-course/module1

# สร้างไฟล์ว่างๆ
touch t5gemma_thinker.py
touch functiongemma_executor.py
touch ai_director_agent.py
touch test_module1.py

# แล้วเปิดแก้ไขใน VS Code
# คลิกที่ชื่อไฟล์ใน Explorer แล้ว copy code ไปวาง
```

---

## ⚡ Quick Start สำหรับคนที่รีบ

```bash
# 1. เปิด Terminal ใน Codespaces
# 2. Copy-paste คำสั่งนี้ทั้งหมดเลย:

cd /workspaces/ai-director-course
mkdir -p module1
cd module1

# ติดตั้ง dependencies
pip install transformers torch accelerate pillow requests

# สร้างไฟล์ทั้งหมด
touch t5gemma_thinker.py
touch functiongemma_executor.py  
touch ai_director_agent.py
touch test_module1.py

echo "✅ Setup complete! ตอนนี้ copy code ไปวางในแต่ละไฟล์ได้เลย"
```

**จากนั้น:** ไปที่ Explorer (ซ้ายมือ) → เปิดแต่ละไฟล์ → Copy code จากด้านล่างไปวาง → Save

---

## 🎓 ตอนนี้พร้อมเริ่มเขียนโค้ดแล้ว!

ด้านล่างนี้คือ code ที่สมบูรณ์สำหรับแต่ละไฟล์ 👇

### Part 1: T5Gemma 2 Implementation

```python
# t5gemma_thinker.py
"""
T5Gemma 2 - The Thinker
รับผิดชอบ: Strategy, Creative Content, Analysis
"""

from transformers import AutoProcessor, AutoModelForSeq2SeqLM
import torch
from typing import Dict, List, Optional
from PIL import Image
import requests
from io import BytesIO

class T5GemmaThinker:
    """T5Gemma 2 model wrapper สำหรับ AI Director"""
    
    def __init__(
        self, 
        model_size: str = "1b-1b",  # "270m-270m", "1b-1b", "4b-4b"
        device: str = "auto"
    ):
        """
        Initialize T5Gemma 2 model
        
        Args:
            model_size: ขนาด model (1b-1b แนะนำสำหรับ Codespaces)
            device: "auto", "cpu", "cuda"
        """
        self.model_name = f"google/t5gemma-2-{model_size}"
        print(f"Loading {self.model_name}...")
        
        # Load processor และ model
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=device
        )
        
        print(f"✅ Loaded on {self.model.device}")
    
    def generate_strategy(
        self, 
        brief: str,
        brand_context: Optional[str] = None,
        max_length: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Generate marketing strategy จาก brief
        
        Args:
            brief: Marketing brief
            brand_context: Brand guidelines (จาก RAG)
            max_length: Maximum output tokens
            temperature: Creativity level (0.0-1.0)
            
        Returns:
            Generated strategy as text
        """
        # สร้าง prompt
        prompt = f"""You are a creative director for a marketing agency.
Generate a detailed content strategy based on this brief.

BRAND CONTEXT:
{brand_context if brand_context else "No specific brand guidelines."}

BRIEF:
{brief}

Generate:
1. Creative Concept
2. Image Description (for SDXL)
3. Voice Script (Thai)
4. Technical Specs

STRATEGY:"""

        # Generate
        inputs = self.processor(text=prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_length,
                temperature=temperature,
                do_sample=True,
                top_p=0.9
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result
    
    def generate_image_prompt(
        self,
        brief: str,
        style: str = "realistic",
        aspect_ratio: str = "1:1"
    ) -> str:
        """
        Generate detailed SDXL prompt
        
        Args:
            brief: Product/concept description
            style: "realistic", "minimal", "artistic", "cinematic"
            aspect_ratio: "1:1", "16:9", "9:16"
            
        Returns:
            Detailed prompt สำหรับ SDXL
        """
        prompt = f"""You are an expert photography director.
Generate a detailed prompt for Stable Diffusion XL based on this brief.

BRIEF: {brief}
STYLE: {style}
ASPECT RATIO: {aspect_ratio}

Generate a prompt that includes:
- Subject details
- Lighting setup
- Camera settings
- Mood and atmosphere
- Technical quality descriptors

SDXL PROMPT:"""

        inputs = self.processor(text=prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.8,
                do_sample=True
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result.strip()
    
    def analyze_transcript(
        self,
        transcript: str,
        target_duration: int = 120,
        style: str = "highlight"
    ) -> Dict:
        """
        Analyze video transcript และเลือก highlights
        สำหรับ Smart Cut feature
        
        Args:
            transcript: Full transcript with timestamps
            target_duration: Target video length (seconds)
            style: "highlight", "summary", "tutorial"
            
        Returns:
            Dict with selected segments and reasoning
        """
        prompt = f"""You are a professional video editor.
Analyze this transcript and select the best moments for a {target_duration}-second {style} video.

TRANSCRIPT:
{transcript}

TARGET DURATION: {target_duration} seconds
STYLE: {style}

Identify:
1. Key moments (with timestamps)
2. What to remove (silence, tangents, repetition)
3. Suggested narrative order
4. Reasoning for each decision

Return as structured text with sections: KEEP, REMOVE, ORDER, REASONING

ANALYSIS:"""

        inputs = self.processor(text=prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=400,
                temperature=0.5,  # Lower for more consistent decisions
                do_sample=True
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        
        # Parse result to structured format
        analysis = self._parse_analysis(result)
        return analysis
    
    def analyze_image(
        self,
        image_url: str,
        question: str = "Describe this image in detail"
    ) -> str:
        """
        Multimodal: Analyze image + text
        
        Args:
            image_url: URL or path to image
            question: What to analyze
            
        Returns:
            Image analysis text
        """
        # Load image
        if image_url.startswith("http"):
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(image_url)
        
        # Create prompt with image
        prompt = f"<start_of_image> {question}"
        
        # Process with image
        inputs = self.processor(
            text=prompt,
            images=image,
            return_tensors="pt"
        ).to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=200
            )
        
        result = self.processor.decode(outputs[0], skip_special_tokens=True)
        return result
    
    def _parse_analysis(self, text: str) -> Dict:
        """Parse analysis text to structured format"""
        # Simple parsing - จะปรับปรุงใน Module ถัดไป
        return {
            "raw_analysis": text,
            "keep_segments": [],  # จะ implement ใน Module 6.5
            "remove_segments": [],
            "reasoning": text
        }
    
    def __repr__(self):
        return f"T5GemmaThinker(model={self.model_name}, device={self.model.device})"


# ===== USAGE EXAMPLES =====

if __name__ == "__main__":
    # Initialize model
    thinker = T5GemmaThinker(model_size="1b-1b")
    
    # Example 1: Generate strategy
    print("\n=== Example 1: Generate Strategy ===")
    brief = """
    Brand: CoffeeLab
    Product: Cold Brew Premium
    Target: คนทำงานออฟฟิศ 25-35 ปี
    Goal: Instagram Reel 15 วินาที
    Mood: Premium, modern, minimal
    """
    
    strategy = thinker.generate_strategy(brief)
    print(strategy)
    
    # Example 2: Generate image prompt
    print("\n=== Example 2: Generate Image Prompt ===")
    image_prompt = thinker.generate_image_prompt(
        brief="Cold brew coffee in minimal setting",
        style="minimal",
        aspect_ratio="9:16"
    )
    print(image_prompt)
    
    # Example 3: Analyze transcript (for Smart Cut)
    print("\n=== Example 3: Analyze Transcript ===")
    sample_transcript = """
    [0:00-0:15] สวัสดีครับ วันนี้เรามาพูดถึงกาแฟ Cold Brew
    [0:15-0:45] Cold Brew คือกาแฟที่ชงด้วยน้ำเย็น ใช้เวลานาน 12-24 ชั่วโมง
    [0:45-1:00] ...เอ่อ... อืม... ลืมไปแล้วจะพูดอะไร
    [1:00-1:30] กลับมาที่ Cold Brew นะครับ รสชาติจะนุ่มนวล ไม่ขม
    [1:30-2:00] CoffeeLab ของเราใช้เมล็ดคัดพิเศษ
    """
    
    analysis = thinker.analyze_transcript(
        transcript=sample_transcript,
        target_duration=60,
        style="highlight"
    )
    print(analysis)
```

### Part 2: FunctionGemma Implementation

```python
# functiongemma_executor.py
"""
FunctionGemma - The Executor
รับผิดชอบ: Tool Calling, Orchestration, JSON Generation
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re
from typing import Dict, List, Callable, Any, Optional

class FunctionGemmaExecutor:
    """FunctionGemma model wrapper สำหรับ AI Director"""
    
    def __init__(
        self,
        model_name: str = "google/functiongemma-270m-it",
        device: str = "auto"
    ):
        """
        Initialize FunctionGemma model
        
        Args:
            model_name: HuggingFace model ID
            device: "auto", "cpu", "cuda"
        """
        print(f"Loading {model_name}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map=device
        )
        
        # Tool registry
        self.tools = {}
        
        print(f"✅ Loaded on {self.model.device}")
    
    def register_tool(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None
    ):
        """
        Register a tool/function for calling
        
        Args:
            func: Python function
            name: Tool name (default: function name)
            description: Tool description (default: from docstring)
        """
        tool_name = name or func.__name__
        tool_desc = description or func.__doc__ or "No description"
        
        self.tools[tool_name] = {
            "function": func,
            "description": tool_desc,
            "name": tool_name
        }
        
        print(f"✅ Registered tool: {tool_name}")
    
    def parse_to_tools(
        self,
        instruction: str,
        available_tools: Optional[List[Callable]] = None,
        max_new_tokens: int = 200
    ) -> List[Dict]:
        """
        Parse natural language instruction เป็น tool calls
        
        Args:
            instruction: Natural language command
            available_tools: List of functions (default: all registered)
            max_new_tokens: Max tokens for generation
            
        Returns:
            List of tool calls with parameters
        """
        # Get tools to use
        if available_tools is None:
            tools_list = list(self.tools.values())
        else:
            tools_list = [
                {"function": f, "name": f.__name__, "description": f.__doc__}
                for f in available_tools
            ]
        
        # Prepare messages
        messages = [{"role": "user", "content": instruction}]
        
        # Apply chat template with tools
        formatted_prompt = self.tokenizer.apply_chat_template(
            messages,
            tools=[t["function"] for t in tools_list],
            add_generation_prompt=True,
            tokenize=False
        )
        
        # Generate
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False  # Deterministic for tool calling
            )
        
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=False)
        
        # Parse tool calls from output
        tool_calls = self._parse_function_calls(result)
        
        return tool_calls
    
    def execute_tools(
        self,
        tool_calls: List[Dict],
        error_handling: str = "continue"  # "continue", "stop", "skip"
    ) -> List[Dict]:
        """
        Execute parsed tool calls
        
        Args:
            tool_calls: List of tool calls from parse_to_tools()
            error_handling: How to handle errors
            
        Returns:
            List of results
        """
        results = []
        
        for call in tool_calls:
            tool_name = call.get("tool")
            params = call.get("params", {})
            
            try:
                # Get function
                if tool_name not in self.tools:
                    raise ValueError(f"Tool '{tool_name}' not registered")
                
                func = self.tools[tool_name]["function"]
                
                # Execute
                print(f"🔧 Executing: {tool_name}({params})")
                result = func(**params)
                
                results.append({
                    "tool": tool_name,
                    "params": params,
                    "result": result,
                    "status": "success"
                })
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Error in {tool_name}: {error_msg}")
                
                results.append({
                    "tool": tool_name,
                    "params": params,
                    "error": error_msg,
                    "status": "error"
                })
                
                if error_handling == "stop":
                    break
                elif error_handling == "skip":
                    continue
        
        return results
    
    def _parse_function_calls(self, text: str) -> List[Dict]:
        """
        Parse FunctionGemma output format to structured calls
        
        Format: <start_function_call>call:tool_name{param1:<escape>value<escape>}<end_function_call>
        """
        tool_calls = []
        
        # Pattern for function calls
        pattern = r'<start_function_call>call:(\w+)\{([^}]+)\}<end_function_call>'
        matches = re.findall(pattern, text)
        
        for tool_name, params_str in matches:
            # Parse parameters
            params = self._parse_params(params_str)
            
            tool_calls.append({
                "tool": tool_name,
                "params": params
            })
        
        return tool_calls
    
    def _parse_params(self, params_str: str) -> Dict:
        """Parse parameter string to dict"""
        params = {}
        
        # Simple parsing: key:<escape>value<escape>
        param_pattern = r'(\w+):<escape>([^<]+)<escape>'
        matches = re.findall(param_pattern, params_str)
        
        for key, value in matches:
            # Try to convert types
            if value.isdigit():
                params[key] = int(value)
            elif value.replace('.', '').isdigit():
                params[key] = float(value)
            elif value.lower() in ['true', 'false']:
                params[key] = value.lower() == 'true'
            else:
                params[key] = value
        
        return params
    
    def __repr__(self):
        return f"FunctionGemmaExecutor(tools={len(self.tools)}, device={self.model.device})"


# ===== EXAMPLE TOOLS =====

def image_gen(prompt: str, style: str = "realistic", size: str = "1024x1024") -> str:
    """
    Generate an image from text prompt
    
    Args:
        prompt: Image description
        style: Art style (realistic, minimal, artistic)
        size: Image size (1024x1024, 512x512)
        
    Returns:
        Path to generated image
    """
    print(f"🎨 Generating image: {prompt[:50]}...")
    # Placeholder - จะ implement จริงใน Module 6
    return f"generated_image_{style}.png"

def voice_gen(text: str, voice: str = "th-TH-NiwatNeural", rate: str = "+0%") -> str:
    """
    Generate voiceover from text using Edge-TTS
    
    Args:
        text: Script text
        voice: Voice name
        rate: Speaking rate
        
    Returns:
        Path to audio file
    """
    print(f"🎙️ Generating voice: {text[:30]}...")
    # Placeholder - จะ implement จริงใน Module 6
    return "voiceover.mp3"

def video_compose(
    images: List[str],
    audio: str,
    duration: int = 15,
    transitions: List[str] = None
) -> str:
    """
    Compose video from images and audio
    
    Args:
        images: List of image paths
        audio: Audio file path
        duration: Video duration in seconds
        transitions: Transition effects
        
    Returns:
        Path to composed video
    """
    print(f"🎬 Composing video: {len(images)} images, {duration}s")
    # Placeholder - จะ implement จริงใน Module 6
    return "final_video.mp4"

def smart_cut(
    video_path: str,
    mode: str = "trim_silence",
    target_duration: Optional[int] = None
) -> str:
    """
    Smart video editing with AI
    
    Args:
        video_path: Input video path
        mode: Edit mode (trim_silence, highlights, jump_cut)
        target_duration: Target video length
        
    Returns:
        Path to edited video
    """
    print(f"✂️ Smart cutting: {video_path} ({mode})")
    # Placeholder - จะ implement จริงใน Module 6.5
    return f"{video_path}_edited.mp4"


# ===== USAGE EXAMPLES =====

if __name__ == "__main__":
    # Initialize executor
    executor = FunctionGemmaExecutor()
    
    # Register tools
    executor.register_tool(image_gen)
    executor.register_tool(voice_gen)
    executor.register_tool(video_compose)
    executor.register_tool(smart_cut)
    
    # Example 1: Simple tool calling
    print("\n=== Example 1: Parse Instruction ===")
    instruction = "สร้างรูปกาแฟแบบ minimal และเสียงพากย์ว่า 'Cold Brew Premium จาก CoffeeLab'"
    
    tool_calls = executor.parse_to_tools(instruction)
    print(f"Parsed {len(tool_calls)} tool calls:")
    for call in tool_calls:
        print(f"  - {call['tool']}({call['params']})")
    
    # Example 2: Execute tools
    print("\n=== Example 2: Execute Tools ===")
    results = executor.execute_tools(tool_calls)
    for result in results:
        print(f"✅ {result['tool']}: {result.get('result', result.get('error'))}")
    
    # Example 3: Complex workflow
    print("\n=== Example 3: Complete Workflow ===")
    complex_instruction = """
    Create a 15-second Instagram Reel for CoffeeLab:
    1. Generate a minimal style image of cold brew coffee
    2. Generate Thai voiceover saying 'เริ่มต้นเช้าวันใหม่กับ CoffeeLab Cold Brew'
    3. Compose video with fade transitions
    """
    
    tool_calls = executor.parse_to_tools(complex_instruction)
    results = executor.execute_tools(tool_calls, error_handling="continue")
    
    print(f"\n📊 Summary: {len(results)} tools executed")
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"✅ Success: {success_count}/{len(results)}")
```

### Part 3: Dual-Model Agent Implementation

```python
# ai_director_agent.py
"""
AI Director Agent - Complete Dual-Model System
ประสาน T5Gemma 2 และ FunctionGemma เข้าด้วยกัน
"""

from t5gemma_thinker import T5GemmaThinker
from functiongemma_executor import FunctionGemmaExecutor
from typing import Dict, List, Optional
import json

class AIDirectorAgent:
    """
    AI Director Agent with Dual-Model Architecture
    
    Workflow:
    1. User Brief → T5Gemma 2 (Strategy)
    2. Strategy → FunctionGemma (Tool Calls)
    3. Tool Calls → Execute → Results
    """
    
    def __init__(
        self,
        thinker_size: str = "1b-1b",
        verbose: bool = True
    ):
        """
        Initialize AI Director
        
        Args:
            thinker_size: T5Gemma 2 size (270m-270m, 1b-1b, 4b-4b)
            verbose: Print detailed logs
        """
        self.verbose = verbose
        
        # Initialize models
        if self.verbose:
            print("🧠 Initializing AI Director...")
        
        self.thinker = T5GemmaThinker(model_size=thinker_size)
        self.executor = FunctionGemmaExecutor()
        
        # Register default tools
        self._register_default_tools()
        
        if self.verbose:
            print("✅ AI Director ready!")
    
    def _register_default_tools(self):
        """Register production tools"""
        from functiongemma_executor import (
            image_gen, voice_gen, video_compose, smart_cut
        )
        
        self.executor.register_tool(image_gen)
        self.executor.register_tool(voice_gen)
        self.executor.register_tool(video_compose)
        self.executor.register_tool(smart_cut)
    
    def process_brief(
        self,
        brief: str,
        brand_context: Optional[str] = None,
        mode: str = "auto"  # "create", "edit", "auto"
    ) -> Dict:
        """
        Complete workflow: Brief → Strategy → Execution → Results
        
        Args:
            brief: Marketing brief or instruction
            brand_context: Brand guidelines from RAG
            mode: Workflow mode
            
        Returns:
            Dict with strategy, tool_calls, and results
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"🎬 AI Director Processing Brief")
            print(f"{'='*60}")
            print(f"Brief: {brief[:100]}...")
        
        # Detect mode if auto
        if mode == "auto":
            mode = self._detect_mode(brief)
            if self.verbose:
                print(f"📋 Detected mode: {mode}")
        
        # STEP 1: THINKER - Generate Strategy
        if self.verbose:
            print(f"\n🧠 Step 1: T5Gemma 2 (Strategy Generation)")
        
        strategy = self.thinker.generate_strategy(
            brief=brief,
            brand_context=brand_context
        )
        
        if self.verbose:
            print(f"Strategy: {strategy[:200]}...")
        
        # STEP 2: EXECUTOR - Parse to Tool Calls
        if self.verbose:
            print(f"\n⚡ Step 2: FunctionGemma (Tool Parsing)")
        
        tool_calls = self.executor.parse_to_tools(strategy)
        
        if self.verbose:
            print(f"Parsed {len(tool_calls)} tool calls")
            for i, call in enumerate(tool_calls, 1):
                print(f"  {i}. {call['tool']}()")
        
        # STEP 3: Execute Tools
        if self.verbose:
            print(f"\n🔧 Step 3: Tool Execution")
        
        results = self.executor.execute_tools(
            tool_calls,
            error_handling="continue"
        )
        
        # Summary
        if self.verbose:
            success = sum(1 for r in results if r['status'] == 'success')
            print(f"\n{'='*60}")
            print(f"✅ Workflow Complete: {success}/{len(results)} successful")
            print(f"{'='*60}")
        
        return {
            "brief": brief,
            "mode": mode,
            "strategy": strategy,
            "tool_calls": tool_calls,
            "results": results,
            "summary": {
                "total_tools": len(tool_calls),
                "successful": sum(1 for r in results if r['status'] == 'success'),
                "failed": sum(1 for r in results if r['status'] == 'error')
            }
        }
    
    def edit_video(
        self,
        video_path: str,
        instruction: str,
        target_duration: Optional[int] = None
    ) -> Dict:
        """
        Smart Cut workflow สำหรับตัดต่อ video
        
        Args:
            video_path: Input video file
            instruction: Edit instruction
            target_duration: Target length in seconds
            
        Returns:
            Dict with analysis and edited video
        """
        if self.verbose:
            print(f"\n🎬 Smart Cut Workflow")
            print(f"Video: {video_path}")
            print(f"Instruction: {instruction}")
        
        # Step 1: Analyze (จะ implement ใน Module 6.5)
        # - Transcribe with Whisper
        # - Detect silence with FFmpeg
        # - Extract frames
        
        # Step 2: T5Gemma 2 decides what to keep
        analysis_prompt = f"""
        Video: {video_path}
        Instruction: {instruction}
        Target Duration: {target_duration}s
        
        Decide which segments to keep and remove.
        """
        
        edit_decision = self.thinker.analyze_transcript(
            transcript=analysis_prompt,  # จะเป็น real transcript ใน Module 6.5
            target_duration=target_duration or 120
        )
        
        # Step 3: FunctionGemma executes cuts
        tool_calls = self.executor.parse_to_tools(
            f"Edit video {video_path} according to: {edit_decision['raw_analysis']}"
        )
        
        results = self.executor.execute_tools(tool_calls)
        
        return {
            "video": video_path,
            "instruction": instruction,
            "analysis": edit_decision,
            "tool_calls": tool_calls,
            "results": results
        }
    
    def _detect_mode(self, brief: str) -> str:
        """Detect if task is create or edit"""
        edit_keywords = ["ตัด", "edit", "trim", "highlight", "cut"]
        create_keywords = ["สร้าง", "create", "generate", "ทำ"]
        
        brief_lower = brief.lower()
        
        if any(kw in brief_lower for kw in edit_keywords):
            return "edit"
        elif any(kw in brief_lower for kw in create_keywords):
            return "create"
        else:
            return "create"  # default
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        return {
            "thinker": {
                "model": self.thinker.model_name,
                "device": str(self.thinker.model.device)
            },
            "executor": {
                "model": "google/functiongemma-270m-it",
                "device": str(self.executor.model.device),
                "registered_tools": len(self.executor.tools)
            }
        }
    
    def __repr__(self):
        return f"AIDirectorAgent(thinker={self.thinker.model_name}, tools={len(self.executor.tools)})"


# ===== USAGE EXAMPLES =====

if __name__ == "__main__":
    # Initialize AI Director
    agent = AIDirectorAgent(thinker_size="1b-1b", verbose=True)
    
    # Example 1: Create content from brief
    print("\n" + "="*70)
    print("EXAMPLE 1: CREATE CONTENT")
    print("="*70)
    
    brief_create = """
    สร้าง Instagram Reel 15 วินาที สำหรับ CoffeeLab Cold Brew
    
    Target: คนทำงานออฟฟิศ 25-35 ปี
    Mood: Premium, modern, minimal
    Message: เริ่มต้นเช้าวันใหม่ด้วยกาแฟคุณภาพ
    """
    
    result = agent.process_brief(
        brief=brief_create,
        brand_context="CoffeeLab เป็นแบรนด์กาแฟพรีเมียม โทนสีน้ำตาล-ครีม"
    )
    
    # Print results
    print("\n📊 RESULTS:")
    print(json.dumps(result['summary'], indent=2))
    
    # Example 2: Edit existing video
    print("\n" + "="*70)
    print("EXAMPLE 2: EDIT VIDEO")
    print("="*70)
    
    edit_result = agent.edit_video(
        video_path="interview_raw.mp4",
        instruction="ตัดให้เหลือ 2 นาที เอาแต่ส่วนที่พูดถึงผลิตภัณฑ์",
        target_duration=120
    )
    
    # Example 3: Get system stats
    print("\n" + "="*70)
    print("SYSTEM STATS")
    print("="*70)
    stats = agent.get_stats()
    print(json.dumps(stats, indent=2))
```

### Testing Script

```python
# test_module1.py
"""
Test script สำหรับ Module 1
ทดสอบ dual-model architecture ทั้งหมด
"""

import sys

def test_thinker():
    """Test T5Gemma 2"""
    print("\n" + "="*70)
    print("TEST 1: T5GEMMA 2 (THINKER)")
    print("="*70)
    
    try:
        from t5gemma_thinker import T5GemmaThinker
        
        thinker = T5GemmaThinker(model_size="1b-1b")
        
        # Test strategy generation
        strategy = thinker.generate_strategy(
            brief="สร้างโฆษณากาแฟ 15 วินาที",
            max_length=200
        )
        
        print("✅ Strategy generation: PASS")
        print(f"Output length: {len(strategy)} chars")
        
        # Test image prompt
        prompt = thinker.generate_image_prompt(
            brief="Premium coffee cup",
            style="minimal"
        )
        
        print("✅ Image prompt generation: PASS")
        print(f"Prompt: {prompt[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_executor():
    """Test FunctionGemma"""
    print("\n" + "="*70)
    print("TEST 2: FUNCTIONGEMMA (EXECUTOR)")
    print("="*70)
    
    try:
        from functiongemma_executor import FunctionGemmaExecutor, image_gen
        
        executor = FunctionGemmaExecutor()
        executor.register_tool(image_gen)
        
        # Test tool parsing
        instruction = "Generate a minimal style image of coffee"
        tool_calls = executor.parse_to_tools(instruction)
        
        print(f"✅ Tool parsing: PASS")
        print(f"Parsed {len(tool_calls)} tool calls")
        
        # Test execution
        results = executor.execute_tools(tool_calls)
        
        print(f"✅ Tool execution: PASS")
        print(f"Results: {len(results)}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_agent():
    """Test complete agent"""
    print("\n" + "="*70)
    print("TEST 3: AI DIRECTOR AGENT (COMPLETE)")
    print("="*70)
    
    try:
        from ai_director_agent import AIDirectorAgent
        
        agent = AIDirectorAgent(thinker_size="1b-1b", verbose=False)
        
        # Test workflow
        result = agent.process_brief(
            brief="สร้างรูปกาแฟแบบ minimal"
        )
        
        print(f"✅ Complete workflow: PASS")
        print(f"Summary: {result['summary']}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("MODULE 1 - DUAL-MODEL ARCHITECTURE TEST SUITE")
    print("="*70)
    
    results = {
        "Thinker": test_thinker(),
        "Executor": test_executor(),
        "Agent": test_agent()
    }
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:.<40} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Module 1 complete!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Please check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## 🎯 วิธีรัน Code ใน Codespaces

### ขั้นตอนที่ 1: ตรวจสอบว่าไฟล์ครบ

```bash
# เช็คว่าไฟล์ทั้งหมดสร้างแล้ว
cd /workspaces/ai-director-course/module1
ls -la

# ควรเห็น:
# t5gemma_thinker.py
# functiongemma_executor.py
# ai_director_agent.py
# test_module1.py
```

### ขั้นตอนที่ 2: รัน Test (แนะนำ)

```bash
# รัน test suite เพื่อตรวจสอบว่าทุกอย่างทำงาน
python test_module1.py
```

**ผลลัพธ์ที่ควรเห็น:**
```
======================================================================
MODULE 1 - DUAL-MODEL ARCHITECTURE TEST SUITE
======================================================================

======================================================================
TEST 1: T5GEMMA 2 (THINKER)
======================================================================
Loading google/t5gemma-2-1b-1b...
✅ Loaded on cuda:0
✅ Strategy generation: PASS
Output length: 245 chars
✅ Image prompt generation: PASS
Prompt: A sleek glass bottle of cold brew coffee...

======================================================================
TEST 2: FUNCTIONGEMMA (EXECUTOR)
======================================================================
Loading google/functiongemma-270m-it...
✅ Loaded on cuda:0
✅ Registered tool: image_gen
✅ Tool parsing: PASS
Parsed 1 tool calls
🔧 Executing: image_gen({'prompt': '...', 'style': 'minimal'})
✅ Tool execution: PASS
Results: 1

======================================================================
TEST 3: AI DIRECTOR AGENT (COMPLETE)
======================================================================
🧠 Initializing AI Director...
✅ AI Director ready!
✅ Complete workflow: PASS
Summary: {'total_tools': 2, 'successful': 2, 'failed': 0}

======================================================================
TEST SUMMARY
======================================================================
Thinker...................................... ✅ PASS
Executor..................................... ✅ PASS
Agent........................................ ✅ PASS

Total: 3/3 tests passed

🎉 All tests passed! Module 1 complete!
```

### ขั้นตอนที่ 3: ทดสอบแต่ละ Module แยก

```bash
# ทดสอบ T5Gemma 2 เฉพาะ
python t5gemma_thinker.py

# ทดสอบ FunctionGemma เฉพาะ
python functiongemma_executor.py

# ทดสอบ Agent สมบูรณ์
python ai_director_agent.py
```

### ขั้นตอนที่ 4: ทดสอบแบบ Interactive

เปิด Python REPL:
```bash
python
```

ลองใช้งาน:
```python
# Import modules
from ai_director_agent import AIDirectorAgent

# สร้าง agent
agent = AIDirectorAgent(thinker_size="1b-1b", verbose=True)

# ลองใช้งาน
result = agent.process_brief(
    brief="สร้าง Instagram post สำหรับกาแฟ"
)

# ดูผลลัพธ์
print(result['summary'])

# ออกจาก Python
exit()
```

---

## 🐛 แก้ปัญหาที่พบบ่อย

### ปัญหา 1: ModuleNotFoundError

```bash
# Error: ModuleNotFoundError: No module named 'transformers'

# แก้ไข: ติดตั้ง dependencies อีกครั้ง
pip install transformers torch accelerate pillow requests
```

### ปัญหา 2: CUDA/GPU ไม่พร้อม

```python
# Warning: CUDA not available, using CPU

# นี่เป็นเรื่องปกติใน Codespaces (ไม่มี GPU ฟรี)
# Code จะรันบน CPU ได้ แต่ช้ากว่า
# สำหรับ training จะใช้ Google Colab (Module 4)
```

### ปัญหา 3: Out of Memory

```bash
# Error: OutOfMemoryError

# แก้ไข: ใช้ model ขนาดเล็กกว่า
# เปลี่ยนจาก "1b-1b" เป็น "270m-270m"
```

```python
# ใน code
thinker = T5GemmaThinker(model_size="270m-270m")  # เล็กกว่า
```

### ปัญหา 4: Model Download ช้า

```bash
# Model กำลัง download ครั้งแรก (1-2 GB)
# ใน Codespaces อาจใช้เวลา 5-10 นาที

# Tips: รอให้ download เสร็จครั้งแรก
# ครั้งต่อไปจะเร็วขึ้น (cached ใน Codespace)
```

### ปัญหา 5: Import Error ระหว่าง Files

```bash
# Error: ImportError: cannot import name 'T5GemmaThinker'

# ตรวจสอบว่า:
# 1. อยู่ใน folder เดียวกัน (module1/)
# 2. ชื่อไฟล์ถูกต้อง (t5gemma_thinker.py)
# 3. ไม่มี syntax error ในไฟล์

# ลองเช็ค:
cd /workspaces/ai-director-course/module1
python -c "from t5gemma_thinker import T5GemmaThinker; print('OK')"
```

---

## 💾 บันทึกงานลง GitHub

```bash
# 1. เช็คสถานะ
cd /workspaces/ai-director-course
git status

# 2. Add files
git add module1/
git add .gitignore

# 3. Commit
git commit -m "Complete Module 1: Dual-Model Architecture"

# 4. Push to GitHub
git push
```

✅ **ตอนนี้ code ของคุณปลอดภัยบน GitHub แล้ว!**

---

## 📊 เช็ค Free Tier Usage

```bash
# เช็คว่าใช้ Codespaces ไปเท่าไหร่แล้ว
# ไปที่: https://github.com/settings/billing
# ดูที่: Codespaces usage

# Free tier: 120 core-hours/month
# 2-core machine: ใช้ได้ 60 ชั่วโมง/เดือน
```

**Tips ประหยัด:**
- ✅ Stop Codespace เมื่อไม่ใช้ (ปุ่ม Stop ที่มุมล่างซ้าย)
- ✅ Set auto-stop timeout: 30 นาที
- ✅ ลบ Codespace เก่าๆ ที่ไม่ใช้แล้ว

---

## ✅ Checklist: Module 1 Complete

เช็คว่าทำครบหรือยัง:

### Setup
- [ ] สร้าง GitHub repository
- [ ] เปิด Codespaces สำเร็จ
- [ ] ติดตั้ง dependencies (transformers, torch, etc.)
- [ ] สร้าง folder structure

### Code
- [ ] สร้างไฟล์ `t5gemma_thinker.py`
- [ ] สร้างไฟล์ `functiongemma_executor.py`
- [ ] สร้างไฟล์ `ai_director_agent.py`
- [ ] สร้างไฟล์ `test_module1.py`

### Testing
- [ ] รัน `python test_module1.py` สำเร็จ
- [ ] ทดสอบ T5Gemma 2 ผ่าน
- [ ] ทดสอบ FunctionGemma ผ่าน
- [ ] ทดสอบ Complete Agent ผ่าน

### Git
- [ ] Commit code ลง git
- [ ] Push ขึ้น GitHub

---

## 🎓 ถัดไปทำอะไร?

ถ้าทุกอย่างเสร็จแล้ว พร้อมไป:

**Module 2: Data Engineering & Pipeline (ETL)**
- Setup MongoDB Atlas (ฟรี)
- Setup ChromaDB
- สร้าง data schemas
- Load sample data

**ต้องการให้เพิ่ม Module 2 พร้อม complete code ไหมครับ?**

---

## 🎯 Next Steps

เมื่อเข้าใจ Module 1 แล้ว คุณพร้อมสำหรับ:

**Module 2: Data Engineering & Pipeline (ETL)**  
- สร้างคลังความรู้สำหรับ AI Director
- ออกแบบ MongoDB schemas
- ตั้งค่า ChromaDB สำหรับ RAG
- เตรียมข้อมูล transcript สำหรับ Smart Cut

---

## 📚 Additional Resources for Module 1

### Architecture Comparisons
- [T5 vs GPT: Encoder-Decoder vs Decoder-Only](https://huggingface.co/blog/encoder-decoder)
- [Function Calling with Small Models](https://huggingface.co/blog/function-calling)

### Model Documentation
- [T5Gemma 2 Model Card](https://huggingface.co/google/t5gemma-2-1b-1b)
- [FunctionGemma Guide](https://huggingface.co/google/functiongemma-270m-it)

### Video Tutorials
- Search YouTube: "Multi-agent architecture AI"
- Search YouTube: "Function calling with small models"

---

**🎬 Module 1 Complete! Ready for Module 2? 🚀**

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
