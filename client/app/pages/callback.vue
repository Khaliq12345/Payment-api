<template>
    <UCard class="max-w-2xl mx-auto mt-10">
        <template #header>
            <h2 class="text-2xl text-center font-bold">Résultat du paiement</h2>
            <UProgress animation="swing" v-if="loading" />
        </template>

        <!-- Succès -->
        <div v-if="transaction && status == 'approved'" class="space-y-8">
            <!-- Statut -->
            <div
                class="flex justify-between items-center py-4 border-b border-gray-200"
            >
                <span class="text-lg font-semibold">Statut du paiement</span>
                <UBadge
                    :color="
                        transaction.status === 'approved' ? 'success' : 'error'
                    "
                    variant="solid"
                >
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
                color="success"
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
                color="success"
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
                            color="success"
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
        </div>

        <!-- Échec -->
        <div
            v-if="status !== 'approved'"
            class="text-center bg-red-50 border-2 border-red-300 rounded-xl p-8"
        >
            <UIcon
                name="i-heroicons-x-circle"
                class="w-16 h-16 text-red-600 mx-auto mb-4"
            />
            <p class="text-xl font-bold text-red-800">Paiement non validé</p>
            <p class="mt-3 text-red-700">Statut : {{ status }}</p>
        </div>
    </UCard>
</template>

<script setup lang="ts">
import type { Transaction, TransactionResponse } from "~/types/transaction";
import type { WhatsAppAddResponse } from "~/types/whatsapp";

const route = useRoute();

// États WhatsApp
const loading = ref(false);
const adding = ref(false);
const hasAdded = ref(false);
const inviteLink = ref<string | null>(null);

// Récupération transaction
const status = ref(route.query.status);
const transId = route.query.id;
const transaction = ref<Transaction>();

//toast
const toast = useToast();

onMounted(async () => {
    // check if the transaction is approved
    if (status.value !== "approved") return {};
    loading.value = true;
    try {
        // send the requests to get the transaction info
        const response = await $fetch<TransactionResponse>(
            "/api/fedapay/transaction",
            {
                query: { transactionId: transId },
            },
        );

        // extract the transaction info and display success notification
        transaction.value = response["v1/transaction"];
        status.value = transaction.value.status;
        toast.add({
            title: "Verification de transaction reussi",
            icon: "i-lucide-check-check",
            color: "success",
        });
    } catch (err) {
        // log error to the console and display error notification
        console.log(`Error - ${err}`);
        toast.add({
            title: "Erreur lors dela verification de la transaction; re-actualiser pour re-verifier",
            icon: "i-lucide-bug",
            color: "error",
        });
    } finally {
        loading.value = false;
    }
});

// Ajout au groupe WhatsApp
const addToWhatsappGroup = async () => {
    // verify if we have info about the transaction
    if (!transaction.value) return;
    adding.value = true;
    try {
        // send the requests to add the user to the group
        const response = await $fetch<WhatsAppAddResponse>(
            "/api/whatsapp/add",
            {
                method: "POST",
                query: {
                    groupId: transaction.value.custom_metadata.group_id,
                    phone: transaction.value.custom_metadata.whatsapp_number,
                },
            },
        );

        // check if user is added and display success notification
        if (response.addParticipant === true) {
            hasAdded.value = true;
            inviteLink.value = `https://chat.whatsapp.com/${transaction.value.custom_metadata.group_id}`;
            toast.add({
                title: "Vous êtes déjà dans le groupe",
                icon: "i-lucide-badge-check",
                color: "success",
            });
        } else {
            // display warning notification if user is not added
            toast.add({
                title: "Vous êtes déjà dans le groupe ou l'ajout a échoué.",
                icon: "i-lucide-circle-alert",
                color: "warning",
            });
        }
    } catch (err) {
        // in case of error, log the error and display the notification
        console.error(err);
        toast.add({
            title: "Erreur réseau. Réessayez dans quelques instants.",
            icon: "i-lucide-bug",
            color: "error",
        });
    } finally {
        adding.value = false;
    }
};

const formatWhatsapp = (num: number) => `+${num}`;
const formatDate = (dateStr: string) =>
    new Date(dateStr).toLocaleString("fr-FR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });
const fullName = computed(() =>
    transaction.value
        ? `${transaction.value.metadata.paid_customer.firstname} ${transaction.value.metadata.paid_customer.lastname}`.trim()
        : "",
);
</script>
