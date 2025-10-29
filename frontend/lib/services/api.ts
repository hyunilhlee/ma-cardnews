/**
 * Axios 기본 설정 및 API 클라이언트
 */

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// 디버깅: 환경 변수 확인
if (typeof window !== 'undefined') {
  console.log('🔧 NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL);
  console.log('🌐 API_URL:', API_URL);
}

// Axios 인스턴스 생성
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30초
});

// 요청 인터셉터
api.interceptors.request.use(
  (config) => {
    // 요청 전 처리 (예: 인증 토큰 추가)
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 에러 처리
    if (error.response) {
      // 서버가 응답했지만 에러 상태 코드
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // 요청은 보냈지만 응답을 받지 못함
      console.error('Network Error:', error.message);
    } else {
      // 요청 설정 중 에러
      console.error('Request Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;

