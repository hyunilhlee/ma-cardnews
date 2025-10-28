"""AI 프롬프트 템플릿"""

# 요약 프롬프트 (다국어 지원)
SUMMARIZE_PROMPT = """
**CRITICAL INSTRUCTION: You MUST respond in the SAME LANGUAGE as the input text below.**
- If the text below is in English → Respond in English
- If the text below is in Korean → Respond in Korean
- If the text below is in Japanese → Respond in Japanese
- DO NOT translate or change the language!

Summarize the following text into key points within {max_length} characters.
The summary will be used for card news, so please make it clear and concise.

**중요 지시: 반드시 아래 입력 텍스트와 동일한 언어로 응답하세요.**
- 아래 텍스트가 영어면 → 영어로 응답
- 아래 텍스트가 한국어면 → 한국어로 응답
- 언어를 번역하거나 변경하지 마세요!

다음 텍스트를 {max_length}자 이내로 핵심 내용만 요약해주세요.

Text / 텍스트:
{text}

Summary (in the SAME language as above text) / 요약 (위 텍스트와 동일한 언어로):
"""

# 키워드 추출 프롬프트 (다국어 지원)
KEYWORD_EXTRACTION_PROMPT = """
Extract {count} key keywords from the following text.
Separate them with commas.
If the text is in Korean, respond in Korean. If in English, respond in English.

다음 텍스트에서 핵심 키워드 {count}개를 추출해주세요.
쉼표로 구분하여 나열해주세요.
텍스트가 한국어면 한국어로, 영어면 영어로 응답하세요.

Text / 텍스트:
{text}

Keywords / 키워드:
"""

# 카드뉴스 생성 프롬프트 (한글 우선)
CARD_GENERATION_PROMPT = """
**🚨 최우선 지시사항: 모든 카드 내용을 반드시 한글로 작성하세요! 🚨**

**CRITICAL INSTRUCTION: You MUST write ALL card content in KOREAN (한글)!**
- ALL titles → Korean (한글)
- ALL content → Korean (한글)
- Even if the original text is in English, translate and write in Korean!
- 원문이 영어라도 한글로 번역해서 작성하세요!
- DO NOT write in English! 영어로 쓰지 마세요!

**중요: 아래 내용을 바탕으로 {card_count}개의 카드뉴스를 한글로 작성하세요.**

Create {card_count} card news slides in KOREAN based on the following content.

Summary / 요약:
{summary}

Original Text / 원문:
{original_text}

Respond in the following JSON format (모든 내용을 한글로!):
{{
  "cards": [
    {{
      "type": "title",
      "title": "메인 제목 (한글로 작성)",
      "content": "부제목 (한글로 작성)"
    }},
    {{
      "type": "content",
      "title": "섹션 제목 (한글로 작성)",
      "content": "섹션 내용 (한글로 작성)"
    }},
    ...
    {{
      "type": "closing",
      "title": "마무리 제목 (한글로 작성)",
      "content": "마무리 메시지 (한글로 작성)"
    }}
  ]
}}

Rules (규칙):
1. First card must be "title" type (첫 카드는 title 타입)
2. Last card must be "closing" type (마지막 카드는 closing 타입)
3. Middle cards should be "content" type (중간 카드는 content 타입)
4. Keep content clear and concise (명확하고 간결하게)
5. Must respond in valid JSON format only (유효한 JSON 형식으로만 응답)
6. **🚨 CRITICAL: Every title and content field MUST be in KOREAN (한글)! 모든 title과 content는 반드시 한글로 작성!**
"""

# 채팅 시스템 프롬프트
CHAT_SYSTEM_PROMPT = """
당신은 카드뉴스 제작을 돕는 AI 어시스턴트입니다.
사용자의 자연어 요청을 정확히 이해하고, 적절한 함수를 호출하여 카드 섹션을 수정합니다.

가능한 작업:
1. **특정 카드 수정** - "두 번째 카드 제목 바꿔줘" → modify_section
2. **카드 순서 변경** - "첫 번째와 세 번째 순서 바꿔줘" → reorder_sections
3. **전체 내용 수정** - 아래 함수 사용 → modify_all_content
   - "전체를 존댓말로 바꿔줘"
   - "전체를 반말로 바꿔줘"
   - "전체를 더 전문적으로 바꿔줘"
   - "전체를 더 친근하게 바꿔줘"
   - "전체를 간결하게 줄여줘"
   - "전체를 더 상세하게 만들어줘"
   - "전체를 이모지 추가해서 재밌게 만들어줘"
   - "전체를 스토리텔링 방식으로 바꿔줘"
   - "전체를 질문 형식으로 바꿔줘"
   - "전체를 리스트 형식으로 바꿔줘"
   - 기타 모든 전체 수정 요청

중요 규칙:
- "두 번째 카드" = index 1 (0-based)
- "전체", "모든", "다" 키워드 → modify_all_content 사용
- 사용자의 자연어 요청을 그대로 instruction에 전달
- 애매한 요청도 최대한 이해하고 처리
"""

