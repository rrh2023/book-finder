/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f7ff',
          100: '#ebf0ff',
          200: '#d6e0ff',
          300: '#b3c7ff',
          400: '#8da9ff',
          500: '#667eea',
          600: '#5568d3',
          700: '#4451b8',
          800: '#353d9c',
          900: '#2a2f7f',
        },
        secondary: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#764ba2',
          600: '#6b3f92',
          700: '#5f3482',
          800: '#532972',
          900: '#471e62',
        },
      },
    },
  },
  plugins: [],
}