/**
 * 프로젝트 관련 TypeScript 타입 정의
 */

export type SourceType = 'url' | 'text' | 'rss';
export type ProjectStatus = 'draft' | 'summarized' | 'completed';

export interface Project {
  id: string;
  source_type: SourceType;
  source_content?: string; // RSS 프로젝트는 null일 수 있음
  source_url?: string; // RSS 프로젝트의 원본 URL
  summary?: string;
  keywords?: string[];
  recommended_card_count?: number;
  created_at: string;
  updated_at: string;
  status: ProjectStatus;
  model?: string;
  card_start_type?: 'title' | 'content';
  site_id?: string; // RSS 사이트 ID
  site_name?: string; // RSS 사이트 이름
  last_error?: string; // 에러 메시지
  version?: number; // 버전 관리
}

export interface ProjectCreateRequest {
  source_type: SourceType;
  source_content: string;
  card_start_type?: 'title' | 'content';
  model?: string;
}

export interface SummarizeResponse {
  summary: string;
  keywords: string[];
  recommended_card_count: number;
}

