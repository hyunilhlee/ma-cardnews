/**
 * 헤더 컴포넌트
 */

import React from 'react';
import Link from 'next/link';

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="flex items-center space-x-2">
            <div className="text-2xl font-bold text-blue-600">
              📰 CardNews AI
            </div>
          </Link>
          
          <nav className="flex items-center space-x-4">
            <Link
              href="/"
              className="text-gray-700 hover:text-blue-600 transition-colors"
            >
              홈
            </Link>
            <Link
              href="/about"
              className="text-gray-700 hover:text-blue-600 transition-colors"
            >
              소개
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

