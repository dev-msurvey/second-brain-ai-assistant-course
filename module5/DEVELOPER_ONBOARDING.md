# Module 5 Developer Onboarding Guide 🚀

> **คู่มือสำหรับ AI Agent/Developer ที่จะมาพัฒนางานต่อ**

**Last Updated**: January 6, 2026  
**Branch**: `feature/module5-vector-rag`  
**Status**: ✅ Production Ready (Core Complete)

---

## 📚 เอกสารที่ต้องอ่านก่อนเริ่มงาน (ตามลำดับ)

### 1️⃣ เอกสารหลัก (MUST READ - อ่านก่อน)

**อ่านตามลำดับนี้:**

1. **[QUICKSTART.md](QUICKSTART.md)** (15 นาที)
   - เข้าใจภาพรวมของ Module 5
   - Setup MongoDB Atlas (ถ้ายังไม่มี)
   - ลองรัน basic tests
   - **ทำไมต้องอ่าน**: รู้ว่าระบบทำงานยังไงโดยรวม

2. **[README.md](README.md)** (30 นาที)
   - Architecture แบบละเอียด
   - ทุก features ที่มี (Vector, BM25, Hybrid, API, Evaluation)
   - Performance benchmarks
   - Deployment guide
   - **ทำไมต้องอ่าน**: เข้าใจ technical details ครบถ้วน

3. **[COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)** (10 นาที)
   - สรุปทุกอย่างที่สร้างมา
   - Performance results
   - Files ที่สำคัญ
   - **ทำไมต้องอ่าน**: รู้ว่าทำอะไรไปแล้วบ้าง

4. **[../course_ai-assistant_v3.4.2.md](../course_ai-assistant_v3.4.2.md)** (ส่วน Module 5)
   - บริบทของ AI Director project
   - Module 5 fits ใน bigger picture อย่างไร
   - Zero-cost philosophy
   - **ทำไมต้องอ่าน**: เข้าใจเป้าหมายของโปรเจค

---

### 2️⃣ เอกสารเฉพาะทาง (อ่านตามที่ต้องการ)

**MongoDB Setup:**
- **[MONGODB_SETUP.md](MONGODB_SETUP.md)** (800+ บรรทัด)
  - Step-by-step MongoDB Atlas setup
  - Troubleshooting ทุกกรณี
  - **เมื่อไหร่อ่าน**: ถ้าต้อง setup MongoDB ใหม่ หรือแก้ปัญหา connection

**API Usage:**
- **[tools/API_GUIDE.md](tools/API_GUIDE.md)**
  - FastAPI endpoints ทั้งหมด
  - curl examples
  - Python client examples
  - **เมื่อไหร่อ่าน**: ถ้าต้องใช้งาน API หรือเพิ่ม endpoints

**Quick Reference:**
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**
  - Commands, configs, troubleshooting สั้นๆ
  - **เมื่อไหร่อ่าน**: ต้องการ quick lookup

---

### 3️⃣ Source Code ที่ต้องเข้าใจ

**ลำดับการอ่าน code:**

1. **[src/module5/embedding_models.py](src/module5/embedding_models.py)** (180 lines)
   - เข้าใจว่า embeddings ทำงานยังไง
   - SentenceTransformerEmbedder, OpenAIEmbedder
   - Interface ง่าย: `embed_documents()`, `embed_query()`

2. **[src/module5/mongodb_vector.py](src/module5/mongodb_vector.py)** (309 lines)
   - **IMPORTANT**: มี bugs ที่ fix แล้ว (line 219, ObjectId conversion)
   - MongoDBVectorStore class
   - Methods: `vector_search()`, `get_parent_document()`, `insert_documents()`
   - เข้าใจ MongoDB Atlas Vector Search

3. **[src/module5/parent_child_retriever.py](src/module5/parent_child_retriever.py)** (315 lines)
   - Parent-Child retrieval strategy
   - ParentChildRetriever, ProductionRAG classes
   - Vector search เบื้องต้น

4. **[src/module5/hybrid_retriever.py](src/module5/hybrid_retriever.py)** (~400 lines)
   - **MOST COMPLEX FILE** - ใจความสำคัญของ Module 5
   - HybridRetriever: Vector + BM25 + RRF fusion
   - HybridProductionRAG: Production-ready wrapper
   - อ่านละเอียด: `build_bm25_index()`, `reciprocal_rank_fusion()`

---

## 🏗️ Architecture Overview

### System Components

```
┌────────────────────────────────────────────────────────────┐
│                   MODULE 5 ARCHITECTURE                    │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  USER QUERY ──┐                                           │
│               ├──▶ [HybridRetriever] ─────┐               │
│               │                           │               │
│               │    ┌──────────────────┐   │               │
│               └───▶│  Vector Search   │───┤               │
│                    │  (MongoDB Atlas) │   │               │
│                    └──────────────────┘   │               │
│                                           ├──▶ [RRF Fusion]│
│                    ┌──────────────────┐   │               │
│                    │   BM25 Search    │───┤               │
│                    │  (rank-bm25)     │   │               │
│                    └──────────────────┘   │               │
│                                           │               │
│                                           ▼               │
│                                   ┌──────────────┐        │
│                                   │ Top-K Results│        │
│                                   │ (with scores)│        │
│                                   └──────────────┘        │
│                                           │               │
│                    ┌──────────────────────┘               │
│                    │                                      │
│                    ▼                                      │
│         ┌────────────────────────┐                        │
│         │ Parent-Child Retrieval │                        │
│         │ Search: Child docs     │                        │
│         │ Return: Parent docs    │                        │
│         └────────────────────────┘                        │
│                    │                                      │
│                    ▼                                      │
│            [Rich Context for LLM]                         │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. JSON Data (brands_v2.json)
   ↓
2. Ingestion Pipeline (pipelines/json_ingestion.py)
   ↓
3. MongoDB Atlas (brand_vectors collection)
   ├─ 8 Parent docs (full brand info)
   └─ 30 Child docs (chunks with embeddings)
   ↓
4. Vector Search Index (384-dim, cosine similarity)
   ↓
5. Retrieval Methods:
   ├─ Vector Search (semantic)
   ├─ BM25 Search (keyword)
   └─ Hybrid Search (fusion)
   ↓
6. FastAPI (tools/app.py)
   ↓
7. Client Applications
```

---

## 🎯 Current State (สิ่งที่ทำเสร็จแล้ว)

### ✅ Core Features Complete

1. **Vector Search System**
   - MongoDB Atlas M0 integration
   - Sentence-transformers embeddings (all-MiniLM-L6-v2)
   - Parent-Child retrieval strategy
   - Vector index with filters (brand_name, doc_type)

2. **Hybrid Retrieval System** 🥇
   - Vector Search (semantic)
   - BM25 Search (keyword matching)
   - RRF Score Fusion (configurable weights)
   - Best performance: F1=0.570, 100% success rate

3. **Production FastAPI**
   - 9 REST endpoints (health, search, brands, stats)
   - Auto-generated docs (Swagger UI, ReDoc)
   - CORS enabled
   - Pydantic validation
   - Error handling

4. **Evaluation System**
   - Comprehensive metrics: P@K, R@K, F1, MRR, NDCG
   - 10 test cases with ground truth
   - Benchmark comparison (3 methods)
   - Results saved to JSON

5. **Configuration Management**
   - 5 YAML config files
   - default.yaml (reference)
   - vector_search.yaml
   - hybrid_search.yaml (recommended)
   - api.yaml
   - ingestion.yaml

6. **Complete Documentation**
   - README.md (40KB+)
   - QUICKSTART.md (13KB)
   - MONGODB_SETUP.md (30KB)
   - COMPLETION_SUMMARY.md
   - QUICK_REFERENCE.md
   - API_GUIDE.md

---

## 🔧 Important Technical Decisions

### Why These Choices?

**1. MongoDB Atlas M0 (Free Tier)**
- ✅ Zero cost
- ✅ Built-in Vector Search
- ✅ 512MB storage (enough for demo)
- ✅ Cloud-based (no local setup)
- ⚠️ Shared resources (slower)

**2. sentence-transformers (all-MiniLM-L6-v2)**
- ✅ Free, local execution
- ✅ 384 dimensions (small, fast)
- ✅ Good quality for general use
- ✅ CPU-friendly
- ❌ Not as good as OpenAI embeddings

**3. Hybrid Retrieval (Vector + BM25)**
- ✅ Best quality (F1=0.570)
- ✅ Handles both semantic and keyword queries
- ✅ 100% success rate
- ⚠️ Slower than single method (456ms)

**4. Parent-Child Strategy**
- ✅ Best of both worlds: precision + context
- ✅ Search on small chunks (precise)
- ✅ Return full documents (rich context)
- ✅ Reduces storage (only children have embeddings)

**5. FastAPI**
- ✅ Modern, fast
- ✅ Auto-generated docs
- ✅ Async support
- ✅ Pydantic validation
- ✅ Easy deployment

---

## 🐛 Known Issues & Workarounds

### 1. MongoDB Bugs (FIXED)

**Issue**: Vector search aggregation pipeline error
- **Location**: `mongodb_vector.py` line 219
- **Fix**: Moved `filter_dict` into `$vectorSearch` stage
- **Status**: ✅ Fixed

**Issue**: ObjectId conversion error in parent retrieval
- **Location**: `mongodb_vector.py` `get_parent_document()`
- **Fix**: Added `ObjectId()` conversion
- **Status**: ✅ Fixed

### 2. Integration with Module 4

**Issue**: Requires GPU for model loading (3.09GB)
- **Workaround**: Use `test_integration_quick.py` (no model)
- **Status**: ⚠️ Known limitation

### 3. BM25 NLTK Dependency

**Issue**: punkt_tab tokenizer not found
- **Location**: `hybrid_retriever.py`
- **Fix**: Added `nltk.download('punkt_tab', quiet=True)`
- **Status**: ✅ Fixed

---

## 📊 Performance Benchmarks (Reference)

### Retrieval Methods Comparison (10 queries, K=3)

| Method | Precision@3 | Recall@3 | F1 | MRR | NDCG@3 | Success | Latency |
|--------|-------------|----------|-----|-----|--------|---------|---------|
| **Hybrid** | **0.433** 🥇 | **0.900** | **0.570** | **0.950** | **0.890** | **100%** | 456ms |
| Vector | 0.400 | 0.850 | 0.530 | 0.833 | 0.830 | 90% | 34ms ⚡ |
| BM25 | 0.367 | 0.800 | 0.490 | 0.900 | 0.820 | 90% | 9.4ms ⚡⚡ |

**Key Insights for Future Development:**
- Hybrid is best for quality (use for production)
- BM25 is fastest (use for real-time with keyword queries)
- Vector is balanced (good default)

---

## 🔐 Important Context (ต้องรู้!)

### 1. ระบบไม่มี Docker

**จาก conversation**: "ระบบเราไม่มี Docker ครับ"

ดังนั้น:
- ❌ ห้ามใช้ Docker deployment
- ✅ ใช้ systemd (Linux), PM2 (cross-platform), หรือ simple Python
- ✅ Deployment guide มีอยู่ใน README.md แล้ว

### 2. Zero-Cost Philosophy

**จาก course file**: "ห้ามเสียเงินแม้แต่บาทเดียว"

ดังนั้น:
- ✅ MongoDB Atlas M0 (free)
- ✅ sentence-transformers (free)
- ✅ All libraries open-source
- ❌ ห้ามใช้ OpenAI API (ต้องจ่ายเงิน)
- ❌ ห้ามใช้ MongoDB M10+ (ต้องจ่ายเงิน)

### 3. Current Database

**MongoDB Atlas Cluster:**
- Name: `ai-director`
- Region: Singapore (ap-southeast-1)
- Tier: M0 Free (512MB)
- Database: `ai_director`
- Collection: `brand_vectors`
- Documents: 38 (8 parents + 30 children)
- Index: `vector_index` (READY, 100% indexed)

**Credentials** (บันทึกไว้):
```
Username: ai-director_db
Password: b6ePMwfs1f3jqYNT
URI: mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?appName=ai-director
```

### 4. Test Data

**Source**: `module2/data/raw/brands_v2.json`

**Brands** (8 total):
1. CoffeeLab - Coffee & Beverage
2. FitFlow - Fitness & Wellness
3. GreenLeaf - Eco-friendly Products
4. TechZone - Technology & Gadgets
5. UrbanNest - Home & Lifestyle
6. PetPals - Pet Care
7. GlowLab - Beauty & Skincare
8. EduKid - Education & Kids

---

## 🚀 Next Steps (งานที่ควรทำต่อ)

### Priority 1: Immediate Improvements

1. **Add Caching Layer**
   - Use Redis or in-memory cache
   - Cache frequent queries
   - Reduce latency for common searches
   - **Impact**: 50-80% latency reduction

2. **Optimize Hybrid Latency**
   - Current: 456ms (slow)
   - Goal: <100ms
   - Methods:
     - Parallel execution of Vector + BM25
     - Cache embeddings
     - Pre-build BM25 index on startup
   - **Impact**: Better user experience

3. **Add Query Preprocessing**
   - Thai language processing
   - Query expansion with synonyms
   - Spelling correction
   - **Impact**: Better accuracy

### Priority 2: Advanced Features

4. **Re-ranking with Cross-Encoder**
   - Use cross-encoder model for final re-ranking
   - Improves relevance of top results
   - **Impact**: +5-10% F1 score

5. **Multi-lingual Support**
   - Use multilingual embedding model
   - Support English + Thai queries
   - **Impact**: Wider use cases

6. **Contextual Embeddings**
   - Add chunk context (before/after text)
   - Improves semantic understanding
   - **Impact**: +3-5% accuracy

### Priority 3: Production Features

7. **Monitoring & Observability**
   - Add Prometheus metrics
   - Grafana dashboards
   - Query logging
   - Performance tracking
   - **Impact**: Better ops

8. **A/B Testing Framework**
   - Test different retrieval methods
   - Test different weights
   - Track user feedback
   - **Impact**: Data-driven improvements

9. **User Feedback Loop**
   - Click tracking
   - Relevance feedback
   - Learning from user behavior
   - **Impact**: Continuous improvement

### Priority 4: Integration

10. **Module 4 + 5 Integration**
    - Connect with fine-tuned models
    - End-to-end RAG pipeline
    - GPU deployment guide
    - **Impact**: Complete system

11. **Module 6 Integration**
    - Connect with production tools
    - Image generation with RAG
    - Voice generation with context
    - **Impact**: Full AI Director

---

## 📁 Important Files Reference

### Source Code (Must Understand)

```
src/module5/
├── __init__.py              - Module exports
├── embedding_models.py      - Embedder wrappers (180 lines)
├── mongodb_vector.py        - Vector store + BUGS FIXED (309 lines)
├── parent_child_retriever.py - Vector retrieval (315 lines)
└── hybrid_retriever.py      - Hybrid retrieval ⭐ (400 lines)
```

### Scripts (For Testing)

```
scripts/
├── test_retrieval.py        - Basic tests (346 lines)
├── test_hybrid_retrieval.py - Hybrid benchmark (300 lines)
├── inference_rag_v2.py      - Module 4+5 integration (401 lines)
├── test_integration.py      - Full integration (280 lines)
└── test_integration_quick.py - Quick test (150 lines)
```

### Tools (Production)

```
tools/
├── app.py                   - FastAPI server ⭐ (260 lines)
├── evaluate_rag.py          - Evaluation metrics (450 lines)
├── test_api.sh              - API test suite (100 lines)
└── API_GUIDE.md             - API documentation
```

### Configuration

```
configs/
├── default.yaml             - Main reference config
├── vector_search.yaml       - Vector-only setup
├── hybrid_search.yaml       - Hybrid setup ⭐ (recommended)
├── api.yaml                 - FastAPI settings
└── ingestion.yaml           - Data loading config
```

---

## 🎓 Learning Path (สำหรับ AI Agent)

### Week 1: Understanding

1. **Day 1-2**: อ่านเอกสารหลัก (QUICKSTART, README, COMPLETION_SUMMARY)
2. **Day 3**: ลองรัน tests ทั้งหมด, เข้าใจ outputs
3. **Day 4**: อ่าน source code (embedding → mongodb → parent_child)
4. **Day 5**: อ่าน hybrid_retriever.py แบบละเอียด

### Week 2: Experimentation

1. **Day 6-7**: ทดลอง change weights, parameters
2. **Day 8**: ทดลอง add test cases
3. **Day 9**: Profile performance (find bottlenecks)
4. **Day 10**: Plan improvements

### Week 3: Development

1. **Day 11-15**: Implement Priority 1 improvements

---

## 🔍 Code Patterns & Conventions

### 1. Embedding Pattern

```python
# All embedders follow this interface
embedder = get_embedder(embedder_type="sentence-transformers")

# For documents
embeddings = embedder.embed_documents(texts)  # List[str] → List[List[float]]

# For queries
embedding = embedder.embed_query(text)  # str → List[float]
```

### 2. Retrieval Pattern

```python
# All retrievers return consistent format
retriever = HybridProductionRAG()

# Main retrieval method
results = retriever.retrieve(
    query="search query",
    k=3,
    method="hybrid"  # or "vector" or "bm25"
)
# Returns: List[str] (formatted brand contexts)
```

### 3. Configuration Pattern

```python
import yaml

# Load config
with open("configs/hybrid_search.yaml") as f:
    config = yaml.safe_load(f)

# Use config
rag = HybridProductionRAG(
    vector_weight=config["hybrid"]["vector_weight"],
    bm25_weight=config["hybrid"]["bm25_weight"]
)
```

### 4. Error Handling Pattern

```python
try:
    results = retriever.retrieve(query, k=3)
except Exception as e:
    logger.error(f"Retrieval failed: {e}")
    # Fallback or raise
```

---

## 🧪 Testing Guidelines

### Before Making Changes

```bash
# 1. Test basic retrieval
python scripts/test_retrieval.py --test basic

# 2. Test hybrid benchmark
python scripts/test_hybrid_retrieval.py

# 3. Test API
cd tools
bash test_api.sh

# 4. Test evaluation
python tools/evaluate_rag.py --methods hybrid vector bm25 -k 3
```

### After Making Changes

```bash
# Run all tests again
# Compare results with baseline (evaluation_results.json)
# Check performance regression
```

---

## 📞 Getting Help

### Documentation

1. **Module 5 Docs**: อ่าน README.md section ที่เกี่ยวข้อง
2. **MongoDB Issues**: อ่าน MONGODB_SETUP.md Troubleshooting
3. **API Issues**: อ่าน API_GUIDE.md
4. **Quick Lookup**: ใช้ QUICK_REFERENCE.md

### Code References

1. **Example Usage**: ดูใน `scripts/test_*.py`
2. **API Examples**: ดูใน `tools/API_GUIDE.md`
3. **Config Examples**: ดูใน `configs/*.yaml`

---

## ✅ Checklist: Ready to Start?

**Pre-requisites:**

- [ ] อ่าน QUICKSTART.md เสร็จ
- [ ] อ่าน README.md เสร็จ
- [ ] อ่าน COMPLETION_SUMMARY.md เสร็จ
- [ ] เข้าใจ Architecture diagram
- [ ] เข้าใจ Parent-Child strategy
- [ ] เข้าใจ Hybrid retrieval (Vector + BM25 + RRF)
- [ ] รู้ว่าไฟล์ไหนทำอะไร
- [ ] รู้ Performance benchmarks
- [ ] รู้ Known issues
- [ ] รู้ว่า MongoDB Atlas setup ยังไง
- [ ] ลองรัน tests แล้ว (ผ่านหมด)

**Ready to develop?**

- [ ] เข้าใจ current state
- [ ] รู้ next steps ที่ควรทำ
- [ ] รู้ testing guidelines
- [ ] รู้ code patterns
- [ ] รู้ zero-cost philosophy
- [ ] รู้ว่าระบบไม่มี Docker

**ถ้าทำครบแล้ว → เริ่มพัฒนาได้เลย! 🚀**

---

## 🎯 Summary: What to Read First

**Essential (ต้องอ่าน):**
1. QUICKSTART.md
2. README.md
3. COMPLETION_SUMMARY.md
4. This file (DEVELOPER_ONBOARDING.md)

**Source Code (ต้องเข้าใจ):**
1. src/module5/hybrid_retriever.py ⭐
2. src/module5/mongodb_vector.py
3. src/module5/parent_child_retriever.py

**References (อ้างอิงเมื่อต้องการ):**
1. MONGODB_SETUP.md (MongoDB issues)
2. API_GUIDE.md (API development)
3. QUICK_REFERENCE.md (Quick lookup)

---

**Happy Coding! 🎉**

**Questions?** Read the docs first, then experiment!

**Remember:**
- Zero cost (no paid services)
- No Docker
- Production ready
- Well documented
- Test everything

**Version**: 1.0  
**Last Updated**: January 6, 2026  
**Status**: ✅ Ready for Next Developer
