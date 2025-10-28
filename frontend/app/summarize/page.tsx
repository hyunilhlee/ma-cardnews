'use client';

import { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'react-hot-toast';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

type SummaryLength = 'short' | 'medium' | 'long';

interface SummaryOptions {
  length: SummaryLength;
  customRequest: string;
}

export default function SummarizePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  // URL 파라미터에서 정보 가져오기
  const source = searchParams.get('source') || 'url';
  const url = searchParams.get('url') || '';
  const title = searchParams.get('title') || '';
  const siteId = searchParams.get('site_id') || '';
  const siteName = searchParams.get('site_name') || '';
  const rssPostId = searchParams.get('rss_post_id') || '';
  
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState('');
  const [keywords, setKeywords] = useState<string[]>([]);
  const [recommendedCards, setRecommendedCards] = useState(3);
  
  // 요약 옵션
  const [options, setOptions] = useState<SummaryOptions>({
    length: 'medium',
    customRequest: ''
  });
  
  // 초기 로딩 시 자동 요약 생성
  useEffect(() => {
    if (url) {
      generateSummary('medium', '');
    }
  }, [url]);
  
  const generateSummary = async (length: SummaryLength, customRequest: string) => {
    setLoading(true);
    
    try {
      toast.loading('요약을 생성하고 있습니다...', { id: 'summarizing' });
      
      // 길이별 추가 지시사항
      const lengthInstructions: Record<SummaryLength, string> = {
        short: '매우 간결하게 핵심만 요약해주세요. 3-5문장 이내로 작성하세요.',
        medium: '적절한 길이로 요약해주세요. 5-8문장 정도로 작성하세요.',
        long: '상세하게 요약해주세요. 8-12문장으로 자세히 작성하세요.'
      };
      
      // API 호출
      const response = await axios.post(`${API_URL}/api/projects/summarize`, {
        source_type: source === 'rss' ? 'rss' : 'url',
        source_url: url,
        additional_instructions: `${lengthInstructions[length]} ${customRequest}`.trim()
      });
      
      setSummary(response.data.summary || '');
      setKeywords(response.data.keywords || []);
      setRecommendedCards(response.data.recommended_cards || 3);
      
      toast.success('요약 생성 완료!', { id: 'summarizing' });
      
    } catch (error: any) {
      console.error('Failed to generate summary:', error);
      toast.error(error.message || '요약 생성 실패', { id: 'summarizing' });
    } finally {
      setLoading(false);
    }
  };
  
  const handleLengthChange = (length: SummaryLength) => {
    setOptions(prev => ({ ...prev, length }));
    generateSummary(length, options.customRequest);
  };
  
  const handleCustomRequest = () => {
    if (!options.customRequest.trim()) {
      toast.error('요청 내용을 입력해주세요');
      return;
    }
    generateSummary(options.length, options.customRequest);
  };
  
  const handleCreateCardnews = async () => {
    if (!summary) {
      toast.error('요약을 먼저 생성해주세요');
      return;
    }
    
    setLoading(true);
    
    try {
      toast.loading('카드뉴스를 생성하고 있습니다...', { id: 'creating' });
      
      // 프로젝트 생성 및 카드뉴스 생성
      const response = await axios.post(`${API_URL}/api/projects`, {
        source_type: source === 'rss' ? 'rss' : 'url',
        source_url: url,
        title: title,
        summary: summary,
        keywords: keywords,
        recommended_cards: recommendedCards,
        ...(source === 'rss' && {
          source_site_id: siteId,
          source_site_name: siteName
        })
      });
      
      const projectId = response.data.id;
      
      // 카드뉴스 생성
      await axios.post(`${API_URL}/api/projects/${projectId}/generate`, {
        summary: summary,
        original_text: '', // RSS에서는 원본 텍스트가 없을 수 있음
        recommended_cards: recommendedCards
      });
      
      toast.success('카드뉴스 생성 완료!', { id: 'creating' });
      
      // 편집 페이지로 이동
      router.push(`/edit/${projectId}`);
      
    } catch (error: any) {
      console.error('Failed to create cardnews:', error);
      toast.error(error.message || '카드뉴스 생성 실패', { id: 'creating' });
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* 헤더 */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📝 요약 생성
          </h1>
          <p className="text-gray-600">
            원하는 스타일로 요약을 생성하고 카드뉴스를 만드세요
          </p>
        </div>

        {/* 원본 정보 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">📰 원본 정보</h2>
          
          <div className="space-y-3">
            {siteName && (
              <div className="flex items-start">
                <span className="text-sm font-medium text-gray-600 w-24">사이트:</span>
                <span className="text-sm text-gray-900">{siteName}</span>
              </div>
            )}
            
            <div className="flex items-start">
              <span className="text-sm font-medium text-gray-600 w-24">제목:</span>
              <span className="text-sm text-gray-900">{title || '제목 없음'}</span>
            </div>
            
            <div className="flex items-start">
              <span className="text-sm font-medium text-gray-600 w-24">URL:</span>
              <a 
                href={url} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-sm text-blue-600 hover:underline break-all"
              >
                {url}
              </a>
            </div>
          </div>
        </div>

        {/* 요약 옵션 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">⚙️ 요약 옵션</h2>
          
          {/* 길이 선택 */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              요약 길이
            </label>
            <div className="grid grid-cols-3 gap-4">
              {[
                { value: 'short' as SummaryLength, label: '짧게', desc: '3-5문장' },
                { value: 'medium' as SummaryLength, label: '중간', desc: '5-8문장' },
                { value: 'long' as SummaryLength, label: '길게', desc: '8-12문장' }
              ].map(option => (
                <button
                  key={option.value}
                  onClick={() => handleLengthChange(option.value)}
                  disabled={loading}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    options.length === option.value
                      ? 'border-blue-600 bg-blue-50 text-blue-900'
                      : 'border-gray-300 bg-white text-gray-900 hover:border-blue-300'
                  } disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  <div className="font-semibold text-lg mb-1">{option.label}</div>
                  <div className="text-sm text-gray-600">{option.desc}</div>
                </button>
              ))}
            </div>
          </div>

          {/* 자연어 요청 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              💬 자연어 요청 (선택)
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={options.customRequest}
                onChange={(e) => setOptions(prev => ({ ...prev, customRequest: e.target.value }))}
                onKeyPress={(e) => e.key === 'Enter' && handleCustomRequest()}
                placeholder="예: 전문적인 톤으로, 이모지 추가, 핵심만 강조..."
                disabled={loading}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 disabled:opacity-50"
              />
              <button
                onClick={handleCustomRequest}
                disabled={loading || !options.customRequest.trim()}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                적용
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              💡 팁: "전문적으로", "이모지 추가", "핵심만", "스토리텔링 방식으로" 등
            </p>
          </div>
        </div>

        {/* 생성된 요약 */}
        {summary && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">📄 생성된 요약</h2>
            
            <div className="prose max-w-none mb-6">
              <p className="text-gray-800 whitespace-pre-wrap leading-relaxed">
                {summary}
              </p>
            </div>

            {/* 키워드 */}
            {keywords.length > 0 && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-gray-700 mb-2">🏷️ 추출된 키워드</h3>
                <div className="flex flex-wrap gap-2">
                  {keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="inline-block px-3 py-1 text-sm font-medium text-blue-600 bg-blue-50 rounded-full"
                    >
                      #{keyword}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* 추천 카드 수 */}
            <div className="text-sm text-gray-600">
              💡 추천 카드 수: <span className="font-semibold">{recommendedCards}개</span>
            </div>
          </div>
        )}

        {/* 액션 버튼 */}
        <div className="flex gap-4">
          <button
            onClick={() => router.back()}
            className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
          >
            ← 뒤로가기
          </button>
          
          <button
            onClick={handleCreateCardnews}
            disabled={loading || !summary}
            className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? '생성 중...' : '🎨 카드뉴스 생성'}
          </button>
        </div>
      </div>
    </div>
  );
}

