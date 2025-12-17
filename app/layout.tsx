import type { Metadata } from "next";
import "./globals.css";
import { Space_Grotesk } from "next/font/google";

const spaceGrotesk = Space_Grotesk({ subsets: ["latin"], variable: "--font-space" });

export const metadata: Metadata = {
  title: "Real Estate Data Analytics & Workflow Automation Case Study",
  description: "Gautham Gongada's Project Destined-focused analytics, SQL, and automation walkthrough."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={spaceGrotesk.variable}>
      <body className="bg-slate-950 text-slate-50 antialiased min-h-screen">
        {/* Background layers (images + overlay) */}
        <div className="page-bg" aria-hidden="true" />
        <div className="page-overlay" aria-hidden="true" />
        {/* Content above background */}
        <div className="relative z-10 min-h-screen">{children}</div>
      </body>
    </html>
  );
}
