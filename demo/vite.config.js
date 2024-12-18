/*
 * Copyright DB InfraGO AG and contributors
 * SPDX-License-Identifier: Apache-2.0
 */

import { fileURLToPath, URL } from "node:url";

import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools()],
  define: {
    VITE_CCDD_BACKEND_HOST: JSON.stringify(process.env.VITE_CCDD_BACKEND_HOST),
    VITE_CCDD_BACKEND_PORT: JSON.stringify(process.env.VITE_CCDD_BACKEND_PORT),
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
