export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  const params = getQuery(event);

  try {
    const response = await $fetch(event.path, {
      method: "GET",
      baseURL: config.public.apiUrl,
      query: {
        product_id: params.product_id,
      },
    });

    return response;
  } catch (error: any) {
    const status = error.response?.status || 500;
    let message =
      "Une erreur inattendue est survenue lors de la création du produit.";

    // Personnalisation des messages selon le code d'erreur
    switch (status) {
      case 401:
        message =
          "Session expirée ou accès non autorisé. Veuillez vous reconnecter.";
        break;
      case 403:
        message =
          "Vous n'avez pas les permissions nécessaires pour effectuer cette action.";
        break;
      case 404:
        message = "Le service de destination est introuvable.";
        break;
      case 409:
        message = "Ce produit (ou cet identifiant) existe déjà.";
        break;
      case 429:
        message = "Trop de requêtes envoyées. Veuillez patienter un instant.";
        break;
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
