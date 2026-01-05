export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event);
  const { email } = getQuery(event);

  try {
    const response = await $fetch("/api/fedapay/get-customer", {
      baseURL: config.public.apiUrl,
      method: "GET",
      params: {
        email: email,
      },
    });

    if (response.message) {
      // Erreur de l'API
      throw createError({ statusCode: 400, statusMessage: response.message });
    }

    if (!response["v1/customer"]) {
      throw createError({
        statusCode: 500,
        statusMessage: "Réponse API invalide",
      });
    }

    return response["v1/customer"];
  } catch (error: any) {
    let errorMessage = "Erreur lors de la création du client";
    const status = error.response?.status || 500;

    // Extraction propre du message d'erreur Swagger (422)
    if (status === 422 && error.data?.detail?.[0]?.msg) {
      errorMessage = error.data.detail[0].msg;
    } else if (typeof error.data === "string") {
      errorMessage = error.data;
    }

    throw createError({
      statusCode: status,
      statusMessage: errorMessage,
    });
  }
});
