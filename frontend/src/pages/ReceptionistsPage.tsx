import { Check, Pencil, Plus, Search, UserRound, X } from "lucide-react";
import { useEffect, useMemo, useState, type FormEvent } from "react";

import { ApiError, apiRequest } from "../api/client";
import { PasswordInput } from "../components/PasswordInput";
import type { Receptionist, ReceptionistPayload } from "../types";

const emptyForm: ReceptionistPayload = {
  username: "",
  name: "",
  password: "",
  is_active: true,
};

function FieldError({ messages }: { messages?: string[] }) {
  if (!messages?.length) return null;
  return <small className="field__error">{messages[0]}</small>;
}

export function ReceptionistsPage() {
  const [receptionists, setReceptionists] = useState<Receptionist[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Receptionist | null>(null);
  const [form, setForm] = useState<ReceptionistPayload>(emptyForm);
  const [fields, setFields] = useState<Record<string, string[]>>({});
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let cancelled = false;
    apiRequest<Receptionist[]>("/api/staff/receptionists/")
      .then((data) => {
        if (!cancelled) setReceptionists(data);
      })
      .catch(() => {
        if (!cancelled) setMessage("Não foi possível carregar a equipe.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const filtered = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    if (!normalized) return receptionists;
    return receptionists.filter(
      (item) =>
        item.name.toLowerCase().includes(normalized) ||
        item.username.toLowerCase().includes(normalized),
    );
  }, [query, receptionists]);

  function openCreateForm() {
    setEditing(null);
    setForm(emptyForm);
    setFields({});
    setMessage("");
    setFormOpen(true);
  }

  function openEditForm(receptionist: Receptionist) {
    setEditing(receptionist);
    setForm({
      username: receptionist.username,
      name: receptionist.name,
      password: "",
      is_active: receptionist.is_active,
    });
    setFields({});
    setMessage("");
    setFormOpen(true);
  }

  function closeForm() {
    setFormOpen(false);
    setEditing(null);
    setFields({});
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setFields({});
    setMessage("");

    try {
      if (editing) {
        const payload: Partial<ReceptionistPayload> = {
          username: form.username,
          name: form.name,
          is_active: form.is_active,
        };
        if (form.password) payload.password = form.password;
        await apiRequest<Receptionist>(`/api/staff/receptionists/${editing.id}/`, {
          method: "PATCH",
          body: JSON.stringify(payload),
        });
      } else {
        await apiRequest<Receptionist>("/api/staff/receptionists/", {
          method: "POST",
          body: JSON.stringify(form),
        });
      }
      setReceptionists(await apiRequest<Receptionist[]>("/api/staff/receptionists/"));
      closeForm();
      setMessage(editing ? "Recepcionista atualizado." : "Recepcionista cadastrado.");
    } catch (caught) {
      if (caught instanceof ApiError) {
        setFields(caught.fields);
        setMessage(caught.message);
      } else {
        setMessage("Não foi possível salvar o cadastro.");
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page">
      <div className="page-heading page-heading--with-action">
        <div>
          <p className="eyebrow">Controle de acesso</p>
          <h1>Recepcionistas</h1>
          <p>Cadastre e mantenha os acessos da equipe de recepção.</p>
        </div>
        <button className="button button--primary" type="button" onClick={openCreateForm}>
          <Plus size={18} />
          Nova recepcionista
        </button>
      </div>

      {message && (
        <div className={`alert ${fields && Object.keys(fields).length ? "alert--error" : "alert--success"}`} role="status">
          {message}
        </div>
      )}

      <section className="data-card" aria-labelledby="team-list-title">
        <div className="data-card__header">
          <div>
            <h2 id="team-list-title">Equipe cadastrada</h2>
            <p>{receptionists.length} usuário(s) de recepção</p>
          </div>
          <label className="search-field">
            <Search size={17} aria-hidden="true" />
            <span className="sr-only">Buscar recepcionista</span>
            <input
              type="search"
              placeholder="Buscar por nome ou usuário"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </label>
        </div>

        {loading ? (
          <div className="empty-state" aria-live="polite"><span className="spinner" />Carregando equipe...</div>
        ) : filtered.length ? (
          <div className="staff-list">
            {filtered.map((receptionist) => (
              <article className="staff-row" key={receptionist.id}>
                <span className="avatar" aria-hidden="true"><UserRound size={20} /></span>
                <div className="staff-row__identity">
                  <strong>{receptionist.name}</strong>
                  <span>@{receptionist.username}</span>
                </div>
                <span className={`status-pill ${receptionist.is_active ? "status-pill--active" : ""}`}>
                  {receptionist.is_active ? <Check size={14} /> : <X size={14} />}
                  {receptionist.is_active ? "Ativa" : "Inativa"}
                </span>
                <button
                  type="button"
                  className="button button--secondary button--small"
                  onClick={() => openEditForm(receptionist)}
                >
                  <Pencil size={15} />
                  Editar
                </button>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span className="empty-state__icon"><UserRound size={22} /></span>
            <strong>Nenhuma recepcionista encontrada</strong>
            <p>{query ? "Tente buscar por outro termo." : "Cadastre o primeiro acesso da equipe."}</p>
          </div>
        )}
      </section>

      {formOpen && (
        <div className="modal-layer" role="presentation">
          <button className="modal-backdrop" type="button" aria-label="Fechar formulário" onClick={closeForm} />
          <section className="modal" role="dialog" aria-modal="true" aria-labelledby="staff-form-title">
            <div className="modal__header">
              <div>
                <p className="eyebrow">{editing ? "Atualizar acesso" : "Novo acesso"}</p>
                <h2 id="staff-form-title">{editing ? "Editar recepcionista" : "Cadastrar recepcionista"}</h2>
              </div>
              <button className="icon-button" type="button" aria-label="Fechar" onClick={closeForm}><X size={20} /></button>
            </div>
            <form className="staff-form" onSubmit={handleSubmit}>
              <div className="field">
                <label htmlFor="staff-name">Nome completo</label>
                <input
                  id="staff-name"
                  value={form.name}
                  onChange={(event) => setForm({ ...form, name: event.target.value })}
                  autoComplete="name"
                  required
                  autoFocus
                />
                <FieldError messages={fields.name} />
              </div>
              <div className="field">
                <label htmlFor="staff-username">Nome de usuário</label>
                <input
                  id="staff-username"
                  value={form.username}
                  onChange={(event) =>
                    setForm({ ...form, username: event.target.value.toLowerCase() })
                  }
                  autoComplete="off"
                  required
                />
                <small className="field__hint">Letras minúsculas, números, ponto, hífen ou sublinhado.</small>
                <FieldError messages={fields.username} />
              </div>
              <PasswordInput
                id="staff-password"
                label={editing ? "Nova senha (opcional)" : "Senha inicial"}
                value={form.password}
                onChange={(event) => setForm({ ...form, password: event.target.value })}
                autoComplete="new-password"
                required={!editing}
                hint="Mínimo de 8 caracteres, com maiúscula, minúscula, número e símbolo."
                error={fields.password?.[0]}
              />
              {editing && (
                <label className="switch-field">
                  <input
                    type="checkbox"
                    checked={form.is_active}
                    onChange={(event) => setForm({ ...form, is_active: event.target.checked })}
                  />
                  <span><strong>Acesso ativo</strong><small>Ao desativar, a sessão atual será encerrada.</small></span>
                </label>
              )}
              <div className="modal__actions">
                <button className="button button--secondary" type="button" onClick={closeForm}>Cancelar</button>
                <button className="button button--primary" type="submit" disabled={submitting}>
                  {submitting ? "Salvando..." : editing ? "Salvar alterações" : "Cadastrar acesso"}
                </button>
              </div>
            </form>
          </section>
        </div>
      )}
    </div>
  );
}
