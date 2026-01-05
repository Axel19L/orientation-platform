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
          DEFAULT: '#0B758C',
          dark: '#094d5e',
          light: '#0d8fa9',
        },
        secondary: {
          DEFAULT: '#F2EBDC',
          dark: '#e6dcc4',
          light: '#f8f3e8',
        },
        accent: {
          burgundy: '#732231',
          pink: '#F24B6A',
          'pink-soft': '#D97789',
        },
      },
    },
  },
  plugins: [],
}
