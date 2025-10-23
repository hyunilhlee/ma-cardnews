"""
인메모리 저장소 (Firebase 없이도 작동하도록)

주의: 서버 재시작 시 모든 데이터가 사라집니다.
개발 및 테스트용으로만 사용하세요.
"""

from typing import Dict, List

# 전역 저장소 (싱글톤)
_memory_projects: Dict[str, dict] = {}
_memory_sections: Dict[str, List[dict]] = {}


def get_projects_store() -> Dict[str, dict]:
    """프로젝트 저장소 반환"""
    return _memory_projects


def get_sections_store() -> Dict[str, List[dict]]:
    """섹션 저장소 반환"""
    return _memory_sections


def clear_all():
    """모든 데이터 삭제 (테스트용)"""
    _memory_projects.clear()
    _memory_sections.clear()

