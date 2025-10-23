"""채팅 관련 Pydantic 모델"""

from pydantic import BaseModel
from typing import List, Dict, Optional, Literal


class ChatMessage(BaseModel):
    """채팅 메시지"""
    role: Literal['user', 'assistant', 'system']
    content: str


class ChatRequest(BaseModel):
    """채팅 요청"""
    project_id: str
    user_message: str
    current_sections: List[Dict]
    conversation_history: Optional[List[Dict]] = None


class ChatResponse(BaseModel):
    """채팅 응답"""
    ai_response: str
    updated_sections: Optional[List[Dict]] = None
    action_taken: Literal['modify', 'reorder', 'none']

