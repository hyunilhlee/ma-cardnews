/**
 * 카드 섹션 관련 TypeScript 타입 정의
 */

export type CardType = 'title' | 'content' | 'closing';

export interface DesignConfig {
  background_color: string;
  font_family: string;
  font_size: number;
}

export interface CardSection {
  id: string;
  project_id: string;
  order: number;
  type: CardType;
  title?: string;
  content: string;
  design_config: DesignConfig;
}

export interface SectionUpdate {
  title?: string;
  content?: string;
  order?: number;
}

