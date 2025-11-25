<template>
    <div>
        <Header />
        <UContainer class="py-8">
            <!-- Page Header -->
            <div class="mb-8">
                <h1
                    class="text-3xl font-bold text-gray-900 dark:text-white mb-2"
                >
                    Groupes WhatsApp
                </h1>
                <p class="text-gray-600 dark:text-gray-400">
                    Gérez les contributions de votre groupe
                </p>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="space-y-4">
                <USkeleton class="h-32 w-full" v-for="i in 3" :key="i" />
            </div>

            <!-- Groups Grid -->
            <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                <UCard
                    v-for="(group, index) in groups"
                    :key="index"
                    :ui="{
                        body: { padding: 'p-6' },
                        ring: 'ring-1 ring-gray-200 dark:ring-gray-800',
                        rounded: 'rounded-xl',
                    }"
                    class="hover:shadow-lg transition-shadow duration-300"
                >
                    <!-- Group Header -->
                    <div class="flex items-start justify-between mb-4">
                        <div class="flex-1 min-w-0">
                            <NuxtLink
                                :to="`/whatsapp/${group.id}`"
                                class="group block"
                            >
                                <h3
                                    class="text-lg font-semibold text-gray-900 dark:text-white truncate group-hover:text-primary-500 transition-colors"
                                >
                                    {{ group.name }}
                                </h3>
                                <p
                                    class="text-sm text-gray-500 dark:text-gray-400 mt-1"
                                >
                                    ID: {{ group.id }}
                                </p>
                            </NuxtLink>
                        </div>

                        <!-- Group Icon/Avatar -->
                        <div class="ml-4">
                            <UAvatar
                                icon="i-heroicons-user-group"
                                size="lg"
                                :ui="{
                                    background:
                                        'bg-primary-100 dark:bg-primary-900',
                                }"
                            />
                        </div>
                    </div>

                    <UDivider class="my-4" />

                    <!-- Amount Input Section -->
                    <div class="space-y-2">
                        <label
                            class="text-sm font-medium text-gray-700 dark:text-gray-300"
                        >
                            Montant de la contribution
                        </label>
                        <UInputNumber
                            v-model="group.amount"
                            size="lg"
                            @update:model-value="updateGroupAmount(group)"
                            :format-options="{
                                style: 'currency',
                                currency: 'XOF',
                                currencyDisplay: 'code',
                                currencySign: 'accounting',
                            }"
                            :ui="{
                                rounded: 'rounded-lg',
                            }"
                        />
                    </div>

                    <!-- Action Button -->
                    <UButton
                        @click="copyGroupUrl(group.id)"
                        color="primary"
                        variant="soft"
                        block
                        class="mt-4"
                        trailing-icon="i-heroicons-clipboard-document"
                    >
                        Copier le lien
                    </UButton>
                </UCard>
            </div>

            <!-- Empty State -->
            <div
                v-if="!loading && groups.length === 0"
                class="text-center py-12"
            >
                <UIcon
                    name="i-heroicons-inbox"
                    class="mx-auto h-12 w-12 text-gray-400"
                />
                <h3
                    class="mt-4 text-lg font-semibold text-gray-900 dark:text-white"
                >
                    Aucun groupe trouvé
                </h3>
                <p class="mt-2 text-gray-500 dark:text-gray-400">
                    Vous n'avez pas encore de groupes WhatsApp.
                </p>
            </div>
        </UContainer>
    </div>
</template>

<script setup lang="ts">
const groups = ref([]);
const Amountloading = ref(false);
const loading = ref(false);
const toast = useToast();

// Load all the group with their amount
const loadGroups = async () => {
    loading.value = true;
    try {
        const response = await $fetch("/api/whatsapp/chats");
        const groups_raw = Object.values(response);
        groups.value = groups_raw;
    } catch (err) {
        console.log(err);
        //show error message
        toast.add({
            title: "Erreur lors de chargement des groups whatsapp",
            icon: "i-lucide-bug",
            color: "error",
        });
    } finally {
        loading.value = false;
    }
};

// Update the group price function
const updateGroupAmount = async (group: object) => {
    Amountloading.value = true;
    try {
        await $fetch("/api/whatsapp/update-group-amount", {
            method: "POST",
            params: {
                group_id: group.id,
                amount: group.amount,
            },
        });
    } catch (err) {
        console.log(err);
        //show error message
        toast.add({
            title: "Erreur lors de la modification du prix de groupe",
            icon: "i-lucide-bug",
            color: "error",
        });
    } finally {
        Amountloading.value = false;
    }
};

// copy url to clipboard
const copyGroupUrl = async (groupId) => {
    const url = `${window.location.origin}/whatsapp/${groupId}`;
    try {
        await navigator.clipboard.writeText(url);
        toast.add({ title: "Lien copié!", color: "success" });
    } catch (err) {
        console.error("Failed to copy URL:", err);
    }
};

onMounted(async () => {
    groups.value = [];
    await loadGroups();
});
</script>
