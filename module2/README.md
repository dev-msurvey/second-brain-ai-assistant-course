# 📦 Module 2 - ETL Pipeline

**Course:** AI Director v3.4  
**Module:** Extract, Transform, Load Pipeline  
**Prerequisites:** Module 1 completed  
**Duration:** 2-3 hours

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. **Extract** data from various sources (JSON, text files, APIs)
2. **Transform** raw data into structured formats
3. **Load** data into MongoDB Atlas (cloud database)
4. **Validate** data quality and integrity
5. **Build** complete ETL pipelines for AI applications
6. **Understand** data schemas for brand knowledge base

---

## 📋 Module Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     ETL PIPELINE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   EXTRACT                 TRANSFORM                LOAD          │
│   ┌────────┐            ┌─────────┐            ┌────────┐      │
│   │ Brand  │            │ Clean   │            │MongoDB │      │
│   │  Data  │───────────▶│Validate │───────────▶│ Atlas  │      │
│   │ (JSON) │            │ Enrich  │            │ (M0)   │      │
│   └────────┘            └─────────┘            └────────┘      │
│                                                                  │
│   ┌────────┐            ┌─────────┐            ┌────────┐      │
│   │Campaign│            │ Score   │            │ Brands │      │
│   │  Brief │───────────▶│Quality  │───────────▶│Collection │   │
│   │ (TXT)  │            │ Format  │            └────────┘      │
│   └────────┘            └─────────┘                             │
│                                                                  │
│   ┌────────┐            ┌─────────┐            ┌────────┐      │
│   │Video   │            │ Extract │            │Transcripts│   │
│   │Transcr.│───────────▶│Metadata │───────────▶│Collection │   │
│   │ (SRT)  │            │ Parse   │            └────────┘      │
│   └────────┘            └─────────┘                             │
│                                                                  │
│   OUTPUT: Structured knowledge base ready for RAG (Module 5)    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Module Structure

```
module2/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── setup.sh                     # Setup script
├── etl_pipeline.py              # Main ETL pipeline
│
├── scripts/
│   ├── extract.py               # Data extraction
│   ├── transform.py             # Data transformation
│   ├── load.py                  # Data loading to MongoDB
│   └── validate.py              # Data validation
│
├── examples/
│   ├── example_extract.py       # Extraction examples
│   ├── example_transform.py     # Transformation examples
│   └── example_load.py          # Loading examples
│
├── data/
│   ├── raw/                     # Raw input data
│   │   ├── brands.json          # Brand information
│   │   ├── campaigns.json       # Campaign briefs
│   │   └── transcripts/         # Video transcripts
│   └── processed/               # Processed data
│
├── CHEATSHEET.md                # Quick reference
└── LESSON_LEARNED.md            # Summary (created after completion)
```

---

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Navigate to module2
cd /workspaces/second-brain-ai-assistant-course/module2

# Run setup script
bash setup.sh

# Verify MongoDB connection
python scripts/validate.py --check-mongodb
```

### 2. MongoDB Atlas Setup (One-time)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create M0 (free) cluster
   - Cluster Name: `ai-director`
   - Provider: AWS
   - Region: Singapore (ap-southeast-1)
4. Database Access
   - Create user: `ai_director_user`
   - Password: (save it!)
5. Network Access
   - Add IP: `0.0.0.0/0` (development only)
6. Get Connection String
   - Click "Connect" → "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password

```bash
# Set environment variable
export MONGO_URI="mongodb+srv://ai_director_user:<password>@ai-director.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# Or create .env file
echo 'MONGO_URI="your_connection_string_here"' > .env
```

### 3. Run ETL Pipeline

```bash
# Full pipeline (Extract → Transform → Load)
python etl_pipeline.py

# Or step by step
python scripts/extract.py         # Step 1: Extract
python scripts/transform.py       # Step 2: Transform
python scripts/load.py             # Step 3: Load
```

### 4. Verify Data

```bash
# Check loaded data
python scripts/validate.py --check-data

# View data in MongoDB Atlas
# Go to Atlas → Browse Collections → ai_director database
```

---

## 📊 Data Schemas

### 1. Brand Schema

```python
{
    "_id": ObjectId("..."),
    "name": str,                      # "CoffeeLab"
    "description": str,                # "Premium coffee brand..."
    "tone": str,                       # "friendly, premium, modern"
    "colors": [str],                   # ["#8B4513", "#F5F5DC"]
    "fonts": [str],                    # ["Montserrat", "Open Sans"]
    "target_audience": str,            # "young professionals 25-35"
    "brand_values": [str],             # ["quality", "sustainability"]
    "social_media": {
        "instagram": str,
        "facebook": str,
        "tiktok": str
    },
    "created_at": datetime,
    "updated_at": datetime
}
```

### 2. Campaign Schema

```python
{
    "_id": ObjectId("..."),
    "brand_name": str,                 # "CoffeeLab"
    "campaign_name": str,              # "Cold Brew Launch 2025"
    "brief": str,                      # Full campaign brief
    "objectives": [str],               # ["awareness", "sales"]
    "target_metrics": {
        "reach": int,
        "engagement_rate": float,
        "conversion_rate": float
    },
    "content_requirements": {
        "image_count": int,
        "video_count": int,
        "formats": [str]               # ["reel", "story", "post"]
    },
    "generated_assets": [{
        "type": str,                   # "image|video|audio"
        "url": str,
        "prompt": str,
        "created_at": datetime
    }],
    "status": str,                     # "draft|active|completed"
    "created_at": datetime,
    "updated_at": datetime
}
```

### 3. Transcript Schema

```python
{
    "_id": ObjectId("..."),
    "video_id": str,                   # "coffee_tutorial_001"
    "filename": str,                   # "coffee_brewing.mp4"
    "duration": float,                 # 180.5 (seconds)
    "language": str,                   # "th" or "en"
    "segments": [{
        "id": int,
        "start": float,                # 0.0
        "end": float,                  # 5.2
        "text": str,                   # "สวัสดีครับ วันนี้..."
        "speaker": str                 # "narrator"
    }],
    "metadata": {
        "resolution": str,             # "1920x1080"
        "fps": int,                    # 30
        "bitrate": int                 # 5000 (kbps)
    },
    "quality_score": float,            # 0.85 (0-1)
    "keywords": [str],                 # ["coffee", "brewing"]
    "created_at": datetime
}
```

---

## 🔧 ETL Components

### Extract (E)

**Purpose:** Read data from various sources

**Supported Sources:**
- ✅ JSON files (brand data, campaigns)
- ✅ Text files (briefs, scripts)
- ✅ SRT files (transcripts)
- ✅ CSV files (metrics, analytics)

**Example:**
```python
from scripts.extract import extract_brands, extract_campaigns

# Extract brand data
brands = extract_brands("data/raw/brands.json")

# Extract campaigns
campaigns = extract_campaigns("data/raw/campaigns.json")
```

### Transform (T)

**Purpose:** Clean, validate, and enrich data

**Operations:**
- ✅ Data cleaning (remove nulls, fix formats)
- ✅ Validation (required fields, data types)
- ✅ Quality scoring (content quality 0-1)
- ✅ Enrichment (add timestamps, IDs)
- ✅ Normalization (consistent formats)

**Example:**
```python
from scripts.transform import transform_brands, score_quality

# Transform and clean
clean_brands = transform_brands(brands)

# Add quality scores
scored_brands = score_quality(clean_brands)
```

### Load (L)

**Purpose:** Insert data into MongoDB Atlas

**Operations:**
- ✅ Connect to MongoDB
- ✅ Create collections
- ✅ Insert documents
- ✅ Create indexes
- ✅ Verify insertion

**Example:**
```python
from scripts.load import load_to_mongodb

# Load brands to MongoDB
result = load_to_mongodb(
    data=scored_brands,
    collection_name="brands",
    clear_existing=True
)
print(f"Loaded {result['count']} documents")
```

---

## 📝 Usage Examples

### Example 1: Extract Brand Data

```bash
python examples/example_extract.py
```

Demonstrates:
- Reading JSON files
- Parsing brand information
- Handling missing fields
- Output validation

### Example 2: Transform Campaign Briefs

```bash
python examples/example_transform.py
```

Demonstrates:
- Text cleaning
- Quality scoring
- Field normalization
- Data enrichment

### Example 3: Load to MongoDB

```bash
python examples/example_load.py
```

Demonstrates:
- MongoDB connection
- Batch insertion
- Index creation
- Error handling

---

## 🎯 Module Tasks

### Task 1: Setup MongoDB Atlas ✅

- [ ] Create MongoDB Atlas account
- [ ] Create M0 (free) cluster
- [ ] Create database user
- [ ] Whitelist IP address
- [ ] Get connection string
- [ ] Test connection

### Task 2: Run Extract Script ✅

- [ ] Review raw data in `data/raw/`
- [ ] Run extraction script
- [ ] Verify extracted data
- [ ] Check data completeness

### Task 3: Run Transform Script ✅

- [ ] Apply data cleaning
- [ ] Calculate quality scores
- [ ] Add metadata
- [ ] Validate transformed data

### Task 4: Run Load Script ✅

- [ ] Connect to MongoDB
- [ ] Create collections
- [ ] Insert documents
- [ ] Verify in Atlas dashboard

### Task 5: Run Full Pipeline ✅

- [ ] Run `etl_pipeline.py`
- [ ] Check all 3 collections populated
- [ ] Verify data counts
- [ ] Test queries

---

## 🧪 Testing

### Unit Tests

```bash
# Test extraction
pytest tests/test_extract.py

# Test transformation
pytest tests/test_transform.py

# Test loading
pytest tests/test_load.py
```

### Integration Test

```bash
# Test full pipeline
pytest tests/test_pipeline.py
```

### Manual Verification

```bash
# Check MongoDB data
python scripts/validate.py --full-check

# Query samples
python scripts/validate.py --sample-brands 5
python scripts/validate.py --sample-campaigns 5
```

---

## 📊 Expected Outcomes

After completing this module:

✅ **MongoDB Collections:**
- `brands` - 5+ brand documents
- `campaigns` - 10+ campaign documents
- `transcripts` - 20+ transcript documents

✅ **Data Quality:**
- All required fields present
- Quality scores calculated
- Timestamps added
- Consistent formatting

✅ **Skills Gained:**
- ETL pipeline design
- MongoDB operations
- Data validation
- Quality scoring

---

## ⚠️ Troubleshooting

### MongoDB Connection Failed

```python
# Error: MongoServerError: authentication failed

# Solution:
# 1. Check username/password in connection string
# 2. Verify IP whitelist (add 0.0.0.0/0)
# 3. Check network connectivity
```

### Data Extraction Error

```python
# Error: FileNotFoundError: data/raw/brands.json

# Solution:
# 1. Check file path
# 2. Ensure data files exist in data/raw/
# 3. Run setup.sh to create sample data
```

### Quality Score Issues

```python
# Error: Quality score always 0

# Solution:
# 1. Check text content not empty
# 2. Verify language detection working
# 3. Review scoring algorithm
```

---

## 🔗 Related Modules

- **Module 1:** Dual-Model Architecture (prerequisite)
- **Module 3:** Dataset Generation (uses this data)
- **Module 5:** RAG Implementation (uses this data)

---

## 📚 Additional Resources

### MongoDB Atlas
- [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)
- [PyMongo Tutorial](https://pymongo.readthedocs.io/en/stable/tutorial.html)
- [MongoDB University Free Courses](https://university.mongodb.com/)

### ETL Best Practices
- [ETL vs ELT](https://www.ibm.com/cloud/blog/etl-vs-elt)
- [Data Pipeline Design Patterns](https://medium.com/data-reply-it-datatech/data-pipeline-design-patterns-100afa4b93e3)

### Python Libraries
- [pymongo](https://pymongo.readthedocs.io/) - MongoDB driver
- [pydantic](https://docs.pydantic.dev/) - Data validation
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variables

---

## 🎓 Key Concepts

### ETL vs ELT

**ETL (Extract, Transform, Load):**
- Transform BEFORE loading
- Good for: Clean, structured data
- Use when: Limited storage, strict schema

**ELT (Extract, Load, Transform):**
- Load FIRST, transform later
- Good for: Big data, flexible schema
- Use when: Lots of storage, exploration needed

**This module uses ETL** because:
- ✅ Small dataset size
- ✅ Clear schema requirements
- ✅ MongoDB is cost-optimized (512MB free)

### Data Quality Scoring

```python
def calculate_quality_score(text: str) -> float:
    """Calculate quality score 0-1"""
    score = 0.0
    
    # Length (25%)
    if len(text) > 100:
        score += 0.25
    
    # Language confidence (25%)
    lang_conf = detect_language_confidence(text)
    score += lang_conf * 0.25
    
    # Keyword density (25%)
    keyword_score = calculate_keyword_density(text)
    score += keyword_score * 0.25
    
    # Readability (25%)
    readability = calculate_readability(text)
    score += readability * 0.25
    
    return score
```

### MongoDB Indexing

```python
# Create index for fast queries
collection.create_index([("brand_name", 1)])
collection.create_index([("created_at", -1)])
collection.create_index([("quality_score", -1)])

# Compound index
collection.create_index([
    ("brand_name", 1),
    ("status", 1)
])

# Text search index
collection.create_index([("description", "text")])
```

---

## 💡 Tips & Best Practices

### 1. Data Validation

```python
# Always validate before loading
from pydantic import BaseModel, Field

class Brand(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    tone: str
    colors: list[str] = Field(default_factory=list)
    
    class Config:
        validate_assignment = True
```

### 2. Error Handling

```python
# Handle errors gracefully
try:
    result = load_to_mongodb(data, collection_name)
except ConnectionFailure:
    logger.error("MongoDB connection failed")
    # Fallback: save to JSON
    save_to_json(data, "backup.json")
```

### 3. Batch Processing

```python
# Process in batches for large datasets
def batch_insert(collection, documents, batch_size=100):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        collection.insert_many(batch)
        logger.info(f"Inserted batch {i//batch_size + 1}")
```

### 4. Idempotency

```python
# Make pipeline idempotent (safe to run multiple times)
def load_to_mongodb(data, collection_name, clear_existing=True):
    if clear_existing:
        collection.delete_many({})  # Clear before insert
    
    # Upsert instead of insert
    for doc in data:
        collection.replace_one(
            {"_id": doc["_id"]},
            doc,
            upsert=True
        )
```

---

## 🎯 Success Criteria

- ✅ MongoDB Atlas M0 cluster running
- ✅ All 3 collections created and populated
- ✅ Data quality scores > 0.7 average
- ✅ All validation tests passing
- ✅ ETL pipeline runs end-to-end
- ✅ Data queryable from Atlas dashboard

**Time to Complete:** 2-3 hours  
**Cost:** $0.00 (using free tier only)

---

**Next Module:** [Module 3 - Dataset Generation](../module3/README.md)

**Need Help?** Check [CHEATSHEET.md](CHEATSHEET.md) for quick reference

---

📝 **Note:** After completing this module, create `LESSON_LEARNED.md` to document your experience and learnings!
