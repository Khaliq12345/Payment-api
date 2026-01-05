<template>
    <div class="w-full lg:max-w-9/12 xl:max-w-1/2 mx-auto">
        <!-- Header and title -->
        <PageHeader description="Vos Produits"></PageHeader>

        <UPageBody>
            <!-- Filters for the products -->
            <UPageCard class="m-2 dark: bg-green-700 light:bg-green-50">
                <div class="flex flex-col gap-4">
                    <UTextarea
                        icon="i-lucide-search"
                        size="md"
                        variant="outline"
                        placeholder="Rechercher..."
                        :rows="1"
                        v-model="filterState.name"
                    ></UTextarea>
                    <div class="gap-5 grid lg:grid-cols-2">
                        <UInputNumber
                            v-model="filterState.price"
                            placeholder="Prix"
                        />
                        <USelectMenu
                            v-model="filterState.platform"
                            :items="items"
                            clear
                            clear-icon="i-lucide-trash"
                        />
                        <!-- Date -->
                        <UInputDate ref="inputDate" v-model="date" range>
                            <template #trailing>
                                <UPopover
                                    :reference="inputDate?.inputsRef[0]?.$el"
                                >
                                    <UButton
                                        color="neutral"
                                        variant="link"
                                        size="sm"
                                        icon="i-lucide-calendar"
                                        aria-label="Sélectionner une plage de dates"
                                        class="px-0"
                                    />

                                    <template #content>
                                        <UCalendar
                                            v-model="date"
                                            class="p-2"
                                            :number-of-months="2"
                                            range
                                        />
                                    </template>
                                </UPopover>
                            </template>
                        </UInputDate>
                    </div>
                </div>
                <UButton @click="loadProducts()">Recharger</UButton>
            </UPageCard>

            <!-- Pagination for the products -->
            <div class="flex justify-center mt-5">
                <Pagination
                    v-model:filterState="filterState"
                    :total="products.length"
                    @load-products="loadProducts()"
                ></Pagination>
            </div>

            <UProgress animation="swing" v-if="isLoading" />
            <ProductListing
                :products="products"
                @deleted="loadProducts()"
            ></ProductListing>

            <!-- Pagination for the products -->
            <div class="flex justify-center mt-5">
                <Pagination
                    v-model:filterState="filterState"
                    :total="products.length"
                    @load-products="loadProducts()"
                ></Pagination>
            </div>
        </UPageBody>
    </div>
</template>

<script setup lang="ts">
import type { SelectItem } from "@nuxt/ui";
import { CalendarDate } from "@internationalized/date";

const date = shallowRef({
    start: undefined,
    end: undefined,
});

const inputDate = useTemplateRef("inputDate");

// Setup all variables to use
const items = ref<SelectItem[]>([
    {
        label: "Email",
        value: "email",
    },
    {
        label: "WhatsApp",
        value: "whatsapp",
    },
    {
        label: "Tous",
        value: "all",
    },
]);

const products = ref([]);
const isLoading: Ref<boolean> = ref(false);

const filterState = reactive({
    platform: undefined,
    price: undefined,
    page: 1,
    name: undefined,
});

const toast = useToast();

// The server that will call the products
const loadProducts = async () => {
    try {
        isLoading.value = true;
        const response = await $fetch("/api/products", {
            method: "GET",
            query: {
                platform: filterState.platform?.value,
                price: filterState.price,
                page: filterState.page,
                name: filterState.name,
                start_date: date.value.start?.toString(),
                end_date: date.value.end?.toString(),
            },
        });
        products.value = response;
        toast.add({
            title: "Produits chargés",
            color: "success",
        });
    } catch (error) {
        console.log(error);
        toast.add({
            title: "Erreur lors du chargement des produits",
            color: "error",
        });
    } finally {
        isLoading.value = false;
    }
};

// What to run the moment the page is mounted
onMounted(async () => {
    await loadProducts();
});
</script>
