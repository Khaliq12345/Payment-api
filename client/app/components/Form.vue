<template>
    <UCard class="max-w-xl mx-auto mt-10">
        <template #header>
            <h2 class="text-xl font-bold">Nouveau Client</h2>
        </template>

        <UForm
            :schema="schema"
            :state="state"
            class="space-y-4"
            @submit="onFormSubmit"
        >
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <UFormGroup label="Prénom" name="first_name" required>
                    <UInput v-model="state.first_name" />
                </UFormGroup>

                <UFormGroup label="Nom" name="last_name" required>
                    <UInput v-model="state.last_name" />
                </UFormGroup>
            </div>

            <UFormGroup label="Email" name="email" required>
                <UInput v-model="state.email" type="email" />
            </UFormGroup>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <UFormGroup label="WhatsApp" name="whatsapp_number" required>
                    <UInput
                        v-model="state.whatsapp_number"
                        placeholder="+229..."
                    />
                </UFormGroup>

                <UFormGroup
                    label="Confirmer"
                    name="confirm_whatsapp_number"
                    required
                >
                    <UInput
                        v-model="state.confirm_whatsapp_number"
                        placeholder="Répéter..."
                    />
                </UFormGroup>
            </div>

            <UFormGroup label="Pays" name="country" required>
                <USelect
                    v-model="state.country"
                    :options="countries"
                    option-attribute="label"
                    value-attribute="value"
                />
            </UFormGroup>

            <div class="pt-4">
                <UButton type="submit" block :loading="loading">
                    Enregistrer
                </UButton>
            </div>
        </UForm>
    </UCard>
</template>

<script setup lang="ts">
import * as v from "valibot";
import type { CreatedCustomer, SuccessData } from "~/types/fedapay";

// 1. Définition du schéma simplifié (Juste "Requis" partout)
const schema = v.object({
    first_name: v.pipe(v.string(), v.minLength(1, "Requis")),
    last_name: v.pipe(v.string(), v.minLength(1, "Requis")),
    email: v.pipe(v.string(), v.minLength(1, "Requis")),
    whatsapp_number: v.pipe(v.string(), v.minLength(1, "Requis")),
    confirm_whatsapp_number: v.pipe(v.string(), v.minLength(1, "Requis")),
    country: v.pipe(v.string(), v.minLength(1, "Requis")),
});

// Type inféré automatiquement
type Schema = v.InferOutput<typeof schema>;

// 2. Props
const props = defineProps<{
    loading?: boolean;
}>();

// Émettre l'événement de succès
const emit = defineEmits<{
    success: [data: SuccessData];
}>();

const toast = useToast();

// Options pour le menu déroulant
const countries = [
    { label: "Bénin", value: "bj" },
    { label: "Togo", value: "tg" },
    { label: "Côte d'Ivoire", value: "ci" },
    { label: "Sénégal", value: "sn" },
];

// État initial
const state = reactive<Schema>({
    first_name: "",
    last_name: "",
    email: "",
    whatsapp_number: "",
    confirm_whatsapp_number: "",
    country: "bj",
});

// Soumission du formulaire
const onFormSubmit = async () => {
    if (props.loading) return;

    try {
        const response = await $fetch<CreatedCustomer>(
            "/api/fedapay/create-customer",
            {
                method: "POST",
                body: state,
            },
        );
        console.log("Client créé:", response);
        toast.add({
            title: "Client créé",
            description: `Bienvenue ${response.full_name}`,
        });
        emit("success", {
            customer: response,
            whatsapp_number: state.whatsapp_number,
        });
    } catch (error: any) {
        console.error("Erreur lors de la création du client:", error);
        const status = error?.status || 500;
        const message =
            error?.data?.message || error?.message || "Une erreur est survenue";
        toast.add({
            title: "Erreur",
            description: `Erreur ${status}: ${message}`,
            color: "red",
        });
    }
};
</script>
