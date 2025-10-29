'use client';

import { useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { toast } from 'react-hot-toast';
import { createCardnewsFromFeed } from '@/lib/api/library';

function GeneratingContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const generateCardnews = async () => {
      try {
        const rssPostId = searchParams.get('rss_post_id');
        const siteId = searchParams.get('site_id');
        const url = searchParams.get('url');
        const title = searchParams.get('title');
        const summary = searchParams.get('summary');

        if (!rssPostId || !siteId || !url || !title || !summary) {
          throw new Error('필수 파라미터가 누락되었습니다.');
        }

        toast.loading('카드뉴스를 생성하고 있습니다...', { id: 'generating' });

        const result = await createCardnewsFromFeed({
          rss_post_id: rssPostId,
          site_id: siteId,
          url: url,
          title: title,
          content: summary
        });

        toast.success('카드뉴스 생성 완료!', { id: 'generating' });

        // 편집 페이지로 이동
        router.push(`/edit/${result.project_id}`);
      } catch (error: any) {
        console.error('Failed to generate cardnews:', error);
        toast.error(error.message || '카드뉴스 생성 실패', { id: 'generating' });
        
        // 3초 후 Library로 돌아가기
        setTimeout(() => {
          router.push('/library');
        }, 3000);
      }
    };

    generateCardnews();
  }, [router, searchParams]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center">
        {/* 로딩 스피너 */}
        <div className="mb-8">
          <div className="inline-block relative">
            {/* 외부 원 */}
            <div className="w-32 h-32 border-8 border-blue-200 rounded-full"></div>
            {/* 회전하는 원 */}
            <div className="absolute top-0 left-0 w-32 h-32 border-8 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
          </div>
        </div>

        {/* 메시지 */}
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          🎨 카드뉴스 생성 중...
        </h1>
        <p className="text-gray-600 text-lg mb-2">
          AI가 콘텐츠를 분석하고 있습니다
        </p>
        <p className="text-gray-500 text-sm">
          잠시만 기다려 주세요 (약 10-30초 소요)
        </p>

        {/* 진행 단계 표시 */}
        <div className="mt-12 max-w-md mx-auto">
          <div className="space-y-4">
            {[
              { icon: '📄', text: '콘텐츠 분석 중...' },
              { icon: '✨', text: 'AI 요약 생성 중...' },
              { icon: '🎨', text: '카드뉴스 디자인 중...' }
            ].map((step, index) => (
              <div
                key={index}
                className="flex items-center gap-3 bg-white/50 backdrop-blur-sm rounded-lg p-4 animate-pulse"
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                <span className="text-2xl">{step.icon}</span>
                <span className="text-gray-700 font-medium">{step.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function GeneratingPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="mb-8">
            <div className="inline-block relative">
              <div className="w-32 h-32 border-8 border-blue-200 rounded-full"></div>
              <div className="absolute top-0 left-0 w-32 h-32 border-8 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            🎨 카드뉴스 생성 중...
          </h1>
        </div>
      </div>
    }>
      <GeneratingContent />
    </Suspense>
  );
}

