<template>
    <div class="w-full lg:max-w-9/12 xl:max-w-1/2 mx-auto flex flex-col gap-5">
        <!-- Header and title -->
        <PageHeader description="Détails du produit"></PageHeader>
        <!-- #Product Details -->
        <UProgress animation="swing" v-if="isLoading" />
        <UPageCard
            :title="product?.title"
            :description="product?.description"
            variant="soft"
            class="m-1"
        />
        <!-- Product Customers -->
        <ProductCustomerListing :customers="customers"></ProductCustomerListing>
    </div>
</template>

<script setup lang="ts">
const route = useRoute();
const isLoading: Ref<boolean> = ref(false);
const product = ref();
const customers = ref([]);
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
        product.value = response;
        toast.add({
            title: "Produit chargé",
            color: "success",
        });
    } catch (error) {
        console.log(error);
        toast.add({
            title: "Erreur lors du chargement du produit",
            color: "error",
        });
    } finally {
        isLoading.value = false;
    }
};
// The server that will call the customers
const loadCustomers = async () => {
    try {
        isLoading.value = true;
        const response = await $fetch(`/api/products/customers`, {
            method: "GET",
            query: {
                product_id: route.params.productId,
            },
        });
        customers.value = response.map((customer) => ({
            name: `${customer.first_name} ${customer.last_name}`,
            description: `${customer.email} || ${customer.phone}`,
        }));
        toast.add({
            title: "Clients chargés",
            color: "success",
        });
    } catch (error) {
        console.log(error);
        toast.add({
            title: "Erreur lors du chargement des clients",
            color: "error",
        });
    } finally {
        isLoading.value = false;
    }
};
// What to run the moment the page is mounted
onMounted(async () => {
    await loadProductInfo();
    await loadCustomers();
});
</script>
