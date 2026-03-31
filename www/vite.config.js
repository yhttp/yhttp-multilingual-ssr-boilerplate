import path from 'path';
import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  server: {
    cors: {
      origin: 'http://localhost:8080',
    },
  },
  plugins: [
    tailwindcss(),
  ],
  build: {
    manifest: true,
    outDir: './static',
    cssCodeSplit: false,
    modulePreload: {
      polyfill: false,
    },
    rolldownOptions: {
      devtools: {},
      input: [
        './src/main.js',
      ]
    },
  },
})
