/**
 * RSS Library API 클라이언트
 */

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface FeedSource {
  site_id?: string | null;
  site_name: string;
  site_url: string;
}

export interface LibraryFeedItem {
  id: string;
  type: 'project' | 'rss_post';
  title: string;
  source: FeedSource;
  keywords: string[];
  summary: string;
  published_at: string | null;
  url: string;
  has_cardnews: boolean;
  project_id: string | null;
  status: 'draft' | 'summarized' | 'completed' | null;
  is_new: boolean;
}

export interface LibraryFeedResponse {
  total: number;
  page: number;
  page_size: number;
  items: LibraryFeedItem[];
}

export interface CreateCardnewsRequest {
  rss_post_id: string;
  site_id: string;
  url: string;
  title: string;
  content: string;
}

export interface CreateCardnewsResponse {
  project_id: string;
  status: 'draft' | 'summarized' | 'completed';
}

/**
 * RSS Library 통합 피드 조회
 */
export async function getLibraryFeed(params: {
  site_id?: string;
  start_date?: string;
  end_date?: string;
  keyword?: string;
  year_month?: string;
  page?: number;
  page_size?: number;
}): Promise<LibraryFeedResponse> {
  const queryParams = new URLSearchParams();
  
  if (params.site_id) queryParams.append('site_id', params.site_id);
  if (params.start_date) queryParams.append('start_date', params.start_date);
  if (params.end_date) queryParams.append('end_date', params.end_date);
  if (params.keyword) queryParams.append('keyword', params.keyword);
  if (params.year_month) queryParams.append('year_month', params.year_month);
  if (params.page) queryParams.append('page', params.page.toString());
  if (params.page_size) queryParams.append('page_size', params.page_size.toString());
  
  const response = await axios.get<LibraryFeedResponse>(
    `${API_URL}/api/library/feed?${queryParams.toString()}`
  );
  
  return response.data;
}

/**
 * RSS 게시물에서 카드뉴스 생성
 */
export async function createCardnewsFromFeed(
  request: CreateCardnewsRequest
): Promise<CreateCardnewsResponse> {
  const response = await axios.post<CreateCardnewsResponse>(
    `${API_URL}/api/library/create-cardnews`,
    request
  );
  
  return response.data;
}

