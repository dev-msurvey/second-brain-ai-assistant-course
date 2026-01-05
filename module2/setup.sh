#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║            📦 MODULE 2 - ETL PIPELINE SETUP                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python --version

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Dependencies installed:"
pip show pymongo python-dotenv pydantic loguru | grep "Name\|Version"

# Create necessary directories
echo ""
echo "📁 Creating directories..."
mkdir -p data/raw data/processed tests

# Create sample data files
echo ""
echo "📝 Creating sample data..."

# Create sample brands.json
cat > data/raw/brands.json << 'EOF'
[
  {
    "name": "CoffeeLab",
    "description": "Premium coffee brand for young professionals. We source beans from sustainable farms and craft every cup with precision.",
    "tone": "friendly, premium, modern",
    "colors": ["#8B4513", "#F5F5DC", "#2C1810"],
    "fonts": ["Montserrat", "Open Sans"],
    "target_audience": "young professionals 25-35, urban, health-conscious",
    "brand_values": ["quality", "sustainability", "innovation", "community"],
    "social_media": {
      "instagram": "@coffeelab_th",
      "facebook": "CoffeeLabThailand",
      "tiktok": "@coffeelab"
    }
  },
  {
    "name": "FitFlow",
    "description": "Modern fitness center combining technology with personal training. Smart workouts for busy people.",
    "tone": "energetic, motivational, tech-savvy",
    "colors": ["#FF6B35", "#004E89", "#F7FFF7"],
    "fonts": ["Roboto", "Poppins"],
    "target_audience": "fitness enthusiasts 20-40, tech-savvy, goal-oriented",
    "brand_values": ["health", "technology", "results", "community"],
    "social_media": {
      "instagram": "@fitflow_gym",
      "facebook": "FitFlowGym",
      "tiktok": "@fitflow_workouts"
    }
  },
  {
    "name": "GreenLeaf",
    "description": "Organic food delivery service. Farm-fresh vegetables and sustainable packaging delivered to your door.",
    "tone": "natural, caring, transparent",
    "colors": ["#2D6A4F", "#95D5B2", "#D8F3DC"],
    "fonts": ["Lato", "Merriweather"],
    "target_audience": "health-conscious families 30-50, eco-friendly, urban",
    "brand_values": ["sustainability", "health", "transparency", "local"],
    "social_media": {
      "instagram": "@greenleaf_organic",
      "facebook": "GreenLeafOrganic",
      "tiktok": "@greenleaf_th"
    }
  }
]
EOF

# Create sample campaigns.json
cat > data/raw/campaigns.json << 'EOF'
[
  {
    "brand_name": "CoffeeLab",
    "campaign_name": "Cold Brew Launch 2025",
    "brief": "Launch new Cold Brew product line targeting young professionals. Create Instagram Reels showing the cold brew process, emphasizing premium quality and convenience. Use minimal aesthetic with warm tones.",
    "objectives": ["brand awareness", "product launch", "social engagement"],
    "target_metrics": {
      "reach": 100000,
      "engagement_rate": 0.05,
      "conversion_rate": 0.02
    },
    "content_requirements": {
      "image_count": 5,
      "video_count": 3,
      "formats": ["reel", "story", "post"]
    },
    "status": "draft"
  },
  {
    "brand_name": "FitFlow",
    "campaign_name": "New Year Transformation",
    "brief": "New Year fitness campaign encouraging people to start their fitness journey. Show real member transformations and introduce 30-day challenge program. Energetic and motivational tone.",
    "objectives": ["membership sales", "challenge signups", "community building"],
    "target_metrics": {
      "reach": 150000,
      "engagement_rate": 0.08,
      "conversion_rate": 0.03
    },
    "content_requirements": {
      "image_count": 8,
      "video_count": 5,
      "formats": ["reel", "story", "post", "carousel"]
    },
    "status": "draft"
  },
  {
    "brand_name": "GreenLeaf",
    "campaign_name": "Farm to Table Series",
    "brief": "Educational content series showing journey from farm to customer's table. Introduce farmers, show organic farming practices, and demonstrate meal prep. Authentic and transparent approach.",
    "objectives": ["education", "trust building", "subscription growth"],
    "target_metrics": {
      "reach": 80000,
      "engagement_rate": 0.06,
      "conversion_rate": 0.025
    },
    "content_requirements": {
      "image_count": 6,
      "video_count": 4,
      "formats": ["reel", "story", "post", "igtv"]
    },
    "status": "active"
  }
]
EOF

echo "✅ Sample data created:"
echo "   - data/raw/brands.json (3 brands)"
echo "   - data/raw/campaigns.json (3 campaigns)"

# Check for .env file
echo ""
if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << 'EOF'
# MongoDB Atlas Connection String
# Replace <password> with your actual password
# MONGO_URI="mongodb+srv://ai_director_user:<password>@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority"
MONGO_URI=""

# Database name
MONGO_DB_NAME="ai_director"
EOF
    echo "📝 Created .env template. Please add your MongoDB connection string."
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                   ✅ SETUP COMPLETE!                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next steps:"
echo "   1. Setup MongoDB Atlas: https://www.mongodb.com/cloud/atlas"
echo "   2. Add MONGO_URI to .env file"
echo "   3. Run: python etl_pipeline.py"
echo ""
echo "💡 Quick test: python -c 'import pymongo; print(pymongo.version)'"
echo ""
