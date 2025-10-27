/**
 * 채팅 관련 API 서비스
 */

import api from './api';
import { ChatRequest, ChatResponse } from '../types/chat';

export const chatService = {
  /**
   * AI 채팅 메시지 전송
   */
  sendMessage: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post('/api/chat', request);
    return response.data;
  },

  /**
   * 대화 이력 조회
   */
  getHistory: async (projectId: string, limit: number = 10) => {
    const response = await api.get(`/api/chat/${projectId}/history`, {
      params: { limit },
    });
    return response.data.conversations;
  },
};

