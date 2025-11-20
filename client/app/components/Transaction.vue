<template>
    <UCard>
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

            <UFormGroup label="Devise" name="currency">
                <UInput v-model="form.currency" placeholder="XOF" />
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
        </div>
    </UCard>
</template>

<script setup lang="ts">
import type { TransactionPayload } from '~/types/transaction'

const form = defineModel<TransactionPayload>({ required: true })
</script>

