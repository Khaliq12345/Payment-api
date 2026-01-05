<template>
    <UPageCard title="Produit" class="w-full">
        <template #description>
            <div class="flex items-center gap-3">
                <a
                    :href="props.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-primary hover:underline break-all text-xl"
                >
                    {{ props.url }}
                </a>
                <UButton
                    icon="i-heroicons-clipboard-document"
                    size="xs"
                    color="gray"
                    variant="ghost"
                    @click="copyUrl"
                    :ui="{ rounded: 'rounded-md' }"
                />
            </div>
        </template>
    </UPageCard>
</template>

<script setup lang="ts">
const toast = useToast();

const props = defineProps<{
    url: string;
}>();

const copyUrl = async () => {
    try {
        await navigator.clipboard.writeText(props.url);
        toast.add({ title: "URL copied to clipboard!", color: "success" });
    } catch (err) {
        toast.add({ title: "URL copied to clipboard!", color: "error" });
    }
};
</script>
