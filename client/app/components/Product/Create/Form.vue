<template>
    <ProductCreateUrlCard
        :url="productUrl"
        v-if="productUrl"
    ></ProductCreateUrlCard>

    <UForm :schema="schema" :state="state" @submit="onSubmit" v-else>
        <!-- Just the title and description form -->
        <div class="gap-5 flex-col flex">
            <UFormField label="Titre" name="title">
                <UInput
                    placeholder="Entrez le titre du produit"
                    class="w-full"
                    v-model="state.title"
                />
            </UFormField>

            <UFormField label="Description" name="description">
                <UTextarea
                    placeholder="Entrez la description du produit"
                    class="w-full"
                    v-model="state.description"
                />
            </UFormField>
        </div>

        <USeparator label="Détails" class="my-8" />

        <!-- Other details like price and platform -->
        <div class="grid grid-cols-1 md:grid-cols-2 w-full gap-5">
            <UFormField label="Prix" name="price">
                <UInputNumber
                    placeholder="Prix du produit"
                    class="w-full"
                    v-model="state.price"
                />
            </UFormField>

            <UFormField label="Plateforme" name="platform">
                <USelect
                    v-model="state.platform"
                    :items="items"
                    class="w-full"
                />
            </UFormField>

            <UFormField
                v-if="state.platform == 'email'"
                name="drive_link"
                label="Lien Drive/Événement"
                description="Collez le lien vers le drive ou l'événement"
            >
                <UInput
                    placeholder=""
                    class="w-full"
                    v-model="state.drive_link"
                />
            </UFormField>

            <UFormField
                v-if="
                    state.drive_link &&
                    state.drive_link.startsWith('https://drive.google.com')
                "
                name="service_email_added"
            >
                <UCheckbox
                    v-model="state.service_email_added"
                    label="Confirmer que l'email de service a été ajouté"
                />
                <div class="text-xs font-bold w-full">
                    {{ EMAIL_SERVICE }}
                </div>
            </UFormField>

            <UFormField
                name="whatsapp_groupid"
                v-if="state.platform == 'whatsapp'"
                label="Lien du groupe WhatsApp"
                description="Collez le lien vers le groupe WhatsApp"
            >
                <USelect
                    class="w-full"
                    :search-input="{
                        placeholder: 'Filtrer...',
                        icon: 'i-lucide-search',
                    }"
                    v-model="state.whatsapp_groupid"
                    :items="chats"
                    placeholder="Sélectionnez un groupe WhatsApp"
                />
            </UFormField>
        </div>

        <UButton type="submit" class="mt-10 bg-green-500" block>
            Soumettre
        </UButton>
    </UForm>
</template>

<script setup lang="ts">
import type { SelectItem, SelectMenuItem } from "@nuxt/ui";
import * as v from "valibot";

const props = defineProps<{
    chats: SelectMenuItem[];
}>();

let EMAIL_SERVICE;
const config = useRuntimeConfig();
console.log(config);
EMAIL_SERVICE = config.public.emailService;
const productUrl = ref();
const chat = ref();

// # Setup the form validator schema
const schema = v.object({
    title: v.string("Le titre du produit ne peut pas être null"),
    description: v.string("La description du produit ne peut pas être null"),
    price: v.pipe(
        v.number("Le prix doit être un nombre"),
        v.minValue(100, "Le prix doit être plus que 100 XOF"),
    ),
    platform: v.string("La plateforme ne peut pas être null"),
    drive_link: v.pipe(
        v.string(),
        v.check(
            (value) =>
                value.includes("drive.google.com") ||
                value.includes("calendar.app.google"),
            "L'entrée doit être un lien Google Drive ou Google Calendar",
        ),
    ),
    whatsapp_groupid: v.string(),
});

type Schema = v.InferOutput<typeof schema>;

// Setup the reactive state to hold the form values
const state = reactive({
    title: null,
    description: null,
    price: 0,
    platform: null,
    drive_link: "",
    whatsapp_groupid: "",
    service_email_added: null,
});

const items = ref<SelectItem[]>([
    {
        label: "WhatsApp",
        value: "whatsapp",
    },
    {
        label: "Email",
        value: "email",
    },
]);

const toast = useToast();

// Server to create the product
async function onSubmit(event) {
    if (!state.service_email_added) {
        toast.add({
            title: "Erreur",
            description:
                "Veuillez ajouter l'email de service au dossier Google Drive avant de continuer",
            color: "error",
        });
        return;
    }
    try {
        const response = await $fetch("/api/products/add", {
            method: "POST",
            body: state,
        });
        const product_id = response.id;
        productUrl.value = `${config.public.FRONTEND_URL}/product/${product_id}`;
        toast.add({
            title: "Succès",
            description: "Produit créé avec succès",
            color: "success",
        });
    } catch (error) {
        console.log(error);
        toast.add({
            title: "Erreur",
            description: error.data.message,
            color: "error",
        });
    }
}
</script>
