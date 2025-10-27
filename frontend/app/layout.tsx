import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Toaster } from 'react-hot-toast';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'CardNews AI Generator',
  description: 'AI 기반 카드뉴스 자동 생성 서비스',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko" suppressHydrationWarning>
      <head>
        {/* MetaMask 및 기타 확장 프로그램 오류 필터링 */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
              // MetaMask 및 브라우저 확장 프로그램 오류 필터링
              const originalError = console.error;
              console.error = function(...args) {
                const errorString = args.join(' ');
                // MetaMask 관련 오류 무시
                if (errorString.includes('MetaMask') || 
                    errorString.includes('chrome-extension://') ||
                    errorString.includes('extension not found')) {
                  return;
                }
                originalError.apply(console, args);
              };
            `,
          }}
        />
      </head>
      <body className={inter.className} suppressHydrationWarning>
        <div className="min-h-screen flex flex-col">
          <Header />
          <main className="flex-1 py-8 px-4 sm:px-6 lg:px-8">
            {children}
          </main>
          <Footer />
        </div>
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 3000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              iconTheme: {
                primary: '#4ade80',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </body>
    </html>
  );
}
