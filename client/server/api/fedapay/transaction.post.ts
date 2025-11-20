import { TransactionPayload } from '../../../app/types/transaction'

export default defineEventHandler(async (event) => {
  const body = await readBody<TransactionPayload>(event)

  if (!body) throw createError({ statusCode: 400, statusMessage: 'Payload manquant' })

  try {
    const response = await $fetch<any>('http://0.0.0.0:5000/api/fedapay/transaction', {
      method: 'POST',
      body: body
    })

    console.log('Raw Transaction API response:', response)

    if (!response.transaction_link) {
      throw createError({ statusCode: 500, statusMessage: 'Lien de transaction manquant' })
    }

    return response.transaction_link

  } catch (error: any) {
    console.error('Transaction API Error:', error)
    let errorMessage = 'Erreur lors de la génération du lien.'
    const status = error.response?.status || 500

    // Gestion des erreurs
    if (status === 422 && error.data?.detail) {
       errorMessage = Array.isArray(error.data.detail) 
        ? error.data.detail[0].msg 
        : JSON.stringify(error.data.detail)
    } else if (error.data && typeof error.data === 'string') {
      errorMessage = error.data
    }

    throw createError({
      statusCode: status,
      statusMessage: errorMessage
    })
  }
})
