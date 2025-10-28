"""AI 요약 서비스"""

from openai import OpenAI
from typing import Dict, List, Optional
from app.config import settings
from app.utils.prompts import SUMMARIZE_PROMPT, KEYWORD_EXTRACTION_PROMPT
import logging
import re

logger = logging.getLogger(__name__)


class AISummarizer:
    """OpenAI API를 사용한 텍스트 요약 서비스"""
    
    def __init__(self, model: str = None):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model or settings.OPENAI_MODEL
    
    def summarize(
        self, 
        text: str, 
        max_length: int = 200,
        additional_instructions: Optional[str] = None
    ) -> Dict:
        """
        텍스트를 요약하고 키워드 추출
        
        Args:
            text: 요약할 원본 텍스트
            max_length: 요약문 최대 길이
            
        Returns:
            {
                'summary': str,          # 핵심 요약
                'keywords': List[str],   # 주요 키워드
                'card_count': int        # 추천 카드 수
            }
        """
        logger.info(f"Starting summarization for text of length: {len(text)}")
        
        # 텍스트 길이 제한 (토큰 절약)
        truncated_text = self._truncate_text(text, max_chars=3000)
        
        # 1. 핵심 요약 생성
        summary = self._generate_summary(truncated_text, max_length, additional_instructions)
        logger.info(f"Summary generated: {summary[:50]}...")
        
        # 2. 키워드 추출
        keywords = self._extract_keywords(truncated_text)
        logger.info(f"Keywords extracted: {keywords}")
        
        # 3. 카드 수 추천 (텍스트 길이 기반)
        card_count = self._recommend_card_count(text)
        logger.info(f"Recommended card count: {card_count}")
        
        return {
            'summary': summary,
            'keywords': keywords,
            'card_count': card_count
        }
    
    def _generate_summary(
        self, 
        text: str, 
        max_length: int,
        additional_instructions: Optional[str] = None
    ) -> str:
        """
        GPT를 사용하여 요약 생성
        
        Args:
            text: 요약할 텍스트
            max_length: 최대 길이
            
        Returns:
            요약문
        """
        # 언어 감지
        detected_lang = self._detect_language(text)
        logger.info(f"Detected language: {detected_lang}")
        
        # 언어별 시스템 메시지
        system_messages = {
            'en': "You are a professional content summarization expert. You MUST respond in English ONLY. Do not translate to other languages.",
            'ko': "당신은 전문 콘텐츠 요약 전문가입니다. 반드시 한국어로만 응답하세요. 다른 언어로 번역하지 마세요.",
            'ja': "あなたはプロのコンテンツ要約専門家です。必ず日本語のみで応答してください。"
        }
        
        system_message = system_messages.get(detected_lang, system_messages['en'])
        prompt = SUMMARIZE_PROMPT.format(text=text, max_length=max_length)
        
        # 추가 지시사항이 있으면 프롬프트에 추가
        if additional_instructions:
            prompt += f"\n\n추가 요구사항: {additional_instructions}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # 일관성 있는 요약을 위해 낮은 온도
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            raise ValueError(f"요약 생성 실패: {str(e)}")
    
    def _extract_keywords(self, text: str, count: int = 5) -> List[str]:
        """
        GPT를 사용하여 키워드 추출
        
        Args:
            text: 키워드를 추출할 텍스트
            count: 추출할 키워드 수
            
        Returns:
            키워드 리스트
        """
        # 언어 감지
        detected_lang = self._detect_language(text)
        
        # 언어별 시스템 메시지
        system_messages = {
            'en': "You are a keyword extraction expert. Extract keywords in English ONLY.",
            'ko': "당신은 키워드 추출 전문가입니다. 키워드를 한국어로만 추출하세요.",
            'ja': "あなたはキーワード抽出の専門家です。日本語のみでキーワードを抽出してください。"
        }
        
        system_message = system_messages.get(detected_lang, system_messages['en'])
        prompt = KEYWORD_EXTRACTION_PROMPT.format(text=text, count=count)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            keywords_text = response.choices[0].message.content.strip()
            # 쉼표로 구분된 키워드를 리스트로 변환
            keywords = [k.strip() for k in keywords_text.split(',')]
            
            return keywords[:count]
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {str(e)}")
            return []
    
    def _recommend_card_count(self, text: str) -> int:
        """
        텍스트 길이에 따라 카드 수 추천
        
        Args:
            text: 원본 텍스트
            
        Returns:
            추천 카드 수
        """
        length = len(text)
        
        if length < 500:
            return 3  # 제목 + 내용 1개 + 마무리
        elif length < 1500:
            return 5  # 제목 + 내용 3개 + 마무리
        elif length < 3000:
            return 7  # 제목 + 내용 5개 + 마무리
        else:
            return 9  # 제목 + 내용 7개 + 마무리
    
    def _truncate_text(self, text: str, max_chars: int = 3000) -> str:
        """
        토큰 절약을 위해 텍스트 자르기
        
        Args:
            text: 원본 텍스트
            max_chars: 최대 문자 수
            
        Returns:
            잘린 텍스트
        """
        if len(text) <= max_chars:
            return text
        
        return text[:max_chars] + "..."
    
    def _detect_language(self, text: str) -> str:
        """
        텍스트 언어 감지 (간단한 휴리스틱)
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            언어 코드 ('en', 'ko', 'ja', etc.)
        """
        # 한글 문자 비율 확인
        korean_chars = len(re.findall(r'[가-힣]', text))
        # 일본어 문자 비율 확인
        japanese_chars = len(re.findall(r'[ぁ-んァ-ヶー一-龯]', text))
        # 전체 문자 수 (공백 제외)
        total_chars = len(re.sub(r'\s', '', text))
        
        if total_chars == 0:
            return 'en'  # 기본값
        
        korean_ratio = korean_chars / total_chars
        japanese_ratio = japanese_chars / total_chars
        
        if korean_ratio > 0.3:
            return 'ko'
        elif japanese_ratio > 0.3:
            return 'ja'
        else:
            return 'en'

