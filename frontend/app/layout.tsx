import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "GPS 위치 확인",
  description: "버튼을 눌러 현재 GPS 위치를 확인합니다",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
