<template>
    <div class="flex justify-center mt-5">
        <div class="flex items-center gap-3">
            <UButton
                class="px-3 py-1 rounded border disabled:opacity-50"
                :disabled="filterState.page === 1"
                @click="
                    filterState.page--;
                    $emit('loadProducts');
                "
            >
                Précédent
            </UButton>
            <span class="text-sm"> Page {{ filterState.page }} </span>
            <UButton
                class="px-3 py-1 rounded border disabled:opacity-50"
                @click="
                    filterState.page++;
                    $emit('loadProducts');
                "
                :disabled="total == 0"
            >
                Suivant
            </UButton>
        </div>
    </div>
</template>
<script setup lang="ts">
const filterState = defineModel("filterState");
defineProps<{
    total: number;
}>();
</script>
