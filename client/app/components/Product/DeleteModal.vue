<template>
    <UModal
        v-model:open="isOpen"
        title="Supprimer le produit"
        description="Êtes-vous sûr de vouloir supprimer ce produit ?"
        :close="{
            color: 'primary',
            variant: 'outline',
            class: 'rounded-full',
        }"
    >
        <UButton
            label="Supprimer"
            color="red"
            variant="soft"
            icon="i-heroicons-trash-20-solid"
        />
        <template #body>
            <p class="text-gray-600 dark:text-gray-400">
                Cette action est irréversible. Le produit sera définitivement
                supprimé ainsi que toutes les données associées.
            </p>
        </template>
        <template #footer>
            <UButton
                label="Annuler"
                color="gray"
                variant="soft"
                @click="isOpen = false"
            />
            <UButton
                label="Supprimer"
                color="red"
                variant="soft"
                icon="i-heroicons-trash-20-solid"
                :loading="loading"
                @click="deleteProduct"
            />
        </template>
    </UModal>
</template>
<script setup lang="ts">
const props = defineProps<{
    productId: string;
}>();
const emit = defineEmits(["deleted"]);
const toast = useToast();
const loading = ref(false);
const isOpen = ref(false);
const deleteProduct = async () => {
    try {
        loading.value = true;
        await $fetch("/api/products/delete", {
            method: "DELETE",
            query: {
                product_id: props.productId,
            },
        });
        toast.add({
            title: "Produit supprimé !",
            icon: "i-lucide-check-circle",
            color: "success",
        });
        isOpen.value = false;
        emit("deleted");
    } catch (error) {
        console.error("Échec de la suppression du produit", error);
        toast.add({
            title: "Erreur lors de la suppression du produit !",
            icon: "i-lucide-bug",
            color: "error",
        });
    } finally {
        loading.value = false;
    }
};
</script>
