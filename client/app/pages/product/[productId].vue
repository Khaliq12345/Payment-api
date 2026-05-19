<template>
    <div class="lg:max-w-9/12 xl:max-w-1/2 mx-auto flex flex-col gap-10">
        <!-- Hero Image Cover -->
        <div
            v-if="productData?.media_url"
            class="w-full overflow-hidden rounded-b-2xl shadow-lg"
        >
            <img
                :src="productData?.media_url"
                :alt="productData?.title"
                class="w-full h-auto block"
            />
        </div>

        <div class="p-3 flex flex-col gap-10">
            <!-- Header of the page -->
            <UPageHeader
                :headline="`Prix: ${productData?.price} XOF`"
                :title="productData?.title"
                :description="productData?.description"
                :ui="{
                    title: 'text-xl',
                    description: 'text-sm',
                }"
            />
            <UProgress animation="swing" v-if="isLoading" />
            <!-- Customer Form to fill -->
            <ProductCustomerForm v-model="customerData" v-if="!customerData" />
            <!-- Affiche la transaction une fois le client créé -->
            <Transaction v-else :customer="customerData" />
        </div>
    </div>
</template>

<script setup lang="ts">
import type { CustomerState } from "~/types/fedapay";

const route = useRoute();
const productId = route.params.productId;

const customerData = ref(null);
const productData = ref();
const isLoading: Ref<boolean> = ref(false);

const toast = useToast();
// The server that will call the product
const loadProductInfo = async () => {
    try {
        isLoading.value = true;
        const response = await $fetch(
            `/api/products/${route.params.productId}`,
            {
                method: "GET",
            },
        );
        productData.value = response;
        console.log(productData.value);
        toast.add({
            title: "Product Loaded",
            color: "success",
        });
    } catch (error) {
        console.log(error);
        toast.add({
            title: "Error loading product",
            color: "error",
        });
    } finally {
        isLoading.value = false;
    }
};

onMounted(async () => {
    await loadProductInfo();
});
</script>
