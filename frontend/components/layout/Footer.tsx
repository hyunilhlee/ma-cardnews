/**
 * 푸터 컴포넌트
 */

import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center text-gray-600">
          <p className="text-sm">
            © 2025 CardNews AI Generator. All rights reserved.
          </p>
          <p className="text-xs mt-2 text-gray-500">
            AI 기반 카드뉴스 자동 제작 서비스
          </p>
        </div>
      </div>
    </footer>
  );
};

