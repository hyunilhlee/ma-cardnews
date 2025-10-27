'use client';

import { useState, useEffect } from 'react';
import { getProjects, deleteProject } from '@/lib/api/projects';
import { ProjectListItem } from '@/lib/api/projects';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import Link from 'next/link';

export default function ProjectsPage() {
  const [projects, setProjects] = useState<ProjectListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterSourceType, setFilterSourceType] = useState<string>('all');

  const fetchProjects = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getProjects(
        filterStatus === 'all' ? undefined : filterStatus,
        filterSourceType === 'all' ? undefined : filterSourceType
      );
      setProjects(data);
    } catch (error: any) {
      setError(error.message || '프로젝트 목록을 불러오는 데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
  }, [filterStatus, filterSourceType]);

  const handleDelete = async (projectId: string) => {
    if (!confirm('정말로 이 프로젝트를 삭제하시겠습니까?')) return;
    try {
      await deleteProject(projectId);
      alert('프로젝트가 삭제되었습니다.');
      fetchProjects();
    } catch (error: any) {
      alert('삭제 실패: ' + error.message);
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

  const stats = {
    total: projects.length,
    rssGenerated: projects.filter(p => p.is_auto_generated && p.source_type === 'rss').length,
    draft: projects.filter(p => p.status === 'draft' || p.status === 'summarized').length,
    completed: projects.filter(p => p.status === 'completed').length,
    manual: projects.filter(p => !p.is_auto_generated).length,
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">생성된 카드뉴스 프로젝트</h1>
              <p className="text-gray-600 mt-1">AI가 자동 생성하거나 수동으로 생성한 모든 프로젝트</p>
            </div>
            <div className="flex gap-2">
              <Link
                href="/"
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
              >
                ← 홈으로
              </Link>
              <button
                onClick={fetchProjects}
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
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {/* 총 프로젝트 */}
          <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-5 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-sm font-medium text-gray-600">총 프로젝트</div>
              <span className="text-2xl">📊</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{stats.total}</div>
            <div className="text-xs text-gray-500 mt-1">전체 생성된 카드뉴스</div>
          </div>

          {/* RSS 자동생성 */}
          <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-5 rounded-xl shadow-sm border border-purple-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-sm font-medium text-purple-700">RSS 자동생성</div>
              <span className="text-2xl">✨</span>
            </div>
            <div className="text-3xl font-bold text-purple-800">{stats.rssGenerated}</div>
            <div className="text-xs text-purple-600 mt-1">AI가 RSS에서 자동 생성</div>
          </div>

          {/* 작업 중 (초안) */}
          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-5 rounded-xl shadow-sm border border-yellow-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-sm font-medium text-yellow-700">작업 중</div>
              <span className="text-2xl">📝</span>
            </div>
            <div className="text-3xl font-bold text-yellow-800">{stats.draft}</div>
            <div className="text-xs text-yellow-600 mt-1">편집 중인 프로젝트</div>
          </div>

          {/* 저장 완료 */}
          <div className="bg-gradient-to-br from-green-50 to-green-100 p-5 rounded-xl shadow-sm border border-green-200 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <div className="text-sm font-medium text-green-700">저장 완료</div>
              <span className="text-2xl">✅</span>
            </div>
            <div className="text-3xl font-bold text-green-800">{stats.completed}</div>
            <div className="text-xs text-green-600 mt-1">편집 완료된 카드뉴스</div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
          <div className="flex gap-4">
            <div>
              <label className="text-sm font-medium text-gray-700 mr-2">상태:</label>
              <select
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">모든 상태</option>
                <option value="draft">초안</option>
                <option value="summarized">요약됨</option>
                <option value="completed">완료</option>
                <option value="published">발행됨</option>
                <option value="archived">보관됨</option>
              </select>
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 mr-2">소스 유형:</label>
              <select
                value={filterSourceType}
                onChange={(e) => setFilterSourceType(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">모든 유형</option>
                <option value="url">URL</option>
                <option value="text">텍스트</option>
                <option value="rss">RSS 자동</option>
              </select>
            </div>
          </div>
        </div>

        {/* Projects List */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  요약
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  키워드
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  소스
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  상태
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  생성일
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  삭제
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {projects.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-gray-500">
                    생성된 프로젝트가 없습니다.
                  </td>
                </tr>
              ) : (
                projects.map((project) => (
                  <tr 
                    key={project.id} 
                    onClick={() => window.location.href = `/edit/${project.id}`}
                    className="hover:bg-blue-50 cursor-pointer transition-colors"
                  >
                    <td className="px-6 py-4">
                      <div className="max-w-md text-sm text-gray-900 line-clamp-2">
                        {project.summary || '요약 없음'}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-wrap gap-1">
                        {project.keywords && project.keywords.length > 0 ? (
                          project.keywords.slice(0, 3).map((keyword, idx) => (
                            <span
                              key={idx}
                              className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full"
                            >
                              {keyword}
                            </span>
                          ))
                        ) : (
                          <span className="text-xs text-gray-400">없음</span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      {project.is_auto_generated ? (
                        <div className="flex items-center gap-1">
                          <span className="text-purple-600">✨</span>
                          <span className="text-xs text-purple-700 font-medium">AI 자동</span>
                          {project.source_site_name && (
                            <span className="text-xs text-gray-500">({project.source_site_name})</span>
                          )}
                        </div>
                      ) : (
                        <span className="text-sm text-gray-600">
                          {project.source_type === 'url' ? 'URL' : project.source_type === 'text' ? '텍스트' : 'RSS'}
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4" onClick={(e) => e.stopPropagation()}>
                      <span
                        className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          project.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : project.status === 'published'
                            ? 'bg-blue-100 text-blue-800'
                            : project.status === 'draft'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {project.status === 'draft' ? '📝 초안' : 
                         project.status === 'completed' ? '✅ 저장됨' : 
                         project.status === 'published' ? '🚀 발행됨' : 
                         project.status === 'archived' ? '📦 보관됨' : project.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">{formatDateTime(project.created_at)}</td>
                    <td className="px-6 py-4 text-right text-sm font-medium">
                      <button
                        onClick={(e) => {
                          e.stopPropagation(); // 행 클릭 이벤트 방지
                          handleDelete(project.id);
                        }}
                        className="text-red-600 hover:text-red-900 transition-colors"
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
      </div>
    </div>
  );
}
