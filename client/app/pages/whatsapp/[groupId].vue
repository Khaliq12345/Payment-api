<template>
    <div class="p-6">
        <h1 class="text-2xl font-bold text-center mb-6">
            Groupe : {{ groupId }}
        </h1>

        <Form :loading="isLoading" @success="onCustomerCreated" />

        <div v-if="createdCustomer" class="mt-10">
            <Transaction
                v-model="transactionForm"
                :customer="createdCustomer"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import Form from "~/components/Form.vue";
import Transaction from "~/components/Transaction.vue";
import type { CreatedCustomer, SuccessData } from "~/types/fedapay";
import type { TransactionPayload } from "~/types/transaction";

const route = useRoute();
const groupId = Number(route.params.groupId);
const isLoading = ref(false);
const createdCustomer = ref<CreatedCustomer | null>(null);
const transactionForm = reactive<TransactionPayload>({
    description: `Cotisation Groupe ${groupId}`,
    amount: 1000,
    callback_url: "https://ton-site.com/callback",
    customer_id: "",
    whatsapp_number: "",
    first_name: "",
    last_name: "",
    email: "",
    confirm_whatsapp_number: "",
    country: "bj",
    group_id: groupId,
});

const onCustomerCreated = (data: {
    customer: CreatedCustomer;
    whatsapp_number: string;
}) => {
    console.log("Événement success reçu:", data);
    createdCustomer.value = data.customer;
    transactionForm.customer_id = data.customer.account_id.toString();
    transactionForm.whatsapp_number = data.whatsapp_number;
};
</script>
