import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react";

import { AUTH_EXPIRED_EVENT, apiRequest } from "../api/client";
import type { CurrentUser } from "../types";
import { AuthContext } from "./AuthContext";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest<CurrentUser>("/api/auth/me/")
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    const handleExpiredSession = () => setUser(null);
    window.addEventListener(AUTH_EXPIRED_EVENT, handleExpiredSession);
    return () => window.removeEventListener(AUTH_EXPIRED_EVENT, handleExpiredSession);
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const currentUser = await apiRequest<CurrentUser>("/api/auth/login/", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    setUser(currentUser);
    return currentUser;
  }, []);

  const logout = useCallback(async () => {
    try {
      await apiRequest<void>("/api/auth/logout/", { method: "POST" });
    } finally {
      setUser(null);
    }
  }, []);

  const value = useMemo(
    () => ({ user, loading, login, logout }),
    [user, loading, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
