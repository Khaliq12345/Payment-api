import type { WhatsAppChatsResponse } from "../../../app/types/whatsapp";

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  try {
    const response: WhatsAppChatsResponse = await $fetch(
      "/api/whatsapp/chats",
      {
        method: "GET",
        baseURL: config.API_URL,
      },
    );

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
