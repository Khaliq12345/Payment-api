<template>
    <UForm
        :schema="schema"
        :state="state"
        class="space-y-7"
        @submit="onFormSubmit"
    >
        <!-- Prénom et Nom -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <UFormField label="Prénom" name="first_name" required>
                <UInput
                    v-model="state.first_name"
                    placeholder="Ex: Jean"
                    class="w-full"
                />
            </UFormField>

            <UFormField label="Nom" name="last_name" required>
                <UInput
                    v-model="state.last_name"
                    placeholder="Ex: Dupont"
                    class="w-full"
                />
            </UFormField>
        </div>

        <!-- Email -->
        <UFormField label="Email" name="email" required>
            <UInput
                v-model="state.email"
                type="email"
                placeholder="exemple@email.com"
                class="w-full"
            />
        </UFormField>

        <!-- WhatsApp et Confirmation -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pb-4">
            <UFormField
                label="WhatsApp"
                name="whatsapp_number"
                help="Format: 229..."
                description="Votre numéro qui est connecter a Whatsapp"
                required
            >
                <UInput
                    v-model="state.whatsapp_number"
                    placeholder="22997000000"
                    type="tel"
                    class="w-full"
                    :loading="isLoading"
                />
            </UFormField>

            <UFormField
                label="Confirmer WhatsApp"
                name="confirm_whatsapp_number"
                description="Répéter le numéro"
                required
            >
                <UInput
                    v-model="state.confirm_whatsapp_number"
                    placeholder="22997000000"
                    type="tel"
                    class="w-full"
                />
            </UFormField>
        </div>

        <!-- Telephone Mobile -->
        <div class="flex flex-col gap-5">
            <UCheckbox
                v-model="state.whatsapp_is_phone"
                class="w-full"
                label="Utiliser mon numéro WhatsApp comme numéro de téléphone"
                required
            />
            <!-- Phone, if whatsapp is not phone -->
            <UFormField
                label="Telephone"
                name="phone"
                v-if="!state.whatsapp_is_phone"
            >
                <UInput
                    v-model="state.phone"
                    placeholder="22997000000"
                    type="tel"
                    class="w-full"
                />
            </UFormField>
        </div>

        <!-- Pays -->
        <UFormField label="Pays" name="country" required>
            <USelect
                v-model="state.country"
                :items="countries"
                class="w-full"
            />
        </UFormField>

        <!-- Bouton de soumission -->
        <UButton
            type="submit"
            block
            size="lg"
            :loading="isLoading"
            class="mt-5"
        >
            Enregistrer
        </UButton>
    </UForm>
</template>

<script setup lang="ts">
import * as v from "valibot";
import type { CreatedCustomer, CustomerState } from "~/types/fedapay";

// Utilisation de defineModel pour mettre à jour l'état dans le parent
const model = defineModel<CustomerState>({ required: true });

const toast = useToast();
const isLoading = ref(false);

const route = useRoute();

// Options pour le menu déroulant
const countries = [
    { label: "Bénin", value: "bj" },
    { label: "Togo", value: "tg" },
    { label: "Côte d'Ivoire", value: "ci" },
    { label: "Sénégal", value: "sn" },
    { label: "Niger", value: "ne" },
    { label: "Mali", value: "ml" },
    { label: "Burkina Faso", value: "bf" },
];

// Regex simple pour numéros (autorise +, espaces, et chiffres, min 8 caractères)
const phoneRegex = /^\+?[0-9\s]{8,13}$/;

const schema = v.pipeAsync(
    v.objectAsync({
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
        whatsapp_number: v.pipeAsync(
            v.string(),
            v.checkAsync(async (input) => {
                const isValide = phoneRegex.test(input);
                if (!isValide) {
                    return false;
                } else {
                    return true;
                }
                // const isVerified = await verifyNumber(input);
                // console.log(`isVerified - ${isVerified}`);
                // return isVerified;
            }, "Numéro n'est pas sur whatsapp"),
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
    whatsapp_is_phone: true,
    phone: undefined,
});

const verifyNumber = async (number: number) => {
    isLoading.value = true;
    try {
        const response = await $fetch("/api/whatsapp/verify", {
            query: {
                number: number,
            },
        });
        return response.existsWhatsapp;
    } catch (error) {
        console.log(error);
        return false;
    } finally {
        isLoading.value = false;
    }
};

// Soumission
const onFormSubmit = async (event: any) => {
    isLoading.value = true;

    try {
        const response = await $fetch("/api/fedapay/create-customer", {
            method: "POST",
            body: {
                firstName: state.first_name,
                lastName: state.last_name,
                email: state.email,
                phone: state.whatsapp_is_phone
                    ? state.whatsapp_number
                    : state.phone,
                whatsappPhone: state.whatsapp_number,
                country: state.country,
                productId: route.params.productId,
            },
        });

        toast.add({
            title: "Succès",
            description: `Client ${response.full_name} créé avec succès`,
            color: "success",
        });

        // Mise à jour du model
        model.value = response;
        console.log(response);
    } catch (error: any) {
        console.error("Erreur API:", error);
        const status = error?.status || 500;
        const message =
            error?.data?.message || error?.message || "Une erreur est survenue";

        toast.add({
            title: "Erreur",
            description: `(${status}) ${message}`,
            color: "error",
        });
    } finally {
        isLoading.value = false;
    }
};
</script>
