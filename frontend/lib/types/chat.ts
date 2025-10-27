/**
 * 채팅 관련 TypeScript 타입 정의
 */

import { CardSection } from './section';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatRequest {
  project_id: string;
  user_message: string;
  current_sections: CardSection[];
  conversation_history?: ChatMessage[];
}

export interface ChatResponse {
  ai_response: string;
  updated_sections?: CardSection[];
  action_taken: 'modify' | 'reorder' | 'none';
}

