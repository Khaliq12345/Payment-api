<template>
    <UHeader title="DIGI-PRODUCTS">
        <UNavigationMenu :items="items" v-if="isAdmin()" />
        <template #right>
            <UColorModeButton />
            <UTooltip text="Déconnexion" v-if="isAdmin()">
                <UButton
                    color="neutral"
                    variant="ghost"
                    icon="i-lucide-log-out"
                    aria-label="Déconnexion"
                    @click="logout()"
                />
            </UTooltip>
        </template>
        <template #body>
            <UNavigationMenu
                :items="items"
                orientation="vertical"
                class="-mx-2.5"
            />
        </template>
    </UHeader>
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";
const route = useRoute();
const items = computed<NavigationMenuItem[]>(() => [
    {
        label: "Produits",
        to: "/admin/products",
        icon: "i-lucide-book-open",
    },
    {
        label: "Ajouter un nouveau produit",
        icon: "i-lucide-box",
        to: "/admin/products/create",
    },
]);
const isAdmin = () => {
    if (route.path.includes("/admin")) {
        return true;
    }
    return false;
};
const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("expired_at");
    navigateTo("/login");
};
</script>
