// server/api/whatsapp/add.post.ts
import type { WhatsAppAddQuery, WhatsAppAddResponse } from "~/types/whatsapp";

export default defineEventHandler(
  async (event): Promise<WhatsAppAddResponse> => {
    const query = getQuery(event) as WhatsAppAddQuery;
    const config = useRuntimeConfig(event);

    if (!query.groupId || !query.phone) {
      throw createError({
        statusCode: 400,
        statusMessage: "groupId et phone sont requis",
      });
    }

    try {
      const response = await $fetch<WhatsAppAddResponse>("/api/whatsapp/add", {
        method: "POST",
        query: query,
        baseURL: config.API_URL,
      });

      return response;
    } catch (error: any) {
      console.error("WhatsApp Add Error:", error);
      throw createError({
        statusCode: error.response?.status || 500,
        statusMessage: "Impossible d’ajouter l’utilisateur au groupe WhatsApp",
      });
    }
  },
);
