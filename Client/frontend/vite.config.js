// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        home: resolve(__dirname, 'src/home.html'),
        font: resolve(__dirname, 'src/assets/fonts/nunito-v16-latin-regular.woff2'),
        login: resolve(__dirname, 'src/login.html'),
        items: resolve(__dirname, 'src/items.html'),
        times: resolve(__dirname, 'src/times.html'),
      }
    }
  }
})
