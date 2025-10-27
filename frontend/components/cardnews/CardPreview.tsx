/**
 * 카드 미리보기 컴포넌트
 */

'use client';

import React from 'react';
import { CardSection } from '@/lib/types/section';

interface CardPreviewProps {
  section: CardSection;
}

export const CardPreview: React.FC<CardPreviewProps> = ({ section }) => {
  const { type, title, content, design_config } = section;

  // 카드 타입별 스타일
  const getTypeStyles = () => {
    switch (type) {
      case 'title':
        return 'border-blue-500';
      case 'content':
        return 'border-gray-300';
      case 'closing':
        return 'border-green-500';
      default:
        return 'border-gray-300';
    }
  };

  return (
    <div
      className={`relative rounded-lg border-4 ${getTypeStyles()} overflow-hidden shadow-lg transition-transform hover:scale-105`}
      style={{
        backgroundColor: design_config.background_color,
        aspectRatio: '1 / 1.4',
        minHeight: '400px',
      }}
    >
      <div className="absolute inset-0 flex flex-col justify-center items-center p-8 text-center">
        {title && (
          <h3
            className="font-bold mb-4"
            style={{
              fontFamily: design_config.font_family,
              fontSize: `${design_config.font_size + 8}px`,
              color: design_config.background_color === '#FFFFFF' ? '#000000' : '#FFFFFF',
            }}
          >
            {title}
          </h3>
        )}
        <p
          className="leading-relaxed"
          style={{
            fontFamily: design_config.font_family,
            fontSize: `${design_config.font_size}px`,
            color: design_config.background_color === '#FFFFFF' ? '#333333' : '#F5F5F5',
          }}
        >
          {content}
        </p>
      </div>

      {/* 카드 타입 뱃지 */}
      <div className="absolute top-2 right-2">
        <span className="px-2 py-1 bg-black bg-opacity-50 text-white text-xs rounded">
          {type === 'title' ? '제목' : type === 'content' ? '내용' : '마무리'}
        </span>
      </div>
    </div>
  );
};

