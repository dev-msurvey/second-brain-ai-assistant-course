#!/bin/bash
# API Test Script for Module 5

API_URL="${API_URL:-http://localhost:8000}"

echo "========================================"
echo "🧪 MODULE 5 API TEST SUITE"
echo "========================================"
echo "API URL: $API_URL"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test function
test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4
    
    echo -n "Testing $name... "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" "$API_URL$endpoint")
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$API_URL$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data")
    fi
    
    http_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✅ PASS${NC} (HTTP $http_code)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (HTTP $http_code)"
        echo "Response: $body"
        return 1
    fi
}

# Test 1: Health Check
echo "----------------------------------------"
echo "1️⃣  Health Check"
echo "----------------------------------------"
test_endpoint "Health" "GET" "/health"
echo ""

# Test 2: Root endpoint
echo "----------------------------------------"
echo "2️⃣  Root Endpoint"
echo "----------------------------------------"
test_endpoint "Root" "GET" "/"
echo ""

# Test 3: List brands
echo "----------------------------------------"
echo "3️⃣  List Brands"
echo "----------------------------------------"
test_endpoint "Brands" "GET" "/brands"
echo ""

# Test 4: System stats
echo "----------------------------------------"
echo "4️⃣  System Statistics"
echo "----------------------------------------"
test_endpoint "Stats" "GET" "/stats"
echo ""

# Test 5: Vector search
echo "----------------------------------------"
echo "5️⃣  Vector Search"
echo "----------------------------------------"
test_endpoint "Vector Search" "POST" "/search" \
    '{"query":"luxury fashion brand","k":2,"method":"vector"}'
echo ""

# Test 6: BM25 search
echo "----------------------------------------"
echo "6️⃣  BM25 Search"
echo "----------------------------------------"
test_endpoint "BM25 Search" "POST" "/search" \
    '{"query":"CoffeeLab coffee","k":2,"method":"bm25"}'
echo ""

# Test 7: Hybrid search
echo "----------------------------------------"
echo "7️⃣  Hybrid Search"
echo "----------------------------------------"
test_endpoint "Hybrid Search" "POST" "/search" \
    '{"query":"eco-friendly sustainable","k":3,"method":"hybrid"}'
echo ""

# Test 8: Brand filter
echo "----------------------------------------"
echo "8️⃣  Brand-Specific Search"
echo "----------------------------------------"
test_endpoint "Brand Filter" "POST" "/search" \
    '{"query":"product information","k":1,"brand_filter":"FitFlow","method":"hybrid"}'
echo ""

# Test 9: GET search endpoint
echo "----------------------------------------"
echo "9️⃣  GET Search Endpoint"
echo "----------------------------------------"
test_endpoint "GET Search" "GET" "/search/simple?query=fitness&k=2&method=vector"
echo ""

# Summary
echo "========================================"
echo "📊 TEST SUMMARY"
echo "========================================"
echo "All critical endpoints tested ✅"
echo ""
echo "💡 View detailed API docs:"
echo "   http://localhost:8000/docs"
echo ""
echo "========================================"
