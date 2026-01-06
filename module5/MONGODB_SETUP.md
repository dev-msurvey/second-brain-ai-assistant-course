# MongoDB Atlas Setup Guide (เริ่มต้นตั้งแต่ศูนย์) 🗄️

> **วิธีการ setup MongoDB Atlas แบบละเอียดทุกขั้นตอน สำหรับ Module 5**

**เวลาที่ใช้**: ~15-20 นาที  
**ค่าใช้จ่าย**: $0 (ใช้ M0 Free Tier)  
**ไม่ต้องใส่บัตรเครดิต**: ✅

---

## 📚 สารบัญ

1. [สร้าง MongoDB Atlas Account](#1-สร้าง-mongodb-atlas-account)
2. [สร้าง Free Cluster M0](#2-สร้าง-free-cluster-m0)
3. [สร้าง Database User](#3-สร้าง-database-user)
4. [Whitelist IP Address](#4-whitelist-ip-address)
5. [Get Connection String](#5-get-connection-string)
6. [Create Database and Collection](#6-create-database-and-collection)
7. [Create Vector Search Index](#7-create-vector-search-index)
8. [Test Connection](#8-test-connection)
9. [Troubleshooting](#troubleshooting)

---

## 1. สร้าง MongoDB Atlas Account

### ขั้นตอนที่ 1.1: ลงทะเบียน

**1. เข้าไปที่:**
- URL: https://www.mongodb.com/cloud/atlas/register

**2. เลือกวิธีการสมัคร:**
- **Option A (แนะนำ)**: Click **Sign up with Google**
  - เลือก Google account ที่ต้องการ
  - รวดเร็ว ไม่ต้องกรอกอะไร
  
- **Option B**: Sign up with Email
  - กรอก First Name, Last Name
  - กรอก Email
  - สร้าง Password (8+ characters)
  - ติ๊ก checkbox: "I agree to the Terms of Service..."
  - Click **Create your Atlas Account**

**3. Verify Email (ถ้าใช้ Email signup):**
- เช็ค Email inbox
- Click link ในอีเมล "Verify Your Email Address"

**✅ สำเร็จ:** เข้าสู่หน้า MongoDB Atlas Dashboard

---

### ขั้นตอนที่ 1.2: Welcome Survey (ข้ามได้)

MongoDB จะถามคำถามเหล่านี้:

- **What is your goal today?**  
  เลือก: `Learn MongoDB`

- **What type of application are you building?**  
  เลือก: `AI / ML`

- **What is your preferred programming language?**  
  เลือก: `Python`

- **How do you want to use MongoDB?**  
  เลือก: `In the Cloud`

Click **Finish** หรือ **Skip**

---

### ขั้นตอนที่ 1.3: Create Organization (ถ้าเป็นครั้งแรก)

**1. Organization Setup:**
- **Organization Name**: `AI Director` (ตั้งชื่ออะไรก็ได้)
- **Cloud Service**: เลือก **MongoDB Atlas** (default)
- Click **Next**

**2. Organization Settings:**
- **Allow Multi-Factor Authentication**: ปิดได้ (development)
- Click **Create Organization**

---

### ขั้นตอนที่ 1.4: Create Project

**1. Project Setup:**
- **Project Name**: `ai-director-project` (ตั้งชื่ออะไรก็ได้)
- คำอธิบาย (optional): `AI Director Vector RAG System`
- Click **Next**

**2. Add Members (optional):**
- ข้ามไปก่อน (เพิ่มทีหลังได้)
- Click **Create Project**

**✅ สำเร็จ:** เข้าสู่หน้า Project Dashboard

---

## 2. สร้าง Free Cluster M0

### ขั้นตอนที่ 2.1: เริ่มสร้าง Cluster

**1. เริ่มต้น:**
- Click **+ Create** (มุมขวาบน)
- หรือ Click **Build a Database** (กลางหน้าจอ)

**2. เลือก Deployment Type:**
- เห็น 3 ตัวเลือก:
  - **M0** → **FREE** ← เลือกตัวนี้!
  - M10 → $0.08/hour (ไม่เอา)
  - M30 → $0.54/hour (ไม่เอา)

- Click **Create** button ใต้ **M0 FREE**

---

### ขั้นตอนที่ 2.2: เลือก Cloud Provider & Region

**1. Cloud Provider:**
- เลือก **AWS** (แนะนำสำหรับไทย)
- หรือ **GCP**, **Azure** (ได้เหมือนกัน)

**2. Region:**
- แนะนำ: **Singapore (ap-southeast-1)** ← เร็วที่สุดสำหรับไทย
- ทางเลือกอื่น:
  - Mumbai (ap-south-1)
  - Hong Kong (ap-east-1)
  - Tokyo (ap-northeast-1)

⚠️ **หมายเหตุ:**
- M0 free tier มีใน regions เฉพาะบางแห่ง
- ถ้า region ที่ต้องการไม่มี M0 ให้เลือก region ใกล้ที่สุด

**3. Cluster Tier:**
- ตรวจสอบว่าเห็น: **M0 Sandbox** (Free tier)
- Storage: **512 MB**
- RAM: **Shared**
- vCPU: **Shared**

---

### ขั้นตอนที่ 2.3: Additional Settings

**1. Cluster Name:**
- ชื่อ default: `Cluster0`
- เปลี่ยนเป็น: `ai-director` (หรือชื่ออื่นที่ต้องการ)
- **ชื่อต้องไม่มี special characters** (ยกเว้น `-`, `_`)

**2. Additional Settings (ค่อนข้างซ่อน):**
- Click **Additional Settings** (ถ้ามี)
- **MongoDB Version**: เลือก **7.0** (ล่าสุด)
- **Backup**: ❌ Not available on M0
- **Auto-Expand Storage**: ❌ Not available on M0

---

### ขั้นตอนที่ 2.4: Create Cluster

**1. Review Settings:**
- Cloud Provider: AWS
- Region: Singapore (ap-southeast-1)
- Cluster Tier: M0 Sandbox
- Cluster Name: ai-director
- Monthly Cost: **$0.00** ← ต้องเป็น $0!

**2. Create:**
- Click **Create Deployment** (button สีเขียว)

**3. Wait for Deployment:**
- เห็นหน้าจอ "Deploying your cluster..."
- รอ ~1-2 นาที ⏱️
- จะเห็น progress bar หรือ animation

**✅ สำเร็จ:** เมื่อ cluster พร้อม จะเห็นหน้าต่าง **Security Quickstart**

---

## 3. สร้าง Database User

### ขั้นตอนที่ 3.1: Create User (หลัง Cluster สร้างเสร็จ)

**หลัง cluster deploy เสร็จ จะเห็นหน้าต่าง popup: "Security Quickstart"**

**1. Authentication Method:**
- เลือก **Username and Password** (default)

**2. Username:**
- กรอก: `ai-director_db`
- **ห้ามมี special characters** นอกจาก `_`, `-`
- ตัวอย่างที่ใช้ได้: `aidirector`, `ai_director`, `ai-director-db`

**3. Password:**
- **Option A (แนะนำ)**: Click **Autogenerate Secure Password**
  - ระบบจะสร้าง password ยาว 20+ characters
  - **คัดลอกและบันทึกทันที!** (จะไม่แสดงอีก)
  - ตัวอย่าง: `b6ePMwfs1f3jqYNT`
  
- **Option B**: ตั้งเอง
  - ความยาว 8+ characters
  - ควรมี uppercase, lowercase, numbers
  - ⚠️ **หลีกเลี่ยง special characters** (@, :, /, ?, #) หรือต้อง URL encode

**4. Database User Privileges:**
- ตรวจสอบว่าเลือก: **Read and write to any database** (default)
- Role: `atlasAdmin` หรือ `readWriteAnyDatabase`

**5. บันทึก Credentials:**
```
Username: ai-director_db
Password: b6ePMwfs1f3jqYNT
```

📝 **บันทึกลง text file ที่ปลอดภัย หรือ password manager**

**6. Create:**
- Click **Create Database User** (button สีเขียว)

**✅ สำเร็จ:** เห็นข้อความ "User created successfully"

---

### ขั้นตอนที่ 3.2: Create User (ถ้าพลาดหน้า Security Quickstart)

**1. Navigate to Database Access:**
- ไปที่เมนูซ้าย: **Security → Database Access**

**2. Add New User:**
- Click **+ ADD NEW DATABASE USER** (มุมขวาบน)

**3. Authentication Method:**
- เลือก **Password**

**4. กรอกข้อมูล:**
- Username: `ai-director_db`
- Password: **Autogenerate** หรือตั้งเอง
- บันทึก password!

**5. Database User Privileges:**
- เลือก **Built-in Role**
- Role: **Read and write to any database**

**6. Restrict Access (optional):**
- ปิดไว้ (Grant access to all clusters and any database)

**7. Temporary User (optional):**
- ปิดไว้ (Permanent user)

**8. Add User:**
- Click **Add User**

---

## 4. Whitelist IP Address

### ขั้นตอนที่ 4.1: Add IP (หน้า Security Quickstart)

**หลังสร้าง user เสร็จ จะเห็นหน้า "Where would you like to connect from?"**

**1. เลือกตัวเลือก:**
- เลือก **My Local Environment** (default)

**2. Add IP Address:**
- เห็น Current IP: `xxx.xxx.xxx.xxx`
- **Option A (Development - แนะนำ)**:
  - Click **Add My Current IP Address**
  - IP จะถูกเพิ่มอัตโนมัติ
  
- **Option B (Development - All IPs)**:
  - ไปที่ตรง IP Address List
  - Click **Add a Different IP Address**
  - IP Address: `0.0.0.0/0`
  - Description: `Allow all IPs (Development)`
  - Click **Add Entry**

⚠️ **0.0.0.0/0 = Allow all IPs** - ใช้สำหรับ development เท่านั้น!

**3. Finish:**
- Click **Finish and Close**

**✅ สำเร็จ:** Cluster พร้อมใช้งาน!

---

### ขั้นตอนที่ 4.2: Add IP (ถ้าพลาดหน้า Security Quickstart)

**1. Navigate to Network Access:**
- ไปที่เมนูซ้าย: **Security → Network Access**

**2. Add IP Address:**
- Click **+ ADD IP ADDRESS** (มุมขวาบน)

**3. Add IP Entry:**
- **Option A**: Add Current IP Address
  - Click **ADD CURRENT IP ADDRESS**
  - Description: `My IP` (auto-fill)
  
- **Option B**: Allow Access from Anywhere (Development)
  - Click **ALLOW ACCESS FROM ANYWHERE**
  - IP Address: `0.0.0.0/0` (auto-fill)
  - Description: `Development - Allow all IPs`

**4. Confirm:**
- Click **Confirm**

**5. Wait:**
- Status จะเป็น **Pending** ~30 วินาที
- จนกลายเป็น **Active** (สีเขียว)

---

### ⚠️ IP Whitelist Best Practices

**Development:**
- ✅ 0.0.0.0/0 (allow all) - สะดวก แต่ไม่ปลอดภัย
- ✅ Current IP - ปลอดภัยกว่า แต่ IP อาจเปลี่ยน

**Production:**
- ⚠️ เฉพาะ production server IPs
- ⚠️ เฉพาะ office IP ranges
- ⚠️ เฉพาะ VPN gateway IPs

**Example Production IPs:**
```
18.142.123.45/32  # Production server 1
52.220.67.89/32   # Production server 2
203.144.0.0/16    # Office network
```

---

## 5. Get Connection String

### ขั้นตอนที่ 5.1: Copy Connection URI

**1. Navigate to Database:**
- ไปที่เมนูซ้าย: **Database**
- เห็น cluster: `ai-director`

**2. Connect Button:**
- Click **Connect** button (ข้างชื่อ cluster)

**3. Choose Connection Method:**
- เห็น 3 ตัวเลือก:
  - **Drivers** ← เลือกตัวนี้
  - Shell
  - Compass

- Click **Drivers**

**4. Select Driver:**
- Driver: **Python**
- Version: **3.12 or later** (หรือ version ที่ใช้)

**5. Copy Connection String:**
เห็น connection string template:

```
mongodb+srv://<username>:<password>@<cluster-url>/?retryWrites=true&w=majority&appName=<appName>
```

ตัวอย่างที่เห็น:
```
mongodb+srv://ai-director_db:<password>@ai-director.k5cjwah.mongodb.net/?retryWrites=true&w=majority&appName=ai-director
```

- Click **Copy** button
- บันทึกไว้ใน text editor

---

### ขั้นตอนที่ 5.2: แทนค่า Password

**1. แทนที่ `<password>`:**

**Before (ยังไม่แทนค่า):**
```
mongodb+srv://ai-director_db:<password>@ai-director.k5cjwah.mongodb.net/?retryWrites=true&w=majority&appName=ai-director
```

**After (แทนค่าด้วย password จริง):**
```
mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?retryWrites=true&w=majority&appName=ai-director
```

⚠️ **ระวัง**: ใช้ password ที่บันทึกไว้ตอนสร้าง user (Step 3)

---

### ขั้นตอนที่ 5.3: URL Encode Special Characters

**ถ้า password มี special characters ต้อง URL encode:**

| Character | Encoded |
|-----------|---------|
| @ | %40 |
| : | %3A |
| / | %2F |
| ? | %3F |
| # | %23 |
| [ | %5B |
| ] | %5D |
| $ | %24 |
| & | %26 |
| + | %2B |
| , | %2C |
| ; | %3B |
| = | %3D |
| space | %20 |

**ตัวอย่าง:**
```bash
# Original password: P@ssw0rd!#
# Encoded password: P%40ssw0rd!%23

# Connection string:
mongodb+srv://user:P%40ssw0rd!%23@cluster.mongodb.net/?appName=ai-director
```

**Online URL Encoder:**
- https://www.urlencoder.org/
- กรอก password → กด Encode → copy ผลลัพธ์

---

### ขั้นตอนที่ 5.4: Set Environment Variable

**Linux / Mac / Codespaces:**
```bash
export MONGO_URI="mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?retryWrites=true&w=majority&appName=ai-director"

# Verify
echo $MONGO_URI
```

**ถาวร (บันทึกไว้ในไฟล์ profile):**
```bash
# เพิ่มใน ~/.bashrc (Linux) หรือ ~/.zshrc (Mac)
echo 'export MONGO_URI="mongodb+srv://..."' >> ~/.bashrc

# Reload
source ~/.bashrc

# Verify
echo $MONGO_URI
```

**Windows (Command Prompt):**
```cmd
set MONGO_URI=mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?appName=ai-director

echo %MONGO_URI%
```

**Windows (PowerShell):**
```powershell
$env:MONGO_URI="mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?appName=ai-director"

echo $env:MONGO_URI
```

---

### ขั้นตอนที่ 5.5: Use .env File (แนะนำ)

**1. Install python-dotenv:**
```bash
pip install python-dotenv
```

**2. Create .env file:**
```bash
# .env (อยู่ใน root ของ project)
MONGO_URI="mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?appName=ai-director"
```

**3. Add .env to .gitignore:**
```bash
echo ".env" >> .gitignore
```

**4. Load in Python:**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file
MONGO_URI = os.getenv("MONGO_URI")

print(f"MONGO_URI loaded: {MONGO_URI[:30]}...")
```

---

## 6. Create Database and Collection

### ขั้นตอนที่ 6.1: Test Connection

**1. Create test script:**
```bash
cd /workspaces/second-brain-ai-assistant-course/module5
nano test_connection.py
```

**2. Paste code:**
```python
from pymongo import MongoClient
import os

# Get MONGO_URI from environment
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("❌ MONGO_URI not set!")
    print("Run: export MONGO_URI='mongodb+srv://...'")
    exit(1)

print(f"📡 Connecting to MongoDB...")
print(f"URI: {MONGO_URI[:50]}...")

try:
    # Create client
    client = MongoClient(MONGO_URI)
    
    # Test connection
    client.admin.command('ping')
    
    print("✅ Connected to MongoDB Atlas!")
    print(f"✅ Server version: {client.server_info()['version']}")
    
    # List databases
    databases = client.list_database_names()
    print(f"✅ Databases: {databases}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)
```

**3. Run:**
```bash
python test_connection.py
```

**Expected output:**
```
📡 Connecting to MongoDB...
URI: mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@...
✅ Connected to MongoDB Atlas!
✅ Server version: 7.0.8
✅ Databases: ['admin', 'local']
```

---

### ขั้นตอนที่ 6.2: Create Database and Collection

**1. Create script:**
```python
from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

print("📦 Creating database and collection...")

# Create database
db = client["ai_director"]
print(f"✅ Database 'ai_director' created/accessed")

# Create collection
collection = db["brand_vectors"]
print(f"✅ Collection 'brand_vectors' created/accessed")

# Insert test document (MongoDB creates collection on first insert)
test_doc = {
    "name": "test_document",
    "purpose": "Initialize collection",
    "created_at": datetime.now()
}

result = collection.insert_one(test_doc)
print(f"✅ Test document inserted: {result.inserted_id}")

# Delete test document
collection.delete_one({"_id": result.inserted_id})
print(f"✅ Test document deleted")

# Verify collection exists
collections = db.list_collection_names()
print(f"✅ Collections in database: {collections}")

print("\n✅ Database setup complete!")
```

**2. Run:**
```bash
python create_database.py
```

---

### ขั้นตอนที่ 6.3: Verify in Atlas UI

**1. Navigate to Database:**
- ไปที่ **Database** (เมนูซ้าย)
- Click **Browse Collections** (ข้างชื่อ cluster)

**2. Check:**
- Database: `ai_director` ← ควรเห็นตรงนี้
- Collection: `brand_vectors` ← ควรเห็นตรงนี้
- Documents: 0 (ยังว่าง)

**✅ สำเร็จ:** Database and collection พร้อมใช้งาน!

---

## 7. Create Vector Search Index

### ขั้นตอนที่ 7.1: Navigate to Search

**1. Go to Database:**
- ไปที่ **Database** (เมนูซ้าย)
- เห็นชื่อ cluster: `ai-director`

**2. Go to Search Tab:**
- Click **Search** tab (ข้าง Overview, Browse Collections)
- หรือ Click **Atlas Search** (ข้างชื่อ cluster)

**3. Create Search Index:**
- Click **Create Search Index** (button สีเขียว)

---

### ขั้นตอนที่ 7.2: Select Configuration Method

**1. Choose Configuration Method:**
เห็น 2 ตัวเลือก:
- **Visual Editor** - สำหรับมือใหม่
- **JSON Editor** ← เลือกตัวนี้

**2. Click JSON Editor:**
- Click **JSON Editor**
- Click **Next**

---

### ขั้นตอนที่ 7.3: Select Database and Collection

**1. กรอกข้อมูล:**
- **Database**: เลือก `ai_director`
- **Collection**: เลือก `brand_vectors`
- **Index Name**: `vector_index` (ชื่อที่จะใช้ใน code)

**2. ตรวจสอบ:**
```
Database: ai_director
Collection: brand_vectors
Index Name: vector_index
```

---

### ขั้นตอนที่ 7.4: Paste Index Definition

**1. เห็น JSON editor:**
มี template default:
```json
{
  "mappings": {
    "dynamic": true
  }
}
```

**2. ลบและวาง JSON configuration นี้:**
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

---

### คำอธิบาย Configuration:

```json
{
  "mappings": {
    "dynamic": true,  // อนุญาตให้ index fields อื่นๆ อัตโนมัติ
    
    "fields": {
      // Vector field สำหรับ semantic search
      "embedding": {
        "type": "knnVector",      // Vector type
        "dimensions": 384,        // 384 dims (all-MiniLM-L6-v2)
        "similarity": "cosine"    // Cosine similarity
      },
      
      // Filter field 1: brand name
      "brand_name": {
        "type": "token"           // Exact match filter
      },
      
      // Filter field 2: document type (parent/child)
      "doc_type": {
        "type": "token"           // Exact match filter
      }
    }
  }
}
```

**สำคัญ:**
- `dimensions: 384` - ต้องตรงกับ embedding model (all-MiniLM-L6-v2)
- `similarity: cosine` - ใช้ cosine similarity สำหรับการคำนวณ
- Filter fields - สำหรับ filter results (ค้นหาเฉพาะแบรนด์, เฉพาะ parent/child)

---

### ขั้นตอนที่ 7.5: Create Index

**1. Review:**
- ตรวจสอบ JSON configuration
- Database: ai_director
- Collection: brand_vectors
- Index Name: vector_index

**2. Click Next:**
- Click **Next** (button สีเขียว)

**3. Review Settings:**
เห็นหน้า summary:
```
Index Name: vector_index
Database: ai_director
Collection: brand_vectors
Configuration: Custom (JSON Editor)
```

**4. Create Search Index:**
- Click **Create Search Index**

---

### ขั้นตอนที่ 7.6: Wait for Index to Build

**1. Building Status:**
หลัง create จะเห็นหน้าต่าง:
```
Status: Building...
Progress: █████░░░░░ 50%
```

**รอ ~2-3 นาที** ⏱️

**2. Active Status:**
เมื่อเสร็จจะเห็น:
```
Status: Active ✅
Queryable: Yes
Index Size: 0 KB (ยังไม่มีข้อมูล)
```

**✅ สำเร็จ:** Vector Search Index พร้อมใช้งาน!

---

### ขั้นตอนที่ 7.7: Verify Index

**1. Check Index List:**
- ไปที่ **Database → Search**
- เห็น index: `vector_index`
- Status: **Active** (สีเขียว)

**2. Index Details:**
- Click index name: `vector_index`
- เห็น configuration ที่สร้างไว้
- Queryable: **Yes**

---

## 8. Test Connection

### ขั้นตอนที่ 8.1: Test MongoDB Connection

```python
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

try:
    # Ping server
    client.admin.command('ping')
    
    # Get server info
    info = client.server_info()
    
    print("✅ MongoDB Atlas Connection Test:")
    print(f"  - Status: Connected")
    print(f"  - Version: {info['version']}")
    print(f"  - Uptime: {info['uptimeMillis'] / 1000:.0f}s")
    
    # List databases
    databases = client.list_database_names()
    print(f"  - Databases: {len(databases)}")
    
    # Access ai_director database
    db = client["ai_director"]
    collections = db.list_collection_names()
    print(f"  - Collections in ai_director: {collections}")
    
    # Check brand_vectors collection
    collection = db["brand_vectors"]
    doc_count = collection.count_documents({})
    print(f"  - Documents in brand_vectors: {doc_count}")
    
except Exception as e:
    print(f"❌ Connection test failed: {e}")
```

---

### ขั้นตอนที่ 8.2: Test Vector Index

```python
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["ai_director"]
collection = db["brand_vectors"]

# Insert test document with embedding
test_doc = {
    "text": "Test document for vector search",
    "embedding": [0.1] * 384,  # 384-dim zero vector
    "brand_name": "TestBrand",
    "doc_type": "child"
}

# Insert
result = collection.insert_one(test_doc)
print(f"✅ Test document inserted: {result.inserted_id}")

# Test vector search
pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": [0.1] * 384,
            "numCandidates": 10,
            "limit": 1
        }
    }
]

try:
    results = list(collection.aggregate(pipeline))
    if results:
        print(f"✅ Vector search working! Found: {results[0]['text']}")
    else:
        print("⚠️ No results (index might still be building)")
except Exception as e:
    print(f"❌ Vector search failed: {e}")
    print("   → Check if vector index status is 'Active'")

# Clean up
collection.delete_one({"_id": result.inserted_id})
print("✅ Test document deleted")
```

---

### ขั้นตอนที่ 8.3: Test with Module 5 Code

```bash
cd /workspaces/second-brain-ai-assistant-course/module5

# Test MongoDB connection
python -c "
from module5.mongodb_vector import MongoDBVectorStore
store = MongoDBVectorStore()
print('✅ MongoDBVectorStore initialized')
stats = store.get_collection_stats()
print(f'✅ Collection stats: {stats}')
"
```

---

## Troubleshooting

### 1. "ServerSelectionTimeoutError"

**สาเหตุ:**
- IP ไม่ได้ whitelist
- Network ปัญหา
- Credentials ผิด

**แก้ไข:**
```bash
# 1. Check MONGO_URI
echo $MONGO_URI

# 2. Check IP whitelist
# ไปที่ Atlas → Network Access
# เพิ่ม current IP หรือ 0.0.0.0/0

# 3. Test DNS
nslookup ai-director.k5cjwah.mongodb.net

# 4. Test connectivity
ping mongodb.com
```

---

### 2. "Authentication failed"

**สาเหตุ:**
- Username/Password ผิด
- User ยังไม่มี privileges

**แก้ไข:**
```bash
# 1. ตรวจสอบ credentials
# ไปที่ Atlas → Database Access
# ตรวจสอบ username

# 2. Reset password
# Click ... → Edit → Reset Password

# 3. อัปเดต MONGO_URI
export MONGO_URI="mongodb+srv://NEW_USER:NEW_PASS@cluster.mongodb.net/?appName=ai-director"
```

---

### 3. "Database/Collection not found"

**แก้ไข:**
```python
# Create database and collection
from pymongo import MongoClient
client = MongoClient(MONGO_URI)
db = client["ai_director"]
collection = db["brand_vectors"]

# Insert dummy document
collection.insert_one({"test": "data"})
collection.delete_one({"test": "data"})
```

---

### 4. "Vector index not found"

**แก้ไข:**
1. ไปที่ Atlas → Database → Search
2. ตรวจสอบว่ามี index ชื่อ `vector_index`
3. Status ต้องเป็น **Active**
4. ถ้าไม่มี ให้สร้างใหม่ (Step 7)

---

### 5. "Index is building"

**รอจนกว่า index จะ Active:**
```python
import time
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client["ai_director"]

while True:
    try:
        # Try vector search
        collection = db["brand_vectors"]
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": [0.1] * 384,
                    "numCandidates": 10,
                    "limit": 1
                }
            }
        ]
        list(collection.aggregate(pipeline))
        print("✅ Vector index is ready!")
        break
    except:
        print("⏳ Index still building... waiting 10s")
        time.sleep(10)
```

---

### 6. "Password contains special characters"

**แก้ไข: URL encode special characters**

```python
from urllib.parse import quote_plus

password = "P@ssw0rd!#"
encoded = quote_plus(password)
print(f"Encoded password: {encoded}")
# Output: P%40ssw0rd%21%23

# Use in MONGO_URI
MONGO_URI = f"mongodb+srv://user:{encoded}@cluster.mongodb.net/?appName=ai-director"
```

---

## ✅ Checklist: MongoDB Setup Complete

- [ ] MongoDB Atlas account สร้างแล้ว
- [ ] Cluster M0 free tier deploy แล้ว (Region: Singapore)
- [ ] Database user สร้างแล้ว (username + password บันทึกไว้)
- [ ] IP whitelist เพิ่มแล้ว (0.0.0.0/0 หรือ current IP)
- [ ] Connection string คัดลอกและแทนค่า password แล้ว
- [ ] MONGO_URI environment variable set แล้ว
- [ ] Database `ai_director` สร้างแล้ว
- [ ] Collection `brand_vectors` สร้างแล้ว
- [ ] Vector Search Index `vector_index` สร้างและ Active แล้ว
- [ ] Test connection สำเร็จ (ping, list databases)
- [ ] Test vector search สำเร็จ

---

## 🚀 Next Steps

**MongoDB setup เสร็จแล้ว! ตอนนี้:**

1. **กลับไปที่ Module 5 QUICKSTART:**
   - [QUICKSTART.md](QUICKSTART.md)

2. **Run Ingestion:**
   ```bash
   python pipelines/json_ingestion.py --clear
   ```

3. **Test Retrieval:**
   ```bash
   python scripts/test_retrieval.py --test basic
   ```

4. **Start FastAPI:**
   ```bash
   cd tools
   python app.py --host 0.0.0.0 --port 8000
   ```

---

**สำเร็จแล้ว! 🎉**  
MongoDB Atlas พร้อมใช้งานสำหรับ Module 5 Vector RAG System
