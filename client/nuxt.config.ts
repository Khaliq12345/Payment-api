export default defineNuxtConfig({
  modules: ["@nuxt/ui"],
  css: ["~/assets/css/main.css"],
  runtimeConfig: {
    public: {
      FRONTEND_URL: "http://localhost:3000",
      apiUrl: "http://0.0.0.0:7000",
      emailService: "",
    },
  },
});
