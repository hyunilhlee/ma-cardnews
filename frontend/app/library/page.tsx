'use client';

import { useState, useEffect } from 'react';
import { toast } from 'react-hot-toast';
import { 
  LibraryFeedItem, 
  getLibraryFeed, 
  createCardnewsFromFeed 
} from '@/lib/api/library';
import { FeedCard } from '@/components/library/FeedCard';
import { FeedFilters } from '@/components/library/FeedFilters';
import { useRouter } from 'next/navigation';

export default function LibraryPage() {
  const router = useRouter();
  const [feed, setFeed] = useState<LibraryFeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [filters, setFilters] = useState({
    siteId: null as string | null,
    keyword: '',
    yearMonth: null as string | null,
    page: 1,
    pageSize: 20
  });
  const [creatingIds, setCreatingIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    loadFeed();
  }, [filters]);

  const loadFeed = async () => {
    setLoading(true);
    try {
      const data = await getLibraryFeed({
        site_id: filters.siteId || undefined,
        keyword: filters.keyword || undefined,
        year_month: filters.yearMonth || undefined,
        page: filters.page,
        page_size: filters.pageSize
      });
      
      setFeed(data.items);
      setTotal(data.total);
    } catch (error: any) {
      console.error('Failed to load feed:', error);
      toast.error(error.message || 'RSS Library 로딩 실패');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCardnews = async (item: LibraryFeedItem) => {
    // 중복 생성 방지
    if (creatingIds.has(item.id)) {
      toast.error('이미 생성 중입니다');
      return;
    }

    setCreatingIds(prev => new Set([...prev, item.id]));
    
    try {
      toast.loading('카드뉴스를 생성하고 있습니다...', { id: 'creating' });
      
      // URL에서 전체 콘텐츠를 가져와야 하지만, 
      // 여기서는 요약을 content로 사용 (실제로는 스크래핑 필요)
      const response = await createCardnewsFromFeed({
        rss_post_id: item.id,
        site_id: item.source.site_id || '',
        url: item.url,
        title: item.title,
        content: item.summary  // 실제로는 전체 콘텐츠 필요
      });
      
      toast.success('카드뉴스 생성 완료!', { id: 'creating' });
      
      // 편집 페이지로 이동
      router.push(`/edit/${response.project_id}`);
      
    } catch (error: any) {
      console.error('Failed to create cardnews:', error);
      toast.error(error.message || '카드뉴스 생성 실패', { id: 'creating' });
    } finally {
      setCreatingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(item.id);
        return newSet;
      });
    }
  };

  const handlePageChange = (newPage: number) => {
    setFilters(prev => ({ ...prev, page: newPage }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const totalPages = Math.ceil(total / filters.pageSize);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* 헤더 */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📚 RSS Library
          </h1>
          <p className="text-gray-600">
            등록된 모든 RSS 사이트의 게시물을 한눈에 확인하세요
          </p>
        </div>

        {/* 필터 */}
        <FeedFilters 
          filters={filters}
          onChange={setFilters}
        />

        {/* 통계 */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              총 <span className="font-bold text-blue-600">{total}</span>개의 게시물
              {filters.keyword && (
                <span className="ml-2">
                  (키워드: <span className="font-semibold">{filters.keyword}</span>)
                </span>
              )}
            </div>
            <button
              onClick={loadFeed}
              disabled={loading}
              className="text-sm text-blue-600 hover:text-blue-700 font-medium disabled:text-gray-400"
            >
              🔄 새로고침
            </button>
          </div>
        </div>

        {/* 피드 목록 */}
        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">로딩 중...</p>
          </div>
        ) : feed.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-6xl mb-4">📭</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">
              게시물이 없습니다
            </h3>
            <p className="text-gray-600">
              RSS 사이트를 등록하거나 필터를 변경해보세요
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-6">
              {feed.map(item => (
                <FeedCard
                  key={item.id}
                  item={item}
                  onCreateCardnews={handleCreateCardnews}
                />
              ))}
            </div>

            {/* 페이지네이션 */}
            {totalPages > 1 && (
              <div className="mt-8 flex items-center justify-center gap-2">
                <button
                  onClick={() => handlePageChange(filters.page - 1)}
                  disabled={filters.page === 1}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-gray-900"
                >
                  이전
                </button>
                
                <div className="flex items-center gap-2">
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                    const pageNum = i + 1;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => handlePageChange(pageNum)}
                        className={`px-4 py-2 rounded-lg font-medium ${
                          filters.page === pageNum
                            ? 'bg-blue-600 text-white'
                            : 'bg-white border border-gray-300 hover:bg-gray-50 text-gray-900'
                        }`}
                      >
                        {pageNum}
                      </button>
                    );
                  })}
                  {totalPages > 5 && (
                    <>
                      <span className="text-gray-500">...</span>
                      <button
                        onClick={() => handlePageChange(totalPages)}
                        className={`px-4 py-2 rounded-lg font-medium ${
                          filters.page === totalPages
                            ? 'bg-blue-600 text-white'
                            : 'bg-white border border-gray-300 hover:bg-gray-50 text-gray-900'
                        }`}
                      >
                        {totalPages}
                      </button>
                    </>
                  )}
                </div>

                <button
                  onClick={() => handlePageChange(filters.page + 1)}
                  disabled={filters.page === totalPages}
                  className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-gray-900"
                >
                  다음
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

