import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAuth } from "../auth/useAuth";
import { LoadingScreen } from "./LoadingScreen";

export function ProtectedRoute() {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) return <LoadingScreen />;
  if (!user) return <Navigate to="/login" state={{ from: location }} replace />;
  return <Outlet />;
}

export function ManagerRoute() {
  const { user } = useAuth();
  if (user?.role !== "MANAGER") return <Navigate to="/" replace />;
  return <Outlet />;
}

