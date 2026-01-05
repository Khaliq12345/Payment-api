<template>
    <div class="w-full flex items-center flex-col">
        <div class="lg:max-w-9/12 xl:max-w-1/2 w-full">
            <!-- Header of the page -->
            <PageHeader description="Créer un nouveau produit"></PageHeader>

            <!-- Product form -->
            <UPageBody>
                <UPageCard class="border-2 border-green-100 m-2">
                    <ProductCreateForm :chats="chats"></ProductCreateForm>
                </UPageCard>
            </UPageBody>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { SelectMenuItem } from "@nuxt/ui";

const chats = ref<SelectMenuItem[]>([]);

onMounted(async () => {
    const response = await $fetch("/api/whatsapp/chats", {
        method: "GET",
    });

    response.forEach((chat) => {
        if (!chat.notSpam) return;
        chats.value.push({
            label: chat.name,
            value: chat.id,
        });
    });
});
</script>
