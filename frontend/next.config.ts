import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Vercel 배포를 위한 설정
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
