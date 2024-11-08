/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pinch/pages/**/*.py", // scans all Python files in the pages directory
    "./pinch/components/**/*.py", // scans all Python files in the components directory
    "./pinch/app/**/*.py", // scans all Python files in the app directory
    "./pinch/app.py", // scans all Python files in the lib directory
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
