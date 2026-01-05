<template>
    <!-- Succès -->
    <div v-if="sent" class="text-center">
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
                    :to="transaction.drive_link"
                    target="_blank"
                    color="success"
                    size="xl"
                    block
                    class="text-xl font-bold py-6"
                >
                    Go to the folder / Go to the meeting page to book your place
                </UButton>
            </template>
        </UCard>
    </div>

    <!-- Bouton Send the email -->
    <UButton
        v-if="transaction.status === 'approved' && !sent"
        @click="sendClientEmail"
        :loading="sending"
        color="success"
        size="xl"
        block
        class="font-bold text-xl py-8 shadow-xl hover:shadow-2xl transition-all duration-300"
    >
        Envoie moi le lien
    </UButton>
</template>

<script setup lang="ts">
const props = defineProps<{
    transaction: object;
}>();

// États WhatsApp
const sending = ref(false);
const productLink = ref<string | null>(null);
const sent = ref(false);

const toast = useToast();
// Send client the email
const sendClientEmail = async () => {
    // verify if we have info about the transaction
    if (!props.transaction) return;
    sending.value = true;
    try {
        // send the requests to add the user to the group
        const response = await $fetch("/api/email/send", {
            method: "POST",
            query: {
                transaction_id: props.transaction.id,
            },
        });

        sent.value = true;
        toast.add({
            title: "We sent you an email with the product",
            icon: "i-lucide-badge-check",
            color: "success",
        });
    } catch (err) {
        // in case of error, log the error and display the notification
        console.error(err);
        toast.add({
            title: "Erreur réseau. Réessayez dans quelques instants.",
            icon: "i-lucide-bug",
            color: "error",
        });
    } finally {
        sending.value = false;
    }
};
</script>
