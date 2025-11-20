
export interface CustomerFormState {
  first_name: string;
  last_name: string;
  email: string;
  whatsapp_number: string;
  confirm_whatsapp_number: string;
  country: string;
}

// Payload envoyé à l'API 
export interface FedaPayCustomerPayload {
  first_name: string;
  last_name: string;
  email: string;
  phone_number: string;
  country: string;
}


export type FedaPayResponse = string;

// Gestion d'erreur Swagger (422)
export interface FedaPayValidationError {
  detail: {
    msg: string;
  }[];
}