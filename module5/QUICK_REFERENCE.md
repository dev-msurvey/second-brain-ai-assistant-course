# Module 5 Quick Reference Card

## 🚀 Quick Commands

### Setup
```bash
# Install
pip install -r requirements.txt

# Set MongoDB
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/?appName=ai-director"

# Ingest data
python pipelines/json_ingestion.py --clear
```

### Vector Search
```python
from module5.parent_child_retriever import ProductionRAG

rag = ProductionRAG()
results = rag.retrieve("coffee shop", k=3)
rag.close()
```

### Hybrid Search (RECOMMENDED)
```python
from module5.hybrid_retriever import HybridProductionRAG

rag = HybridProductionRAG()
results = rag.retrieve("coffee shop", k=3, method="hybrid")
rag.close()
```

### FastAPI
```bash
# Start server
cd tools
python app.py --host 0.0.0.0 --port 8000

# Test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "coffee", "k": 3, "method": "hybrid"}'
```

### Evaluation
```bash
cd tools
python evaluate_rag.py --methods hybrid vector bm25 -k 3 --save
```

---

## 📊 Performance Reference

| Method | F1 | Latency | Use Case |
|--------|-------|---------|----------|
| **Hybrid** | **0.570** 🥇 | 456ms | Production (best quality) |
| **Vector** | 0.530 | 34ms ⚡ | Semantic queries |
| **BM25** | 0.490 | 9.4ms ⚡⚡ | Keyword queries |

---

## 🔧 Configuration

### Hybrid Weights
```python
rag = HybridProductionRAG(
    vector_weight=0.5,  # Semantic
    bm25_weight=0.5,    # Keyword
    rrf_k=60            # Fusion parameter
)
```

### Using YAML Configs
```python
import yaml

with open("configs/hybrid_search.yaml") as f:
    config = yaml.safe_load(f)

rag = HybridProductionRAG(
    vector_weight=config["hybrid"]["vector_weight"],
    bm25_weight=config["hybrid"]["bm25_weight"]
)
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| POST | `/search` | Main search (JSON body) |
| GET | `/search/simple` | Simple GET search |
| GET | `/brands` | List all brands |
| GET | `/stats` | System statistics |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc |

---

## 🐛 Troubleshooting

### No MONGO_URI
```bash
export MONGO_URI="mongodb+srv://..."
```

### No Results
```bash
# Check documents
python -c "from module5.mongodb_vector import MongoDBVectorStore; print(MongoDBVectorStore().get_collection_stats())"

# Re-ingest
python pipelines/json_ingestion.py --clear
```

### Vector Index Missing
Go to MongoDB Atlas → Database → Search → Create Search Index

### API Won't Start
```bash
# Check port
lsof -i :8000

# Kill process
kill -9 $(lsof -t -i :8000)
```

---

## 📁 Config Files

| File | Purpose |
|------|---------|
| `default.yaml` | Complete reference config |
| `vector_search.yaml` | Vector-only setup |
| `hybrid_search.yaml` | Hybrid setup (RECOMMENDED) |
| `api.yaml` | FastAPI production settings |
| `ingestion.yaml` | Data loading config |

---

## 📚 Documentation

- **README**: [README.md](README.md) - Complete documentation
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - 10-minute setup
- **API Guide**: [tools/API_GUIDE.md](tools/API_GUIDE.md) - API usage
- **Completion**: [COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md) - What's built

---

## 🎯 Recommendations

### For Production
✅ Use **Hybrid** method (best quality)  
✅ Enable **caching** (configs/api.yaml)  
✅ Use **systemd** or **PM2** (deployment)  
✅ Add **nginx** reverse proxy  
✅ Monitor with `/health` endpoint

### For Development
✅ Use **Vector** method (balanced)  
✅ Test with `test_api.sh`  
✅ Run evaluation regularly  
✅ Use YAML configs for experiments

### For Speed
✅ Use **BM25** method (9.4ms)  
✅ Enable `cache_embeddings: true`  
✅ Use `build_bm25_on_startup: true`

---

## 💡 Tips

1. **Method Selection**: `method="hybrid"` (quality), `"bm25"` (speed), `"vector"` (balanced)
2. **K Parameter**: Start with k=3, increase if needed (max 10 recommended)
3. **Weights**: Adjust `vector_weight` and `bm25_weight` based on use case
4. **Monitoring**: Use `/stats` endpoint to check system health
5. **Evaluation**: Run regularly to track performance changes

---

**Version**: 1.0 | **Status**: Production Ready ✅
