export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  full_name: string;
  email: string;
  password: string;
  role?: string;
}

export interface UserResponse {
  id?: number;
  user_id?: number;
  email?: string;
  full_name?: string;
  role?: string;
  detail?: string;
}

export interface AuthResponse {
  access_token?: string;
  token_type?: string;
  user_id?: number;
  email?: string;
  role?: string;
  detail?: string;
}
