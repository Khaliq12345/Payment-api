export interface CreatedCustomer {
  id: number; //Ajout de l'ID pour correction
  firstname: string;
  lastname: string;
  full_name: string;
  email: string;
  account_id: number;
  phone_number_id?: number;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string | null;
}

export type CustomerState = {
  response: CreatedCustomer;
  whatsapp_number: string;
} | null;

export interface CreateCustomerResponse {
  "v1/customer": CreatedCustomer;
}
