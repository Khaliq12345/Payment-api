export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)

  try {
    const body = await readBody(event)

    // Convert JSON body to FormData 
    const formData = new FormData()
    formData.append('username', body.username)
    formData.append('password', body.password)

    const response = await $fetch<{ login: boolean }>("/api/auth/login", {
      method: "POST",
      baseURL: config.API_URL,
      body: formData
    })

    return response
  } catch (error: any) {
    console.error("Login Error:", error)

    const status = error.response?.status || 500
    const message = error.response?._data?.detail || "Erreur lors de la connexion"

    throw createError({
      statusCode: status,
      statusMessage: message,
    })
  }
})
