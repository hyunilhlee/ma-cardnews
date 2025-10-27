/**
 * AI 채팅 인터페이스 컴포넌트
 */

'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage } from '@/lib/types/chat';
import { Button } from '../common/Button';

interface ChatInterfaceProps {
  messages: ChatMessage[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  onSendMessage,
  isLoading = false,
}) => {
  const [input, setInput] = useState('');
  const [isExpanded, setIsExpanded] = useState(true); // 모바일에서 확장/축소 상태
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 새 메시지가 추가되면 스크롤을 아래로
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    onSendMessage(input);
    setInput('');
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      {/* 채팅 헤더 */}
      <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-gray-900">💬 AI와 대화하기</h2>
          <p className="text-sm text-gray-600 hidden md:block">내용 수정, 순서 변경 등을 자연어로 요청하세요</p>
        </div>
        {/* 모바일 전용 숨기기/보이기 버튼 */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="md:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
          aria-label={isExpanded ? '채팅 숨기기' : '채팅 보이기'}
        >
          {isExpanded ? '▼' : '▲'}
        </button>
      </div>

      {/* 메시지 목록 */}
      <div className={`flex-1 overflow-y-auto p-6 space-y-4 ${isExpanded ? 'block' : 'hidden md:block'}`}>
        {messages.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500 mb-4">AI에게 무엇을 도와드릴까요?</p>
            <div className="space-y-2 text-sm text-gray-400">
              <p>예: "첫 번째 카드의 제목을 더 강렬하게 바꿔줘"</p>
              <p>예: "두 번째와 세 번째 카드의 순서를 바꿔줘"</p>
              <p>예: "마지막 카드에 행동 유도 문구를 추가해줘"</p>
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[70%] rounded-lg px-4 py-3 ${
                    message.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">
                    {message.content}
                  </p>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </>
        )}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-lg px-4 py-3">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 입력 영역 */}
      <div className={`px-6 py-4 border-t border-gray-200 ${isExpanded ? 'block' : 'hidden md:block'}`}>
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="메시지를 입력하세요..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
            disabled={isLoading}
          />
          <Button
            type="submit"
            variant="primary"
            disabled={!input.trim() || isLoading}
          >
            전송
          </Button>
        </form>
      </div>
    </div>
  );
};

