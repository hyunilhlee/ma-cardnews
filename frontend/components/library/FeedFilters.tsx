'use client';

import { useState, useEffect } from 'react';
import { getSites } from '@/lib/api/sites';

interface Site {
  id: string;
  name: string;
  status: string;
}

interface FeedFiltersProps {
  filters: {
    siteId: string | null;
    keyword: string;
    yearMonth: string | null;
    page: number;
  };
  onChange: (filters: any) => void;
}

export function FeedFilters({ filters, onChange }: FeedFiltersProps) {
  const [sites, setSites] = useState<Site[]>([]);
  const [localKeyword, setLocalKeyword] = useState(filters.keyword || '');

  useEffect(() => {
    loadSites();
  }, []);

  const loadSites = async () => {
    try {
      const data = await getSites();
      setSites(data);
    } catch (error) {
      console.error('Failed to load sites:', error);
    }
  };

  const handleSiteChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value === '' ? null : e.target.value;
    onChange({ ...filters, siteId: value, page: 1 });
  };

  const handleKeywordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setLocalKeyword(e.target.value);
  };

  const handleKeywordSearch = () => {
    onChange({ ...filters, keyword: localKeyword, page: 1 });
  };

  const handleKeywordKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleKeywordSearch();
    }
  };

  const handleYearMonthChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value === '' ? null : e.target.value;
    onChange({ ...filters, yearMonth: value, page: 1 });
  };

  const handleReset = () => {
    setLocalKeyword('');
    onChange({ siteId: null, keyword: '', yearMonth: null, page: 1 });
  };

  // 2025년 9월부터 현재까지의 월 생성
  const generateMonthOptions = () => {
    const options = [];
    const now = new Date();
    const startDate = new Date(2025, 8, 1); // 2025년 9월 (0-indexed: 8)
    
    // 시작 월부터 현재까지 반복
    const currentDate = new Date(startDate);
    while (currentDate <= now) {
      const yearMonth = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}`;
      const label = `${currentDate.getFullYear()}년 ${currentDate.getMonth() + 1}월`;
      options.push({ value: yearMonth, label });
      
      // 다음 월로 이동
      currentDate.setMonth(currentDate.getMonth() + 1);
    }
    
    // 최신순으로 정렬 (역순)
    return options.reverse();
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        {/* 사이트 선택 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📍 사이트 선택
          </label>
          <select
            value={filters.siteId || ''}
            onChange={handleSiteChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          >
            <option value="">전체 사이트</option>
            {sites
              .filter(site => site.status === 'active')
              .map(site => (
                <option key={site.id} value={site.id}>
                  {site.name}
                </option>
              ))}
          </select>
        </div>

        {/* 월별 필터 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            📅 월별 필터
          </label>
          <select
            value={filters.yearMonth || ''}
            onChange={handleYearMonthChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
          >
            <option value="">전체 기간</option>
            {generateMonthOptions().map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        {/* 키워드 검색 */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            🔍 키워드 검색
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={localKeyword}
              onChange={handleKeywordChange}
              onKeyPress={handleKeywordKeyPress}
              placeholder="제목, 요약, 키워드 검색..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
            />
            <button
              onClick={handleKeywordSearch}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              검색
            </button>
          </div>
        </div>
      </div>

      {/* 초기화 버튼 */}
      <div className="flex justify-end">
        <button
          onClick={handleReset}
          className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
        >
          🔄 초기화
        </button>
      </div>

      {/* 활성 필터 표시 */}
      {(filters.siteId || filters.keyword || filters.yearMonth) && (
        <div className="mt-4 flex items-center gap-2 text-sm text-gray-600 flex-wrap">
          <span className="font-medium">활성 필터:</span>
          {filters.siteId && (
            <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
              사이트: {sites.find(s => s.id === filters.siteId)?.name || '알 수 없음'}
            </span>
          )}
          {filters.yearMonth && (
            <span className="inline-block px-3 py-1 bg-purple-100 text-purple-700 rounded-full">
              기간: {filters.yearMonth}
            </span>
          )}
          {filters.keyword && (
            <span className="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full">
              키워드: {filters.keyword}
            </span>
          )}
        </div>
      )}
    </div>
  );
}

