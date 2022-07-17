// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        font: resolve(__dirname, 'src/assets/fonts/nunito-v16-latin-regular.woff2'),
        login: resolve(__dirname, 'src/login.html'),
        devices: resolve(__dirname, 'src/devices.html'),
        times: resolve(__dirname, 'src/times.html'),
      }
    }
  }
})
