"""Firebase Firestore 연동 유틸리티"""

import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import logging
import os

logger = logging.getLogger(__name__)

# Firebase 초기화 상태
_app_initialized = False
_db = None


def initialize_firebase():
    """
    Firebase Admin SDK 초기화
    환경 변수에서 설정을 읽어옴
    """
    global _app_initialized, _db
    
    if _app_initialized:
        return _db
    
    try:
        # 서비스 계정 키 파일 경로
        cred_path = os.getenv('FIREBASE_PRIVATE_KEY_PATH', './serviceAccountKey.json')
        
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized with service account")
        else:
            # 서비스 계정 파일이 없으면 기본 초기화 (로컬 개발용)
            logger.warning(f"Service account key not found at {cred_path}, using default credentials")
            firebase_admin.initialize_app()
        
        _db = firestore.client()
        _app_initialized = True
        logger.info("Firestore client initialized")
        return _db
        
    except Exception as e:
        logger.error(f"Firebase initialization failed: {str(e)}")
        # 에러가 발생해도 None을 반환하여 계속 진행
        return None


def get_db():
    """Firestore 클라이언트 가져오기"""
    global _db
    if _db is None:
        _db = initialize_firebase()
    return _db


# 프로젝트 CRUD

def create_project(data: Dict) -> Dict:
    """
    프로젝트 생성
    
    Args:
        data: 프로젝트 데이터
        
    Returns:
        생성된 프로젝트
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    project_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    project_data = {
        'id': project_id,
        'source_type': data.get('source_type'),
        'source_content': data.get('source_content'),
        'summary': None,
        'keywords': None,
        'recommended_card_count': None,
        'created_at': now,
        'updated_at': now,
        'status': 'draft'
    }
    
    db.collection('projects').document(project_id).set(project_data)
    logger.info(f"Project created: {project_id}")
    
    return project_data


def get_project(project_id: str) -> Optional[Dict]:
    """
    프로젝트 조회
    
    Args:
        project_id: 프로젝트 ID
        
    Returns:
        프로젝트 데이터 또는 None
        
    Raises:
        ValueError: Firestore가 초기화되지 않은 경우
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    doc = db.collection('projects').document(project_id).get()
    
    if doc.exists:
        return doc.to_dict()
    return None


def update_project(project_id: str, data: Dict) -> Dict:
    """
    프로젝트 업데이트
    
    Args:
        project_id: 프로젝트 ID
        data: 업데이트할 데이터
        
    Returns:
        업데이트된 프로젝트
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    data['updated_at'] = datetime.utcnow()
    
    db.collection('projects').document(project_id).update(data)
    logger.info(f"Project updated: {project_id}")
    
    return get_project(project_id)


# 섹션 CRUD

def create_sections(project_id: str, sections: List[Dict]) -> List[Dict]:
    """
    카드 섹션 생성
    
    Args:
        project_id: 프로젝트 ID
        sections: 섹션 리스트
        
    Returns:
        생성된 섹션 리스트
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    created_sections = []
    
    for section in sections:
        section_id = str(uuid.uuid4())
        section_data = {
            'id': section_id,
            'project_id': project_id,
            'order': section.get('order'),
            'type': section.get('type'),
            'title': section.get('title'),
            'content': section.get('content'),
            'design_config': section.get('design_config', {}),
            'created_at': datetime.utcnow()
        }
        
        db.collection('projects').document(project_id)\
          .collection('sections').document(section_id).set(section_data)
        
        created_sections.append(section_data)
    
    logger.info(f"Created {len(created_sections)} sections for project {project_id}")
    return created_sections


def get_sections(project_id: str) -> List[Dict]:
    """
    프로젝트의 섹션 목록 조회
    
    Args:
        project_id: 프로젝트 ID
        
    Returns:
        섹션 리스트 (order 순으로 정렬)
    """
    db = get_db()
    if db is None:
        return []
    
    sections_ref = db.collection('projects').document(project_id)\
                     .collection('sections')\
                     .order_by('order')
    
    sections = []
    for doc in sections_ref.stream():
        sections.append(doc.to_dict())
    
    return sections


def update_section(project_id: str, section_id: str, data: Dict) -> Dict:
    """
    섹션 업데이트
    
    Args:
        project_id: 프로젝트 ID
        section_id: 섹션 ID
        data: 업데이트할 데이터
        
    Returns:
        업데이트된 섹션
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    data['updated_at'] = datetime.utcnow()
    
    db.collection('projects').document(project_id)\
      .collection('sections').document(section_id).update(data)
    
    logger.info(f"Section updated: {section_id}")
    
    doc = db.collection('projects').document(project_id)\
            .collection('sections').document(section_id).get()
    
    return doc.to_dict() if doc.exists else None


def delete_section(project_id: str, section_id: str):
    """
    섹션 삭제
    
    Args:
        project_id: 프로젝트 ID
        section_id: 섹션 ID
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    db.collection('projects').document(project_id)\
      .collection('sections').document(section_id).delete()
    
    logger.info(f"Section deleted: {section_id}")


# 대화 이력 저장

def save_conversation(project_id: str, user_message: str, ai_response: str):
    """
    대화 이력 저장
    
    Args:
        project_id: 프로젝트 ID
        user_message: 사용자 메시지
        ai_response: AI 응답
    """
    db = get_db()
    if db is None:
        return
    
    conversation_id = str(uuid.uuid4())
    conversation_data = {
        'id': conversation_id,
        'user_message': user_message,
        'ai_response': ai_response,
        'timestamp': datetime.utcnow()
    }
    
    db.collection('projects').document(project_id)\
      .collection('conversations').document(conversation_id).set(conversation_data)
    
    logger.info(f"Conversation saved for project {project_id}")


def get_conversations(project_id: str, limit: int = 10) -> List[Dict]:
    """
    대화 이력 조회
    
    Args:
        project_id: 프로젝트 ID
        limit: 최대 조회 개수
        
    Returns:
        대화 이력 리스트
    """
    db = get_db()
    if db is None:
        return []
    
    conversations_ref = db.collection('projects').document(project_id)\
                          .collection('conversations')\
                          .order_by('timestamp', direction=firestore.Query.DESCENDING)\
                          .limit(limit)
    
    conversations = []
    for doc in conversations_ref.stream():
        conversations.append(doc.to_dict())
    
    # 시간순으로 정렬 (오래된 것부터)
    conversations.reverse()
    
    return conversations

