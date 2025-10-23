#!/bin/bash

echo "🧪 Render API 테스트 시작..."
echo ""

echo "1️⃣ 헬스 체크..."
curl -s https://ma-cardnews-api.onrender.com/health | jq .
echo ""

echo "2️⃣ OpenAI 상태 체크..."
curl -s https://ma-cardnews-api.onrender.com/api/status/openai | jq .
echo ""

echo "3️⃣ 루트 엔드포인트..."
curl -s https://ma-cardnews-api.onrender.com/ | jq .
echo ""

echo "✅ 테스트 완료!"

