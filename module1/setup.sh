#!/bin/bash

# Quick Start Script for Module 1
# AI Director v3.4 - Dual-Model Architecture

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                  🎬 AI DIRECTOR MODULE 1 SETUP                    ║"
echo "║              Dual-Model Architecture Design                        ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the module1 directory"
    echo "   cd module1 && bash setup.sh"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
echo ""
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python version
echo "🐍 Python Environment:"
python --version
echo ""

# Check installed packages
echo "📦 Key Packages:"
pip list | grep -E "(transformers|torch|accelerate)" || echo "⚠️ Some packages may be missing"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Module 1 Setup Complete!"
echo ""
echo "📚 Next Steps:"
echo ""
echo "   1. Test T5Gemma 2 (Thinker):"
echo "      python 01_t5gemma_thinker.py"
echo ""
echo "   2. Test FunctionGemma (Executor):"
echo "      python 02_functiongemma_executor.py"
echo ""
echo "   3. Test Complete AI Director:"
echo "      python 03_ai_director_agent.py"
echo ""
echo "   4. Run All Tests:"
echo "      python 04_test_module1.py"
echo ""
echo "   5. Try Examples:"
echo "      python examples/example_strategy.py"
echo "      python examples/example_tool_calling.py"
echo "      python examples/example_smart_cut.py"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📖 Documentation: See README.md for detailed information"
echo ""
echo "🚀 Happy Learning!"
echo ""
