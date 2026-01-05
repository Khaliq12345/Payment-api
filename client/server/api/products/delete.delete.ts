export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  const body = await readBody(event);
  const query = getQuery(event);

  try {
    const response = await $fetch(event.path, {
      method: "DELETE",
      baseURL: config.public.apiUrl,
      query: {
        product_id: query.product_id,
      },
    });

    return response;
  } catch (error: any) {
    const status = error.response?.status || 500;
    let message =
      "Une erreur inattendue est survenue lors de la création du produit.";

    // Personnalisation des messages selon le code d'erreur
    switch (status) {
      case 500:
        message = "Erreur interne du serveur. Nos équipes ont été notifiées.";
        break;
    }
    console.error(`[${status}] Erreur API :`, error.data || error.message);

    throw createError({
      statusCode: status,
      statusMessage: message,
      data: error.data,
    });
  }
});
