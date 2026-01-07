export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const config = useRuntimeConfig(event);

  if (!body)
    throw createError({ statusCode: 400, statusMessage: "Données manquantes" });

  const externalPayload = {
    first_name: body.firstName,
    last_name: body.lastName,
    email: body.email,
    phone: body.phone,
    whatsapp_phone: body.whatsappPhone,
    country: body.country,
    product_id: body.productId,
  };
  try {
    const response = await $fetch<any>(event.path, {
      method: "POST",
      body: JSON.stringify(externalPayload),
      headers: {
        accept: "application/json",
        "Content-Type": "application/json",
      },
      baseURL: config.public.apiUrl,
    });
    console.log("Raw API response:", response);
    return response;
  } catch (error: any) {
    let errorMessage =
      "Erreur lors de la création du client; verifiez votre address email";
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
