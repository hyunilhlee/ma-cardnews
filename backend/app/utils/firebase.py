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
_app = None


def initialize_firebase():
    """
    Firebase Admin SDK 초기화
    환경 변수에서 설정을 읽어옴
    """
    global _app_initialized, _db, _app
    
    if _app_initialized:
        return _db
    
    try:
        # 기존 앱이 있으면 삭제
        try:
            if firebase_admin._apps:
                for app in firebase_admin._apps.values():
                    firebase_admin.delete_app(app)
                logger.info("Deleted existing Firebase app instances")
        except:
            pass
        
        # 서비스 계정 키 파일 경로
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH', './serviceAccountKey.json')
        project_id = os.getenv('FIREBASE_PROJECT_ID', 'ma-cardnews')
        
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            # Firebase 앱 초기화
            _app = firebase_admin.initialize_app(cred)
            logger.info(f"Firebase initialized with service account (project: {project_id})")
        else:
            # 서비스 계정 파일이 없으면 기본 초기화 (로컬 개발용)
            logger.warning(f"Service account key not found at {cred_path}, using default credentials")
            _app = firebase_admin.initialize_app()
        
        # Firestore 클라이언트 초기화
        _db = firestore.client()
        _app_initialized = True
        logger.info("Firestore client initialized successfully")
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


# Phase 2: Sites CRUD

def create_site(data: Dict) -> Dict:
    """
    사이트 생성
    
    Args:
        data: 사이트 데이터
        
    Returns:
        생성된 사이트
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    site_id = str(uuid.uuid4())
    now = datetime.utcnow()
    
    site_data = {
        'id': site_id,
        'name': data.get('name'),
        'url': data.get('url'),
        'rss_url': data.get('rss_url'),
        'crawl_interval': data.get('crawl_interval', 30),
        'status': data.get('status', 'inactive'),
        'last_crawled_at': None,
        'next_crawl_at': None,
        'total_crawls': 0,
        'success_count': 0,
        'error_count': 0,
        'total_posts_found': 0,
        'created_at': now,
        'updated_at': now
    }
    
    db.collection('sites').document(site_id).set(site_data)
    logger.info(f"Site created: {site_id}")
    
    return site_data


def get_site(site_id: str) -> Optional[Dict]:
    """사이트 조회"""
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    doc = db.collection('sites').document(site_id).get()
    return doc.to_dict() if doc.exists else None


def get_all_sites() -> List[Dict]:
    """모든 사이트 조회"""
    db = get_db()
    if db is None:
        return []
    
    sites_ref = db.collection('sites').order_by('created_at', direction=firestore.Query.DESCENDING)
    sites = []
    for doc in sites_ref.stream():
        sites.append(doc.to_dict())
    
    return sites


def update_site(site_id: str, data: Dict) -> Dict:
    """사이트 업데이트"""
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    data['updated_at'] = datetime.utcnow()
    
    db.collection('sites').document(site_id).update(data)
    logger.info(f"Site updated: {site_id}")
    
    return get_site(site_id)


def delete_site(site_id: str):
    """사이트 삭제"""
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    db.collection('sites').document(site_id).delete()
    logger.info(f"Site deleted: {site_id}")


# Phase 2: CrawlLogs CRUD

def create_crawl_log(data: Dict) -> Dict:
    """
    크롤링 로그 생성
    
    Args:
        data: 로그 데이터
        
    Returns:
        생성된 로그
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    log_id = str(uuid.uuid4())
    
    log_data = {
        'id': log_id,
        'site_id': data.get('site_id'),
        'site_name': data.get('site_name'),
        'status': data.get('status', 'running'),
        'posts_found': data.get('posts_found', 0),
        'new_posts': data.get('new_posts', 0),
        'projects_created': data.get('projects_created', 0),
        'error_message': data.get('error_message'),
        'error_details': data.get('error_details'),
        'started_at': data.get('started_at', datetime.utcnow()),
        'completed_at': data.get('completed_at'),
        'duration_seconds': data.get('duration_seconds'),
        'post_titles': data.get('post_titles', [])
    }
    
    db.collection('crawl_logs').document(log_id).set(log_data)
    logger.info(f"Crawl log created: {log_id}")
    
    return log_data


def update_crawl_log(log_id: str, data: Dict) -> Dict:
    """크롤링 로그 업데이트"""
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    db.collection('crawl_logs').document(log_id).update(data)
    logger.info(f"Crawl log updated: {log_id}")
    
    doc = db.collection('crawl_logs').document(log_id).get()
    return doc.to_dict() if doc.exists else None


def get_crawl_logs(site_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
    """
    크롤링 로그 조회
    
    Args:
        site_id: 사이트 ID (None이면 전체)
        limit: 최대 조회 개수
        
    Returns:
        로그 리스트
    """
    db = get_db()
    if db is None:
        return []
    
    try:
        query = db.collection('crawl_logs')
        
        if site_id:
            # 복합 인덱스가 필요하므로, 일단 모든 로그를 가져온 후 Python에서 필터링
            # TODO: Firebase Console에서 복합 인덱스 생성 후 제거
            all_logs = []
            for doc in query.stream():
                log_data = doc.to_dict()
                if log_data.get('site_id') == site_id:
                    all_logs.append(log_data)
            
            # Python에서 정렬
            all_logs.sort(key=lambda x: x.get('started_at', datetime.min), reverse=True)
            return all_logs[:limit]
        else:
            # site_id 필터 없이 order_by만 사용 (단일 필드 인덱스는 자동 생성)
            query = query.order_by('started_at', direction=firestore.Query.DESCENDING).limit(limit)
            
            logs = []
            for doc in query.stream():
                logs.append(doc.to_dict())
            
            return logs
            
    except Exception as e:
        logger.error(f"Failed to get crawl logs: {str(e)}")
        return []


# Phase 2: Projects 확장 (목록 조회)

def get_all_projects(limit: int = 100, status: Optional[str] = None) -> List[Dict]:
    """
    모든 프로젝트 조회
    
    Args:
        limit: 최대 조회 개수
        status: 상태 필터 (None이면 전체)
        
    Returns:
        프로젝트 리스트
    """
    db = get_db()
    if db is None:
        return []
    
    query = db.collection('projects')
    
    if status:
        query = query.where('status', '==', status)
    
    query = query.order_by('created_at', direction=firestore.Query.DESCENDING).limit(limit)
    
    projects = []
    for doc in query.stream():
        projects.append(doc.to_dict())
    
    return projects


def delete_project(project_id: str):
    """
    프로젝트 삭제
    
    Args:
        project_id: 프로젝트 ID
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    # 프로젝트 문서 삭제
    db.collection('projects').document(project_id).delete()
    
    # 서브컬렉션 삭제 (sections, conversations)
    # Note: Firestore는 문서 삭제 시 서브컬렉션을 자동 삭제하지 않음
    # 필요 시 별도 삭제 로직 추가
    
    logger.info(f"Project deleted: {project_id}")


# ==================================================
# RSS Posts (Phase 2.5)
# ==================================================

def create_rss_post(post_data: Dict) -> str:
    """
    RSS 게시물 생성 (DB 영구 저장)
    
    Args:
        post_data: RSS 게시물 데이터
        
    Returns:
        생성된 RSS 게시물 ID
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    import hashlib
    from datetime import datetime, timezone
    
    # URL을 해시하여 ID 생성 (중복 방지)
    post_id = hashlib.md5(post_data['url'].encode()).hexdigest()
    
    # 기존 게시물 확인
    existing_doc = db.collection('rss_posts').document(post_id).get()
    if existing_doc.exists:
        logger.info(f"RSS post already exists: {post_id}")
        return post_id
    
    # 새 게시물 저장
    post_doc = {
        'id': post_id,
        'site_id': post_data['site_id'],
        'site_name': post_data['site_name'],
        'title': post_data['title'],
        'url': post_data['url'],
        'content': post_data.get('content', ''),
        'summary': post_data.get('summary', ''),
        'author': post_data.get('author'),
        'published_at': post_data['published_at'],
        'crawled_at': datetime.now(timezone.utc),
        'has_cardnews': False,
        'project_id': None
    }
    
    db.collection('rss_posts').document(post_id).set(post_doc)
    logger.info(f"RSS post created: {post_id}")
    
    return post_id


def get_rss_post(post_id: str) -> Optional[Dict]:
    """
    RSS 게시물 조회
    
    Args:
        post_id: RSS 게시물 ID
        
    Returns:
        RSS 게시물 데이터
    """
    db = get_db()
    if db is None:
        return None
    
    doc = db.collection('rss_posts').document(post_id).get()
    
    if not doc.exists:
        return None
    
    return doc.to_dict()


def get_all_rss_posts(
    site_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    year_month: Optional[str] = None,
    limit: int = 1000
) -> List[Dict]:
    """
    RSS 게시물 목록 조회
    
    Args:
        site_id: 사이트 ID 필터
        start_date: 시작 날짜
        end_date: 종료 날짜
        year_month: 연월 필터 (YYYY-MM 형식)
        limit: 최대 개수
        
    Returns:
        RSS 게시물 리스트
    """
    db = get_db()
    if db is None:
        return []
    
    query = db.collection('rss_posts')
    
    # 사이트 필터
    if site_id:
        query = query.where('site_id', '==', site_id)
    
    # 연월 필터 (YYYY-MM)
    if year_month:
        from datetime import datetime
        import calendar
        
        # YYYY-MM을 파싱하여 해당 월의 시작일과 끝일 계산
        year, month = map(int, year_month.split('-'))
        start_date = datetime(year, month, 1)
        last_day = calendar.monthrange(year, month)[1]
        end_date = datetime(year, month, last_day, 23, 59, 59)
    
    # 날짜 필터
    if start_date:
        query = query.where('published_at', '>=', start_date)
    if end_date:
        query = query.where('published_at', '<=', end_date)
    
    # 최신순 정렬
    query = query.order_by('published_at', direction='DESCENDING')
    
    # 제한
    query = query.limit(limit)
    
    posts = []
    for doc in query.stream():
        posts.append(doc.to_dict())
    
    return posts


def update_rss_post(post_id: str, data: Dict) -> Dict:
    """
    RSS 게시물 업데이트
    
    Args:
        post_id: RSS 게시물 ID
        data: 업데이트할 데이터
        
    Returns:
        업데이트된 RSS 게시물
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    db.collection('rss_posts').document(post_id).update(data)
    logger.info(f"RSS post updated: {post_id}")
    
    doc = db.collection('rss_posts').document(post_id).get()
    return doc.to_dict() if doc.exists else None


def update_rss_post_project_link(post_id: str, project_id: str):
    """
    RSS 게시물과 프로젝트 연결
    
    Args:
        post_id: RSS 게시물 ID
        project_id: 프로젝트 ID
    """
    db = get_db()
    if db is None:
        raise ValueError("Firestore not initialized")
    
    db.collection('rss_posts').document(post_id).update({
        'has_cardnews': True,
        'project_id': project_id
    })
    
    logger.info(f"RSS post linked to project: {post_id} -> {project_id}")

