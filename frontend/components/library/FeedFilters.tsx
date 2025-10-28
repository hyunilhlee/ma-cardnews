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

  const handleReset = () => {
    setLocalKeyword('');
    onChange({ siteId: null, keyword: '', page: 1 });
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex flex-col md:flex-row gap-4">
        {/* 사이트 선택 */}
        <div className="flex-1">
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

        {/* 키워드 검색 */}
        <div className="flex-1">
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

        {/* 초기화 버튼 */}
        <div className="flex items-end">
          <button
            onClick={handleReset}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
          >
            🔄 초기화
          </button>
        </div>
      </div>

      {/* 활성 필터 표시 */}
      {(filters.siteId || filters.keyword) && (
        <div className="mt-4 flex items-center gap-2 text-sm text-gray-600">
          <span className="font-medium">활성 필터:</span>
          {filters.siteId && (
            <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
              사이트: {sites.find(s => s.id === filters.siteId)?.name || '알 수 없음'}
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

