<template>
    <div class="w-full">
        <UInput
            :model-value="text"
            readonly
            class="flex-1 w-full"
            color="gray"
            variant="outline"
            size="sm"
        >
            <template #trailing>
                <UButton
                    color="gray"
                    variant="ghost"
                    icon="i-lucide-copy"
                    size="xs"
                    @click.stop.prevent="handleCopy()"
                />
            </template>
        </UInput>
    </div>
</template>

<script setup lang="ts">
const props = defineProps<{
    productId: string;
}>();
const { copyToClipboard } = useClipboard();
const config = useRuntimeConfig();
const text = `${config.public.FRONTEND_URL}/product/${props.productId}`;

const handleCopy = () => {
    copyToClipboard(text);
};

// const toast = useToast();
// const copyToClipboard = async () => {
//     try {
//         await navigator.clipboard.writeText(text);
//         // Optional: Show a success notification
//         toast.add({
//             title: "Lien copié !",
//             icon: "i-lucide-check-circle",
//             color: "green",
//             timeout: 2000,
//         });
//     } catch (err) {
//         console.error("Échec de la copie : ", err);
//     }
// };
</script>
