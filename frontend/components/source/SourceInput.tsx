/**
 * 소스 입력 컴포넌트 (Step 1)
 */

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Textarea } from '../common/Textarea';
import { StatusBadge } from '../common/StatusBadge';
import { projectService } from '@/lib/services/projectService';
import { SourceType } from '@/lib/types/project';
import { AI_MODELS, formatPrice } from '@/lib/constants/aiModels';
import toast from 'react-hot-toast';

type CardStartType = 'title' | 'content';

export const SourceInput: React.FC = () => {
  const router = useRouter();
  const [sourceType, setSourceType] = useState<SourceType>('url');  // 기본값: URL
  const [content, setContent] = useState('');
  const [cardStartType, setCardStartType] = useState<CardStartType>('title');
  const [selectedModel, setSelectedModel] = useState('gpt-4.1-nano'); // 기본값: GPT-4.1 Nano
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!content.trim()) {
      toast.error('내용을 입력해주세요');
      return;
    }

    setIsLoading(true);

    try {
      const project = await projectService.create({
        source_type: sourceType,
        source_content: content,
        card_start_type: cardStartType,
        model: selectedModel,
      });

      toast.success('프로젝트가 생성되었습니다!');
      router.push(`/project/${project.id}`);
    } catch (error: any) {
      console.error('프로젝트 생성 실패:', error);
      toast.error(error.response?.data?.detail || '오류가 발생했습니다');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        {/* 헤더와 상태 */}
        <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  카드뉴스 제작 시작
                </h1>
                <p className="text-gray-600">
                  링크나 텍스트를 입력하여 AI가 자동으로 카드뉴스를 생성합니다
                </p>
              </div>
            </div>
            
            {/* AI 상태 및 모델 선택 */}
            <div className="mb-6 pb-6 border-b border-gray-200 space-y-4">
              {/* AI 연결 상태 */}
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-800">🤖 AI 설정</h2>
                <StatusBadge />
              </div>
              
              {/* AI 모델 선택 카드 */}
              <div className="bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-50 rounded-xl p-5 border border-purple-200 shadow-sm">
                <div className="flex items-center justify-between mb-3">
                  <label className="text-sm font-semibold text-gray-800 flex items-center gap-2">
                    <span className="text-2xl">⚡</span>
                    사용할 AI 모델
                  </label>
                </div>
                
                {/* 모델 선택 그리드 */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
                  {AI_MODELS.map((model) => {
                    const isSelected = selectedModel === model.id;
                    return (
                      <button
                        key={model.id}
                        type="button"
                        onClick={() => setSelectedModel(model.id)}
                        className={`relative p-3 rounded-lg border-2 transition-all text-left ${
                          isSelected
                            ? 'border-purple-500 bg-white shadow-md scale-105'
                            : 'border-gray-200 bg-white/80 hover:border-purple-300 hover:shadow-sm'
                        }`}
                      >
                        {model.recommended && (
                          <div className="absolute -top-2 -right-2 bg-gradient-to-r from-yellow-400 to-orange-400 text-white text-xs font-bold px-2 py-0.5 rounded-full shadow-sm">
                            추천
                          </div>
                        )}
                        
                        <div className="space-y-1">
                          {/* 모델명 */}
                          <div className="font-bold text-sm text-gray-900 flex items-center justify-between">
                            <span className="truncate">{model.name}</span>
                            {isSelected && <span className="text-purple-600">✓</span>}
                          </div>
                          
                          {/* 속도/품질 뱃지 */}
                          <div className="flex items-center gap-1">
                            <span className={`text-xs px-1.5 py-0.5 rounded ${
                              model.speed === 'fast' ? 'bg-green-100 text-green-700' :
                              model.speed === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-orange-100 text-orange-700'
                            }`}>
                              {model.speed === 'fast' ? '⚡' : 
                               model.speed === 'medium' ? '⚙️' : 
                               '🐌'}
                            </span>
                            <span className={`text-xs px-1.5 py-0.5 rounded ${
                              model.quality === 'good' ? 'bg-blue-100 text-blue-700' :
                              model.quality === 'better' ? 'bg-indigo-100 text-indigo-700' :
                              'bg-purple-100 text-purple-700'
                            }`}>
                              {model.quality === 'good' ? '👍' : 
                               model.quality === 'better' ? '⭐' : 
                               '🌟'}
                            </span>
                          </div>
                          
                          {/* 가격 */}
                          <div className="text-xs text-gray-600 space-y-0.5">
                            <div className="flex justify-between">
                              <span>입력:</span>
                              <span className="font-mono font-semibold text-gray-800">{formatPrice(model.inputPrice)}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>출력:</span>
                              <span className="font-mono font-semibold text-gray-800">{formatPrice(model.outputPrice)}</span>
                            </div>
                          </div>
                        </div>
                      </button>
                    );
                  })}
                </div>
                
                {/* 선택된 모델 설명 */}
                {(() => {
                  const currentModel = AI_MODELS.find(m => m.id === selectedModel);
                  return currentModel ? (
                    <div className="mt-3 p-3 bg-white rounded-lg border border-purple-200">
                      <p className="text-sm text-gray-700">
                        <span className="font-semibold text-purple-700">선택됨:</span> {currentModel.description}
                      </p>
                    </div>
                  ) : null;
                })()}
              </div>
            </div>

        {/* 소스 타입 선택 */}
        <div className="mb-6 flex space-x-4">
          <button
            type="button"
            onClick={() => setSourceType('url')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${
              sourceType === 'url'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            🔗 URL 링크 (다중 가능)
          </button>
          <button
            type="button"
            onClick={() => setSourceType('text')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${
              sourceType === 'text'
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            📝 텍스트 직접 입력
          </button>
        </div>

        {/* 입력 폼 */}
        <form onSubmit={handleSubmit}>
          {sourceType === 'url' ? (
            <Textarea
              placeholder="https://example.com/article1&#10;https://example.com/article2&#10;https://example.com/article3"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              label="URL 주소 (여러 개 가능)"
              helperText="💡 각 URL을 줄바꿈(Enter)으로 구분하여 입력하세요. 여러 기사를 하나의 카드뉴스로 합칩니다."
              rows={8}
              required
            />
          ) : (
            <Textarea
              placeholder="카드뉴스로 만들 내용을 입력하세요..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
              label="내용"
              helperText={`${content.length} / 10,000자`}
              rows={12}
              maxLength={10000}
              required
            />
          )}

          {/* 카드뉴스 시작 옵션 */}
          <div className="mt-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              📄 카드뉴스 시작 방식
            </label>
            <div className="grid grid-cols-2 gap-3">
              <button
                type="button"
                onClick={() => setCardStartType('title')}
                className={`p-3 rounded-lg border-2 transition-all text-left ${
                  cardStartType === 'title'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <div className="font-semibold text-sm mb-1 text-gray-900">🎯 제목으로 시작</div>
                <div className="text-xs text-gray-600">
                  첫 페이지에 제목과 부제목 표시
                </div>
              </button>
              <button
                type="button"
                onClick={() => setCardStartType('content')}
                className={`p-3 rounded-lg border-2 transition-all text-left ${
                  cardStartType === 'content'
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <div className="font-semibold text-sm mb-1 text-gray-900">📝 내용으로 시작</div>
                <div className="text-xs text-gray-600">
                  제목 없이 바로 내용 시작
                </div>
              </button>
            </div>
          </div>

          <div className="mt-6">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              isLoading={isLoading}
              className="w-full"
            >
              {isLoading ? '처리 중...' : '카드뉴스 만들기 🚀'}
            </Button>
          </div>
        </form>

        {/* 안내 메시지 */}
        <div className="mt-8 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-2">💡 이렇게 작동합니다</h3>
          <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
            <li>소스를 입력하면 AI가 자동으로 요약합니다</li>
            <li>요약을 바탕으로 카드뉴스 구조를 생성합니다</li>
            <li>AI와 대화하며 내용을 자유롭게 수정할 수 있습니다</li>
          </ol>
          {sourceType === 'url' && (
            <div className="mt-3 p-3 bg-green-50 rounded border border-green-200">
              <p className="text-sm text-green-900 font-semibold mb-2">🎯 다중 URL 사용법</p>
              <ul className="text-xs text-green-800 space-y-1">
                <li>• <strong>줄바꿈(Enter)</strong>으로 URL을 구분합니다</li>
                <li>• 여러 URL의 내용을 합쳐서 하나의 카드뉴스로 만듭니다</li>
                <li>• 각 출처는 자동으로 구분되어 표시됩니다</li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

