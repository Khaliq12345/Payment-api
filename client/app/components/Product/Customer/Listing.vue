<template>
    <UPageList>
        <div class="overline p-2 text-green-700">CLIENTS</div>
        <UPageCard
            v-for="(user, index) in customers"
            :key="index"
            variant="ghost"
        >
            <template #body>
                <UUser
                    :name="user.name"
                    :description="user.description"
                    size="xl"
                    class="relative"
                />
            </template>
        </UPageCard>
    </UPageList>
</template>
<script setup lang="ts">
defineProps<{
    customers: object[];
}>();
</script>
