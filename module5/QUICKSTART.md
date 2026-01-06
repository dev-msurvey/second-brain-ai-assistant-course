# Module 5 Quick Start Guide

> เริ่มต้นใช้งาน Vector RAG + Hybrid Retrieval + Production API ใน 10 นาที

## 📋 Prerequisites

- ✅ Python 3.10+
- ✅ Module 2 (มี brands JSON files)
- ⚠️ **MongoDB Atlas account ยังไม่มี?** → ดู [MongoDB Setup Guide](#mongodb-setup-guide) ด้านล่าง

---

## 🗄️ MongoDB Setup Guide (ถ้ายังไม่มี Account)

### Quick MongoDB Atlas Setup (10 นาที)

**1. สร้าง Account (2 นาที):**
- ไปที่ https://www.mongodb.com/cloud/atlas/register
- Sign up with Google (ไม่ต้องใส่บัตรเครดิต)

**2. สร้าง Cluster (3 นาที):**
- Click **Create → M0 FREE**
- Provider: **AWS**, Region: **Singapore**
- Cluster name: `ai-director`
- Click **Create Deployment**

**3. สร้าง User (1 นาที):**
- Username: `ai-director_db`
- Password: **Autogenerate** (บันทึกไว้!)
- Click **Create Database User**

**4. Whitelist IP (1 นาที):**
- Click **ALLOW ACCESS FROM ANYWHERE**
- IP: `0.0.0.0/0`
- Click **Add Entry**

**5. Get Connection String (1 นาที):**
- Click **Connect → Drivers**
- Copy connection string:
```bash
mongodb+srv://ai-director_db:YOUR_PASSWORD@ai-director.xxxxx.mongodb.net/?appName=ai-director
```

**6. Set Environment Variable:**
```bash
export MONGO_URI="mongodb+srv://ai-director_db:YOUR_PASSWORD@ai-director.xxxxx.mongodb.net/?appName=ai-director"

# Verify
echo $MONGO_URI
```

**7. Create Vector Index (2 นาที):**
- ไปที่ **Database → Search → Create Search Index**
- เลือก **JSON Editor**
- Database: `ai_director`, Collection: `brand_vectors`
- Index name: `vector_index`
- Paste JSON:
```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "type": "knnVector",
        "dimensions": 384,
        "similarity": "cosine"
      },
      "brand_name": {"type": "token"},
      "doc_type": {"type": "token"}
    }
  }
}
```
- Click **Create** → รอ status เป็น **READY** (~2 นาที)

✅ **Done!** MongoDB Atlas พร้อมใช้งาน

**📚 ดูขั้นตอนละเอียดใน [README.md](README.md#mongodb-atlas-setup)**

---

## 🚀 ขั้นตอนการติดตั้ง

### 0. Verify MongoDB Connection (30 วินาที)

```bash
# Test connection
python -c "
from pymongo import MongoClient
import os
client = MongoClient(os.environ['MONGO_URI'])
client.admin.command('ping')
print('✅ MongoDB connected!')
"
```

### 1. Install Dependencies (2 นาที)

```bash
cd /workspaces/second-brain-ai-assistant-course/module5
pip install -r requirements.txt
```

รอ download `sentence-transformers` model (~400MB)

### 2. Set Environment Variables

```bash
# ตรวจสอบว่ามี MONGO_URI หรือยัง
echo $MONGO_URI

# ถ้ายังไม่มี ให้ set (แทน YOUR_PASSWORD ด้วย password จริง)
export MONGO_URI="mongodb+srv://ai-director_db:YOUR_PASSWORD@ai-director.xxxxx.mongodb.net/?appName=ai-director"

# Verify
echo $MONGO_URI
```

**⚠️ ถ้ายังไม่มี MongoDB Atlas:** ดู [MongoDB Setup Guide](#mongodb-setup-guide) ข้างบน

### 3. Create Vector Index (3 นาที)

เนื่องจากใช้ MongoDB M0 (free tier) ต้องสร้าง index ผ่าน UI:

1. เข้า [MongoDB Atlas](https://cloud.mongodb.com/)
2. Database → Search → **Create Search Index**
3. เลือก **JSON Editor**
4. Database: `ai_director`, Collection: `brand_vectors`
5. วาง JSON นี้:

```json
{
  "mappings": {
    "dynamic": true,
    "fields": {
      "embedding": {
        "type": "knnVector",
        "dimensions": 384,
        "similarity": "cosine"
      },
      "brand_name": {
        "type": "token"
      },
      "doc_type": {
        "type": "token"
      }
    }
  }
}
```

6. Index name: `vector_index`
7. สร้างเสร็จรอ ~2-3 นาที

### 4. Run Ingestion (2-5 นาที)

**อ่านจาก JSON files (ไม่ต้อง MongoDB):**

```bash
# อ่านจาก brands_v2.json
python pipelines/json_ingestion.py --clear

# หรือระบุไฟล์เอง
python pipelines/json_ingestion.py --json ../module2/data/raw/brands_v2.json --clear
```

**คาดหวัง**:
```
📥 โหลด 8 brands จาก brands_v2.json
   ตัวอย่าง: CoffeeLab, FitFlow, GreenLeaf, TechZone, UrbanNest, PetPals, GlowLab, EduKid
✅ Inserted 38 documents (8 parents + 30 children)
```

### 5. Test Basic Retrieval (30 วินาที)

```bash
python scripts/test_retrieval.py --test basic
```

**ผลลัพธ์**:
```
Query: luxury coffee shop

1. Brand: CoffeeLab
   Relevance Score: 0.876
   ✅ Working!
```

---

## 🎯 Quick Start Guides

### A. Vector Search (Semantic Similarity)

```python
from module5.parent_child_retriever import ProductionRAG

rag = ProductionRAG()

# ค้นหาแบรนด์ด้วยภาษาธรรมชาติ
results = rag.retrieve(
    query="coffee shop with cozy atmosphere",
    k=3
)

for text in results:
    print(text)
    print("-" * 80)

rag.close()
```

**เมื่อไหร่ควรใช้**: Semantic queries, concept matching, paraphrasing

---

### B. Hybrid Search (Vector + BM25) **[RECOMMENDED]**

```python
from module5.hybrid_retriever import HybridProductionRAG

rag = HybridProductionRAG()

# ค้นหาแบบ Hybrid (ดีที่สุด)
results = rag.retrieve(
    query="luxury coffee shop",
    k=3,
    method="hybrid"  # หรือ "vector" หรือ "bm25"
)

for text in results:
    print(text)
    print("-" * 80)

rag.close()
```

**เมื่อไหร่ควรใช้**: Production use, best quality (F1=0.570, 100% success rate)

**Method Options**:
- `hybrid` - Best quality, combines semantic + keyword (RECOMMENDED)
- `vector` - Semantic search only, fast (~34ms)
- `bm25` - Keyword search only, fastest (~9ms)

---

### C. FastAPI Production API **[RECOMMENDED]**

**1. Start Server** (Terminal 1):
```bash
cd module5/tools

# Set MongoDB URI
export MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net/?appName=ai-director"

# Start server
python app.py --host 0.0.0.0 --port 8000
```

**Expected**:
```
🚀 Loading HybridProductionRAG...
✅ Embedder loaded: sentence-transformers
✅ BM25 index built: 30 documents
✅ API ready!

INFO:     Uvicorn running on http://0.0.0.0:8000
```

**2. Access API Docs**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**3. Test API** (Terminal 2):
```bash
# Health check
curl http://localhost:8000/health

# Search (POST)
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "luxury coffee shop",
    "k": 3,
    "method": "hybrid"
  }'

# Search (GET)
curl "http://localhost:8000/search/simple?query=coffee&k=3&method=hybrid"

# List brands
curl http://localhost:8000/brands

# System stats
curl http://localhost:8000/stats
```

**4. Python Client**:
```python
import requests

# Search
response = requests.post(
    "http://localhost:8000/search",
    json={
        "query": "coffee shop with friendly atmosphere",
        "k": 3,
        "method": "hybrid"
    }
)

data = response.json()
for result in data["results"]:
    print(f"\nBrand: {result['brand_name']}")
    print(f"Score: {result['score']:.3f}")
    print(f"Context: {result['context'][:200]}...")
```

**API Endpoints** (9 total):
- `GET /` - Root (API info)
- `GET /health` - Health check
- `POST /search` - Main search (with method selection)
- `GET /search/simple` - Simple GET search
- `GET /brands` - List all brands
- `GET /stats` - System statistics

See [API_GUIDE.md](tools/API_GUIDE.md) for complete docs.

---

### D. Evaluation & Benchmarking

```bash
cd module5/tools

# Run evaluation on all methods
python evaluate_rag.py --methods hybrid vector bm25 -k 3 --save

# View results
cat evaluation_results.json
```

**Expected Output**:
```
=== RAG EVALUATION RESULTS ===

Method: hybrid
  Precision@3: 0.433
  Recall@3: 0.900
  F1 Score: 0.570 🥇
  MRR: 0.950
  NDCG@3: 0.890
  Success Rate: 100%
  Avg Latency: 456ms

Method: vector
  Precision@3: 0.400
  Recall@3: 0.850
  F1 Score: 0.530
  ...

Method: bm25
  Precision@3: 0.367
  Recall@3: 0.800
  F1 Score: 0.490
  Avg Latency: 9.4ms ⚡
```

---

### E. Using Configuration Files

**1. Load Config**:
```python
import yaml
from module5.hybrid_retriever import HybridProductionRAG

# Load hybrid config (recommended)
with open("configs/hybrid_search.yaml") as f:
    config = yaml.safe_load(f)

rag = HybridProductionRAG(
    vector_weight=config["hybrid"]["vector_weight"],
    bm25_weight=config["hybrid"]["bm25_weight"],
    rrf_k=config["hybrid"]["rrf_k"]
)
```

**2. Available Configs**:
- `configs/default.yaml` - Complete reference config
- `configs/vector_search.yaml` - Vector-only setup
- `configs/hybrid_search.yaml` - Hybrid setup (RECOMMENDED)
- `configs/api.yaml` - FastAPI production settings
- `configs/ingestion.yaml` - Data loading config

**3. Override Settings**:
```python
# Custom weights for hybrid search
rag = HybridProductionRAG(
    vector_weight=0.7,  # Prioritize semantic search
    bm25_weight=0.3,    # Lower keyword weight
    rrf_k=60
)
```

---

## 📊 Performance Comparison

| Method | F1 Score | Latency | When to Use |
|--------|----------|---------|-------------|
| **Hybrid** | **0.570** 🥇 | 456ms | Production (best quality) |
| Vector | 0.530 | 34ms ⚡ | Semantic queries |
| BM25 | 0.490 | 9.4ms ⚡⚡ | Keyword queries |

---

## 🐛 Quick Troubleshooting

**Problem**: `MONGO_URI not set`  
**Solution**: `export MONGO_URI="mongodb+srv://..."`

**Problem**: `No results found`  
**Solution**: Run ingestion first: `python pipelines/json_ingestion.py --clear`

**Problem**: `Vector index not found`  
**Solution**: Create index via Atlas UI (see Step 3)

**Problem**: `API won't start`  
**Solution**: 
```bash
# Check MongoDB connection
python -c "from module5.mongodb_vector import MongoDBVectorStore; print(MongoDBVectorStore().ping())"

# Check port availability
lsof -i :8000
```

---

## 📚 Next Steps

1. **Read Full README**: [README.md](README.md)
2. **API Documentation**: [API_GUIDE.md](tools/API_GUIDE.md)
3. **Deploy to Production**: See "Deployment Guide" in README
4. **Run Benchmarks**: `python scripts/test_hybrid_retrieval.py`
5. **Integration with Module 4**: `python scripts/test_integration_quick.py`

---

## 🎓 Learning Path

1. ✅ **Start Here**: Vector Search (semantic similarity)
2. ✅ **Next**: Hybrid Search (best quality)
3. ✅ **Then**: FastAPI Production API
4. ✅ **Finally**: Evaluation & Optimization

**Total Time**: ~10-15 minutes to get everything running!

for text in results:
    print(text)

rag.close()
```

### Example 2: Integration กับ Module 4

```python
from module5.scripts.inference_rag_v2 import AIDirectorRAGInferenceV2

# Initialize
inferencer = AIDirectorRAGInferenceV2(
    base_model_name="Qwen/Qwen2.5-1.5B-Instruct",
    use_vector_rag=True  # ใช้ Module 5
)

# Generate
output = inferencer.generate(
    instruction="Create Instagram caption",
    brand_name="CoffeeLab"
)

print(output)
inferencer.close()
```

---

## 🔍 ทดสอบทันที

### Test 1: Semantic Search

```bash
python -c "
from module5.parent_child_retriever import ParentChildRetriever
r = ParentChildRetriever()
results = r.retrieve('luxury brand', k=2)
for d in results:
    print(f\"{d['brand_name']}: {d.get('relevance_score', 0):.3f}\")
r.close()
"
```

### Test 2: Performance Benchmark

```bash
python scripts/test_retrieval.py --test benchmark -k 3
```

### Test 3: Full Demo

```bash
python scripts/inference_rag_v2.py --demo
```

---

## ⚠️ Common Issues

### ❌ "MONGO_URI not found"

```bash
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/"
```

### ❌ "No vector index"

สร้าง index ตามขั้นตอนที่ 2

### ❌ "No documents found"

รัน ingestion pipeline:
```bash
python pipelines/json_ingestion.py --clear
```

### ❌ "brands_v2.json not found"

ตรวจสอบว่ามีไฟล์:
```bash
ls -la ../module2/data/raw/brands*.json
```

---

## ✅ Checklist

- [ ] Dependencies installed
- [ ] Vector index created
- [ ] Ingestion completed
- [ ] Basic test passed
- [ ] Ready to use!

---

**เวลารวม**: ~10 นาที  
**ถัดไป**: อ่าน [README.md](README.md) เพื่อเข้าใจ architecture และ advanced features
