'use client';

import { LibraryFeedItem } from '@/lib/api/library';
import { format } from 'date-fns';
import { ko } from 'date-fns/locale';
import Link from 'next/link';

interface FeedCardProps {
  item: LibraryFeedItem;
  onCreateCardnews: (item: LibraryFeedItem) => void;
}

export function FeedCard({ item, onCreateCardnews }: FeedCardProps) {
  const getStatusBadge = () => {
    if (!item.has_cardnews) return null;
    
    const statusColors = {
      draft: 'bg-yellow-100 text-yellow-800',
      summarized: 'bg-blue-100 text-blue-800',
      completed: 'bg-green-100 text-green-800'
    };
    
    const statusLabels = {
      draft: '📝 초안',
      summarized: '✏️ 요약 완료',
      completed: '✅ 생성 완료'
    };
    
    const color = statusColors[item.status || 'draft'];
    const label = statusLabels[item.status || 'draft'];
    
    return (
      <span className={`inline-block px-3 py-1 text-sm font-semibold rounded ${color}`}>
        {label}
      </span>
    );
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return '날짜 없음';
    
    try {
      const date = new Date(dateStr);
      // 날짜 + 시간 표시 (시간 정보가 있으면)
      const hasTime = date.getHours() !== 0 || date.getMinutes() !== 0;
      if (hasTime) {
        return format(date, 'yyyy년 M월 d일 HH:mm', { locale: ko });
      }
      return format(date, 'yyyy년 M월 d일', { locale: ko });
    } catch {
      return '날짜 형식 오류';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border border-gray-200">
      {/* 헤더 */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-2">
            {item.is_new && (
              <span className="inline-block px-2 py-1 text-xs font-bold text-white bg-red-500 rounded mr-2">
                🆕 NEW
              </span>
            )}
            {item.title}
          </h3>
          {/* 원본 제목 (영문 등) */}
          {item.title_original && item.title_original !== item.title && (
            <p className="text-sm text-gray-500 italic mt-1">
              {item.title_original}
            </p>
          )}
        </div>
        
        <div className="ml-4">
          {getStatusBadge()}
        </div>
      </div>

      {/* 메타 정보 */}
      <div className="flex items-center gap-4 text-sm text-gray-600 mb-4 flex-wrap">
        <div className="flex items-center gap-1">
          <span>📍</span>
          <span className="font-medium">{item.source.site_name}</span>
        </div>
        
        <div className="flex items-center gap-1">
          <span>📅</span>
          <span>{formatDate(item.published_at)}</span>
        </div>
        
        <div className="flex items-center gap-1">
          <span>{item.type === 'project' ? '📰' : '🔖'}</span>
          <span className="text-xs">
            {item.type === 'project' ? '프로젝트' : 'RSS 피드'}
          </span>
        </div>
      </div>

      {/* 키워드 */}
      {item.keywords && item.keywords.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {item.keywords.slice(0, 5).map((keyword, index) => (
            <span
              key={index}
              className="inline-block px-3 py-1 text-sm font-medium text-blue-600 bg-blue-50 rounded-full"
            >
              #{keyword}
            </span>
          ))}
        </div>
      )}

      {/* 요약 */}
      <p className="text-gray-700 mb-6 line-clamp-3">
        {item.summary || '요약이 없습니다.'}
      </p>

      {/* 카드뉴스 생성 상태 표시 */}
      {item.has_cardnews && (
        <div className="mb-4 flex items-center gap-2">
          <span className="inline-flex items-center px-3 py-1 text-sm font-semibold text-green-800 bg-green-100 rounded-full">
            ✅ 카드뉴스 생성됨
          </span>
        </div>
      )}

      {/* 액션 버튼 */}
      <div className="flex gap-3 flex-wrap">
        {!item.has_cardnews ? (
          <button
            onClick={() => onCreateCardnews(item)}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold shadow-sm hover:shadow-md"
          >
            🎨 카드뉴스 생성
          </button>
        ) : (
          <Link
            href={`/edit/${item.project_id}`}
            className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-semibold shadow-sm hover:shadow-md inline-flex items-center gap-2"
          >
            <span>📰</span>
            <span>카드뉴스 보기</span>
          </Link>
        )}
        
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-6 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors font-semibold"
        >
          🔗 원본 보기
        </a>
      </div>
    </div>
  );
}

