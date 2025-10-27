/**
 * Sites API 클라이언트
 */

import { Site, SiteCreate, SiteUpdate, SiteResponse, SiteValidationResponse, TriggerCrawlResponse } from '@/lib/types/site';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

/**
 * 모든 사이트 목록 조회
 */
export async function getSites(): Promise<Site[]> {
  const response = await fetch(`${API_BASE_URL}/api/sites`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch sites: ${response.statusText}`);
  }
  
  const data: SiteResponse[] = await response.json();
  
  return data.map(site => ({
    ...site,
    created_at: new Date(site.created_at),
    updated_at: new Date(site.updated_at),
    last_crawled_at: site.last_crawled_at ? new Date(site.last_crawled_at) : undefined,
    next_crawl_at: site.next_crawl_at ? new Date(site.next_crawl_at) : undefined,
  }));
}

/**
 * 특정 사이트 조회
 */
export async function getSite(siteId: string): Promise<Site> {
  const response = await fetch(`${API_BASE_URL}/api/sites/${siteId}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch site: ${response.statusText}`);
  }
  
  const data: SiteResponse = await response.json();
  
  return {
    ...data,
    created_at: new Date(data.created_at),
    updated_at: new Date(data.updated_at),
    last_crawled_at: data.last_crawled_at ? new Date(data.last_crawled_at) : undefined,
    next_crawl_at: data.next_crawl_at ? new Date(data.next_crawl_at) : undefined,
  };
}

/**
 * 새 사이트 생성
 */
export async function createSite(siteData: SiteCreate): Promise<Site> {
  const response = await fetch(`${API_BASE_URL}/api/sites`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(siteData),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to create site: ${response.statusText}`);
  }
  
  const data: SiteResponse = await response.json();
  
  return {
    ...data,
    created_at: new Date(data.created_at),
    updated_at: new Date(data.updated_at),
    last_crawled_at: data.last_crawled_at ? new Date(data.last_crawled_at) : undefined,
    next_crawl_at: data.next_crawl_at ? new Date(data.next_crawl_at) : undefined,
  };
}

/**
 * 사이트 업데이트
 */
export async function updateSite(siteId: string, siteData: SiteUpdate): Promise<Site> {
  const response = await fetch(`${API_BASE_URL}/api/sites/${siteId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(siteData),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to update site: ${response.statusText}`);
  }
  
  const data: SiteResponse = await response.json();
  
  return {
    ...data,
    created_at: new Date(data.created_at),
    updated_at: new Date(data.updated_at),
    last_crawled_at: data.last_crawled_at ? new Date(data.last_crawled_at) : undefined,
    next_crawl_at: data.next_crawl_at ? new Date(data.next_crawl_at) : undefined,
  };
}

/**
 * 사이트 삭제
 */
export async function deleteSite(siteId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/sites/${siteId}`, {
    method: 'DELETE',
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to delete site: ${response.statusText}`);
  }
}

/**
 * RSS URL 유효성 검증
 */
export async function validateRssUrl(rssUrl: string): Promise<SiteValidationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/sites/validate-rss`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ rss_url: rssUrl }),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to validate RSS URL: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * 수동 크롤링 트리거
 */
export async function triggerCrawl(siteId: string): Promise<TriggerCrawlResponse> {
  const response = await fetch(`${API_BASE_URL}/api/sites/${siteId}/trigger-crawl`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to trigger crawl: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * 특정 사이트의 크롤링 로그 조회
 */
export async function getCrawlLogs(siteId: string, limit: number = 20): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/sites/${siteId}/crawl-logs?limit=${limit}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch crawl logs: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * 모든 크롤링 로그 조회
 */
export async function getAllCrawlLogs(limit: number = 50): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/sites/crawl-logs/all?limit=${limit}`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch all crawl logs: ${response.statusText}`);
  }
  
  return response.json();
}
