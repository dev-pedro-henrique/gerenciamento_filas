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

