/**
 * OpenAI 모델 정보 및 가격
 */

export interface AIModel {
  id: string;
  name: string;
  description: string;
  inputPrice: number;  // per 1M tokens
  outputPrice: number; // per 1M tokens
  speed: 'fast' | 'medium' | 'slow';
  quality: 'good' | 'better' | 'best';
  recommended?: boolean;
}

export const AI_MODELS: AIModel[] = [
  {
    id: 'gpt-4.1-nano',
    name: 'GPT-4.1 Nano',
    description: '가장 빠르고 저렴 (경량 작업 최적)',
    inputPrice: 0.10,
    outputPrice: 0.40,
    speed: 'fast',
    quality: 'good',
    recommended: true,
  },
  {
    id: 'gpt-4.1-mini',
    name: 'GPT-4.1 Mini',
    description: '빠르고 효율적 (텍스트 및 비전)',
    inputPrice: 0.15,
    outputPrice: 0.60,
    speed: 'fast',
    quality: 'good',
  },
  {
    id: 'gpt-5-nano',
    name: 'GPT-5 Nano',
    description: '향상된 성능 (리소스 제한 환경)',
    inputPrice: 0.20,
    outputPrice: 0.80,
    speed: 'fast',
    quality: 'better',
  },
  {
    id: 'gpt-5-mini',
    name: 'GPT-5 Mini',
    description: '최신 고성능 (빠른 응답)',
    inputPrice: 0.25,
    outputPrice: 2.00,
    speed: 'medium',
    quality: 'better',
  },
];

export const getModelById = (id: string): AIModel | undefined => {
  return AI_MODELS.find(model => model.id === id);
};

export const formatPrice = (price: number): string => {
  return `$${price.toFixed(2)}/1M`;
};

