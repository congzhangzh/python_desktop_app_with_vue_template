import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    // vue({
    //   template: {
    //     compilerOptions: {
    //       isCustomElement: (tag) => false
    //     }
    //   }
    // }),
    vue(),
    vueJsx(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  // build: {
  //   sourcemap: true, // 生产环境也生成source map
  // },
  // css: {
  //   devSourcemap: true, // CSS source map
  // },
  // server: {
  //   sourcemapIgnoreList: false, // 不忽略任何source map
  // },
})
