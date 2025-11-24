<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-gray-950 p-4">
    <UCard class="w-full max-w-md">
      <UAuthForm
        title="Connexion"
        description="Connectez-vous pour accéder à l'administration"
        icon="i-heroicons-user-circle"
        :fields="fields"
        :schema="schema"
        :loading="loading"
        @submit="onSubmit"
      />
    </UCard>
  </div>
</template>

<script setup lang="ts">
import * as v from 'valibot'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'
import { useToast, navigateTo } from '#imports'

const loading = ref(false)
const toast = useToast()

const fields: AuthFormField[] = [
  {
    name: 'username',
    type: 'text',
    label: "Nom d'utilisateur",
    placeholder: "Entrez votre nom d'utilisateur",
    required: true
  },
  {
    name: 'password',
    type: 'password',
    label: 'Mot de passe',
    placeholder: 'Entrez votre mot de passe',
    required: true
  }
]

const schema = v.object({
  username: v.pipe(v.string(), v.minLength(1, 'Requis')),
  password: v.pipe(v.string(), v.minLength(1, 'Requis'))
})

type Schema = v.InferOutput<typeof schema>

const onSubmit = async (event: FormSubmitEvent<Schema>) => {
  loading.value = true
  try {
    const response: any = await $fetch('/api/auth/login', {
      method: 'POST',
      body: event.data
    })

    if (response.login === true) {
      // Calcul de la date d'expiration (date actuelle + 2 jours)
      const expirationDate = new Date()
      expirationDate.setDate(expirationDate.getDate() + 2)

      // Stockage dans le localStorage
      localStorage.setItem('user', event.data.username)
      localStorage.setItem('expired_at', expirationDate.toISOString())

      toast.add({
        title: 'Connexion réussie',
        icon: 'i-heroicons-check-circle',
        color: 'success'
      })

      // Redirection
      navigateTo('/admin/groups')
    } else {
      throw new Error('Identifiants incorrects')
    }
  } catch (error) {
    toast.add({
      title: 'Erreur de connexion',
      description: 'Vérifiez vos identifiants',
      icon: 'i-heroicons-x-circle',
      color: 'error'
    })
  } finally {
    loading.value = false
  }
}
</script>
