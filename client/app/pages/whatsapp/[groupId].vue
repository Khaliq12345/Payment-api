<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold text-center mb-6">Groupe : {{ groupId }}</h1>
    
    <Form
      :loading="isLoading" 
      :on-submit="createCustomer" 
    />
  </div>
</template>


<script setup lang="ts">
import type { CustomerFormState, FedaPayResponse } from '~/types/fedapay'

const route = useRoute()
const toast = useToast()
const groupId = route.params.groupId
const isLoading = ref(false)

// Cette fonction est passée directement au composant Form
const createCustomer = async (formData: CustomerFormState) => {
  isLoading.value = true
  
  try {
    const response = await $fetch<FedaPayResponse>('/api/fedapay/create-customer', {
      method: 'POST',
      body: formData
    })
    toast.add({ title: 'Succès', description: response || 'Client créé avec succès'})

  } catch (error: any) {
    const status = error?.status || 500
    const message = error?.data?.message || error?.message || 'Une erreur est survenue'
    
    toast.add({ 
      title: 'Erreur', 
      description: `Erreur ${status}: ${message}`
    })
  } finally {
    isLoading.value = false
  }
}
</script>