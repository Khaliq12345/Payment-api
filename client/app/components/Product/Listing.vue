<template>
    <!-- Product Listing -->
    <div v-for="product in products" class="flex flex-col">
        <UPageCard icon="i-lucide-file-digit" variant="soft" class="m-3">
            <template #title>
                <ULink
                    :to="`${$config.public.FRONTEND_URL}/admin/products/${product.id}`"
                    >{{ product.title }}</ULink
                >
            </template>
            <div class="mb-2">Prix : {{ product.price }} XOF</div>
            <!-- Product url to copy -->
            <div class="flex items-center gap-2">
                <ProductCopyURL :product-id="product.id"></ProductCopyURL>
            </div>
            <!-- Edit or delete product -->
            <div class="flex justify-between">
                <ProductEditForm
                    v-model:title="product.title"
                    v-model:description="product.description"
                    v-model:price="product.price"
                    :productId="product.id"
                ></ProductEditForm>

                <ProductDeleteModal
                    :product-id="product.id"
                    @deleted="$emit('deleted')"
                ></ProductDeleteModal>
            </div>
        </UPageCard>
    </div>
</template>
<script setup lang="ts">
defineProps<{
    products: [];
}>();
defineEmits(["deleted"]);
</script>
