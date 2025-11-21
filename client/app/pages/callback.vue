<template>
    <UCard class="max-w-2xl mx-auto mt-10">
        <template #header>
            <h2 class="text-2xl text-center font-bold">Résultat du paiement</h2>
        </template>

        <div v-if="pending" class="text-center py-16 space-y-8">
            <p class="text-sm text-gray-500">
                Cela ne prendra que quelques secondes
            </p>
            <!-- Barre de progression-->
            <UProgress
                animation="carousel"
                size="xl"
                class="w-full max-w-md mx-auto"
                color="primary"
                model="value"
            />
        </div>

        <!-- Erreur -->
        <div v-else-if="error" class="text-center py-12 space-y-6">
            <UIcon
                name="i-heroicons-exclamation-triangle"
                class="w-20 h-20 text-red-500 mx-auto"
            />
            <div>
                <p class="text-xl font-bold text-red-700">
                    Une erreur est survenue
                </p>
                <p class="mt-2 text-red-600">{{ error }}</p>
            </div>
        </div>

        <!-- Succès -->
        <div v-else-if="transaction" class="space-y-8">
            <!-- Statut -->
            <div
                class="flex justify-between items-center py-4 border-b border-gray-200"
            >
                <span class="text-lg font-semibold">Statut du paiement</span>
                <UBadge :color="statusColor" variant="solid">
                    {{ transaction.status.toUpperCase() }}
                </UBadge>
            </div>

            <!-- Infos client -->
            <div class="rounded-xl p-6 space-y-4 text-sm">
                <div class="grid grid-cols-2 gap-x-6 gap-y-3">
                    <div><strong>ID :</strong></div>
                    <div class="font-mono">{{ transaction.id }}</div>
                    <div><strong>Référence :</strong></div>
                    <div class="font-mono">{{ transaction.reference }}</div>
                    <div><strong>Description :</strong></div>
                    <div>{{ transaction.description }}</div>
                    <div><strong>Client :</strong></div>
                    <div class="font-medium">{{ fullName }}</div>
                    <div><strong>WhatsApp :</strong></div>
                    <div class="font-mono">
                        {{
                            formatWhatsapp(
                                transaction.custom_metadata.whatsapp_number,
                            )
                        }}
                    </div>
                    <div><strong>Date :</strong></div>
                    <div>
                        {{
                            formatDate(
                                transaction.approved_at ??
                                    transaction.created_at,
                            )
                        }}
                    </div>
                </div>
            </div>

            <!-- Reçu officiel -->
            <UButton
                v-if="transaction.receipt_url"
                :to="transaction.receipt_url"
                target="_blank"
                color="gray"
                variant="outline"
                block
                size="lg"
            >
                Voir le reçu officiel
            </UButton>

            <!-- Bouton WhatsApp -->
            <UButton
                v-if="
                    transaction.status === 'approved' &&
                    !inviteLink &&
                    !hasAdded
                "
                @click="addToWhatsappGroup"
                :loading="adding"
                color="green"
                size="xl"
                block
                class="font-bold text-xl py-8 shadow-xl hover:shadow-2xl transition-all duration-300"
            >
                Obtenir le lien du groupe WhatsApp
            </UButton>

            <!-- Succès WhatsApp -->
            <div v-if="inviteLink" class="text-center">
                <UCard variant="subtle">
                    <template #header>
                        <div class="flex justify-center">
                            <UIcon
                                name="i-heroicons-check-badge-solid"
                                class="w-24 h-24 text-green-600 text-center mx-auto mb-6"
                            />
                        </div>
                    </template>
                    <template #footer>
                        <UButton
                            :to="inviteLink"
                            target="_blank"
                            color="green"
                            size="xl"
                            block
                            class="text-xl font-bold py-6"
                        >
                            Rejoindre le groupe WhatsApp maintenant
                        </UButton>
                    </template>
                </UCard>
            </div>

            <!-- Déjà ajouté -->
            <div
                v-if="hasAdded && !inviteLink"
                class="text-center bg-green-100 text-green-800 p-6 rounded-xl font-semibold"
            >
                Vous avez déjà été ajouté au groupe WhatsApp
            </div>

            <!-- Pending -->
            <div
                v-if="transaction.status === 'pending'"
                class="text-center bg-amber-50 border-2 border-amber-300 rounded-xl p-8"
            >
                <UIcon
                    name="i-heroicons-clock"
                    class="w-16 h-16 text-amber-600 mx-auto mb-4"
                />
                <p class="text-xl font-bold text-amber-800">
                    Paiement en cours de validation...
                </p>
                <p class="mt-3 text-amber-700">Revenez dans quelques minutes</p>
            </div>

            <!-- Échec -->
            <div
                v-else-if="transaction.status !== 'approved'"
                class="text-center bg-red-50 border-2 border-red-300 rounded-xl p-8"
            >
                <UIcon
                    name="i-heroicons-x-circle"
                    class="w-16 h-16 text-red-600 mx-auto mb-4"
                />
                <p class="text-xl font-bold text-red-800">
                    Paiement non validé
                </p>
                <p class="mt-3 text-red-700">
                    Statut : {{ transaction.status }}
                </p>
            </div>
        </div>

        <!-- Aucun ID -->
        <div v-else class="text-center py-16 text-gray-500">
            <p class="text-lg">
                Aucun identifiant de transaction trouvé dans l'URL.
            </p>
        </div>
    </UCard>
</template>

<script setup lang="ts">
import type { TransactionResponse } from "~/types/transaction";

const route = useRoute();

// États WhatsApp
const adding = ref(false);
const hasAdded = ref(false);
const inviteLink = ref<string | null>(null);

// États loading
const value = ref(null);

// Récupération transaction
const rawId = computed(
    () =>
        (route.query.id ??
            route.query.transactionId ??
            route.query.transaction_id ??
            route.params.id ??
            "") as string,
);
const transactionId = computed(() => {
    const id = rawId.value.trim();
    return id && !isNaN(Number(id)) ? Number(id) : null;
});

const { data, pending, error } = useAsyncData<TransactionResponse | null>(
    "fedapay-transaction",
    async () => {
        if (!transactionId.value) return null;
        return await $fetch("/api/fedapay/transaction", {
            query: { transactionId: transactionId.value },
        });
    },
    { immediate: true, watch: [transactionId] },
);

const transaction = computed(() => data.value?.["v1/transaction"] ?? null);

// Ajout au groupe WhatsApp
const addToWhatsappGroup = async () => {
    if (!transaction.value) return;
    adding.value = true;
    try {
        const response = await $fetch("/api/whatsapp/add", {
            method: "POST",
            query: {
                groupId: transaction.value.custom_metadata.group_id,
                phone: transaction.value.custom_metadata.whatsapp_number,
            },
        });

        if (response.addParticipant === true) {
            hasAdded.value = true;
            inviteLink.value = `https://chat.whatsapp.com/${transaction.value.custom_metadata.group_id}`;
        } else {
            alert("Vous êtes déjà dans le groupe ou l'ajout a échoué.");
        }
    } catch (err) {
        console.error(err);
        alert("Erreur réseau. Réessayez dans quelques instants.");
    } finally {
        adding.value = false;
    }
};

// Helpers
const statusColor = computed(() =>
    transaction.value?.status === "approved"
        ? "green"
        : transaction.value?.status === "pending"
          ? "yellow"
          : "red",
);
const fullName = computed(() =>
    transaction.value
        ? `${transaction.value.metadata.paid_customer.firstname} ${transaction.value.metadata.paid_customer.lastname}`.trim()
        : "",
);
const formatWhatsapp = (num: number) => `+${num}`;
const formatDate = (dateStr: string) =>
    new Date(dateStr).toLocaleString("fr-FR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
</script>
