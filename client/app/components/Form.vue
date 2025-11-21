<template>
    <UCard class="max-w-xl mx-auto shadow-md">
        <template #header>
            <h2 class="text-xl font-bold text-gray-800 dark:text-white">
                Nouveau Client
            </h2>
        </template>

        <UForm
            :schema="schema"
            :state="state"
            class="space-y-5"
            @submit="onFormSubmit"
        >
            <!-- Prénom et Nom -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <UFormGroup label="Prénom" name="first_name" required>
                    <UInput v-model="state.first_name" placeholder="Ex: Jean" />
                </UFormGroup>

                <UFormGroup label="Nom" name="last_name" required>
                    <UInput
                        v-model="state.last_name"
                        placeholder="Ex: Dupont"
                    />
                </UFormGroup>
            </div>

            <!-- Email -->
            <UFormGroup label="Email" name="email" required>
                <UInput
                    v-model="state.email"
                    type="email"
                    placeholder="exemple@email.com"
                />
            </UFormGroup>

            <!-- WhatsApp et Confirmation -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <UFormGroup
                    label="WhatsApp"
                    name="whatsapp_number"
                    help="Format: 229..."
                    required
                >
                    <UInput
                        v-model="state.whatsapp_number"
                        placeholder="22997000000"
                        type="tel"
                    />
                </UFormGroup>

                <UFormGroup
                    label="Confirmer WhatsApp"
                    name="confirm_whatsapp_number"
                    required
                >
                    <UInput
                        v-model="state.confirm_whatsapp_number"
                        placeholder="Répéter le numéro"
                        type="tel"
                    />
                </UFormGroup>
            </div>

            <!-- Pays -->
            <UFormGroup label="Pays" name="country" required>
                <USelect
                    v-model="state.country"
                    :options="countries"
                    option-attribute="label"
                    value-attribute="value"
                />
            </UFormGroup>

            <!-- Bouton de soumission -->
            <div class="pt-4">
                <UButton type="submit" block size="lg" :loading="isLoading">
                    Enregistrer
                </UButton>
            </div>
        </UForm>
    </UCard>
</template>

<script setup lang="ts">
import * as v from "valibot";
import type { CreatedCustomer, CustomerState } from "~/types/fedapay";

// Utilisation de defineModel pour mettre à jour l'état dans le parent
const model = defineModel<CustomerState>({ required: true });

const toast = useToast();
const isLoading = ref(false);

// Options pour le menu déroulant
const countries = [
    { label: "Bénin", value: "bj" },
    { label: "Togo", value: "tg" },
    { label: "Côte d'Ivoire", value: "ci" },
    { label: "Sénégal", value: "sn" },
];

// Regex simple pour numéros (autorise +, espaces, et chiffres, min 8 caractères)
const phoneRegex = /^\+?[0-9\s]{8,13}$/;

const schema = v.pipe(
    v.object({
        first_name: v.pipe(
            v.string(),
            v.minLength(2, "Le prénom doit contenir au moins 2 caractères"),
        ),
        last_name: v.pipe(
            v.string(),
            v.minLength(2, "Le nom doit contenir au moins 2 caractères"),
        ),
        email: v.pipe(
            v.string(),
            v.email("Veuillez entrer une adresse email valide"),
        ),
        whatsapp_number: v.pipe(
            v.string(),
            v.check(
                (input) => phoneRegex.test(input),
                "Numéro invalide (ex: 22997...)",
            ),
        ),
        confirm_whatsapp_number: v.string("La confirmation est requise"),
        country: v.string("Le pays est requis"),
    }),
    // Utilisation de v.forward pour contrôler l'équivalence des numéros WhatsApp
    v.forward(
        v.check(
            (input) => input.whatsapp_number === input.confirm_whatsapp_number,
            "Les numéros WhatsApp ne correspondent pas.",
        ),
        ["confirm_whatsapp_number"],
    ),
);

type Schema = v.InferInput<typeof schema>;

// État initial du formulaire
const state = reactive({
    first_name: "",
    last_name: "",
    email: "",
    whatsapp_number: "",
    confirm_whatsapp_number: "",
    country: "bj", // Valeur par défaut
});

// Soumission
const onFormSubmit = async (event: any) => {
    isLoading.value = true;

    try {
        const response = await $fetch<CreatedCustomer>(
            "/api/fedapay/create-customer",
            {
                method: "POST",
                body: {
                    first_name: state.first_name,
                    last_name: state.last_name,
                    email: state.email,
                    whatsapp_number: state.whatsapp_number,
                    country: state.country,
                },
            },
        );

        toast.add({
            title: "Succès",
            description: `Client ${response.full_name} créé avec succès`,
            color: "green",
        });

        // Mise à jour du model
        model.value = {
            response: response,
            whatsapp_number: state.whatsapp_number,
        };
    } catch (error: any) {
        console.error("Erreur API:", error);
        const status = error?.status || 500;
        const message =
            error?.data?.message || error?.message || "Une erreur est survenue";

        toast.add({
            title: "Erreur",
            description: `(${status}) ${message}`,
            color: "red",
        });
    } finally {
        isLoading.value = false;
    }
};
</script>
