<template>
    <div>
        <h1>WhatsApp Group: {{ groupId }}</h1>
    </div>
</template>

<script setup lang="ts">
const route = useRoute()
const groupId = computed(() => route.params.groupId)
</script>

