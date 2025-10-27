/**
 * 프로젝트 상세 페이지
 */

'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { useProjectStore } from '@/lib/store/projectStore';
import { useUIStore } from '@/lib/store/uiStore';
import { projectService } from '@/lib/services/projectService';
import { chatService } from '@/lib/services/chatService';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { Button } from '@/components/common/Button';
import { SummaryView } from '@/components/summary/SummaryView';
import { CardList } from '@/components/cardnews/CardList';
import { ChatInterface } from '@/components/chat/ChatInterface';
import { ChatMessage } from '@/lib/types/chat';
import toast from 'react-hot-toast';

export default function ProjectPage() {
  const params = useParams();
  const projectId = params.id as string;

  const {
    currentProject,
    setCurrentProject,
    sections,
    setSections,
    isLoading,
    setIsLoading,
    error,
    setError,
  } = useProjectStore();

  const { currentStep, setCurrentStep } = useUIStore();

  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [isChatLoading, setIsChatLoading] = useState(false);

  // 프로젝트 로드
  useEffect(() => {
    loadProject();
  }, [projectId]);

  const loadProject = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const project = await projectService.get(projectId);
      setCurrentProject(project);

      // 프로젝트 상태에 따라 단계 결정
      if (project.status === 'completed') {
        const projectSections = await projectService.getSections(projectId);
        setSections(projectSections);
        setCurrentStep('edit');
      } else if (project.summary) {
        setCurrentStep('generate');
      } else {
        setCurrentStep('summarize');
      }
    } catch (error: any) {
      console.error('프로젝트 로드 실패:', error);
      setError('프로젝트를 불러올 수 없습니다');
      toast.error('프로젝트를 불러올 수 없습니다');
    } finally {
      setIsLoading(false);
    }
  };

  // 요약 생성
  const handleSummarize = async () => {
    if (!currentProject) return;

    setIsLoading(true);
    try {
      const result = await projectService.summarize(projectId);
      setCurrentProject({
        ...currentProject,
        summary: result.summary,
        keywords: result.keywords,
        recommended_card_count: result.recommended_card_count,
      });
      setCurrentStep('generate');
      toast.success('요약이 완료되었습니다!');
    } catch (error: any) {
      console.error('요약 실패:', error);
      toast.error('요약 생성에 실패했습니다');
    } finally {
      setIsLoading(false);
    }
  };

  // 카드 섹션 생성
  const handleGenerateSections = async () => {
    if (!currentProject) return;

    setIsLoading(true);
    try {
      const result = await projectService.generateSections(projectId);
      setSections(result.sections);
      setCurrentStep('edit');
      toast.success('카드뉴스가 생성되었습니다!');
    } catch (error: any) {
      console.error('카드 생성 실패:', error);
      toast.error('카드 생성에 실패했습니다');
    } finally {
      setIsLoading(false);
    }
  };

  // 채팅 메시지 전송
  const handleSendMessage = async (message: string) => {
    if (!currentProject) return;

    // 사용자 메시지 추가
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date(),
    };
    setChatMessages((prev) => [...prev, userMessage]);

    setIsChatLoading(true);
    try {
      const response = await chatService.sendMessage({
        project_id: projectId,
        user_message: message,
        current_sections: sections,
        conversation_history: chatMessages,
      });

      // AI 응답 추가
      const aiMessage: ChatMessage = {
        role: 'assistant',
        content: response.ai_response,
        timestamp: new Date(),
      };
      setChatMessages((prev) => [...prev, aiMessage]);

      // 섹션이 업데이트되었으면 반영
      if (response.updated_sections && response.updated_sections.length > 0) {
        setSections(response.updated_sections);
        toast.success('카드가 업데이트되었습니다!');
      }
    } catch (error: any) {
      console.error('채팅 실패:', error);
      toast.error('메시지 전송에 실패했습니다');
    } finally {
      setIsChatLoading(false);
    }
  };

  // 로딩 중
  if (isLoading && !currentProject) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <LoadingSpinner size="lg" text="프로젝트를 불러오는 중..." />
      </div>
    );
  }

  // 에러
  if (error) {
    return (
      <div className="max-w-2xl mx-auto text-center py-12">
        <div className="text-6xl mb-4">😢</div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">오류가 발생했습니다</h2>
        <p className="text-gray-600 mb-6">{error}</p>
        <Button onClick={() => window.location.href = '/'}>홈으로 돌아가기</Button>
      </div>
    );
  }

  if (!currentProject) {
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto space-y-8">
      {/* Step 표시 */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <StepIndicator step={1} label="요약" active={currentStep === 'summarize'} completed={currentStep !== 'summarize'} />
            <div className="w-12 h-1 bg-gray-300"></div>
            <StepIndicator step={2} label="생성" active={currentStep === 'generate'} completed={currentStep === 'edit'} />
            <div className="w-12 h-1 bg-gray-300"></div>
            <StepIndicator step={3} label="편집" active={currentStep === 'edit'} />
          </div>
        </div>
      </div>

      {/* Step 1: 요약 */}
      {currentStep === 'summarize' && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">원본 내용</h2>
          <div className="bg-gray-50 p-4 rounded-lg mb-6 max-h-96 overflow-y-auto">
            <p className="text-gray-700 whitespace-pre-wrap">{currentProject.source_content}</p>
          </div>
          <Button onClick={handleSummarize} variant="primary" size="lg" className="w-full" isLoading={isLoading}>
            {isLoading ? '요약 생성 중...' : 'AI로 요약하기 🤖'}
          </Button>
        </div>
      )}

      {/* Step 2: 카드 생성 */}
      {currentStep === 'generate' && currentProject.summary && (
        <SummaryView
          summary={currentProject.summary}
          keywords={currentProject.keywords || []}
          recommendedCardCount={currentProject.recommended_card_count || 5}
          onGenerateSections={handleGenerateSections}
          isLoading={isLoading}
        />
      )}

      {/* Step 3: 편집 */}
      {currentStep === 'edit' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* 카드 목록 */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">🎨 카드뉴스</h2>
              <CardList sections={sections} />
            </div>
          </div>

          {/* 채팅 인터페이스 */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 h-[calc(100vh-12rem)]">
              <ChatInterface
                messages={chatMessages}
                onSendMessage={handleSendMessage}
                isLoading={isChatLoading}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Step 표시 컴포넌트
interface StepIndicatorProps {
  step: number;
  label: string;
  active?: boolean;
  completed?: boolean;
}

const StepIndicator: React.FC<StepIndicatorProps> = ({ step, label, active, completed }) => {
  return (
    <div className="flex flex-col items-center">
      <div
        className={`w-10 h-10 rounded-full flex items-center justify-center font-bold ${
          completed
            ? 'bg-green-500 text-white'
            : active
            ? 'bg-blue-600 text-white'
            : 'bg-gray-300 text-gray-600'
        }`}
      >
        {completed ? '✓' : step}
      </div>
      <span className={`text-sm mt-2 ${active ? 'font-semibold text-blue-600' : 'text-gray-600'}`}>
        {label}
      </span>
    </div>
  );
};

