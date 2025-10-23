"""AI 채팅 서비스"""

from typing import List, Dict, Optional
from openai import OpenAI
from app.config import settings
from app.utils.prompts import CHAT_SYSTEM_PROMPT
import json
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """AI와 대화하며 카드뉴스 섹션을 수정하는 서비스"""
    
    def __init__(self, model: str = None):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model or settings.OPENAI_MODEL
    
    def process_chat_message(
        self,
        user_message: str,
        current_sections: List[Dict],
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """
        사용자의 채팅 메시지를 처리하고 섹션 수정 제안
        
        Args:
            user_message: 사용자 메시지 ("두 번째 카드 더 간결하게 해줘")
            current_sections: 현재 카드 섹션 상태
            conversation_history: 이전 대화 이력
            
        Returns:
            {
                'ai_response': str,              # AI의 응답 메시지
                'updated_sections': List[Dict],  # 수정된 섹션 (있을 경우)
                'action_taken': str              # 수행한 작업 ('modify', 'reorder', 'none')
            }
        """
        logger.info(f"Processing chat message: {user_message}")
        
        # 대화 컨텍스트 구성
        messages = [
            {"role": "system", "content": CHAT_SYSTEM_PROMPT}
        ]
        
        # 이전 대화 이력 추가 (최근 5개만)
        if conversation_history:
            messages.extend(conversation_history[-5:])
        
        # 현재 섹션 정보 포함
        sections_context = self._format_sections_for_context(current_sections)
        messages.append({
            "role": "system",
            "content": f"현재 카드 섹션 상태:\n{sections_context}"
        })
        
        # 사용자 메시지 추가
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # GPT 호출 (Function Calling 사용)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                functions=[  # Function calling으로 섹션 수정 명령 구조화
                    {
                        "name": "modify_section",
                        "description": "특정 카드 섹션의 내용을 수정",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "section_index": {
                                    "type": "integer",
                                    "description": "수정할 섹션의 인덱스 (0부터 시작)"
                                },
                                "new_title": {
                                    "type": "string",
                                    "description": "새로운 제목 (변경하지 않으면 생략 가능)"
                                },
                                "new_content": {
                                    "type": "string",
                                    "description": "새로운 내용"
                                }
                            },
                            "required": ["section_index"]
                        }
                    },
                    {
                        "name": "reorder_sections",
                        "description": "카드 섹션의 순서를 변경",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "new_order": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "description": "새로운 순서 배열 (인덱스 리스트)"
                                }
                            },
                            "required": ["new_order"]
                        }
                    },
                    {
                        "name": "modify_all_tone",
                        "description": "모든 카드의 톤(어조)을 변경합니다. 예: 전문적으로, 친근하게, 캐주얼하게, 격식있게, 설득력있게",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "tone": {
                                    "type": "string",
                                    "description": "적용할 톤 (예: '전문적', '친근함', '캐주얼', '격식있음', '설득력있음')"
                                },
                                "instruction": {
                                    "type": "string",
                                    "description": "추가 지시사항 (선택)"
                                }
                            },
                            "required": ["tone"]
                        }
                    },
                    {
                        "name": "modify_all_length",
                        "description": "모든 카드의 길이를 조절합니다. 예: 더 간결하게, 더 상세하게",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "direction": {
                                    "type": "string",
                                    "enum": ["shorter", "longer"],
                                    "description": "'shorter' (더 짧게) 또는 'longer' (더 길게)"
                                },
                                "instruction": {
                                    "type": "string",
                                    "description": "추가 지시사항 (선택)"
                                }
                            },
                            "required": ["direction"]
                        }
                    },
                    {
                        "name": "modify_all_style",
                        "description": "모든 카드의 작성 스타일을 변경합니다. 예: 스토리텔링, 질문형식, 리스트형식, 데이터중심",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "style": {
                                    "type": "string",
                                    "description": "적용할 스타일 (예: '스토리텔링', '질문형식', '리스트형식', '데이터중심', '비유적표현')"
                                },
                                "instruction": {
                                    "type": "string",
                                    "description": "추가 지시사항 (선택)"
                                }
                            },
                            "required": ["style"]
                        }
                    }
                ]
            )
            
            # 응답 처리
            choice = response.choices[0]
            
            if choice.message.function_call:
                # Function call이 있으면 섹션 수정 수행
                return self._handle_function_call(
                    choice.message.function_call,
                    current_sections
                )
            else:
                # 일반 대화 응답
                return {
                    'ai_response': choice.message.content or "알겠습니다.",
                    'updated_sections': None,
                    'action_taken': 'none'
                }
                
        except Exception as e:
            logger.error(f"Chat processing failed: {str(e)}")
            return {
                'ai_response': f"죄송합니다. 요청을 처리하는 중 오류가 발생했습니다: {str(e)}",
                'updated_sections': None,
                'action_taken': 'none'
            }
    
    def _format_sections_for_context(self, sections: List[Dict]) -> str:
        """
        섹션 정보를 GPT가 이해하기 쉬운 형식으로 포맷
        
        Args:
            sections: 섹션 리스트
            
        Returns:
            포맷된 문자열
        """
        formatted = []
        for idx, section in enumerate(sections):
            formatted.append(
                f"카드 {idx + 1} ({section.get('type', 'content')}):\n"
                f"  제목: {section.get('title', 'N/A')}\n"
                f"  내용: {section.get('content', '')[:100]}..."
            )
        return '\n\n'.join(formatted)
    
    def _handle_function_call(self, function_call, current_sections: List[Dict]) -> Dict:
        """
        Function call 처리하여 섹션 수정
        
        Args:
            function_call: OpenAI function call 객체
            current_sections: 현재 섹션 리스트
            
        Returns:
            수정 결과
        """
        function_name = function_call.name
        arguments = json.loads(function_call.arguments)
        
        logger.info(f"Function call: {function_name} with args: {arguments}")
        
        updated_sections = [section.copy() for section in current_sections]
        
        if function_name == "modify_section":
            idx = arguments.get('section_index', 0)
            
            if 0 <= idx < len(updated_sections):
                if 'new_title' in arguments and arguments['new_title']:
                    updated_sections[idx]['title'] = arguments['new_title']
                if 'new_content' in arguments and arguments['new_content']:
                    updated_sections[idx]['content'] = arguments['new_content']
                
                return {
                    'ai_response': f"카드 {idx + 1}의 내용을 수정했습니다.",
                    'updated_sections': updated_sections,
                    'action_taken': 'modify'
                }
            else:
                return {
                    'ai_response': f"카드 {idx + 1}을(를) 찾을 수 없습니다.",
                    'updated_sections': None,
                    'action_taken': 'none'
                }
        
        elif function_name == "reorder_sections":
            new_order = arguments.get('new_order', [])
            
            if len(new_order) == len(current_sections):
                updated_sections = [current_sections[i] for i in new_order]
                # order 필드 업데이트
                for idx, section in enumerate(updated_sections):
                    section['order'] = idx
                
                return {
                    'ai_response': "카드 순서를 변경했습니다.",
                    'updated_sections': updated_sections,
                    'action_taken': 'reorder'
                }
            else:
                return {
                    'ai_response': "순서 변경에 실패했습니다. 올바른 인덱스를 입력해주세요.",
                    'updated_sections': None,
                    'action_taken': 'none'
                }
        
        elif function_name == "modify_all_tone":
            tone = arguments.get('tone', '')
            instruction = arguments.get('instruction', '')
            
            # AI로 전체 카드 톤 변경
            updated_sections = self._modify_all_with_ai(
                current_sections,
                f"모든 카드의 톤을 '{tone}'으로 변경해주세요. {instruction}",
                "tone"
            )
            
            return {
                'ai_response': f"모든 카드를 '{tone}' 톤으로 수정했습니다.",
                'updated_sections': updated_sections,
                'action_taken': 'modify_all_tone'
            }
        
        elif function_name == "modify_all_length":
            direction = arguments.get('direction', 'shorter')
            instruction = arguments.get('instruction', '')
            
            direction_text = "더 간결하고 짧게" if direction == "shorter" else "더 상세하고 길게"
            
            # AI로 전체 카드 길이 조절
            updated_sections = self._modify_all_with_ai(
                current_sections,
                f"모든 카드를 {direction_text} 수정해주세요. {instruction}",
                "length"
            )
            
            return {
                'ai_response': f"모든 카드를 {direction_text} 수정했습니다.",
                'updated_sections': updated_sections,
                'action_taken': 'modify_all_length'
            }
        
        elif function_name == "modify_all_style":
            style = arguments.get('style', '')
            instruction = arguments.get('instruction', '')
            
            # AI로 전체 카드 스타일 변경
            updated_sections = self._modify_all_with_ai(
                current_sections,
                f"모든 카드를 '{style}' 스타일로 재작성해주세요. {instruction}",
                "style"
            )
            
            return {
                'ai_response': f"모든 카드를 '{style}' 스타일로 수정했습니다.",
                'updated_sections': updated_sections,
                'action_taken': 'modify_all_style'
            }
        
        return {
            'ai_response': "요청을 처리할 수 없습니다.",
            'updated_sections': None,
            'action_taken': 'none'
        }
    
    def _modify_all_with_ai(
        self, 
        current_sections: List[Dict], 
        instruction: str,
        modification_type: str
    ) -> List[Dict]:
        """
        AI를 사용하여 모든 섹션을 일괄 수정
        
        Args:
            current_sections: 현재 섹션 리스트
            instruction: 수정 지시사항
            modification_type: 수정 유형 (tone, length, style)
            
        Returns:
            수정된 섹션 리스트
        """
        try:
            # 현재 섹션을 JSON 형태로 포맷
            sections_json = json.dumps([{
                'type': s.get('type', 'content'),
                'title': s.get('title', ''),
                'content': s.get('content', '')
            } for s in current_sections], ensure_ascii=False, indent=2)
            
            prompt = f"""
다음 카드뉴스 섹션들을 수정해주세요.

{instruction}

현재 섹션:
{sections_json}

중요:
1. 카드의 개수는 유지해주세요 ({len(current_sections)}개)
2. 각 카드의 type은 유지해주세요
3. 수정된 결과를 다음 JSON 형식으로만 응답해주세요:

{{
  "sections": [
    {{"type": "...", "title": "...", "content": "..."}},
    ...
  ]
}}
"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 카드뉴스 내용을 수정하는 전문가입니다. 항상 유효한 JSON 형식으로 응답해주세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            # JSON 추출 (마크다운 코드 블록 제거)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            result = json.loads(response_text.strip())
            modified_sections = result.get('sections', [])
            
            # 기존 섹션의 메타데이터 유지하면서 내용만 업데이트
            updated_sections = []
            for idx, (original, modified) in enumerate(zip(current_sections, modified_sections)):
                updated_section = original.copy()
                updated_section['title'] = modified.get('title', original.get('title', ''))
                updated_section['content'] = modified.get('content', original.get('content', ''))
                updated_section['order'] = idx
                updated_sections.append(updated_section)
            
            return updated_sections
            
        except Exception as e:
            logger.error(f"Failed to modify all sections: {str(e)}")
            # 실패 시 원본 반환
            return current_sections

