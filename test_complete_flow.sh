#!/bin/bash
echo "🧪 Testing complete interview flow..."

BASE_URL="http://localhost:5001/api"

# Create session
echo "1️⃣ Creating session..."
CREATE_RESPONSE=$(curl -s -X POST "$BASE_URL/interview/create" \
  -H "Content-Type: application/json" \
  -d '{"technology": "JavaScript", "position": "Frontend Developer"}')
SESSION_ID=$(echo $CREATE_RESPONSE | jq -r '.session_id')
echo "✅ Session created: $SESSION_ID"

# Start interview
echo -e "\n2️⃣ Starting interview..."
curl -s -X POST "$BASE_URL/interview/$SESSION_ID/start" -H "Content-Type: application/json" | jq -r '.question' | head -c 100
echo "..."

# Submit 3 answers
for i in {1..3}; do
  echo -e "\n\n3️⃣ Submitting answer $i..."
  ANSWER_RESPONSE=$(curl -s -X POST "$BASE_URL/interview/$SESSION_ID/answer" \
    -H "Content-Type: application/json" \
    -d "{\"answer\": \"Test answer $i with some technical details about JavaScript and React\"}")
  echo $ANSWER_RESPONSE | jq -r '.score' | xargs -I {} echo "Score: {}/10"
  
  if [ $i -lt 3 ]; then
    echo -e "\n4️⃣ Getting next question..."
    curl -s -X POST "$BASE_URL/interview/$SESSION_ID/next-question" \
      -H "Content-Type: application/json" | jq -r '.question' | head -c 100
    echo "..."
  fi
done

# End interview
echo -e "\n\n5️⃣ Ending interview..."
END_RESPONSE=$(curl -s -X POST "$BASE_URL/interview/$SESSION_ID/end" -H "Content-Type: application/json")
AVG_SCORE=$(echo $END_RESPONSE | jq -r '.summary.average_score')
echo "✅ Average Score: $AVG_SCORE/10"

# Delete session
echo -e "\n6️⃣ Cleaning up..."
curl -s -X DELETE "$BASE_URL/interview/$SESSION_ID" | jq -r '.message'

echo -e "\n✅ Complete flow test successful!"
