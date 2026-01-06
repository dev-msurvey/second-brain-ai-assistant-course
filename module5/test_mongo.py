from pymongo import MongoClient

uri = "mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?appName=ai-director"

try:
    print("🔗 กำลังเชื่อมต่อ MongoDB Atlas...")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ เชื่อมต่อสำเร็จ!")
    print(f"📊 Databases: {client.list_database_names()}")
    client.close()
except Exception as e:
    print(f"❌ Error: {e}")
