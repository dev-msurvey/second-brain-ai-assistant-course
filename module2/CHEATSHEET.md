# 📖 Module 2 - Quick Reference

**Module:** ETL Pipeline  
**AI Director v3.4**

---

## 🚀 Quick Commands

```bash
# Setup
cd module2
bash setup.sh

# Run full pipeline
python etl_pipeline.py

# Test components
python scripts/extract.py
python scripts/transform.py
python scripts/load.py
```

---

## 📦 MongoDB Atlas Setup

### 1. Create Free Cluster

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up (free)
3. Create M0 (free) cluster
   - Provider: AWS
   - Region: Singapore (ap-southeast-1)

### 2. Configure Access

**Database Access:**
```
Username: ai_director_user
Password: (your secure password)
```

**Network Access:**
```
IP Address: 0.0.0.0/0 (development only!)
```

### 3. Get Connection String

```
mongodb+srv://ai_director_user:<password>@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 4. Set Environment Variable

```bash
# Create .env file
echo 'MONGO_URI="your_connection_string"' > .env

# Or export
export MONGO_URI="your_connection_string"
```

---

## 🔧 ETL Components

### Extract

```python
from scripts.extract import DataExtractor

extractor = DataExtractor()
brands = extractor.extract_brands()
campaigns = extractor.extract_campaigns()
```

**Supported Formats:**
- JSON (brands, campaigns)
- TXT (briefs, scripts)
- SRT (transcripts)

### Transform

```python
from scripts.transform import DataTransformer

transformer = DataTransformer()
clean_brands = transformer.transform_brands(brands_raw)
clean_campaigns = transformer.transform_campaigns(campaigns_raw)
```

**Operations:**
- Data cleaning
- Validation (Pydantic)
- Quality scoring
- Timestamp addition

### Load

```python
from scripts.load import MongoDBLoader

loader = MongoDBLoader()
loader.load_brands(brands, clear_existing=True)
loader.load_campaigns(campaigns, clear_existing=True)

stats = loader.get_stats()
loader.close()
```

---

## 📊 Data Schemas

### Brand

```python
{
    "name": str,              # Unique
    "description": str,
    "tone": str,
    "colors": [str],
    "fonts": [str],
    "target_audience": str,
    "brand_values": [str],
    "social_media": dict,
    "quality_score": float,   # 0-1
    "created_at": datetime,
    "updated_at": datetime
}
```

### Campaign

```python
{
    "brand_name": str,
    "campaign_name": str,
    "brief": str,
    "objectives": [str],
    "target_metrics": dict,
    "content_requirements": dict,
    "status": str,            # draft|active|completed
    "quality_score": float,   # 0-1
    "created_at": datetime,
    "updated_at": datetime
}
```

---

## 🗄️ MongoDB Operations

### Connect

```python
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client["ai_director"]
```

### Insert

```python
# Single
db.brands.insert_one(brand_doc)

# Multiple
db.brands.insert_many(brand_docs)
```

### Query

```python
# Find all
brands = list(db.brands.find())

# Find one
brand = db.brands.find_one({"name": "CoffeeLab"})

# Filter
high_quality = db.brands.find({"quality_score": {"$gte": 0.8}})

# Sort
recent = db.campaigns.find().sort("created_at", -1).limit(10)
```

### Update

```python
# Update one
db.brands.update_one(
    {"name": "CoffeeLab"},
    {"$set": {"tone": "premium, modern"}}
)

# Replace
db.brands.replace_one(
    {"name": "CoffeeLab"},
    new_brand_doc,
    upsert=True
)
```

### Delete

```python
# Delete one
db.brands.delete_one({"name": "OldBrand"})

# Delete many
db.campaigns.delete_many({"status": "draft"})

# Clear collection
db.brands.delete_many({})
```

### Count

```python
# Count all
count = db.brands.count_documents({})

# Count filtered
draft_count = db.campaigns.count_documents({"status": "draft"})
```

---

## 📈 Quality Score Calculation

```python
def calculate_quality_score(text, secondary_text, extra_items):
    score = 0.0
    
    # Text length (40%)
    if len(text) >= 100:
        score += 0.4
    elif len(text) >= 50:
        score += 0.2
    
    # Secondary text (30%)
    if len(secondary_text) > 5:
        score += 0.3
    
    # Extra items (30%)
    if extra_items >= 3:
        score += 0.3
    elif extra_items >= 1:
        score += 0.15
    
    return round(score, 2)
```

**Examples:**
- Long description + tone + 3 values = **1.00**
- Medium description + tone + 1 value = **0.65**
- Short description = **0.20**

---

## ⚠️ Troubleshooting

### Connection Failed

```python
# Error: pymongo.errors.ServerSelectionTimeoutError

# Solutions:
1. Check MONGO_URI is set
2. Verify username/password
3. Check IP whitelist (0.0.0.0/0)
4. Test connectivity: ping cluster address
```

### Authentication Error

```python
# Error: pymongo.errors.OperationFailure: Authentication failed

# Solutions:
1. Verify username/password in connection string
2. Check user has readWrite role
3. Database user may need time to propagate
```

### Import Error

```python
# Error: ModuleNotFoundError: No module named 'pymongo'

# Solution:
pip install -r requirements.txt
```

### File Not Found

```python
# Error: FileNotFoundError: data/raw/brands.json

# Solution:
bash setup.sh  # Creates sample data
```

---

## 🔍 Validation Queries

### Check Collections

```python
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client["ai_director"]

print("Collections:", db.list_collection_names())
print("Brands:", db.brands.count_documents({}))
print("Campaigns:", db.campaigns.count_documents({}))
```

### Sample Queries

```python
# Get all brands
brands = list(db.brands.find())

# High quality campaigns
good_campaigns = db.campaigns.find({"quality_score": {"$gte": 0.8}})

# Active campaigns for a brand
active = db.campaigns.find({
    "brand_name": "CoffeeLab",
    "status": "active"
})

# Recent documents
recent = db.brands.find().sort("created_at", -1).limit(5)
```

### Aggregation

```python
# Average quality by brand
pipeline = [
    {"$group": {
        "_id": "$brand_name",
        "avg_quality": {"$avg": "$quality_score"},
        "count": {"$sum": 1}
    }}
]
results = list(db.campaigns.aggregate(pipeline))
```

---

## 📚 Useful Resources

### MongoDB
- [MongoDB Atlas Docs](https://www.mongodb.com/docs/atlas/)
- [PyMongo Tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)
- [Query Operators](https://www.mongodb.com/docs/manual/reference/operator/query/)

### Python Libraries
- [Pydantic Docs](https://docs.pydantic.dev/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [loguru](https://loguru.readthedocs.io/)

### ETL Patterns
- [ETL Best Practices](https://www.ibm.com/cloud/blog/etl-vs-elt)
- [Data Pipeline Design](https://medium.com/data-reply-it-datatech/data-pipeline-design-patterns-100afa4b93e3)

---

## 💡 Tips & Tricks

### 1. Batch Processing

```python
# Process in batches
BATCH_SIZE = 100
for i in range(0, len(docs), BATCH_SIZE):
    batch = docs[i:i+BATCH_SIZE]
    collection.insert_many(batch)
```

### 2. Upsert Pattern

```python
# Insert or update
collection.replace_one(
    {"name": brand["name"]},
    brand,
    upsert=True
)
```

### 3. Error Handling

```python
from pymongo.errors import DuplicateKeyError

try:
    collection.insert_one(doc)
except DuplicateKeyError:
    collection.replace_one({"_id": doc["_id"]}, doc)
```

### 4. Index Creation

```python
# Speed up queries
collection.create_index([("name", 1)], unique=True)
collection.create_index([("quality_score", -1)])
collection.create_index([("brand_name", 1), ("status", 1)])
```

---

## 🎯 Module Checklist

- [x] Setup MongoDB Atlas M0 cluster
- [x] Create database user
- [x] Whitelist IP address
- [x] Get connection string
- [x] Set MONGO_URI in .env
- [x] Run `bash setup.sh`
- [x] Test extraction: `python scripts/extract.py`
- [x] Test transformation: `python scripts/transform.py`
- [x] Test loading: `python scripts/load.py` (requires MongoDB)
- [x] Run full pipeline: `python etl_pipeline.py`
- [x] Verify in MongoDB Atlas dashboard
- [x] Check data quality scores

---

**Time to Complete:** 2-3 hours  
**Cost:** $0.00 (free tier only)  
**Next:** Module 3 - Dataset Generation
