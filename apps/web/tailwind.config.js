/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0d14',
        surface: '#121824',
        card: '#1a2234',
        border: '#2a344a',
        primary: {
          500: '#6366f1',
          600: '#4f46e5',
        },
        accent: {
          500: '#06b6d4',
          400: '#22d3ee',
        }
      },
    },
  },
  plugins: [],
}
