/**
 * 요약 표시 컴포넌트
 */

'use client';

import React from 'react';
import { Button } from '../common/Button';

interface SummaryViewProps {
  summary: string;
  keywords: string[];
  recommendedCardCount: number;
  onGenerateSections: () => void;
  isLoading?: boolean;
}

export const SummaryView: React.FC<SummaryViewProps> = ({
  summary,
  keywords,
  recommendedCardCount,
  onGenerateSections,
  isLoading = false,
}) => {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">
        📝 요약 결과
      </h2>

      {/* 요약 내용 */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">요약</h3>
        <p className="text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg">
          {summary}
        </p>
      </div>

      {/* 키워드 */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-2">핵심 키워드</h3>
        <div className="flex flex-wrap gap-2">
          {keywords.map((keyword, index) => (
            <span
              key={index}
              className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
            >
              {keyword}
            </span>
          ))}
        </div>
      </div>

      {/* 권장 카드 수 */}
      <div className="mb-6 p-4 bg-green-50 rounded-lg">
        <p className="text-green-900 font-medium">
          💡 권장 카드 수: <span className="text-2xl font-bold">{recommendedCardCount}</span>개
        </p>
      </div>

      {/* 카드 생성 버튼 */}
      <Button
        onClick={onGenerateSections}
        variant="primary"
        size="lg"
        isLoading={isLoading}
        className="w-full"
      >
        {isLoading ? '카드 생성 중...' : '카드뉴스 생성하기 🎨'}
      </Button>
    </div>
  );
};

