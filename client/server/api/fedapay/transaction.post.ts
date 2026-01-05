export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  const query = getQuery(event);

  try {
    const response: any = await $fetch("/api/fedapay/transaction", {
      method: "POST",
      query: {
        customer_id: query.customer_id,
        product_id: query.product_id,
        callback_url: query.callback_url,
      },
      baseURL: config.public.apiUrl,
    });

    return response.payment_link;
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
