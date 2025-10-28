/**
 * 메인 대시보드 (Phase 2)
 */
'use client';

import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            카드뉴스 AI 생성기
          </h1>
          <p className="text-xl text-gray-600">
            RSS 자동 생성 또는 수동으로 카드뉴스를 만드세요
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          {/* RSS 사이트 설정 */}
          <div 
            onClick={() => router.push('/sites')}
            className="bg-white rounded-2xl shadow-xl p-8 cursor-pointer hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
          >
            <div className="text-center">
              <div className="text-6xl mb-4">📡</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">RSS 사이트 설정</h2>
              <p className="text-gray-600">
                자동 크롤링할 사이트를 관리하세요
              </p>
            </div>
          </div>

          {/* 수동 생성 */}
          <div 
            onClick={() => router.push('/source')}
            className="bg-white rounded-2xl shadow-xl p-8 cursor-pointer hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
          >
            <div className="text-center">
              <div className="text-6xl mb-4">✏️</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">수동 생성</h2>
              <p className="text-gray-600">
                링크나 텍스트로 직접 만들기
              </p>
            </div>
          </div>

          {/* 저장된 프로젝트 */}
          <div 
            onClick={() => router.push('/projects')}
            className="bg-white rounded-2xl shadow-xl p-8 cursor-pointer hover:shadow-2xl transform hover:scale-105 transition-all duration-200"
          >
            <div className="text-center">
              <div className="text-6xl mb-4">📚</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">저장된 프로젝트</h2>
              <p className="text-gray-600">
                생성된 카드뉴스 보기
              </p>
            </div>
          </div>

          {/* RSS Library - 신규! */}
          <div 
            onClick={() => router.push('/library')}
            className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl shadow-xl p-8 cursor-pointer hover:shadow-2xl transform hover:scale-105 transition-all duration-200 relative"
          >
            <div className="absolute top-2 right-2">
              <span className="inline-block px-3 py-1 text-xs font-bold text-white bg-red-500 rounded-full">
                NEW
              </span>
            </div>
            <div className="text-center">
              <div className="text-6xl mb-4">📰</div>
              <h2 className="text-2xl font-bold text-white mb-2">RSS Library</h2>
              <p className="text-blue-100">
                모든 RSS 피드를 한눈에
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">🤖 Phase 2: RSS 자동 생성</h3>
          <div className="space-y-3 text-sm text-gray-600">
            <div className="flex items-start">
              <span className="text-xl mr-3">1️⃣</span>
              <p>RSS 사이트를 등록하고 활성화하면 자동으로 새 게시물을 감지합니다</p>
            </div>
            <div className="flex items-start">
              <span className="text-xl mr-3">2️⃣</span>
              <p>30분마다 자동으로 크롤링하여 카드뉴스를 생성합니다</p>
            </div>
            <div className="flex items-start">
              <span className="text-xl mr-3">3️⃣</span>
              <p>저장된 프로젝트에서 확인하고 수정할 수 있습니다</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
