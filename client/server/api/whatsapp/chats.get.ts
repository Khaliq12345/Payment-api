import type { WhatsAppChatsResponse } from "../../../app/types/whatsapp";

export default defineEventHandler(async (): Promise<WhatsAppChatsResponse> => {
  try {
    const response: WhatsAppChatsResponse = await $fetch(
      "http://0.0.0.0:5000/api/whatsapp/chats",
      {
        method: "GET",
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
