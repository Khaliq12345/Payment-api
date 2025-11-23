<template>
    <UCard class="max-w-xl mx-auto border-2 border-primary-500/20 shadow-lg">
        <template #header>
            <div class="flex justify-between items-center">
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                    Détails du Client
                </h3>
                <UBadge color="success" variant="subtle" size="lg"
                    >Succès</UBadge
                >
            </div>
        </template>

        <!-- Affichage des infos client -->
        <div class="space-y-4 py-2">
            <div class="flex justify-between border-b border-gray-100 pb-2">
                <span class="text-gray-500">Nom complet</span>
                <span class="font-medium text-gray-900 dark:text-white">{{
                    customer.full_name
                }}</span>
            </div>
            <div class="flex justify-between border-b border-gray-100 pb-2">
                <span class="text-gray-500">Email</span>
                <span class="font-medium text-gray-900 dark:text-white">{{
                    customer.email
                }}</span>
            </div>
            <div class="flex justify-between border-b border-gray-100 pb-2">
                <span class="text-gray-500">ID Client (Système)</span>
                <span class="font-mono text-primary font-bold">{{
                    customer.id
                }}</span>
            </div>
            <div class="flex justify-between">
                <span class="text-gray-500">Prénom / Nom</span>
                <span>{{ customer.firstname }} {{ customer.lastname }}</span>
            </div>
        </div>

        <template #footer>
            <div class="space-y-6">
                <!-- Bouton pour générer le lien -->
                <UButton
                    v-if="!paymentLink"
                    block
                    size="xl"
                    icon="i-heroicons-currency-dollar"
                    :loading="isTransactionLoading"
                    @click="generateLink"
                >
                    Générer le lien de paiement
                </UButton>

                <!-- Affichage du lien avec bouton Payer -->
                <div v-else class="animate-fade-in space-y-2">
                    <label
                        class="text-sm font-medium text-gray-700 dark:text-gray-200"
                    >
                        Lien de paiement généré :
                    </label>

                    <div class="flex gap-2">
                        <!-- Champ input en lecture seule -->
                        <UInput
                            :model-value="paymentLink"
                            readonly
                            icon="i-heroicons-link"
                            class="flex-1 font-mono text-sm"
                            input-class="text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-800"
                        />

                        <!-- Bouton de redirection -->
                        <UButton
                            :to="paymentLink"
                            target="_blank"
                            color="primary"
                            variant="solid"
                            icon="i-heroicons-arrow-top-right-on-square"
                        >
                            Payer
                        </UButton>
                    </div>
                </div>
            </div>
        </template>
    </UCard>
</template>

<script setup lang="ts">
import type { CreatedCustomer } from "~/types/fedapay";

const props = defineProps<{
    customer: CreatedCustomer;
    whatsappNumber: string;
    groupId: string;
}>();

const toast = useToast();
const isTransactionLoading = ref(false);
const paymentLink = ref<string | null>(null);

// Fonction pour générer le lien de paiement
const generateLink = async () => {
    isTransactionLoading.value = true;
    paymentLink.value = null;

    try {
        const payload = {
            description: `Paiment du Groupe ${props.groupId}`,
            amount: 1000,
            currency: "XOF",
            callback_url: window.location.origin + "/callback",
            customer_id: props.customer.id,
            whatsapp_number: props.whatsappNumber,
            group_id: props.groupId,
        };

        const response = await $fetch<any>("/api/fedapay/transaction", {
            method: "POST",
            body: payload,
        });

        // Récupération du lien de paiement depuis la réponse
        paymentLink.value = response.transaction_link || response;

        toast.add({
            title: "Lien généré",
            description: "Le lien est prêt pour le paiement.",
            icon: "i-heroicons-check-circle",
            color: "success",
        });
    } catch (error: any) {
        const status = error?.status || 500;
        const message =
            error?.data?.message ||
            error?.message ||
            "Erreur lors de la génération du lien.";

        toast.add({
            title: "Erreur Transaction",
            description: `Erreur ${status}: ${message}`,
            color: "error",
        });
    } finally {
        isTransactionLoading.value = false;
    }
};
</script>
