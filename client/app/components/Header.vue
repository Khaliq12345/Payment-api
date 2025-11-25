<template>
    <UHeader
        :ui="{
            center: 'flex justify-center w-full',
            left: 'hidden',
            container: 'flex items-center justify-center h-full',
        }"
    >
        <template #default>
            <div class="flex items-center gap-3 w-full justify-around">
                <span class="font-bold text-xl">Paiement Groupe Whatsapp</span>

                <UButton
                    icon="i-heroicons-arrow-right-on-rectangle"
                    color="error"
                    variant="solid"
                    @click="logout"
                    class="ml-2"
                >
                </UButton>
            </div>
        </template>
    </UHeader>
</template>

<script setup lang="ts">
const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("expired_at");
    navigateTo("/login");
};
</script>
