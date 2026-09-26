import { LayoutDashboard, LogOut, Menu, UserRoundPlus, X } from "lucide-react";
import { useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "../auth/useAuth";
import { Brand } from "./Brand";

export function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);

  async function handleLogout() {
    await logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button
          type="button"
          className="mobile-menu"
          aria-label={menuOpen ? "Fechar menu" : "Abrir menu"}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((current) => !current)}
        >
          {menuOpen ? <X size={21} /> : <Menu size={21} />}
        </button>
        <Brand compact />
        <div className="user-summary">
          <span className="status-dot" aria-hidden="true" />
          <span>
            <strong>{user?.name}</strong>
            <small>{user?.role_label}</small>
          </span>
        </div>
      </header>

      <aside className={`sidebar ${menuOpen ? "sidebar--open" : ""}`}>
        <p className="sidebar__eyebrow">Navegação</p>
        <nav aria-label="Navegação principal">
          <NavLink to="/" end onClick={() => setMenuOpen(false)}>
            <LayoutDashboard size={18} />
            Início
          </NavLink>
          {user?.role === "MANAGER" && (
            <NavLink to="/equipe" onClick={() => setMenuOpen(false)}>
              <UserRoundPlus size={18} />
              Recepcionistas
            </NavLink>
          )}
        </nav>
        <div className="sidebar__note">
          <span aria-hidden="true" />
          <strong>Cuidado desde o primeiro contato.</strong>
          <p>Acesso individual e informações protegidas para uma recepção organizada.</p>
        </div>
        <button className="logout-button" type="button" onClick={handleLogout}>
          <LogOut size={17} />
          Encerrar sessão
        </button>
      </aside>

      {menuOpen && (
        <button
          type="button"
          className="sidebar-backdrop"
          aria-label="Fechar menu"
          onClick={() => setMenuOpen(false)}
        />
      )}
      <main className="content-area">
        <Outlet />
      </main>
    </div>
  );
}

