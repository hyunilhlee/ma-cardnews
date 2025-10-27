/**
 * 프로젝트 상태 관리 (Zustand)
 */

import { create } from 'zustand';
import { Project } from '../types/project';
import { CardSection } from '../types/section';

interface ProjectState {
  // 현재 프로젝트
  currentProject: Project | null;
  setCurrentProject: (project: Project | null) => void;

  // 카드 섹션들
  sections: CardSection[];
  setSections: (sections: CardSection[]) => void;
  updateSection: (sectionId: string, updates: Partial<CardSection>) => void;

  // 로딩 상태
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;

  // 에러 상태
  error: string | null;
  setError: (error: string | null) => void;

  // 초기화
  reset: () => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  currentProject: null,
  setCurrentProject: (project) => set({ currentProject: project }),

  sections: [],
  setSections: (sections) => set({ sections }),
  updateSection: (sectionId, updates) =>
    set((state) => ({
      sections: state.sections.map((section) =>
        section.id === sectionId ? { ...section, ...updates } : section
      ),
    })),

  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),

  error: null,
  setError: (error) => set({ error }),

  reset: () =>
    set({
      currentProject: null,
      sections: [],
      isLoading: false,
      error: null,
    }),
}));

