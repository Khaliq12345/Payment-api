<template>
    <div v-if="!submittedCustomer">
        <UCard>
            <UForm @submit="createCustomer" :state="form">
                <div class="flex flex-col gap-4">
                    <UFormGroup label="Description" name="description">
                        <UTextarea
                            v-model="form.description"
                            placeholder="Décrivez la transaction"
                        />
                    </UFormGroup>

                    <UFormGroup label="Montant" name="amount">
                        <UInput
                            v-model.number="form.amount"
                            type="number"
                            placeholder="0"
                            min="0"
                            step="0.01"
                        />
                    </UFormGroup>

                    <UFormGroup label="Callback URL" name="callback_url">
                        <UInput
                            v-model="form.callback_url"
                            type="url"
                            placeholder="https://example.com"
                        />
                    </UFormGroup>

                    <UFormGroup label="ID Client" name="customer_id">
                        <UInput v-model="form.customer_id" placeholder="CUS-12345" />
                    </UFormGroup>

                    <UFormGroup label="Numéro WhatsApp" name="whatsapp_number">
                        <UInput
                            v-model="form.whatsapp_number"
                            type="tel"
                            placeholder="+2290100000000"
                        />
                    </UFormGroup>

                    <div class="grid gap-4 md:grid-cols-2">
                        <UFormGroup label="Prénom" name="first_name">
                            <UInput v-model="form.first_name" placeholder="Jean" />
                        </UFormGroup>

                        <UFormGroup label="Nom" name="last_name">
                            <UInput v-model="form.last_name" placeholder="Dupont" />
                        </UFormGroup>
                    </div>

                    <UFormGroup label="Email" name="email">
                        <UInput
                            v-model="form.email"
                            type="email"
                            placeholder="johndoe@example.com"
                        />
                    </UFormGroup>

                    <UFormGroup label="Confirmer WhatsApp" name="confirm_whatsapp_number">
                        <UInput
                            v-model="form.confirm_whatsapp_number"
                            type="tel"
                            placeholder="Répéter..."
                        />
                    </UFormGroup>

                    <UFormGroup label="Pays" name="country">
                        <USelect 
                          v-model="form.country" 
                          :options="countries" 
                          option-attribute="label"
                          value-attribute="value"
                        />
                    </UFormGroup>

                    <UFormGroup label="Group ID" name="group_id">
                        <UInput v-model.number="form.group_id" type="number" placeholder="1" />
                    </UFormGroup>

                    <div class="pt-4">
                        <UButton type="submit" block :loading="isLoading">
                            Créer le Client
                        </UButton>
                    </div>
                </div>
            </UForm>
        </UCard>
    </div>

    <div v-else>
        <UCard class="max-w-xl mx-auto border-2 border-primary-500/20">
            <template #header>
                <div class="flex justify-between items-center">
                    <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                        Détails du Client
                    </h3>
                    <UBadge color="green" variant="subtle">Succès</UBadge>
                </div>
            </template>

            <div class="space-y-3">
                <div class="flex justify-between border-b border-gray-100 pb-2">
                    <span class="text-gray-500">Nom complet</span>
                    <span class="font-medium">{{ submittedCustomer.full_name }}</span>
                </div>
                <div class="flex justify-between border-b border-gray-100 pb-2">
                    <span class="text-gray-500">Email</span>
                    <span class="font-medium">{{ submittedCustomer.email }}</span>
                </div>
                <div class="flex justify-between border-b border-gray-100 pb-2">
                    <span class="text-gray-500">ID Compte</span>
                    <span class="font-mono text-primary">{{ submittedCustomer.account_id }}</span>
                </div>
                <div class="flex justify-between">
                    <span class="text-gray-500">Prénom / Nom</span>
                    <span>{{ submittedCustomer.firstname }} {{ submittedCustomer.lastname }}</span>
                </div>
            </div>

            <template #footer>
                <div class="flex flex-col gap-3">
                    <UButton 
                        block 
                        size="lg"
                        icon="i-heroicons-currency-dollar"
                        :loading="isTransactionLoading"
                        @click="generateLink"
                    >
                        Générer le lien de paiement
                    </UButton>

                    <UButton 
                        block 
                        variant="ghost" 
                        color="gray" 
                        @click="resetProcess"
                    >
                        Nouveau client
                    </UButton>
                </div>
            </template>
        </UCard>

        <div v-if="paymentLink" class="max-w-xl mx-auto mt-6">
            <UAlert
                title="Lien de paiement prêt !"
                description="Cliquez ci-dessous pour accéder au paiement."
                icon="i-heroicons-check-badge"
                color="green"
                variant="soft"
            >
                <template #description>
                    <div class="mt-2 p-2 bg-white dark:bg-gray-800 rounded border border-green-200 break-all font-mono text-sm">
                        <a :href="paymentLink" target="_blank" class="text-green-600 hover:underline">
                            {{ paymentLink }}
                        </a>
                    </div>
                </template>
            </UAlert>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { TransactionPayload } from '~/types/transaction'
import type { CreatedCustomer } from '~/types/fedapay'

const props = defineProps<{
  customer?: CreatedCustomer
}>()

const form = defineModel<TransactionPayload>({ required: true })
const toast = useToast()

// États pour la carte de succès
const submittedCustomer = ref<CreatedCustomer | null>(props.customer || null)
const isLoading = ref(false)
const isTransactionLoading = ref(false)
const paymentLink = ref<string | null>(null)

// Options pour le menu déroulant
const countries = [
  { label: 'Bénin', value: 'bj' },
  { label: 'Togo', value: 'tg' },
  { label: 'Côte d\'Ivoire', value: 'ci' },
  { label: 'Sénégal', value: 'sn' }
]

// Fonction pour créer le client (si pas de customer passé)
const createCustomer = async () => {
  if (submittedCustomer.value) return // Déjà créé

  isLoading.value = true
  
  try {
    const payload = {
      first_name: form.value.first_name,
      last_name: form.value.last_name,
      email: form.value.email,
      whatsapp_number: form.value.whatsapp_number,
      confirm_whatsapp_number: form.value.confirm_whatsapp_number,
      country: form.value.country
    }
    const response = await $fetch<CreatedCustomer>('/api/fedapay/create-customer', {
      method: 'POST',
      body: payload
    })
    submittedCustomer.value = response

    toast.add({ title: 'Client créé', description: `Bienvenue ${response.full_name}` })

  } catch (error: any) {
    const status = error?.status || 500
    const message = error?.data?.message || error?.message || 'Une erreur est survenue'
    
    toast.add({ 
      title: 'Erreur', 
      description: `Erreur ${status}: ${message}`,
      color: 'red'
    })
  } finally {
    isLoading.value = false
  }
}

// Fonction pour générer le lien de paiement
const generateLink = async () => {
  if (!submittedCustomer.value) return

  isTransactionLoading.value = true
  paymentLink.value = null
  
  try {
    const payload = {
      description: form.value.description,
      amount: form.value.amount,
      currency: 'XOF',
      callback_url: form.value.callback_url,
      customer_id: submittedCustomer.value.account_id,
      whatsapp_number: form.value.whatsapp_number,
      group_id: form.value.group_id
    }

    const link = await $fetch<string>('/api/fedapay/transaction', {
      method: 'POST',
      body: payload
    })

    paymentLink.value = link
    toast.add({ title: 'Lien généré', icon: 'i-heroicons-link', color: 'green' })

  } catch (error: any) {
    const status = error?.status || 500
    const message = error?.data?.message || error?.message || 'Erreur lors de la génération du lien.'
    
    toast.add({ 
      title: 'Erreur Transaction', 
      description: `Erreur ${status}: ${message}`,
      color: 'red'
    })
  } finally {
    isTransactionLoading.value = false
  }
}

// Fonction pour réinitialiser et revenir au formulaire
const resetProcess = () => {
  submittedCustomer.value = null
  paymentLink.value = null
}
</script>
