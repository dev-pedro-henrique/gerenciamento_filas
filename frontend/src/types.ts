export type UserRole = "MANAGER" | "RECEPTIONIST";

export interface CurrentUser {
  id: number;
  username: string;
  name: string;
  role: UserRole;
  role_label: string;
}

export interface Receptionist {
  id: number;
  username: string;
  name: string;
  is_active: boolean;
  date_joined: string;
}

export interface ReceptionistPayload {
  username: string;
  name: string;
  password: string;
  is_active: boolean;
}

export interface Patient {
  id: number;
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  telefone: string;
  email: string;
}

export interface PatientPayload {
  nome_completo: string;
  cpf: string;
  data_nascimento: string;
  telefone: string;
  email: string;
}