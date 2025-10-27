/**
 * UI 상태 관리 (Zustand)
 */

import { create } from 'zustand';

type Step = 'input' | 'summarize' | 'generate' | 'edit';

interface UIState {
  // 현재 단계
  currentStep: Step;
  setCurrentStep: (step: Step) => void;

  // 사이드바 열림 상태
  isSidebarOpen: boolean;
  toggleSidebar: () => void;

  // 모달 상태
  isModalOpen: boolean;
  modalContent: React.ReactNode | null;
  openModal: (content: React.ReactNode) => void;
  closeModal: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  currentStep: 'input',
  setCurrentStep: (step) => set({ currentStep: step }),

  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),

  isModalOpen: false,
  modalContent: null,
  openModal: (content) => set({ isModalOpen: true, modalContent: content }),
  closeModal: () => set({ isModalOpen: false, modalContent: null }),
}));

