import type {
  WhatsAppVerifyQuery,
  WhatsAppVerifyResponse,
} from "../../../app/types/whatsapp";

export default defineEventHandler(
  async (event): Promise<WhatsAppVerifyResponse> => {
    const query = getQuery(event) as WhatsAppVerifyQuery;
    const config = useRuntimeConfig(event);
    if (!query.number) {
      throw createError({
        statusCode: 400,
        statusMessage: "number est requis",
      });
    }

    try {
      const response: WhatsAppVerifyResponse = await $fetch({
        method: "GET",
        query: query.number,
        baseURL: config.API_URL,
      });

      return response;
    } catch (error: any) {
      console.error("WhatsApp Verify Error:", error);

      const status = error.response?.status || 500;
      let message = "Erreur lors de la vérification du numéro.";

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
