<template>
    <UModal>
        <UButton label="Modifier" color="neutral" variant="subtle" />
        <template #content>
            <UCard>
                <UForm :schema="schema" class="space-y-4" @submit="onSubmit">
                    <UFormField label="Titre" name="title">
                        <UInput
                            v-model="title"
                            :placeholder="title"
                            class="w-full"
                        />
                    </UFormField>
                    <UFormField label="Description" name="description">
                        <UTextarea
                            v-model="description"
                            :placeholder="description"
                            class="w-full"
                        />
                    </UFormField>
                    <UFormField label="Prix" name="price">
                        <UInputNumber
                            v-model="price"
                            :placeholder="price.toString()"
                            class="w-full"
                        />
                    </UFormField>
                    <UButton
                        type="submit"
                        :loading="loading"
                        @click="onSubmit()"
                    >
                        Enregistrer les modifications
                    </UButton>
                </UForm>
            </UCard>
        </template>
    </UModal>
</template>

<script setup lang="ts">
import * as v from "valibot";
import type { FormSubmitEvent } from "#ui/types";
const props = defineProps<{
    productId: string;
}>();
const title = defineModel("title");
const description = defineModel("description");
const price = defineModel("price");
const schema = v.object({
    title: v.pipe(v.string(), v.minLength(1, "Le titre est requis")),
    description: v.pipe(
        v.string(),
        v.minLength(1, "La description est requise"),
    ),
    price: v.pipe(
        v.number(),
        v.minValue(100, "Le prix ne peut pas être inférieur à 100 XOF"),
    ),
});
const toast = useToast();
const loading = ref(false);
const onSubmit = async () => {
    try {
        loading.value = true;
        await $fetch("/api/products/update", {
            method: "POST",
            query: {
                product_id: props.productId,
            },
            body: {
                title: title.value,
                description: description.value,
                price: price.value,
            },
        });
        toast.add({
            title: "Produit mis à jour !",
            icon: "i-lucide-check-circle",
            color: "success",
        });
    } catch (error) {
        console.error("Échec de la mise à jour du produit", error);
        toast.add({
            title: "Erreur lors de la mise à jour du produit !",
            icon: "i-lucide-bug",
            color: "error",
        });
    } finally {
        loading.value = false;
    }
};
</script>
