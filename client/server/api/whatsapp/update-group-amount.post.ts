export default defineEventHandler(async (event) => {
  const query = getQuery(event);

  try {
    const response = await $fetch(
      "http://0.0.0.0:5000/api/whatsapp/update-group-amount",
      {
        method: "POST",
        params: {
          group_id: query.group_id,
          amount: query.amount,
        },
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
