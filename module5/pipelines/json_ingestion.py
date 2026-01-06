"""
Simple JSON-based ingestion (ไม่ต้อง MongoDB สำหรับ Module 2)
อ่านจาก brands_v2.json แทนการดึงจาก MongoDB
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path
from bson import ObjectId

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from module5.embedding_models import get_embedder
from module5.mongodb_vector import MongoDBVectorStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextChunker:
    """Split text into chunks for parent-child retrieval"""
    
    def __init__(self, chunk_size: int = 256, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = ["\n\n", "\n", ". ", "! ", "? ", ", "]
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        if not text or len(text) < self.chunk_size:
            return [text] if text else []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            if end < len(text):
                best_break = end
                for separator in self.separators:
                    sep_pos = text.rfind(separator, start, end + 50)
                    if sep_pos > start:
                        best_break = sep_pos + len(separator)
                        break
                end = best_break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - self.chunk_overlap if end < len(text) else end
        
        return chunks


class SimpleJSONIngestion:
    """
    Ingestion pipeline ที่อ่านจาก JSON files (Module 2)
    ไม่ต้อง MongoDB สำหรับการอ่านข้อมูล (แต่ยังใช้ MongoDB Atlas สำหรับ vector store)
    """
    
    def __init__(
        self,
        json_path: str = None,
        embedder_type: str = "sentence-transformers",
        chunk_size: int = 256,
        chunk_overlap: int = 50
    ):
        """
        Args:
            json_path: Path to brands JSON file (default: module2/data/raw/brands_v2.json)
            embedder_type: Embedder type
            chunk_size: Chunk size
            chunk_overlap: Chunk overlap
        """
        # Find JSON file
        if json_path is None:
            # Try to find brands_v2.json in module2
            project_root = Path(__file__).parent.parent.parent
            json_path = project_root / "module2" / "data" / "raw" / "brands_v2.json"
            
            if not json_path.exists():
                # Fallback to brands.json
                json_path = project_root / "module2" / "data" / "raw" / "brands.json"
        
        self.json_path = Path(json_path)
        
        if not self.json_path.exists():
            raise FileNotFoundError(f"❌ ไม่พบไฟล์ {self.json_path}")
        
        self.embedder = get_embedder(embedder_type)
        self.chunker = TextChunker(chunk_size, chunk_overlap)
        self.vector_store = MongoDBVectorStore()
        
        logger.info(f"🚀 Initialized Simple JSON Ingestion")
        logger.info(f"   JSON file: {self.json_path}")
        logger.info(f"   Embedder: {self.embedder}")
        logger.info(f"   Chunk: {chunk_size} tokens, {chunk_overlap} overlap")
    
    def load_brands_from_json(self) -> List[Dict[str, Any]]:
        """
        โหลดข้อมูล brands จาก JSON file
        
        Returns:
            List of brand documents
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                brands = json.load(f)
            
            # Handle both array and object with "brands" key
            if isinstance(brands, dict) and "brands" in brands:
                brands = brands["brands"]
            
            logger.info(f"📥 โหลด {len(brands)} brands จาก {self.json_path.name}")
            
            # Show brand names
            brand_names = [b.get("name", "unknown") for b in brands[:5]]
            logger.info(f"   ตัวอย่าง: {', '.join(brand_names)}...")
            
            return brands
            
        except Exception as e:
            logger.error(f"❌ ไม่สามารถอ่านไฟล์ JSON: {e}")
            return []
    
    def create_parent_document(self, brand: Dict[str, Any]) -> Dict[str, Any]:
        """สร้าง parent document จาก brand data"""
        parent_text_parts = []
        
        # Basic info
        if brand.get("name"):
            parent_text_parts.append(f"Brand Name: {brand['name']}")
        if brand.get("tagline"):
            parent_text_parts.append(f"Tagline: {brand['tagline']}")
        if brand.get("description"):
            parent_text_parts.append(f"Description: {brand['description']}")
        if brand.get("industry"):
            parent_text_parts.append(f"Industry: {brand['industry']}")
        
        # Tone and language
        if brand.get("tone"):
            parent_text_parts.append(f"Tone: {brand['tone']}")
        if brand.get("language"):
            parent_text_parts.append(f"Language: {brand['language']}")
        
        # Target audience
        if brand.get("target_audience"):
            audience = brand["target_audience"]
            if isinstance(audience, dict):
                if audience.get("age_range"):
                    parent_text_parts.append(f"Age Range: {audience['age_range']}")
                if audience.get("demographics"):
                    parent_text_parts.append(f"Demographics: {audience['demographics']}")
                if audience.get("interests"):
                    interests = ", ".join(audience["interests"]) if isinstance(audience["interests"], list) else audience["interests"]
                    parent_text_parts.append(f"Interests: {interests}")
            else:
                parent_text_parts.append(f"Target Audience: {audience}")
        
        # Brand values
        if brand.get("brand_values"):
            values = ", ".join(brand["brand_values"]) if isinstance(brand["brand_values"], list) else brand["brand_values"]
            parent_text_parts.append(f"Brand Values: {values}")
        
        # Colors
        if brand.get("colors"):
            colors = brand["colors"]
            if isinstance(colors, dict) and colors.get("hex_list"):
                color_str = ", ".join(colors["hex_list"])
                parent_text_parts.append(f"Colors: {color_str}")
        
        # Content examples
        if brand.get("content_examples"):
            examples = brand["content_examples"]
            if isinstance(examples, dict):
                if examples.get("caption_good"):
                    captions = examples["caption_good"]
                    if isinstance(captions, list):
                        parent_text_parts.append(f"Good Captions: {' | '.join(captions[:2])}")
                if examples.get("image_style"):
                    parent_text_parts.append(f"Image Style: {examples['image_style']}")
        
        parent_text = "\n".join(parent_text_parts)
        
        # Create parent document
        parent_doc = {
            "_id": ObjectId(),
            "brand_name": brand.get("name", "unknown"),
            "doc_type": "parent",
            "text": parent_text,
            "metadata": {
                "industry": brand.get("industry"),
                "language": brand.get("language"),
                "tone": brand.get("tone"),
                "source": "module2_json"
            },
            "original_brand_data": brand
        }
        
        return parent_doc
    
    def create_child_documents(self, parent_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """สร้าง child documents (chunks) พร้อม embeddings"""
        parent_text = parent_doc["text"]
        chunks = self.chunker.chunk_text(parent_text)
        
        logger.info(f"   Created {len(chunks)} chunks for {parent_doc['brand_name']}")
        
        # Generate embeddings
        embeddings = self.embedder.embed_texts(chunks)
        
        # Create child documents
        child_docs = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            child_doc = {
                "_id": ObjectId(),
                "brand_name": parent_doc["brand_name"],
                "doc_type": "child",
                "parent_id": str(parent_doc["_id"]),
                "text": chunk,
                "embedding": embedding,
                "chunk_index": i,
                "metadata": parent_doc["metadata"]
            }
            child_docs.append(child_doc)
        
        return child_docs
    
    def process_brand(self, brand: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Process single brand"""
        parent_doc = self.create_parent_document(brand)
        child_docs = self.create_child_documents(parent_doc)
        return parent_doc, child_docs
    
    def run_ingestion(self, clear_existing: bool = True) -> Dict[str, int]:
        """
        รัน ingestion pipeline
        
        Args:
            clear_existing: ล้างข้อมูลเดิม
            
        Returns:
            Statistics
        """
        logger.info("🚀 เริ่ม ingestion pipeline (JSON mode)...")
        
        # Load brands from JSON
        brands = self.load_brands_from_json()
        if not brands:
            logger.error("❌ ไม่มี brands")
            return {"brands": 0, "parents": 0, "children": 0}
        
        # Process all brands
        all_documents = []
        parent_count = 0
        child_count = 0
        
        for brand in brands:
            try:
                parent_doc, child_docs = self.process_brand(brand)
                all_documents.append(parent_doc)
                all_documents.extend(child_docs)
                parent_count += 1
                child_count += len(child_docs)
                
                logger.info(f"✅ ประมวลผล: {brand.get('name', 'unknown')} → 1 parent + {len(child_docs)} children")
                
            except Exception as e:
                logger.error(f"❌ Error processing {brand.get('name')}: {e}")
                continue
        
        # Insert to MongoDB Vector Store
        if all_documents:
            inserted = self.vector_store.insert_documents(all_documents, clear_existing=clear_existing)
            logger.info(f"\n✅ Ingestion สำเร็จ!")
            logger.info(f"   เอกสารทั้งหมด: {inserted}")
            logger.info(f"   Parent docs: {parent_count}")
            logger.info(f"   Child docs: {child_count}")
            
            # Show stats
            stats = self.vector_store.get_collection_stats()
            logger.info(f"\n📊 สถิติใน MongoDB:")
            for key, value in stats.items():
                logger.info(f"   {key}: {value}")
            
            return {
                "brands": len(brands),
                "parents": parent_count,
                "children": child_count,
                "total_inserted": inserted
            }
        
        return {"brands": 0, "parents": 0, "children": 0}
    
    def close(self):
        """Clean up"""
        self.vector_store.close()


def main():
    """Run JSON ingestion"""
    import argparse
    
    parser = argparse.ArgumentParser(description="JSON Ingestion Pipeline")
    parser.add_argument("--json", help="Path to brands JSON file")
    parser.add_argument("--chunk-size", type=int, default=256, help="Chunk size")
    parser.add_argument("--clear", action="store_true", help="Clear existing data")
    
    args = parser.parse_args()
    
    pipeline = SimpleJSONIngestion(
        json_path=args.json,
        embedder_type="sentence-transformers",
        chunk_size=args.chunk_size
    )
    
    try:
        stats = pipeline.run_ingestion(clear_existing=args.clear)
        
        print("\n" + "="*60)
        print("📊 สรุปผล INGESTION")
        print("="*60)
        print(f"Brands: {stats['brands']}")
        print(f"Parent documents: {stats['parents']}")
        print(f"Child documents: {stats['children']}")
        print(f"Total inserted: {stats['total_inserted']}")
        print("="*60)
        
    finally:
        pipeline.close()


if __name__ == "__main__":
    main()
