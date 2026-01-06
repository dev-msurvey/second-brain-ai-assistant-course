# FastAPI Production API - Usage Guide

## 🚀 Quick Start

### 1. Start the API Server

```bash
cd module5/tools

# Set MongoDB URI (replace with your connection string)
export MONGO_URI="mongodb+srv://user:password@cluster.mongodb.net/?appName=app"

# Start server
PYTHONPATH=../src:$PYTHONPATH python app.py --host 0.0.0.0 --port 8000
```

Server will start on: `http://localhost:8000`

### 2. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "rag_system": "Hybrid (Vector + BM25)",
  "database": "MongoDB Atlas"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

---

### Search (POST)

```bash
POST /search
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "luxury coffee brand",
  "k": 3,
  "brand_filter": null,
  "method": "hybrid"
}
```

**Parameters:**
- `query` (required): Search query (natural language)
- `k` (optional): Number of results (1-10, default: 3)
- `brand_filter` (optional): Filter by specific brand name
- `method` (optional): Search method
  - `"vector"`: Semantic search only
  - `"bm25"`: Keyword search only
  - `"hybrid"`: Combined (default, recommended)

**Response:**
```json
{
  "query": "luxury coffee brand",
  "method": "hybrid",
  "results": [
    {
      "brand_name": "CoffeeLab",
      "relevance_score": 0.822,
      "text": "Brand Name: CoffeeLab\nTagline: Craft Your Perfect Morning...",
      "matched_chunk": "Premium coffee brand for young professionals..."
    }
  ],
  "latency_ms": 45.2,
  "total_results": 2
}
```

**Examples:**

```bash
# Hybrid search (recommended)
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "luxury coffee brand",
    "k": 2,
    "method": "hybrid"
  }'

# Vector search (semantic)
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "eco-friendly sustainable brand",
    "k": 3,
    "method": "vector"
  }'

# BM25 search (keyword)
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FitFlow fitness workout",
    "k": 2,
    "method": "bm25"
  }'

# Brand-specific search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "product information",
    "k": 1,
    "brand_filter": "CoffeeLab",
    "method": "hybrid"
  }'
```

---

### Search (GET) - Simple

```bash
GET /search/simple?query=luxury+coffee&k=3&method=hybrid
```

**Query Parameters:**
- `query` (required): Search query
- `k` (optional): Number of results (default: 3)
- `brand` (optional): Filter by brand name
- `method` (optional): Search method (default: "hybrid")

**Example:**
```bash
curl "http://localhost:8000/search/simple?query=luxury+coffee&k=2&method=hybrid"
```

---

### List Brands

```bash
GET /brands
```

**Response:**
```json
{
  "brands": ["CoffeeLab", "FitFlow", "GlowLab", ...],
  "total_brands": 8,
  "total_documents": 38,
  "parent_documents": 8,
  "child_documents": 30
}
```

**Example:**
```bash
curl http://localhost:8000/brands
```

---

### System Statistics

```bash
GET /stats
```

**Response:**
```json
{
  "database": "MongoDB Atlas",
  "collection": "brand_vectors",
  "total_documents": 38,
  "parent_documents": 8,
  "child_documents": 30,
  "unique_brands": 8,
  "search_methods": ["vector", "bm25", "hybrid"],
  "embedding_model": "all-MiniLM-L6-v2",
  "embedding_dimensions": 384
}
```

**Example:**
```bash
curl http://localhost:8000/stats
```

---

## 🐍 Python Client Examples

### Using `requests`

```python
import requests

# Initialize
API_URL = "http://localhost:8000"

# Search
response = requests.post(
    f"{API_URL}/search",
    json={
        "query": "luxury coffee brand",
        "k": 3,
        "method": "hybrid"
    }
)

results = response.json()
print(f"Found {results['total_results']} results in {results['latency_ms']:.1f}ms")

for i, result in enumerate(results['results'], 1):
    print(f"{i}. {result['brand_name']} (score: {result['relevance_score']:.3f})")
    print(f"   {result['text'][:100]}...")
```

### Using `httpx` (async)

```python
import httpx
import asyncio

async def search_brands():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/search",
            json={
                "query": "sustainable eco-friendly",
                "k": 2,
                "method": "vector"
            }
        )
        return response.json()

# Run
results = asyncio.run(search_brands())
print(results)
```

---

## 🔧 Configuration

### Environment Variables

```bash
# MongoDB connection (required)
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/"

# Optional: API configuration
export API_HOST="0.0.0.0"
export API_PORT="8000"
```

### Production Deployment

```bash
# With uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4

# With gunicorn + uvicorn workers
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📊 Performance

### Latency Benchmarks

| Method | Avg Latency | Use Case |
|--------|-------------|----------|
| BM25 | ~10ms | Exact keywords, brand names |
| Vector | ~50ms | Semantic queries |
| Hybrid | ~40ms | Best overall quality (recommended) |

### Best Practices

1. **Use Hybrid for most queries**: Best balance of quality and speed
2. **Use BM25 for exact names**: Fastest when searching by brand name
3. **Use Vector for concepts**: Best for semantic/conceptual queries
4. **Set k=3-5**: Optimal balance of results vs latency
5. **Add brand_filter**: Faster when searching within specific brand

---

## 🧪 Testing

### Test Script

```bash
#!/bin/bash
API_URL="http://localhost:8000"

# Health check
echo "Testing health..."
curl -s $API_URL/health | python -m json.tool

# List brands
echo -e "\nListing brands..."
curl -s $API_URL/brands | python -m json.tool

# Search tests
echo -e "\nTesting vector search..."
curl -s -X POST $API_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query":"luxury fashion","k":2,"method":"vector"}' \
  | python -m json.tool

echo -e "\nTesting BM25 search..."
curl -s -X POST $API_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query":"CoffeeLab coffee","k":2,"method":"bm25"}' \
  | python -m json.tool

echo -e "\nTesting hybrid search..."
curl -s -X POST $API_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query":"eco-friendly sustainable","k":2,"method":"hybrid"}' \
  | python -m json.tool
```

---

## 🐛 Troubleshooting

### Issue: "RAG system not initialized"

**Solution:**
```bash
# Ensure MONGO_URI is set
export MONGO_URI="your-connection-string"

# Restart server
python app.py
```

### Issue: "Connection timeout"

**Solution:**
- Check MongoDB Atlas network access (IP whitelist)
- Verify connection string is correct
- Test connection: `python -c "from pymongo import MongoClient; MongoClient('your-uri').admin.command('ping')"`

### Issue: Slow responses

**Solution:**
1. Use BM25 for keyword queries (faster)
2. Reduce k value (fewer results = faster)
3. Add brand_filter to narrow search
4. Check MongoDB Atlas performance metrics

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **Module 5 README**: ../README.md
- **Quick Start Guide**: ../QUICKSTART.md
