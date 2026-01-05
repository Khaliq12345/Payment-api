import process from "node:process";

export default defineNuxtConfig({
  modules: ["@nuxt/ui"],
  css: ["~/assets/css/main.css"],
  runtimeConfig: {
    public: {
      FRONTEND_URL: process.env.NUXT_PUBLIC_FRONTEND_URL,
      apiUrl: process.env.NUXT_PUBLIC_API_URL,
      emailService: process.env.NUXT_PUBLIC_EMAIL_SERVICE,
    },
  },
});
