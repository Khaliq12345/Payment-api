export type TransactionPayload = {
    description: string
    amount: number | undefined;
    currency: string
    callback_url: string
    customer_id: string
    whatsapp_number: string
    first_name: string
    last_name: string
    email: string
}
