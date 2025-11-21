import type {
  WhatsAppAddQuery,
  WhatsAppAddResponse,
} from "../../../app/types/whatsapp";

export default defineEventHandler(
  async (event): Promise<WhatsAppAddResponse> => {
    const query = getQuery(event) as WhatsAppAddQuery;

    if (!query.groupId || !query.phone) {
      throw createError({
        statusCode: 400,
        statusMessage: "groupId et phone sont requis",
      });
    }

    try {
      const response: WhatsAppAddResponse = await $fetch(
        "http://0.0.0.0:5000/api/whatsapp/add",
        {
          method: "POST",
          query,
        },
      );

      return response;
    } catch (error: any) {
      console.error("WhatsApp Add Error:", error);

      const status = error.response?.status || 500;
      let message = "Erreur lors de l’ajout au groupe WhatsApp.";

      if (status === 422 && error.data?.detail) {
        message = Array.isArray(error.data.detail)
          ? error.data.detail[0].msg
          : JSON.stringify(error.data.detail);
      }

      throw createError({
        statusCode: status,
        statusMessage: message,
      });
    }
  },
);
