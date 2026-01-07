#!/bin/bash
# Setup script for Module 7: Integration

set -e

echo "=================================================="
echo "Module 7: Integration - Setup Script"
echo "=================================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p output
mkdir -p temp
mkdir -p logs
mkdir -p configs
echo "   ✅ Directories created"

# Check environment variables
echo ""
echo "🔑 Checking environment variables..."

if [ -z "$MONGODB_URI" ]; then
    echo "   ⚠️  MONGODB_URI not set"
    echo "      Set with: export MONGODB_URI='mongodb+srv://...'"
else
    echo "   ✅ MONGODB_URI set"
fi

if [ -z "$HF_TOKEN" ]; then
    echo "   ⚠️  HF_TOKEN not set"
    echo "      Set with: export HF_TOKEN='hf_...'"
else
    echo "   ✅ HF_TOKEN set"
fi

# Copy example config
echo ""
echo "📝 Setting up configuration..."
if [ ! -f "configs/.env" ]; then
    cp configs/.env.example configs/.env
    echo "   ✅ Created configs/.env from example"
    echo "   ⚠️  Please edit configs/.env with your credentials"
else
    echo "   ℹ️  configs/.env already exists"
fi

# Run tests
echo ""
echo "🧪 Running tests..."
python -m pytest tests/ -v --tb=short || echo "   ⚠️  Some tests failed (expected if modules not configured)"

echo ""
echo "=================================================="
echo "✅ Setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit configs/.env with your credentials"
echo "2. Run example: python examples/example_full_pipeline.py"
echo "3. Start API: python -m api.main"
echo ""
