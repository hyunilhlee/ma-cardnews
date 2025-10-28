"""프로젝트 관련 API 라우터"""

from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel
from app.models.project import ProjectCreate, ProjectResponse, SummarizeRequest, SummarizeResponse
from app.services.scraper import WebScraper
from app.services.summarizer import AISummarizer
from app.services.card_generator import CardNewsGenerator
from app.utils import firebase
from app.utils.memory_store import get_projects_store, get_sections_store
from typing import List, Dict, Optional
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()

# 서비스 인스턴스
scraper = WebScraper()
# summarizer = AISummarizer()  # 프로젝트별로 모델이 다를 수 있으므로 필요시 생성
# card_generator = CardNewsGenerator()  # 프로젝트별로 모델이 다를 수 있으므로 필요시 생성


class SummarizeContentRequest(BaseModel):
    """요약 요청 모델"""
    source_type: str
    source_url: str
    additional_instructions: Optional[str] = None


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_content(request: SummarizeContentRequest):
    """
    콘텐츠 요약 (프로젝트 생성 전)
    
    - URL 스크래핑 후 요약
    - 추가 지시사항 반영 (길이, 톤 등)
    """
    try:
        logger.info(f"Summarizing content from: {request.source_url}")
        
        # URL 스크래핑
        scraped_data = scraper.scrape_url(request.source_url)
        content = scraped_data.get('content', '')
        
        logger.info(f"Scraped content length: {len(content)} characters")
        
        if not content or len(content) < 100:
            logger.warning(f"Content too short: {len(content)} characters (minimum 100)")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"콘텐츠가 너무 짧습니다 ({len(content)}자). 최소 100자 이상 필요합니다."
            )
        
        # 요약 생성
        summarizer = AISummarizer(model='gpt-4.1-nano')
        summary_result = summarizer.summarize(
            content,
            max_length=None,
            additional_instructions=request.additional_instructions
        )
        
        return SummarizeResponse(
            summary=summary_result['summary'],
            keywords=summary_result['keywords'],
            recommended_card_count=summary_result['card_count']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to summarize content: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"요약 생성 실패: {str(e)}"
        )


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    """
    새 프로젝트 생성
    
    - URL 또는 텍스트 소스 입력
    - 인메모리 저장소 또는 Firestore에 저장
    """
    try:
        # URL인 경우 스크래핑
        if project.source_type == 'url':
            # 여러 URL을 줄바꿈으로 구분하여 처리
            urls = [url.strip() for url in project.source_content.split('\n') if url.strip()]
            logger.info(f"Scraping {len(urls)} URL(s)")
            
            all_content = []
            for idx, url in enumerate(urls, 1):
                try:
                    logger.info(f"Scraping [{idx}/{len(urls)}]: {url}")
                    scraped_data = scraper.scrape_url(url)
                    
                    # 출처와 내용을 명확히 구분
                    source_info = f"━━━ 출처 {idx}: {scraped_data['title']} ━━━\n"
                    source_info += f"URL: {url}\n"
                    source_info += f"━━━━━━━━━━━━━━━━━━━━\n\n"
                    source_info += scraped_data['content']
                    
                    all_content.append(source_info)
                    logger.info(f"Successfully scraped [{idx}/{len(urls)}]: {scraped_data['title']}")
                except Exception as e:
                    logger.warning(f"Failed to scrape [{idx}/{len(urls)}] {url}: {str(e)}")
                    # 실패한 URL은 건너뛰고 계속 진행
                    continue
            
            if not all_content:
                raise ValueError("모든 URL 스크래핑에 실패했습니다")
            
            # 모든 내용을 합침 (명확한 구분선 사용)
            separator = "\n\n" + "=" * 60 + "\n\n"
            content = separator.join(all_content)
            
            # 최종 정보 추가
            header = f"📚 총 {len(all_content)}개의 소스에서 수집된 내용\n"
            header += "=" * 60 + "\n\n"
            content = header + content
        else:
            content = project.source_content
        
        # Firebase가 초기화되어 있으면 Firestore 사용, 아니면 인메모리 사용
        try:
            project_data = firebase.create_project({
                'source_type': project.source_type,
                'source_content': content,
                'model': project.model,
                'card_start_type': project.card_start_type
            })
            logger.info("Project saved to Firestore")
        except ValueError:
            # Firebase가 없으면 인메모리 저장소 사용
            project_id = str(uuid.uuid4())
            now = datetime.utcnow().isoformat()
            project_data = {
                'id': project_id,
                'source_type': project.source_type,
                'source_content': content,
                'model': project.model,
                'card_start_type': project.card_start_type,
                'created_at': now,
                'updated_at': now,
                'status': 'draft'
            }
            memory_projects = get_projects_store()
            memory_projects[project_id] = project_data
            logger.info(f"Project saved to memory: {project_id} (model: {project.model})")
        
        return ProjectResponse(**project_data)
        
    except ValueError as e:
        logger.error(f"Project creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="프로젝트 생성 중 오류가 발생했습니다."
        )


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    프로젝트 조회
    """
    # Firebase 먼저 시도, 실패하면 인메모리에서 찾기
    try:
        project = firebase.get_project(project_id)
        logger.info(f"Project loaded from Firebase: {project_id}")
    except Exception as e:
        logger.info(f"Firebase failed ({str(e)}), trying memory...")
        memory_projects = get_projects_store()
        logger.info(f"Memory store size: {len(memory_projects)}, keys: {list(memory_projects.keys())}")
        project = memory_projects.get(project_id)
        if project:
            logger.info(f"Project loaded from memory: {project_id}")
        else:
            logger.warning(f"Project not found in memory: {project_id}")
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="프로젝트를 찾을 수 없습니다."
        )
    
    return ProjectResponse(**project)


@router.post("/{project_id}/summarize", response_model=SummarizeResponse)
async def summarize_project(project_id: str, request: SummarizeRequest = SummarizeRequest()):
    """
    프로젝트 소스 요약
    
    - AI를 사용하여 요약문 생성
    - 키워드 추출
    - 추천 카드 수 계산
    """
    try:
        # 프로젝트 조회 (Firebase 또는 인메모리)
        try:
            project = firebase.get_project(project_id)
        except:
            memory_projects = get_projects_store()
            project = memory_projects.get(project_id)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="프로젝트를 찾을 수 없습니다."
            )
        
        # 요약 생성 (프로젝트에 저장된 모델 사용)
        logger.info(f"Summarizing project: {project_id}")
        project_model = project.get('model', 'gpt-4o-mini')
        project_summarizer = AISummarizer(model=project_model)
        summary_result = project_summarizer.summarize(
            project['source_content'],
            max_length=request.max_length
        )
        
        # 프로젝트 업데이트
        update_data = {
            'summary': summary_result['summary'],
            'keywords': summary_result['keywords'],
            'recommended_card_count': summary_result['card_count'],
            'status': 'summarized',
            'updated_at': datetime.utcnow().isoformat()
        }
        
        try:
            firebase.update_project(project_id, update_data)
        except:
            # 인메모리 업데이트
            memory_projects = get_projects_store()
            if project_id in memory_projects:
                memory_projects[project_id].update(update_data)
        
        return SummarizeResponse(
            summary=summary_result['summary'],
            keywords=summary_result['keywords'],
            recommended_card_count=summary_result['card_count']
        )
        
    except ValueError as e:
        logger.error(f"Summarization failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="요약 생성 중 오류가 발생했습니다."
        )


@router.post("/{project_id}/sections")
async def generate_sections(project_id: str):
    """
    카드뉴스 섹션 자동 생성
    
    - 요약본을 바탕으로 카드뉴스 구조 생성
    - 인메모리 또는 Firestore에 저장
    """
    try:
        # 프로젝트 조회 (Firebase 또는 인메모리)
        try:
            project = firebase.get_project(project_id)
        except:
            memory_projects = get_projects_store()
            project = memory_projects.get(project_id)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="프로젝트를 찾을 수 없습니다."
            )
        
        if not project.get('summary'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="먼저 요약을 생성해주세요."
            )
        
        # 카드 섹션 생성 (프로젝트에 저장된 모델 사용)
        logger.info(f"Generating sections for project: {project_id}")
        project_model = project.get('model', 'gpt-4o-mini')
        project_generator = CardNewsGenerator(model=project_model)
        sections = project_generator.generate_sections(
            summary=project['summary'],
            original_text=project['source_content'],
            card_count=project.get('recommended_card_count', 5)
        )
        
        # 저장 (Firebase 또는 인메모리)
        try:
            created_sections = firebase.create_sections(project_id, sections)
            firebase.update_project(project_id, {'status': 'completed'})
        except:
            # 인메모리 저장
            created_sections = []
            for i, section in enumerate(sections):
                section_data = {
                    'id': str(uuid.uuid4()),
                    'project_id': project_id,
                    'order': i,
                    **section
                }
                created_sections.append(section_data)
            memory_sections = get_sections_store()
            memory_sections[project_id] = created_sections
            
            # 프로젝트 상태 업데이트
            memory_projects = get_projects_store()
            if project_id in memory_projects:
                memory_projects[project_id]['status'] = 'completed'
                memory_projects[project_id]['updated_at'] = datetime.utcnow().isoformat()
        
        return {
            "message": "섹션 생성 완료",
            "sections": created_sections
        }
        
    except ValueError as e:
        logger.error(f"Section generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="섹션 생성 중 오류가 발생했습니다."
        )


@router.get("/{project_id}/sections")
async def get_sections(project_id: str):
    """
    프로젝트의 섹션 목록 조회
    """
    try:
        # Firebase 먼저 시도, 실패하면 인메모리
        try:
            sections = firebase.get_sections(project_id)
        except:
            memory_sections = get_sections_store()
            sections = memory_sections.get(project_id, [])
        
        return {
            "sections": sections
        }
    except Exception as e:
        logger.error(f"Error getting sections: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="섹션 조회 중 오류가 발생했습니다."
        )


# Phase 2: 추가 엔드포인트

@router.get("", response_model=List[ProjectResponse])
async def list_all_projects(
    status_filter: Optional[str] = Query(None, description="상태 필터: draft, summarized, completed"),
    limit: int = Query(100, ge=1, le=500, description="최대 조회 개수"),
    source_type: Optional[str] = Query(None, description="소스 타입 필터: url, text, rss")
):
    """
    모든 프로젝트 목록 조회 (Phase 2)
    
    - **status**: 상태 필터 (옵션)
    - **limit**: 최대 조회 개수 (기본 100, 최대 500)
    - **source_type**: 소스 타입 필터 (옵션)
    
    최근 생성순으로 정렬됨
    """
    try:
        logger.info(f"Fetching all projects (status={status_filter}, limit={limit}, source_type={source_type})")
        
        # Firestore에서 프로젝트 목록 조회
        try:
            projects = firebase.get_all_projects(limit=limit, status=status_filter)
        except:
            # Firebase 실패 시 인메모리 사용
            logger.info("Firebase failed, using memory store")
            memory_projects = get_projects_store()
            projects = list(memory_projects.values())
            
            # 상태 필터링
            if status_filter:
                projects = [p for p in projects if p.get('status') == status_filter]
            
            # 정렬 (최근 생성 순)
            projects.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
            # 제한
            projects = projects[:limit]
        
        # source_type 필터링 (클라이언트 측)
        if source_type:
            projects = [p for p in projects if p.get('source_type') == source_type]
        
        logger.info(f"Found {len(projects)} projects")
        return [ProjectResponse(**project) for project in projects]
        
    except Exception as e:
        logger.error(f"Failed to fetch projects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch projects: {str(e)}"
        )


@router.put("/{project_id}/status", response_model=ProjectResponse)
async def update_project_status(project_id: str, new_status: str):
    """
    프로젝트 상태 변경 (Phase 2)
    
    - **project_id**: 프로젝트 ID
    - **new_status**: 새로운 상태 (draft, summarized, completed)
    """
    try:
        logger.info(f"Updating project status: {project_id} -> {new_status}")
        
        # 프로젝트 존재 확인
        try:
            existing_project = firebase.get_project(project_id)
        except:
            memory_projects = get_projects_store()
            existing_project = memory_projects.get(project_id)
        
        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}"
            )
        
        # 상태 검증
        valid_statuses = ['draft', 'summarized', 'completed']
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status: {new_status}. Must be one of: {', '.join(valid_statuses)}"
            )
        
        # 상태 업데이트
        try:
            updated_project = firebase.update_project(project_id, {'status': new_status})
        except:
            memory_projects = get_projects_store()
            memory_projects[project_id]['status'] = new_status
            memory_projects[project_id]['updated_at'] = datetime.utcnow().isoformat()
            updated_project = memory_projects[project_id]
        
        logger.info(f"Project status updated: {project_id}")
        return ProjectResponse(**updated_project)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update project status {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update project status: {str(e)}"
        )


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_by_id(project_id: str):
    """
    프로젝트 삭제 (Phase 2)
    
    - **project_id**: 프로젝트 ID
    
    ⚠️ 주의: 프로젝트와 모든 연관된 데이터(섹션, 대화)가 삭제됩니다.
    """
    try:
        logger.info(f"Deleting project: {project_id}")
        
        # 프로젝트 존재 확인
        try:
            existing_project = firebase.get_project(project_id)
        except:
            memory_projects = get_projects_store()
            existing_project = memory_projects.get(project_id)
        
        if not existing_project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project not found: {project_id}"
            )
        
        # 프로젝트 삭제
        try:
            firebase.delete_project(project_id)
        except:
            memory_projects = get_projects_store()
            memory_sections = get_sections_store()
            if project_id in memory_projects:
                del memory_projects[project_id]
            if project_id in memory_sections:
                del memory_sections[project_id]
        
        logger.info(f"Project deleted successfully: {project_id}")
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete project {project_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete project: {str(e)}"
        )

