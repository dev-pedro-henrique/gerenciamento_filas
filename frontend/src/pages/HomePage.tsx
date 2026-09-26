import { ArrowRight, ShieldCheck, UserRoundPlus } from "lucide-react";
import { Link } from "react-router-dom";

import { useAuth } from "../auth/useAuth";

export function HomePage() {
  const { user } = useAuth();
  const isManager = user?.role === "MANAGER";

  return (
    <div className="page page--home">
      <div className="page-heading">
        <p className="eyebrow">Visão geral</p>
        <h1>Olá, {user?.name.split(" ")[0]}.</h1>
        <p>
          {isManager
            ? "Gerencie os acessos da equipe e acompanhe a evolução do sistema."
            : "Seu acesso está pronto. Os módulos da recepção aparecerão aqui conforme forem integrados."}
        </p>
      </div>

      <section className="welcome-grid" aria-label="Ações disponíveis">
        {isManager && (
          <Link className="feature-card feature-card--action" to="/equipe">
            <span className="feature-card__icon"><UserRoundPlus size={22} /></span>
            <div>
              <small>Gestão de acesso</small>
              <h2>Recepcionistas</h2>
              <p>Cadastre usuários, atualize dados e controle quem pode entrar no sistema.</p>
            </div>
            <ArrowRight size={20} />
          </Link>
        )}
        <article className="feature-card">
          <span className="feature-card__icon"><ShieldCheck size={22} /></span>
          <div>
            <small>Sessão protegida</small>
            <h2>Acesso individual</h2>
            <p>Sua conta é pessoal e a sessão será encerrada após 15 minutos sem uso.</p>
          </div>
        </article>
      </section>

      <section className="integration-note">
        <span aria-hidden="true" />
        <div>
          <strong>Base pronta para os próximos módulos</strong>
          <p>Cadastro de pacientes e gerenciamento da fila serão integrados pela equipe nas próximas etapas.</p>
        </div>
      </section>
    </div>
  );
}

