export type WhatsAppVerifyQuery = {
  number: number;
};

export type WhatsAppAddQuery = {
  groupId: number;
  phone: number;
};

export type WhatsAppVerifyResponse = string;

export type WhatsAppChatsResponse = string;

export type WhatsAppAddResponse = string;
