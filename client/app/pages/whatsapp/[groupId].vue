<template>
    <div class="p-6 max-w-3xl mx-auto">
        <h1 class="text-2xl font-bold text-center mb-8">
            Groupe : {{ groupId }}
        </h1>

        <Form v-model="customerData" v-if="!customerData" />

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
const groupId = route.params.groupId;

const customerData = ref<CustomerState>(null);

const items = [
    {
        label: "Je suis un nouvel utilisateur",
        icon: "i-lucide-user",
        slot: "new",
    },
    {
        label: "J'ai un compte",
        icon: "i-lucide-lock",
        slot: "old",
    },
];
</script>
