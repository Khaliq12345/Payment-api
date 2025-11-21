export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const config = useRuntimeConfig();

  try {
    const response: any = await $fetch(
      "http://0.0.0.0:5000/api/fedapay/transaction",
      {
        method: "POST",
        body: body,
      },
    );

    const link =
      response.transaction_link || response["v1/transaction"]?.payment_url;

    if (!link) {
      console.error("Structure reçue invalide:", response);
      throw createError({
        statusCode: 500,
        statusMessage: "Lien de transaction introuvable dans la réponse",
      });
    }

    return {
      transaction_link: link,
    };
  } catch (error: any) {
    console.error("Transaction API Error:", error);
    throw createError({
      statusCode: error?.statusCode || 500,
      message:
        error?.data?.message ||
        error?.message ||
        "Erreur lors de la génération du lien.",
    });
  }
});
