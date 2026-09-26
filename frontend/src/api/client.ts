export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly fields: Record<string, string[]> = {},
  ) {
    super(message);
  }
}

export const AUTH_EXPIRED_EVENT = "clinic:auth-expired";

function getCookie(name: string): string | null {
  const prefix = `${name}=`;
  const cookie = document.cookie
    .split(";")
    .map((item) => item.trim())
    .find((item) => item.startsWith(prefix));
  return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : null;
}

async function ensureCsrfToken(): Promise<string> {
  let token = getCookie("csrftoken");
  if (!token) {
    const response = await fetch("/api/auth/csrf/", { credentials: "include" });
    if (!response.ok) {
      throw new ApiError("Não foi possível iniciar uma sessão segura.", response.status);
    }
    token = getCookie("csrftoken");
  }
  if (!token) {
    throw new ApiError("Não foi possível validar a segurança da sessão.", 403);
  }
  return token;
}

function extractError(payload: unknown): {
  message: string;
  fields: Record<string, string[]>;
} {
  if (!payload || typeof payload !== "object") {
    return { message: "Não foi possível concluir a operação.", fields: {} };
  }

  const data = payload as Record<string, unknown>;
  const fields: Record<string, string[]> = {};
  for (const [key, value] of Object.entries(data)) {
    if (Array.isArray(value)) {
      fields[key] = value.map(String);
    }
  }

  const detail = typeof data.detail === "string" ? data.detail : null;
  const firstFieldError = Object.values(fields)[0]?.[0];
  return {
    message: detail ?? firstFieldError ?? "Revise os dados informados.",
    fields,
  };
}

export async function apiRequest<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const method = (init.method ?? "GET").toUpperCase();
  const headers = new Headers(init.headers);
  headers.set("Accept", "application/json");

  if (init.body) {
    headers.set("Content-Type", "application/json");
  }
  if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
    headers.set("X-CSRFToken", await ensureCsrfToken());
  }

  const response = await fetch(path, {
    ...init,
    method,
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => null);
    const { message, fields } = extractError(payload);
    const sessionMissing =
      response.status === 401 ||
      (response.status === 403 &&
        /credenciais de autenticação|authentication credentials/i.test(message));
    if (path !== "/api/auth/login/" && sessionMissing) {
      window.dispatchEvent(new Event(AUTH_EXPIRED_EVENT));
    }
    throw new ApiError(message, response.status, fields);
  }

  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}
