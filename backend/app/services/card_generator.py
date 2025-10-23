"""카드뉴스 생성 서비스"""

from typing import List, Dict
from openai import OpenAI
from app.config import settings
from app.utils.prompts import CARD_GENERATION_PROMPT
import json
import logging

logger = logging.getLogger(__name__)


class CardNewsGenerator:
    """AI를 사용하여 카드뉴스 섹션 자동 생성"""
    
    def __init__(self, model: str = None):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model or settings.OPENAI_MODEL
    
    def generate_sections(
        self, 
        summary: str, 
        original_text: str, 
        card_count: int
    ) -> List[Dict]:
        """
        요약본과 원문을 바탕으로 카드뉴스 섹션 생성
        
        Args:
            summary: 요약된 텍스트
            original_text: 원본 텍스트
            card_count: 생성할 카드 수
            
        Returns:
            카드 섹션 리스트
        """
        logger.info(f"Generating {card_count} card sections")
        
        # 원문 길이 제한 (토큰 절약)
        truncated_text = original_text[:3000] if len(original_text) > 3000 else original_text
        
        # GPT에게 카드뉴스 구조 생성 요청
        prompt = CARD_GENERATION_PROMPT.format(
            summary=summary,
            original_text=truncated_text,
            card_count=card_count
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "당신은 카드뉴스 제작 전문가입니다. 주어진 내용을 카드뉴스 형식으로 구조화합니다. 반드시 유효한 JSON 형식으로만 응답하세요."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2000
            )
            
            # 응답 파싱 (JSON 형식으로 반환되도록 프롬프트 설계)
            content = response.choices[0].message.content.strip()
            
            # JSON 추출 (코드 블록 제거)
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            card_data = json.loads(content)
            
            # CardSection 모델로 변환
            sections = []
            for idx, card in enumerate(card_data.get('cards', [])):
                sections.append({
                    'order': idx,
                    'type': card.get('type', 'content'),
                    'title': card.get('title', ''),
                    'content': card.get('content', ''),
                    'design_config': {
                        'background_color': '#FFFFFF',
                        'font_family': 'Pretendard',
                        'font_size': 16
                    }
                })
            
            logger.info(f"Successfully generated {len(sections)} sections")
            return sections
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {str(e)}")
            logger.error(f"Response content: {content[:200]}")
            # Fallback: 기본 카드 구조 생성
            return self._generate_fallback_sections(summary, card_count)
            
        except Exception as e:
            logger.error(f"Card generation failed: {str(e)}")
            raise ValueError(f"카드뉴스 생성 실패: {str(e)}")
    
    def _generate_fallback_sections(self, summary: str, card_count: int) -> List[Dict]:
        """
        AI 생성 실패 시 기본 카드 구조 생성
        
        Args:
            summary: 요약문
            card_count: 카드 수
            
        Returns:
            기본 카드 섹션 리스트
        """
        logger.info("Generating fallback sections")
        
        sections = [
            {
                'order': 0,
                'type': 'title',
                'title': '카드뉴스',
                'content': summary[:100],
                'design_config': {
                    'background_color': '#FFFFFF',
                    'font_family': 'Pretendard',
                    'font_size': 16
                }
            }
        ]
        
        # 중간 내용 카드들
        for i in range(1, card_count - 1):
            sections.append({
                'order': i,
                'type': 'content',
                'title': f'내용 {i}',
                'content': summary,
                'design_config': {
                    'background_color': '#FFFFFF',
                    'font_family': 'Pretendard',
                    'font_size': 16
                }
            })
        
        # 마무리 카드
        sections.append({
            'order': card_count - 1,
            'type': 'closing',
            'title': '마무리',
            'content': '읽어주셔서 감사합니다.',
            'design_config': {
                'background_color': '#FFFFFF',
                'font_family': 'Pretendard',
                'font_size': 16
            }
        })
        
        return sections

