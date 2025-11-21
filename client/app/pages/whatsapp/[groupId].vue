<template>
    <div class="p-6 max-w-3xl mx-auto">
        <h1 class="text-2xl font-bold text-center mb-8">
            Groupe : {{ groupId }}
        </h1>

        <!-- Affiche le formulaire tant que customerData est null -->
        <Form v-if="!customerData" v-model="customerData" />

        <!-- Affiche la transaction une fois le client créé -->
        <Transaction
            v-else
            :customer="customerData.response"
            :whatsapp-number="customerData.whatsapp_number"
            :group-id="groupId"
        />
    </div>
</template>

<script setup lang="ts">
import type { CustomerState } from "~/types/fedapay";

const route = useRoute();
const groupId = Number(route.params.groupId);

const customerData = ref<CustomerState>(null);
</script>
