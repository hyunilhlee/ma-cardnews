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

# 카드뉴스 생성 프롬프트 (다국어 지원)
CARD_GENERATION_PROMPT = """
**CRITICAL INSTRUCTION: ALL card content (title and content fields) MUST be in the SAME LANGUAGE as the original text below.**
- If original text is in English → Write ALL cards in English
- If original text is in Korean → Write ALL cards in Korean
- If original text is in Japanese → Write ALL cards in Japanese
- DO NOT translate or mix languages!

**중요 지시: 모든 카드 내용(title과 content 필드)은 반드시 아래 원문과 동일한 언어로 작성하세요.**
- 원문이 영어면 → 모든 카드를 영어로 작성
- 원문이 한국어면 → 모든 카드를 한국어로 작성
- 언어를 번역하거나 섞지 마세요!

Create {card_count} card news slides based on the following content.

Summary / 요약:
{summary}

Original Text / 원문:
{original_text}

Respond in the following JSON format:
{{
  "cards": [
    {{
      "type": "title",
      "title": "Main Title (in SAME language as original text)",
      "content": "Subtitle (in SAME language as original text)"
    }},
    {{
      "type": "content",
      "title": "Section Title (in SAME language as original text)",
      "content": "Section content (in SAME language as original text)"
    }},
    ...
    {{
      "type": "closing",
      "title": "Closing Title (in SAME language as original text)",
      "content": "Closing message (in SAME language as original text)"
    }}
  ]
}}

Rules:
1. First card must be "title" type
2. Last card must be "closing" type
3. Middle cards should be "content" type
4. Keep content clear and concise
5. Must respond in valid JSON format only
6. **CRITICAL: Every title and content field MUST be in the SAME LANGUAGE as the original text above!**
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

