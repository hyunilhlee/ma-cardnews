'use client';

import { useState, useEffect } from 'react';
import { getSites, deleteSite, triggerCrawl, createSite, validateRssUrl, getCrawlLogs } from '@/lib/api/sites';
import { Site } from '@/lib/types/site';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import Link from 'next/link';

export default function SitesPage() {
  const [sites, setSites] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // 등록 모달 상태
  const [showAddModal, setShowAddModal] = useState(false);
  const [newSite, setNewSite] = useState({
    name: '',
    url: '',
    rss_url: '',
    crawl_interval: 60,
    status: 'active' as 'active' | 'inactive'
  });
  const [isValidating, setIsValidating] = useState(false);
  const [validationResult, setValidationResult] = useState<{ valid: boolean; message?: string } | null>(null);

  // 크롤링 로그 모달 상태
  const [showLogsModal, setShowLogsModal] = useState(false);
  const [selectedSite, setSelectedSite] = useState<Site | null>(null);
  const [crawlLogs, setCrawlLogs] = useState<any[]>([]);
  const [logsLoading, setLogsLoading] = useState(false);

  const fetchSites = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getSites();
      setSites(data);
    } catch (error: any) {
      setError(error.message || '사이트 목록을 불러오는 데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSites();
  }, []);

  const handleDelete = async (siteId: string, siteName: string) => {
    if (!confirm(`정말로 "${siteName}" 사이트를 삭제하시겠습니까?`)) return;
    try {
      await deleteSite(siteId);
      alert(`${siteName}이(가) 삭제되었습니다.`);
      fetchSites();
    } catch (error: any) {
      alert('삭제 실패: ' + error.message);
    }
  };

  const handleTriggerCrawl = async (siteId: string, siteName: string) => {
    try {
      await triggerCrawl(siteId);
      alert(`${siteName} 크롤링이 시작되었습니다.`);
      setTimeout(fetchSites, 5000);
    } catch (error: any) {
      alert('크롤링 실패: ' + error.message);
    }
  };

  // 크롤링 로그 조회
  const handleViewLogs = async (site: Site) => {
    setSelectedSite(site);
    setShowLogsModal(true);
    setLogsLoading(true);
    setCrawlLogs([]);
    
    try {
      const response = await getCrawlLogs(site.id, 20);
      setCrawlLogs(response.logs || []);
    } catch (error: any) {
      console.error('Failed to fetch logs:', error);
      alert('로그 조회 실패: ' + error.message);
    } finally {
      setLogsLoading(false);
    }
  };

  // RSS URL 검증
  const handleValidateRss = async () => {
    if (!newSite.rss_url) {
      alert('RSS URL을 입력해주세요.');
      return;
    }
    
    setIsValidating(true);
    setValidationResult(null);
    
    try {
      const result = await validateRssUrl(newSite.rss_url);
      
      if (result.is_valid) {
        setValidationResult({ 
          valid: true, 
          message: `유효한 RSS 피드입니다. (${result.entry_count}개 게시물)` 
        });
        
        // 자동으로 name과 url 채우기
        if (!newSite.name && result.title) {
          setNewSite(prev => ({ ...prev, name: result.title }));
        }
        if (!newSite.url && result.link) {
          setNewSite(prev => ({ ...prev, url: result.link }));
        }
      } else {
        setValidationResult({ 
          valid: false, 
          message: result.message || '유효하지 않은 RSS 피드입니다.' 
        });
      }
    } catch (error: any) {
      setValidationResult({ 
        valid: false, 
        message: error.message || 'RSS 검증 중 오류가 발생했습니다.' 
      });
    } finally {
      setIsValidating(false);
    }
  };

  // 새 사이트 등록
  const handleAddSite = async () => {
    if (!newSite.name || !newSite.url || !newSite.rss_url) {
      alert('모든 필수 항목을 입력해주세요.');
      return;
    }

    try {
      await createSite(newSite);
      alert(`${newSite.name} 사이트가 등록되었습니다.`);
      setShowAddModal(false);
      setNewSite({
        name: '',
        url: '',
        rss_url: '',
        crawl_interval: 60,
        status: 'active'
      });
      setValidationResult(null);
      fetchSites();
    } catch (error: any) {
      alert('등록 실패: ' + error.message);
    }
  };

  const formatDateTime = (date?: Date) => {
    if (!date) return 'N/A';
    return date.toLocaleString('ko-KR', {
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  // 통계 계산
  const stats = {
    total: sites.length,
    active: sites.filter(s => s.status === 'active').length,
    inactive: sites.filter(s => s.status === 'inactive').length,
    totalCrawls: sites.reduce((sum, s) => sum + (s.total_crawls || 0), 0),
    totalProjects: sites.reduce((sum, s) => sum + (s.total_projects_created || 0), 0),
    totalPosts: sites.reduce((sum, s) => sum + (s.total_new_posts || 0), 0),
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">RSS 사이트 관리</h1>
              <p className="text-gray-600 mt-1">자동 크롤링할 RSS 사이트를 관리합니다</p>
            </div>
            <div className="flex gap-2">
              <Link
                href="/"
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
              >
                ← 홈으로
              </Link>
              <button
                onClick={() => setShowAddModal(true)}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
              >
                ➕ 새 사이트 등록
              </button>
              <button
                onClick={fetchSites}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                🔄 새로고침
              </button>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-6">
          {/* 총 사이트 */}
          <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-4 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-medium text-gray-600">총 사이트</div>
              <span className="text-xl">📡</span>
            </div>
            <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
            <div className="text-xs text-gray-500 mt-1">등록된 RSS 사이트</div>
          </div>

          {/* 활성 사이트 */}
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-xl shadow-sm border border-green-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-medium text-green-700">활성</div>
              <span className="text-xl">✅</span>
            </div>
            <div className="text-2xl font-bold text-green-800">{stats.active}</div>
            <div className="text-xs text-green-600 mt-1">크롤링 중인 사이트</div>
          </div>

          {/* 총 크롤링 횟수 */}
          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-xl shadow-sm border border-blue-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-medium text-blue-700">총 크롤링</div>
              <span className="text-xl">🔄</span>
            </div>
            <div className="text-2xl font-bold text-blue-800">{stats.totalCrawls}</div>
            <div className="text-xs text-blue-600 mt-1">전체 크롤링 횟수</div>
          </div>

          {/* 발견된 게시물 */}
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-4 rounded-xl shadow-sm border border-yellow-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-medium text-yellow-700">새 글 발견</div>
              <span className="text-xl">📄</span>
            </div>
            <div className="text-2xl font-bold text-yellow-800">{stats.totalPosts}</div>
            <div className="text-xs text-yellow-600 mt-1">누적 새로 발견된 글</div>
          </div>

          {/* 생성된 카드뉴스 */}
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-xl shadow-sm border border-purple-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-medium text-purple-700">카드뉴스</div>
              <span className="text-xl">✨</span>
            </div>
            <div className="text-2xl font-bold text-purple-800">{stats.totalProjects}</div>
            <div className="text-xs text-purple-600 mt-1">누적 자동 생성</div>
          </div>

          {/* 변환율 */}
          <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 p-4 rounded-xl shadow-sm border border-indigo-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-medium text-indigo-700">변환율</div>
              <span className="text-xl">📊</span>
            </div>
            <div className="text-2xl font-bold text-indigo-800">
              {stats.totalPosts > 0 ? Math.round((stats.totalProjects / stats.totalPosts) * 100) : 0}%
            </div>
            <div className="text-xs text-indigo-600 mt-1">게시물 → 카드뉴스</div>
          </div>
        </div>

        {/* Sites List */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  사이트
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  주기
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  상태
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  마지막 크롤링
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  통계
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  작업
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {sites.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    등록된 사이트가 없습니다.
                  </td>
                </tr>
              ) : (
                sites.map((site) => (
                  <tr key={site.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4">
                      <div>
                        <div className="font-medium text-gray-900">{site.name}</div>
                        <a
                          href={site.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-600 hover:underline"
                        >
                          {site.url}
                        </a>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{site.crawl_interval}분</td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          site.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : site.status === 'inactive'
                            ? 'bg-gray-100 text-gray-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {site.status === 'active' ? '활성' : site.status === 'inactive' ? '비활성' : '오류'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm text-gray-900">{formatDateTime(site.last_crawled_at)}</div>
                      {site.next_crawl_at && (
                        <div className="text-xs text-gray-500">다음: {formatDateTime(site.next_crawl_at)}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500">크롤링 횟수:</span>
                          <span className="font-semibold text-blue-600">{site.total_crawls || 0}회</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500">새 글 발견:</span>
                          <span className="font-semibold text-yellow-600">{site.total_new_posts || 0}개</span>
                          <span className="text-xs text-gray-400">(누적)</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-gray-500">카드뉴스:</span>
                          <span className="font-semibold text-purple-600">{site.total_projects_created || 0}개</span>
                          <span className="text-xs text-gray-400">(누적)</span>
                        </div>
                        {site.total_new_posts && site.total_new_posts > 0 && (
                          <div className="flex items-center gap-2">
                            <span className="text-xs text-gray-500">변환율:</span>
                            <span className="font-semibold text-indigo-600">
                              {Math.round(((site.total_projects_created || 0) / site.total_new_posts) * 100)}%
                            </span>
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right text-sm font-medium">
                      <button
                        onClick={() => handleViewLogs(site)}
                        className="text-green-600 hover:text-green-900 mr-3"
                        title="크롤링 로그 보기"
                      >
                        📋
                      </button>
                      <button
                        onClick={() => handleTriggerCrawl(site.id, site.name)}
                        className="text-blue-600 hover:text-blue-900 mr-3"
                        title="수동 크롤링"
                      >
                        🔄
                      </button>
                      <button
                        onClick={() => handleDelete(site.id, site.name)}
                        className="text-red-600 hover:text-red-900"
                        title="삭제"
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* 등록 모달 */}
        {showAddModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-900">새 RSS 사이트 등록</h2>
                <button
                  onClick={() => {
                    setShowAddModal(false);
                    setNewSite({ name: '', url: '', rss_url: '', crawl_interval: 60, status: 'active' });
                    setValidationResult(null);
                  }}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-4">
                {/* RSS URL */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    RSS Feed URL * <span className="text-xs text-gray-500">(먼저 검증해주세요)</span>
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="url"
                      value={newSite.rss_url}
                      onChange={(e) => setNewSite({ ...newSite, rss_url: e.target.value })}
                      placeholder="https://example.com/feed/"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                    <button
                      onClick={handleValidateRss}
                      disabled={isValidating || !newSite.rss_url}
                      className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                    >
                      {isValidating ? '검증 중...' : '✓ 검증'}
                    </button>
                  </div>
                  {validationResult && (
                    <div className={`mt-2 text-sm ${validationResult.valid ? 'text-green-600' : 'text-red-600'}`}>
                      {validationResult.valid ? '✓' : '✗'} {validationResult.message}
                    </div>
                  )}
                </div>

                {/* 사이트 이름 */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    사이트 이름 *
                  </label>
                  <input
                    type="text"
                    value={newSite.name}
                    onChange={(e) => setNewSite({ ...newSite, name: e.target.value })}
                    placeholder="예: TechCrunch"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                {/* 사이트 URL */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    사이트 URL *
                  </label>
                  <input
                    type="url"
                    value={newSite.url}
                    onChange={(e) => setNewSite({ ...newSite, url: e.target.value })}
                    placeholder="https://example.com"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>

                {/* 크롤링 주기 */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    크롤링 주기 (분)
                  </label>
                  <select
                    value={newSite.crawl_interval}
                    onChange={(e) => setNewSite({ ...newSite, crawl_interval: parseInt(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value={15}>15분</option>
                    <option value={30}>30분</option>
                    <option value={60}>1시간</option>
                    <option value={180}>3시간</option>
                    <option value={360}>6시간</option>
                    <option value={720}>12시간</option>
                    <option value={1440}>24시간</option>
                  </select>
                </div>

                {/* 상태 */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    초기 상태
                  </label>
                  <select
                    value={newSite.status}
                    onChange={(e) => setNewSite({ ...newSite, status: e.target.value as 'active' | 'inactive' })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="active">활성</option>
                    <option value="inactive">비활성</option>
                  </select>
                </div>
              </div>

              {/* 버튼 */}
              <div className="flex justify-end gap-3 mt-6">
                <button
                  onClick={() => {
                    setShowAddModal(false);
                    setNewSite({ name: '', url: '', rss_url: '', crawl_interval: 60, status: 'active' });
                    setValidationResult(null);
                  }}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                >
                  취소
                </button>
                <button
                  onClick={handleAddSite}
                  disabled={!validationResult?.valid}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
                >
                  등록
                </button>
              </div>
            </div>
          </div>
        )}

        {/* 크롤링 로그 모달 */}
        {showLogsModal && selectedSite && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">크롤링 로그</h2>
                  <p className="text-sm text-gray-600 mt-1">{selectedSite.name}</p>
                </div>
                <button
                  onClick={() => {
                    setShowLogsModal(false);
                    setSelectedSite(null);
                    setCrawlLogs([]);
                  }}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ✕
                </button>
              </div>

              {logsLoading ? (
                <div className="flex justify-center py-12">
                  <LoadingSpinner />
                </div>
              ) : crawlLogs.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  크롤링 로그가 없습니다.
                </div>
              ) : (
                <div className="space-y-4">
                  {crawlLogs.map((log, index) => (
                    <div
                      key={log.id || index}
                      className={`border rounded-lg p-4 ${
                        log.status === 'success' ? 'border-green-200 bg-green-50' :
                        log.status === 'failed' ? 'border-red-200 bg-red-50' :
                        'border-gray-200 bg-gray-50'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-3">
                        <div className="flex items-center gap-3">
                          <span
                            className={`px-3 py-1 rounded-full text-xs font-semibold ${
                              log.status === 'success' ? 'bg-green-100 text-green-800' :
                              log.status === 'failed' ? 'bg-red-100 text-red-800' :
                              'bg-yellow-100 text-yellow-800'
                            }`}
                          >
                            {log.status === 'success' ? '✓ 성공' :
                             log.status === 'failed' ? '✗ 실패' :
                             '⏳ 진행 중'}
                          </span>
                          <span className="text-sm text-gray-600">
                            {new Date(log.started_at).toLocaleString('ko-KR')}
                          </span>
                        </div>
                        {log.duration_seconds !== undefined && (
                          <span className="text-xs text-gray-500">
                            {log.duration_seconds.toFixed(2)}초
                          </span>
                        )}
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                        <div>
                          <div className="text-xs text-gray-500">RSS 글 수</div>
                          <div className="text-xs text-gray-400 mb-1">(RSS 피드 전체)</div>
                          <div className="text-lg font-bold text-gray-600">{log.posts_found || 0}개</div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-500">새 글 발견</div>
                          <div className="text-xs text-gray-400 mb-1">(이번 크롤링)</div>
                          <div className="text-lg font-bold text-yellow-600">{log.new_posts || 0}개</div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-500">카드뉴스 생성</div>
                          <div className="text-xs text-gray-400 mb-1">(이번 크롤링)</div>
                          <div className="text-lg font-bold text-purple-600">{log.projects_created || 0}개</div>
                        </div>
                        <div>
                          <div className="text-xs text-gray-500">변환율</div>
                          <div className="text-xs text-gray-400 mb-1">(새 글→카드뉴스)</div>
                          <div className="text-lg font-bold text-indigo-600">
                            {log.new_posts > 0 ? Math.round((log.projects_created / log.new_posts) * 100) : 0}%
                          </div>
                        </div>
                      </div>

                      {log.post_titles && log.post_titles.length > 0 && (
                        <div className="mt-3">
                          <div className="text-xs font-semibold text-gray-700 mb-2">발견된 게시물:</div>
                          <ul className="space-y-1">
                            {log.post_titles.map((title: string, idx: number) => (
                              <li key={idx} className="text-sm text-gray-600 flex items-start gap-2">
                                <span className="text-green-600">•</span>
                                <span className="flex-1">{title}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {log.error_message && (
                        <div className="mt-3 p-3 bg-red-100 border border-red-200 rounded text-sm text-red-700">
                          <strong>에러:</strong> {log.error_message}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-6 flex justify-end">
                <button
                  onClick={() => {
                    setShowLogsModal(false);
                    setSelectedSite(null);
                    setCrawlLogs([]);
                  }}
                  className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700"
                >
                  닫기
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
