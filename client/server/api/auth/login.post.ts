export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)

  try {
    const body = await readBody(event)
    
    const response = await $fetch("/api/login", {
      method: "POST",
      baseURL: config.API_URL,
      body: body
    })

    return response
  } catch (error: any) {
    console.error("Login Error:", error)

    const status = error.response?.status || 500
    const message = error.response?._data?.message || "Erreur lors de la connexion"

    throw createError({
      statusCode: status,
      statusMessage: message,
    })
  }
})
