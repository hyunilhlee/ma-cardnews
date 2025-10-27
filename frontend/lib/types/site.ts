/**
 * RSS 사이트 타입 정의
 */

export type SiteStatus = 'active' | 'inactive' | 'error';

export interface Site {
  id: string;
  name: string;
  url: string;
  rss_url: string;
  crawl_interval: number; // 분 단위
  status: SiteStatus;
  last_crawled_at?: Date;
  next_crawl_at?: Date;
  total_crawls: number;
  success_count: number;
  error_count: number;
  total_posts_found: number;
  total_new_posts: number;
  total_projects_created: number;
  last_error?: string;
  created_at: Date;
  updated_at: Date;
}

export interface SiteCreate {
  name: string;
  url: string;
  rss_url: string;
  crawl_interval: number;
  status: SiteStatus;
}

export interface SiteUpdate {
  name?: string;
  url?: string;
  rss_url?: string;
  crawl_interval?: number;
  status?: SiteStatus;
}

export interface SiteResponse {
  id: string;
  name: string;
  url: string;
  rss_url: string;
  crawl_interval: number;
  status: SiteStatus;
  last_crawled_at?: string;
  next_crawl_at?: string;
  total_crawls: number;
  success_count: number;
  error_count: number;
  total_posts_found: number;
  total_new_posts: number;
  total_projects_created: number;
  last_error?: string;
  created_at: string;
  updated_at: string;
}

export interface SiteValidationResponse {
  is_valid: boolean;
  title?: string;
  description?: string;
  link?: string;
  entry_count?: number;
  message?: string;
}

export interface TriggerCrawlResponse {
  message: string;
  site_id: string;
}

