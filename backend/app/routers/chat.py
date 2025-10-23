"""채팅 관련 API 라우터"""

from fastapi import APIRouter, HTTPException, status
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.utils import firebase
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# 서비스 인스턴스 (기본 모델 사용, 실제 사용 시 프로젝트 모델로 재생성)
# chat_service = ChatService()

# 인메모리 저장소
from app.utils.memory_store import get_projects_store, get_sections_store


@router.post("", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    """
    AI 채팅 처리
    
    - 사용자 메시지를 받아 AI가 응답
    - 필요시 카드 섹션 수정
    - 대화 이력 저장
    """
    try:
        # 프로젝트 존재 확인 (Firebase 또는 인메모리)
        try:
            project = firebase.get_project(request.project_id)
        except:
            memory_projects = get_projects_store()
            project = memory_projects.get(request.project_id)
        
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="프로젝트를 찾을 수 없습니다."
            )
        
        # 채팅 처리 (프로젝트에 저장된 모델 사용)
        logger.info(f"Processing chat for project: {request.project_id}")
        project_model = project.get('model', 'gpt-4o-mini')
        project_chat_service = ChatService(model=project_model)
        result = project_chat_service.process_chat_message(
            user_message=request.user_message,
            current_sections=request.current_sections,
            conversation_history=request.conversation_history
        )
        
        # 섹션이 수정되었으면 저장
        if result['updated_sections']:
            logger.info("Updating sections")
            try:
                # Firebase 시도
                existing_sections = firebase.get_sections(request.project_id)
                for section in existing_sections:
                    firebase.delete_section(request.project_id, section['id'])
                firebase.create_sections(request.project_id, result['updated_sections'])
            except:
                # 인메모리 업데이트
                memory_sections = get_sections_store()
                memory_sections[request.project_id] = result['updated_sections']
        
        # 대화 이력 저장 (Firebase만, 실패해도 무시)
        try:
            firebase.save_conversation(
                project_id=request.project_id,
                user_message=request.user_message,
                ai_response=result['ai_response']
            )
        except:
            pass  # 인메모리는 대화 이력 저장 안함
        
        return ChatResponse(
            ai_response=result['ai_response'],
            updated_sections=result['updated_sections'],
            action_taken=result['action_taken']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"채팅 처리 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/{project_id}/history")
async def get_chat_history(project_id: str, limit: int = 10):
    """
    대화 이력 조회
    """
    try:
        # Firebase에서만 조회 (인메모리는 대화 이력 저장 안함)
        try:
            conversations = firebase.get_conversations(project_id, limit)
        except:
            conversations = []  # 인메모리는 빈 배열 반환
        
        return {
            "conversations": conversations
        }
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="대화 이력 조회 중 오류가 발생했습니다."
        )

