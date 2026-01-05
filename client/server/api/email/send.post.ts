// server/api/email/send.post.ts
export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const config = useRuntimeConfig(event);

  try {
    const response = await $fetch(event.path, {
      method: "POST",
      query: {
        transaction_id: query.transaction_id,
      },
      baseURL: config.public.apiUrl,
    });

    return response;
  } catch (error: any) {
    console.error("Sending Email Error:", error);
    throw createError({
      statusCode: error.response?.status || 500,
      statusMessage: `We are unable to send the email due to some issue - ${error}`,
    });
  }
});
