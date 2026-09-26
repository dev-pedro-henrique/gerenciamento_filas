import { ArrowRight, LockKeyhole, ShieldCheck } from "lucide-react";
import { useState, type FormEvent } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";

import { ApiError } from "../api/client";
import { useAuth } from "../auth/useAuth";
import { Brand } from "../components/Brand";
import { PasswordInput } from "../components/PasswordInput";

export function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  if (user) return <Navigate to="/" replace />;

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(username, password);
      const destination = (location.state as { from?: { pathname?: string } } | null)?.from
        ?.pathname;
      navigate(destination ?? "/", { replace: true });
    } catch (caught) {
      setError(
        caught instanceof ApiError ? caught.message : "Não foi possível entrar no sistema.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-intro" aria-labelledby="welcome-title">
        <Brand />
        <div className="login-intro__content">
          <p className="eyebrow">Atendimento com tranquilidade</p>
          <h1 id="welcome-title">Organização para quem cuida e acolhimento para quem espera.</h1>
          <p>
            Um espaço seguro para acompanhar a rotina da clínica com clareza, privacidade e
            simplicidade.
          </p>
          <div className="trust-list" aria-label="Características do acesso">
            <span><ShieldCheck size={18} /> Acesso individual e protegido</span>
            <span><LockKeyhole size={18} /> Sessão encerrada após inatividade</span>
          </div>
        </div>
        <small className="login-intro__footer">Uso exclusivo da equipe da clínica</small>
      </section>

      <section className="login-panel" aria-labelledby="login-title">
        <form className="login-card" onSubmit={handleSubmit} noValidate>
          <p className="eyebrow">Acesso interno</p>
          <h2 id="login-title">Bem-vindo de volta</h2>
          <p className="form-intro">Informe suas credenciais para acessar o sistema.</p>

          {error && (
            <div className="alert alert--error" role="alert">
              {error}
            </div>
          )}

          <div className="field">
            <label htmlFor="username">Nome de usuário</label>
            <input
              id="username"
              name="username"
              autoComplete="username"
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              required
              autoFocus
            />
          </div>

          <PasswordInput
            id="login-password"
            name="password"
            label="Senha"
            autoComplete="current-password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />

          <button className="button button--primary button--full" type="submit" disabled={submitting}>
            {submitting ? "Entrando..." : "Entrar no sistema"}
            {!submitting && <ArrowRight size={18} />}
          </button>
          <p className="login-help">Problemas com o acesso? Procure o gestor ou o suporte técnico.</p>
        </form>
      </section>
    </main>
  );
}
