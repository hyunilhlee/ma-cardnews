/**
 * 소개 페이지
 */

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          📰 CardNews AI Generator
        </h1>

        <div className="prose prose-lg max-w-none">
          <p className="text-xl text-gray-700 mb-8">
            AI 기반으로 카드뉴스를 자동으로 생성하는 서비스입니다.
          </p>

          <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4">주요 기능</h2>
          <ul className="space-y-3 text-gray-700">
            <li className="flex items-start">
              <span className="text-2xl mr-3">🔗</span>
              <div>
                <strong>다양한 소스 입력:</strong> URL 링크나 텍스트를 직접 입력하여 카드뉴스 제작
              </div>
            </li>
            <li className="flex items-start">
              <span className="text-2xl mr-3">🤖</span>
              <div>
                <strong>AI 자동 요약:</strong> GPT-4를 활용한 핵심 내용 추출 및 키워드 분석
              </div>
            </li>
            <li className="flex items-start">
              <span className="text-2xl mr-3">🎨</span>
              <div>
                <strong>자동 카드 생성:</strong> 적절한 구조와 디자인으로 카드뉴스 자동 생성
              </div>
            </li>
            <li className="flex items-start">
              <span className="text-2xl mr-3">💬</span>
              <div>
                <strong>자연어 편집:</strong> AI와 대화하며 내용을 쉽게 수정하고 개선
              </div>
            </li>
          </ul>

          <h2 className="text-2xl font-bold text-gray-900 mt-8 mb-4">사용 방법</h2>
          <ol className="space-y-3 text-gray-700 list-decimal list-inside">
            <li>홈페이지에서 URL 링크 또는 텍스트를 입력합니다</li>
            <li>AI가 자동으로 내용을 분석하고 요약합니다</li>
            <li>"카드뉴스 생성하기" 버튼을 눌러 초안을 만듭니다</li>
            <li>AI 채팅을 통해 원하는 대로 내용을 수정합니다</li>
            <li>완성된 카드뉴스를 확인합니다</li>
          </ol>

          <div className="mt-12 p-6 bg-blue-50 rounded-lg">
            <h3 className="text-xl font-bold text-blue-900 mb-2">기술 스택</h3>
            <div className="grid grid-cols-2 gap-4 text-blue-800">
              <div>
                <strong>Frontend:</strong> Next.js, TypeScript, Tailwind CSS
              </div>
              <div>
                <strong>Backend:</strong> FastAPI, Python
              </div>
              <div>
                <strong>AI:</strong> OpenAI GPT-4o-mini
              </div>
              <div>
                <strong>Database:</strong> Firebase Firestore
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

