export type WhatsAppVerifyQuery = {
  number: number;
};

export type WhatsAppAddQuery = {
  groupId: string;
  phone: number;
};

export type WhatsAppVerifyResponse = string;

export type WhatsAppChatsResponse = string;

export type WhatsAppAddResponse = {
  addParticipant: boolean;
};
