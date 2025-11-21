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

interface PaidCustomer {
  firstname: string;
  lastname: string;
  email: string;
}

interface Metadata {
  expire_schedule_jobid: string;
  paid_customer: PaidCustomer;
  transfer_schedule_jobid: string;
}

interface CustomMetadata {
  whatsapp_number: number;
  group_id: number;
}

export interface Transaction extends TransactionPayload {
  klass: string;
  id: number;
  reference: string;
  status: string;
  currency_id: number;
  mode: string;
  operation: string;
  metadata: Metadata;
  commission: string;
  fees: number;
  fixed_commission: number;
  amount_transferred: number;
  created_at: string;
  updated_at: string;
  approved_at: string | null;
  canceled_at: string | null;
  declined_at: string | null;
  refunded_at: string | null;
  transferred_at: string | null;
  deleted_at: string | null;
  last_error_code: string;
  custom_metadata: CustomMetadata;
  amount_debited: number;
  receipt_url: string;
  payment_method_id: number;
  sub_accounts_commissions: null | unknown;
  transaction_key: string;
  merchant_reference: string | null;
  account_id: number;
  balance_id: number;
  payment_token: string | null;
  payment_url: string | null;
  flags: unknown[];
  to_be_transferred_at: string;
}

export interface TransactionResponse {
  "v1/transaction": Transaction;
}
