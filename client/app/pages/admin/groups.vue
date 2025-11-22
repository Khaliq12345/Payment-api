<template>
    <UContainer class="flex md:justify-center md:w-2xl w-full shadow-xl/30">
        <!-- Loading -->
        <UProgress animation="swing" v-if="loading" />

        <!-- List of the groups -->
        <UPageList>
            <UPageCard
                v-for="(group, index) in groups"
                :key="index"
                variant="ghost"
                target="_blank"
            >
                <!-- Group info and input section -->
                <template #body>
                    <UUser
                        :name="group.name"
                        :description="`ID: ${group.id}`"
                        class="relative"
                        :to="`/whatsapp/${group.id}`"
                        :ui="{
                            name: 'text-sm md:text-md lg:text-lg',
                        }"
                    />
                    <!-- Input section -->
                    <div class="flex-col gap-4">
                        <div class="w-50">
                            <UInputNumber
                                v-model="group.amount"
                                size="sm"
                                @update:model-value="updateGroupAmount(group)"
                                :format-options="{
                                    style: 'currency',
                                    currency: 'XOF',
                                    currencyDisplay: 'code',
                                    currencySign: 'accounting',
                                }"
                            />
                        </div>
                    </div>
                </template>
            </UPageCard>
        </UPageList>
    </UContainer>
</template>

<script setup lang="ts">
import { useClipboard } from "@vueuse/core";

const { copy, copied } = useClipboard();
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

onMounted(async () => {
    groups.value = [];
    await loadGroups();
});
</script>
