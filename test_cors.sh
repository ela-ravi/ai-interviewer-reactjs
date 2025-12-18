#!/bin/bash

# CORS Testing Script for Production Backend
# Usage: ./test_cors.sh

BACKEND_URL="https://ai-interviewer-reactjs.onrender.com"
FRONTEND_URL="https://ai-interviewer-reactjs.vercel.app"

echo "🔍 Testing Backend CORS Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Health Check
echo "1️⃣  Testing Health Endpoint..."
HEALTH=$(curl -k -s "$BACKEND_URL/health")
if [[ $HEALTH == *"healthy"* ]]; then
    echo "   ✅ Backend is healthy"
    echo "   Response: $HEALTH"
else
    echo "   ❌ Backend is not responding"
    echo "   Response: $HEALTH"
fi
echo ""

# Test 2: OPTIONS Preflight (CORS Check)
echo "2️⃣  Testing OPTIONS Preflight (CORS)..."
echo "   Origin: $FRONTEND_URL"
CORS_RESPONSE=$(curl -k -s -I -X OPTIONS \
    -H "Origin: $FRONTEND_URL" \
    -H "Access-Control-Request-Method: POST" \
    -H "Access-Control-Request-Headers: Content-Type" \
    "$BACKEND_URL/api/interview/create")

if [[ $CORS_RESPONSE == *"access-control-allow-origin"* ]]; then
    echo "   ✅ CORS headers present"
    echo "$CORS_RESPONSE" | grep -i "access-control"
else
    echo "   ❌ CORS headers MISSING!"
    echo "   Response headers:"
    echo "$CORS_RESPONSE"
fi
echo ""

# Test 3: POST Request with Origin
echo "3️⃣  Testing POST Request with Origin Header..."
POST_RESPONSE=$(curl -k -s -v -X POST \
    -H "Origin: $FRONTEND_URL" \
    -H "Content-Type: application/json" \
    -d '{"technology":"Python","position":"Developer"}' \
    "$BACKEND_URL/api/interview/create" 2>&1)

if [[ $POST_RESPONSE == *"access-control-allow-origin"* ]]; then
    echo "   ✅ CORS headers in POST response"
    echo "$POST_RESPONSE" | grep -i "access-control-allow-origin"
else
    echo "   ❌ CORS headers MISSING in POST response!"
fi

# Extract JSON response
JSON_RESPONSE=$(echo "$POST_RESPONSE" | grep -o '{.*}')
if [[ $JSON_RESPONSE == *"session_id"* ]]; then
    echo "   ✅ API endpoint working"
    echo "   Response: $JSON_RESPONSE"
else
    echo "   ⚠️  API response unexpected"
fi
echo ""

# Test 4: Wildcard CORS (if enabled)
echo "4️⃣  Testing Wildcard CORS (development mode)..."
WILDCARD_RESPONSE=$(curl -k -s -I -X OPTIONS \
    -H "Origin: http://localhost:3000" \
    "$BACKEND_URL/api/interview/create")

if [[ $WILDCARD_RESPONSE == *"access-control-allow-origin: *"* ]]; then
    echo "   ⚠️  Wildcard CORS enabled (development mode)"
    echo "   This means CORS_ORIGINS is not set or set to '*'"
elif [[ $WILDCARD_RESPONSE == *"access-control-allow-origin"* ]]; then
    echo "   ✅ Specific origin CORS enabled (production mode)"
    echo "$WILDCARD_RESPONSE" | grep -i "access-control-allow-origin"
else
    echo "   ❌ No CORS headers at all"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Summary:"
echo ""
echo "If you see ❌ for CORS headers:"
echo "1. Go to Render Dashboard → Your Backend Service"
echo "2. Click 'Environment' tab"
echo "3. Set: CORS_ORIGINS=$FRONTEND_URL"
echo "4. Click 'Save Changes' and wait for redeploy"
echo ""
echo "Alternatively, to allow all origins (testing only):"
echo "1. Delete CORS_ORIGINS variable or set it to empty"
echo "2. Redeploy backend"

