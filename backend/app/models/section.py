"""카드 섹션 관련 Pydantic 모델"""

from pydantic import BaseModel
from typing import Optional, Literal, Dict


class CardSection(BaseModel):
    """카드 섹션 모델"""
    id: Optional[str] = None
    project_id: str
    order: int
    type: Literal['title', 'content', 'closing']
    title: Optional[str] = None
    content: str
    image_url: Optional[str] = None
    design_config: Dict = {
        'background_color': '#FFFFFF',
        'font_family': 'Pretendard',
        'font_size': 16
    }


class SectionCreate(BaseModel):
    """섹션 생성 요청"""
    order: int
    type: Literal['title', 'content', 'closing']
    title: Optional[str] = None
    content: str


class SectionUpdate(BaseModel):
    """섹션 수정 요청"""
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None


class SectionResponse(BaseModel):
    """섹션 응답"""
    id: str
    project_id: str
    order: int
    type: Literal['title', 'content', 'closing']
    title: Optional[str] = None
    content: str
    design_config: Dict

