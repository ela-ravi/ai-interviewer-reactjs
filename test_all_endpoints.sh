#!/bin/bash

echo "🧪 Testing all API endpoints..."
echo ""

BASE_URL="http://localhost:5001/api"

# Test 1: Health check
echo "1️⃣ Testing health check..."
curl -s "$BASE_URL/health" | jq . || echo "Failed"
echo -e "\n"

# Test 2: Create interview session
echo "2️⃣ Testing POST /interview/create..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/interview/create" \
  -H "Content-Type: application/json" \
  -d '{"technology": "Python", "position": "Backend Developer"}')
echo $CREATE_RESPONSE | jq .
SESSION_ID=$(echo $CREATE_RESPONSE | jq -r '.session_id')
echo "Session ID: $SESSION_ID"
echo -e "\n"

if [ "$SESSION_ID" = "null" ] || [ -z "$SESSION_ID" ]; then
  echo "❌ Failed to create session, stopping tests"
  exit 1
fi

# Test 3: Get session info
echo "3️⃣ Testing GET /interview/$SESSION_ID..."
curl -s "$BASE_URL/interview/$SESSION_ID" | jq . || echo "Failed"
echo -e "\n"

# Test 4: Start interview
echo "4️⃣ Testing POST /interview/$SESSION_ID/start..."
curl -s -X POST "$BASE_URL/interview/$SESSION_ID/start" \
  -H "Content-Type: application/json" | jq . || echo "Failed"
echo -e "\n"

# Test 5: Submit answer
echo "5️⃣ Testing POST /interview/$SESSION_ID/answer..."
curl -s -X POST "$BASE_URL/interview/$SESSION_ID/answer" \
  -H "Content-Type: application/json" \
  -d '{"answer": "I have 5 years of experience with Python and Django"}' | jq . || echo "Failed"
echo -e "\n"

# Test 6: Get next question
echo "6️⃣ Testing GET /interview/$SESSION_ID/next..."
curl -s "$BASE_URL/interview/$SESSION_ID/next" | jq . || echo "Failed"
echo -e "\n"

# Test 7: End interview
echo "7️⃣ Testing POST /interview/$SESSION_ID/end..."
curl -s -X POST "$BASE_URL/interview/$SESSION_ID/end" \
  -H "Content-Type: application/json" | jq . || echo "Failed"
echo -e "\n"

# Test 8: Delete session
echo "8️⃣ Testing DELETE /interview/$SESSION_ID..."
curl -s -X DELETE "$BASE_URL/interview/$SESSION_ID" | jq . || echo "Failed"
echo -e "\n"

echo "✅ All endpoint tests completed!"
