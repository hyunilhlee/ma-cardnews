/**
 * 프로젝트 관련 API 서비스
 */

import api from './api';
import { Project, ProjectCreateRequest, SummarizeResponse } from '../types/project';

export const projectService = {
  /**
   * 새 프로젝트 생성
   */
  create: async (data: ProjectCreateRequest): Promise<Project> => {
    const response = await api.post('/api/projects', data);
    return response.data;
  },

  /**
   * 프로젝트 조회
   */
  get: async (id: string): Promise<Project> => {
    const response = await api.get(`/api/projects/${id}`);
    return response.data;
  },

  /**
   * 프로젝트 요약 생성
   */
  summarize: async (id: string, maxLength: number = 200): Promise<SummarizeResponse> => {
    const response = await api.post(`/api/projects/${id}/summarize`, {
      max_length: maxLength,
    });
    return response.data;
  },

  /**
   * 카드 섹션 자동 생성
   */
  generateSections: async (id: string) => {
    const response = await api.post(`/api/projects/${id}/sections`);
    return response.data;
  },

  /**
   * 섹션 목록 조회
   */
  getSections: async (id: string) => {
    const response = await api.get(`/api/projects/${id}/sections`);
    return response.data.sections;
  },

  /**
   * 프로젝트 상태 업데이트
   */
  updateProjectStatus: async (id: string, status: 'draft' | 'summarized' | 'completed' | 'failed'): Promise<Project> => {
    const response = await api.put(`/api/projects/${id}/status`, { status });
    return response.data;
  },

  /**
   * 프로젝트 목록 조회
   */
  getAll: async (params?: { status?: string; limit?: number; source_type?: string }): Promise<Project[]> => {
    const response = await api.get('/api/projects', { params });
    return response.data;
  },

  /**
   * 프로젝트 삭제
   */
  delete: async (id: string): Promise<void> => {
    await api.delete(`/api/projects/${id}`);
  },
};

