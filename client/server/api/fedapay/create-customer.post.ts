import { FedaPayCustomerPayload, FedaPayResponse, FedaPayValidationError } from '~/types/fedapay'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  if (!body) throw createError({ statusCode: 400, statusMessage: 'Données manquantes' })

  const externalPayload: FedaPayCustomerPayload = {
    first_name: body.first_name,
    last_name: body.last_name,
    email: body.email,
    phone_number: body.whatsapp_number,
    country: body.country,
  }

  try {
    const response = await $fetch<FedaPayResponse>('http://0.0.0.0:5000/api/fedapay/create-customer', {
      method: 'POST',
      body: externalPayload
    })
    return response

  } catch (error: any) {
    let errorMessage = 'Erreur lors de la création du client'
    const status = error.response?.status || 500

    // Extraction propre du message d'erreur Swagger (422)
    if (status === 422 && error.data?.detail?.[0]?.msg) {
      errorMessage = error.data.detail[0].msg
    } else if (typeof error.data === 'string') {
      errorMessage = error.data
    }

    throw createError({
      statusCode: status,
      statusMessage: errorMessage
    })
  }
})