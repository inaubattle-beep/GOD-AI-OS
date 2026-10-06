import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'GOD AI OS — Mother Agent Operating System',
  description: 'Production-Grade Autonomous AI Agent Operating System, Agent Factory & Orchestrator',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased bg-[#090c15] text-slate-100">{children}</body>
    </html>
  )
}
