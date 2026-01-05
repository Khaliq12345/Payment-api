// server/api/whatsapp/add.post.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const config = useRuntimeConfig();

  try {
    const response = await $fetch("/api/whatsapp/add", {
      method: "POST",
      baseURL: config.public.apiUrl,
      query: {
        transaction_id: query.transaction_id,
      },
    });

    return response;
  } catch (error: any) {
    console.error("Error adding user to whatsapp group", error);

    throw createError({
      statusCode: error?.response?.status ?? 500,
      statusMessage: "Unable to add utilisateur au groupe WhatsApp",
    });
  }
});
