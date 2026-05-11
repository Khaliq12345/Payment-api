<template>
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
                    Me rediriger vers le groupe
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

    <!-- Bouton WhatsApp -->
    <UButton
        v-if="transaction.status === 'approved' && !inviteLink && !hasAdded"
        @click="addToWhatsappGroup"
        :loading="adding"
        color="success"
        size="xl"
        block
        class="font-bold text-xl py-8 shadow-xl hover:shadow-2xl transition-all duration-300"
    >
        Rejoindre le groupe WhatsApp maintenant
    </UButton>
</template>

<script setup lang="ts">
const props = defineProps<{
    transaction: object;
}>();

// États WhatsApp
const loading = ref(false);
const adding = ref(false);
const hasAdded = ref(false);
const inviteLink = ref<string | null>(null);

const toast = useToast();
// Ajout au groupe WhatsApp
const addToWhatsappGroup = async () => {
    // verify if we have info about the transaction
    if (!props.transaction) return;
    adding.value = true;
    try {
        // send the requests to add the user to the group
        const response = await $fetch("/api/whatsapp/add", {
            method: "POST",
            query: {
                transaction_id: props.transaction.id,
            },
        });

        // check if user is added and display success notification
        inviteLink.value = response;
        toast.add({
            title: "Clickez sur le lien d'invitation du groupe",
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
        adding.value = false;
    }
};
</script>
