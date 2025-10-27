/**
 * Projects API 클라이언트
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export interface ProjectListItem {
  id: string;
  source_type: 'url' | 'text' | 'rss';
  summary?: string;
  keywords?: string[];
  status: 'draft' | 'summarized' | 'completed' | 'published' | 'archived';
  model: string;
  source_site_id?: string;
  source_site_name?: string;
  is_auto_generated: boolean;
  created_at: Date;
  updated_at: Date;
}

export interface ProjectListResponse {
  id: string;
  source_type: string;
  summary?: string;
  keywords?: string[];
  status: string;
  model: string;
  source_site_id?: string;
  source_site_name?: string;
  is_auto_generated: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * 프로젝트 목록 조회
 */
export async function getProjects(
  status?: string,
  sourceType?: string,
  limit?: number
): Promise<ProjectListItem[]> {
  const params = new URLSearchParams();
  
  if (status) params.append('status', status);
  if (sourceType) params.append('source_type', sourceType);
  if (limit) params.append('limit', limit.toString());
  
  const url = `${API_BASE_URL}/api/projects${params.toString() ? `?${params.toString()}` : ''}`;
  
  const response = await fetch(url);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch projects: ${response.statusText}`);
  }
  
  const data: ProjectListResponse[] = await response.json();
  
  return data.map(project => ({
    ...project,
    source_type: project.source_type as 'url' | 'text' | 'rss',
    status: project.status as 'draft' | 'summarized' | 'completed' | 'published' | 'archived',
    created_at: new Date(project.created_at),
    updated_at: new Date(project.updated_at),
  }));
}

/**
 * 프로젝트 삭제
 */
export async function deleteProject(projectId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/projects/${projectId}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to delete project: ${response.statusText}`);
  }
}

/**
 * 프로젝트 상태 업데이트
 */
export async function updateProjectStatus(
  projectId: string,
  status: 'draft' | 'summarized' | 'completed' | 'published' | 'archived'
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/projects/${projectId}/status`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to update project status: ${response.statusText}`);
  }
}

