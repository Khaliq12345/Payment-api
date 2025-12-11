export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const transactionId = query.transactionId;
  const config = useRuntimeConfig(event);

  if (!transactionId) {
    throw createError({
      statusCode: 400,
      statusMessage: "transactionId manquant",
    });
  }

  try {
    const response = await $fetch("api/fedapay/transaction", {
      method: "GET",
      query: { transactionId },
      baseURL: config.API_URL,
    });
    return response;
  } catch (error) {
    throw createError({
      statusCode: 500,
      statusMessage: "Erreur lors de la récupération de la transaction.",
    });
  }
});
