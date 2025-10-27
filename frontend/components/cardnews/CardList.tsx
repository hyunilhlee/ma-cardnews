/**
 * 카드 목록 컴포넌트
 */

'use client';

import React from 'react';
import { CardSection } from '@/lib/types/section';
import { CardPreview } from './CardPreview';

interface CardListProps {
  sections: CardSection[];
}

export const CardList: React.FC<CardListProps> = ({ sections }) => {
  if (sections.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">아직 생성된 카드가 없습니다.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {sections
        .sort((a, b) => a.order - b.order)
        .map((section, index) => (
          <div key={section.id} className="relative">
            {/* 카드 번호 */}
            <div className="absolute -top-3 -left-3 z-10 bg-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold shadow-md">
              {index + 1}
            </div>
            <CardPreview section={section} />
          </div>
        ))}
    </div>
  );
};

