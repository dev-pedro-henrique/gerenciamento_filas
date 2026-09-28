import { Check, Pencil, Plus, Search, Stethoscope, X } from "lucide-react";
import { useEffect, useMemo, useState, type FormEvent } from "react";

import { ApiError, apiRequest } from "../api/client";
import type { Psychologist, PsychologistPayload } from "../types";

const emptyForm: PsychologistPayload = {
  nome_completo: "",
  ativo: true,
};

function FieldError({ messages }: { messages?: string[] }) {
  if (!messages?.length) return null;
  return <small className="field__error">{messages[0]}</small>;
}

export function PsychologistsPage() {
  const [psychologists, setPsychologists] = useState<Psychologist[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [editing, setEditing] = useState<Psychologist | null>(null);
  const [form, setForm] = useState<PsychologistPayload>(emptyForm);
  const [fields, setFields] = useState<Record<string, string[]>>({});
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function loadPsychologists() {
    setPsychologists(await apiRequest<Psychologist[]>("/api/psicologos/"));
  }

  useEffect(() => {
    let cancelled = false;
    apiRequest<Psychologist[]>("/api/psicologos/")
      .then((data) => {
        if (!cancelled) setPsychologists(data);
      })
      .catch(() => {
        if (!cancelled) setMessage("Não foi possível carregar os psicólogos.");
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
    if (!normalized) return psychologists;
    return psychologists.filter((item) =>
      item.nome_completo.toLowerCase().includes(normalized),
    );
  }, [query, psychologists]);

  function openCreateForm() {
    setEditing(null);
    setForm(emptyForm);
    setFields({});
    setMessage("");
    setFormOpen(true);
  }

  function openEditForm(psychologist: Psychologist) {
    setEditing(psychologist);
    setForm({
      nome_completo: psychologist.nome_completo,
      ativo: psychologist.ativo,
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
        await apiRequest<Psychologist>(`/api/psicologos/${editing.id}/`, {
          method: "PATCH",
          body: JSON.stringify(form),
        });
      } else {
        await apiRequest<Psychologist>("/api/psicologos/", {
          method: "POST",
          body: JSON.stringify(form),
        });
      }
      await loadPsychologists();
      closeForm();
      setMessage(editing ? "Psicólogo atualizado." : "Psicólogo cadastrado com sua fila.");
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

  const hasErrors = Object.keys(fields).length > 0;

  return (
    <div className="page">
      <div className="page-heading page-heading--with-action">
        <div>
          <p className="eyebrow">Configuração operacional</p>
          <h1>Psicólogos</h1>
          <p>Cadastre os profissionais responsáveis pelas filas de atendimento.</p>
        </div>
        <button className="button button--primary" type="button" onClick={openCreateForm}>
          <Plus size={18} />
          Novo psicólogo
        </button>
      </div>

      {message && (
        <div className={`alert ${hasErrors ? "alert--error" : "alert--success"}`} role="status">
          {message}
        </div>
      )}

      <section className="data-card" aria-labelledby="psychologist-list-title">
        <div className="data-card__header">
          <div>
            <h2 id="psychologist-list-title">Profissionais cadastrados</h2>
            <p>{psychologists.length} psicólogo(s)</p>
          </div>
          <label className="search-field">
            <Search size={17} aria-hidden="true" />
            <span className="sr-only">Buscar psicólogo</span>
            <input
              type="search"
              placeholder="Buscar por nome"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
          </label>
        </div>

        {loading ? (
          <div className="empty-state" aria-live="polite">
            <span className="spinner" />Carregando psicólogos...
          </div>
        ) : filtered.length ? (
          <div className="staff-list">
            {filtered.map((psychologist) => (
              <article className="staff-row" key={psychologist.id}>
                <span className="avatar" aria-hidden="true"><Stethoscope size={20} /></span>
                <div className="staff-row__identity">
                  <strong>{psychologist.nome_completo}</strong>
                  <span>Fila #{psychologist.fila_id}</span>
                </div>
                <span className={`status-pill ${psychologist.ativo ? "status-pill--active" : ""}`}>
                  {psychologist.ativo ? <Check size={14} /> : <X size={14} />}
                  {psychologist.ativo ? "Ativo" : "Inativo"}
                </span>
                <button
                  type="button"
                  className="button button--secondary button--small"
                  onClick={() => openEditForm(psychologist)}
                >
                  <Pencil size={15} />
                  Editar
                </button>
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <span className="empty-state__icon"><Stethoscope size={22} /></span>
            <strong>Nenhum psicólogo encontrado</strong>
            <p>{query ? "Tente buscar por outro nome." : "Cadastre o primeiro profissional."}</p>
          </div>
        )}
      </section>

      {formOpen && (
        <div className="modal-layer" role="presentation">
          <button className="modal-backdrop" type="button" aria-label="Fechar formulário" onClick={closeForm} />
          <section className="modal" role="dialog" aria-modal="true" aria-labelledby="psychologist-form-title">
            <div className="modal__header">
              <div>
                <p className="eyebrow">{editing ? "Atualizar profissional" : "Novo profissional"}</p>
                <h2 id="psychologist-form-title">{editing ? "Editar psicólogo" : "Cadastrar psicólogo"}</h2>
              </div>
              <button className="icon-button" type="button" aria-label="Fechar" onClick={closeForm}><X size={20} /></button>
            </div>
            <form className="staff-form" onSubmit={handleSubmit}>
              <div className="field">
                <label htmlFor="psychologist-name">Nome completo</label>
                <input
                  id="psychologist-name"
                  value={form.nome_completo}
                  onChange={(event) => setForm({ ...form, nome_completo: event.target.value })}
                  autoComplete="name"
                  required
                  autoFocus
                />
                <FieldError messages={fields.nome_completo} />
              </div>
              {editing && (
                <label className="switch-field">
                  <input
                    type="checkbox"
                    checked={form.ativo}
                    onChange={(event) => setForm({ ...form, ativo: event.target.checked })}
                  />
                  <span><strong>Psicólogo ativo</strong><small>Profissionais inativos permanecem no histórico.</small></span>
                </label>
              )}
              <div className="modal__actions">
                <button className="button button--secondary" type="button" onClick={closeForm}>Cancelar</button>
                <button className="button button--primary" type="submit" disabled={submitting}>
                  {submitting ? "Salvando..." : editing ? "Salvar alterações" : "Cadastrar psicólogo"}
                </button>
              </div>
            </form>
          </section>
        </div>
      )}
    </div>
  );
}
