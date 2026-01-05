<template>
    <UPageHeader
        :description="description"
        :ui="{
            root: 'p-3',
            description: 'uppercase',
        }"
    />
</template>

<script setup lang="ts">
defineProps<{
    description: string;
}>();
</script>
