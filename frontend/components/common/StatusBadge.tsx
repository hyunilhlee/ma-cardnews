/**
 * GPT 상태 표시 뱃지 컴포넌트
 */

'use client';

import React, { useEffect, useState } from 'react';
import api from '@/lib/services/api';

interface ApiStatus {
  connected: boolean;
  model: string;
  status: string;
  message: string;
}

export const StatusBadge: React.FC = () => {
  const [status, setStatus] = useState<ApiStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkStatus();
    // 30초마다 상태 확인
    const interval = setInterval(checkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkStatus = async () => {
    try {
      const response = await api.get('/api/status/openai');
      setStatus(response.data.api_status);
    } catch (error) {
      setStatus({
        connected: false,
        model: 'Unknown',
        status: '오프라인',
        message: 'API 연결 실패'
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center space-x-2 px-3 py-1.5 bg-gray-100 rounded-full text-xs">
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
        <span className="text-gray-600">확인 중...</span>
      </div>
    );
  }

  if (!status) return null;

  return (
    <div className="flex items-center space-x-3">
      {/* 연결 상태 뱃지 */}
      <div
        className={`flex items-center space-x-2 px-3 py-1.5 rounded-full text-xs font-medium ${
          status.connected
            ? 'bg-green-50 text-green-700 border border-green-200'
            : 'bg-red-50 text-red-700 border border-red-200'
        }`}
      >
        <div
          className={`w-2 h-2 rounded-full ${
            status.connected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
          }`}
        ></div>
        <span>
          {status.connected ? '🤖 AI 연결됨' : '❌ AI 연결 안됨'}
        </span>
      </div>

      {/* 크레딧 안내 */}
      {status.connected && (
        <a
          href="https://platform.openai.com/usage"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center space-x-1 px-3 py-1.5 bg-purple-50 text-purple-700 rounded-full text-xs font-medium border border-purple-200 hover:bg-purple-100 transition-colors"
        >
          <span>💳</span>
          <span>크레딧 확인</span>
          <span>↗</span>
        </a>
      )}
    </div>
  );
};

