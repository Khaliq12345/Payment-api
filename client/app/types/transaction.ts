export type TransactionPayload = {
  description: string;
  amount: number | undefined;
  callback_url: string;
  customer_id: string;
  whatsapp_number: string;
  first_name: string;
  last_name: string;
  email: string;
  confirm_whatsapp_number: string;
  country: string;
  group_id: number;
};
