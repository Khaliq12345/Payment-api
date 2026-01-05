export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  try {
    const response = await $fetch(event.path, {
      method: "GET",
      baseURL: config.public.apiUrl,
    });

    return response;
  } catch (error: any) {
    console.error("WhatsApp Chats Error:", error);

    const status = error.response?.status || 500;
    let message = "Erreur lors de la récupération des discussions.";

    throw createError({
      statusCode: status,
      statusMessage: message,
    });
  }
});
