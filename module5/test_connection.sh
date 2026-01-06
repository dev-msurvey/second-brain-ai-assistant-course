#!/bin/bash
# Script for testing MongoDB Atlas connection repeatedly

MONGO_URI="mongodb+srv://ai-director_db:b6ePMwfs1f3jqYNT@ai-director.k5cjwah.mongodb.net/?appName=ai-director"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🔄 MongoDB Atlas Connection Tester                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "กำลังทดสอบ connection ทุก 10 วินาที..."
echo "กด Ctrl+C เพื่อหยุด"
echo ""

attempt=1
while true; do
    echo "[$attempt] $(date '+%H:%M:%S') - กำลังทดสอบ..."
    
    python3 << PYEOF
from pymongo import MongoClient
import sys

uri = "$MONGO_URI"
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("✅ เชื่อมต่อสำเร็จ! MongoDB Atlas พร้อมใช้งาน!")
    print("")
    print("📊 Databases ที่มี:")
    for db in client.list_database_names():
        print(f"   - {db}")
    client.close()
    sys.exit(0)  # Success - exit script
except Exception as e:
    error_msg = str(e)
    if "SSL" in error_msg or "TLSV1" in error_msg:
        print("❌ SSL Error - Cluster อาจยังไม่พร้อม หรือ IP ยังไม่ได้ whitelist")
    elif "timeout" in error_msg.lower():
        print("❌ Timeout - เช็ค Network Access (IP whitelist)")
    else:
        print(f"❌ Error: {error_msg[:100]}...")
    sys.exit(1)  # Failure - continue loop
PYEOF

    if [ $? -eq 0 ]; then
        echo ""
        echo "═══════════════════════════════════════════════════════════════"
        echo "🎉 พร้อมใช้งานแล้ว! ต่อไปให้รัน:"
        echo ""
        echo "    cd /workspaces/second-brain-ai-assistant-course/module5"
        echo "    python pipelines/json_ingestion.py --clear"
        echo ""
        echo "═══════════════════════════════════════════════════════════════"
        break
    fi
    
    echo "   รอ 10 วินาที แล้วลองใหม่..."
    echo ""
    sleep 10
    ((attempt++))
done
