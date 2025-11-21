export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const transactionId = query.transactionId;

  if (!transactionId) {
    throw createError({
      statusCode: 400,
      statusMessage: "transactionId manquant",
    });
  }

  try {
    const response = await $fetch(
      `http://localhost:8000/api/fedapay/transaction`,
      {
        method: "GET",
        query: { transactionId },
      },
    );
    return response;
  } catch (error) {
    throw createError({
      statusCode: 500,
      statusMessage: "Erreur lors de la récupération de la transaction.",
    });
  }
});
