<template>
    <div class="m-4">
        <UCard class="max-w-2xl mx-auto">
            <template #header>
                <h2 class="text-2xl text-center font-bold">
                    Résultat du paiement
                </h2>
                <UProgress animation="swing" v-if="loading" />
            </template>

            <!-- Succès -->
            <div v-if="transaction && status == 'approved'" class="space-y-8">
                <!-- Statut Section -->
                <div
                    class="flex justify-between items-center py-4 border-b border-gray-200"
                >
                    <span class="text-lg font-semibold"
                        >Statut du paiement</span
                    >
                    <UBadge
                        :color="
                            transaction.status === 'approved'
                                ? 'success'
                                : 'error'
                        "
                        variant="solid"
                    >
                        {{ transaction.status.toUpperCase() }}
                    </UBadge>
                </div>

                <!-- Infos client -->
                <div class="rounded-xl p-6 text-sm">
                    <dl class="grid grid-cols-2 gap-x-6 gap-y-4">
                        <template v-for="item in details" :key="item.label">
                            <dt class="font-bold text-gray-500">
                                {{ item.label }}
                            </dt>
                            <dd
                                :class="{
                                    'font-mono text-xs': item.mono,
                                    'font-medium': item.medium,
                                }"
                            >
                                {{ item.value }}
                            </dd>
                        </template>
                    </dl>
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

                <!-- if email product -->
                <EmailSuccess
                    :transaction="transaction"
                    v-if="transaction.drive_link"
                ></EmailSuccess>
                <!-- if whatsapp product -->
                <WhatsappSuccess
                    :transaction="transaction"
                    v-if="transaction.group_id"
                ></WhatsappSuccess>
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
                <p class="text-xl font-bold text-red-800">
                    Paiement non validé
                </p>
                <p class="mt-3 text-red-700">Statut : {{ status }}</p>
            </div>
        </UCard>
    </div>
</template>

<script setup lang="ts">
const route = useRoute();

// Récupération transaction
const status = ref(route.query.status);
const transId = route.query.id;
const transaction = ref();
const details = ref([]);
const loading = ref(false);

//toast
const toast = useToast();

onMounted(async () => {
    // check if the transaction is approved
    if (status.value !== "approved") return {};
    loading.value = true;
    try {
        // send the requests to get the transaction info
        const response = await $fetch("/api/fedapay/transaction", {
            query: { transactionId: transId },
        });

        // extract the transaction info and display success notification
        transaction.value = response;
        status.value = transaction.value.status;
        toast.add({
            title: "Verification de transaction reussi",
            icon: "i-lucide-check-check",
            color: "success",
        });
        details.value = [
            { label: "ID", value: transaction.value.id, mono: true },
            {
                label: "Référence",
                value: transaction.value.reference,
                mono: true,
            },
            { label: "Titre", value: transaction.value.title },
            {
                label: "Client",
                value: transaction.value.full_name,
                medium: true,
            },
            {
                label: "WhatsApp",
                value: formatWhatsapp(transaction.value.whatsapp_phone),
                mono: true,
            },
            {
                label: "Date",
                value: formatDate(
                    transaction.value.approved_at ??
                        transaction.value.created_at,
                ),
            },
        ];
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
