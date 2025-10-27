/**
 * 프로젝트 관련 TypeScript 타입 정의
 */

export type SourceType = 'url' | 'text';
export type ProjectStatus = 'draft' | 'summarized' | 'completed';

export interface Project {
  id: string;
  source_type: SourceType;
  source_content: string;
  summary?: string;
  keywords?: string[];
  recommended_card_count?: number;
  created_at: string;
  updated_at: string;
  status: ProjectStatus;
  model?: string;
  card_start_type?: 'title' | 'content';
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

