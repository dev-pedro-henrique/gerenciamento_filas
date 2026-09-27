import { Search, UserRound, UserRoundPlus } from "lucide-react";
import { useState, type FormEvent } from "react";

import { ApiError, apiRequest } from "../api/client";

import type { Patient, PatientPayload } from "../types";

const emptyForm: PatientPayload = {
  nome_completo: "",
  cpf: "",
  data_nascimento: "",
  telefone: "",
  email: "",
};

function FieldError({ messages }: { messages?: string[] }) {
  if (!messages?.length) return null;

  return <small className="field__error">{messages[0]}</small>;
}

export function PacientesPage() {
  const [form, setForm] = useState<PatientPayload>(emptyForm);
  const [searchCpf, setSearchCpf] = useState("");

  const [patient, setPatient] = useState<Patient | null>(null);

  const [fields, setFields] = useState<Record<string, string[]>>({});
  const [message, setMessage] = useState("");
  const [error, setError] = useState(false);

  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);

  function handleChange(
    field: keyof PatientPayload,
    value: string,
  ) {
    setForm((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setLoading(true);
    setFields({});
    setMessage("");
    setError(false);

    try {
      await apiRequest<Patient>("/api/pacientes/", {
        method: "POST",
        body: JSON.stringify(form),
      });

      setForm(emptyForm);
      setMessage("Paciente cadastrado com sucesso.");
    } catch (caught) {
      setError(true);

      if (caught instanceof ApiError) {
        setFields(caught.fields);
        setMessage(caught.message);
      } else {
        setMessage("Não foi possível cadastrar o paciente.");
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleSearch(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    setSearching(true);
    setPatient(null);
    setFields({});
    setMessage("");
    setError(false);

    try {
      const result = await apiRequest<Patient>(
        "/api/pacientes/buscar/",
        {
          method: "POST",
          body: JSON.stringify({
            cpf: searchCpf,
          }),
        },
      );

      setPatient(result);
    } catch (caught) {
      setError(true);

      if (caught instanceof ApiError) {
        setFields(caught.fields);
        setMessage(caught.message);
      } else {
        setMessage("Não foi possível localizar o paciente.");
      }
    } finally {
      setSearching(false);
    }
  }

  return (
    <div className="page">
      <div className="page-heading">
        <p className="eyebrow">Atendimento</p>

        <h1>Pacientes</h1>

        <p>
          Cadastre e localize pacientes da clínica.
        </p>
      </div>

      {message && (
        <div
          className={`alert ${
            error ? "alert--error" : "alert--success"
          }`}
          role="status"
        >
          {message}
        </div>
      )}

      <div className="welcome-grid">
        <section className="data-card">
          <div className="data-card__header">
            <div>
              <h2>Localizar paciente</h2>

              <p>
                Pesquise pelo CPF cadastrado.
              </p>
            </div>
          </div>

          <form
            onSubmit={handleSearch}
            style={{ padding: "24px" }}
          >
            <div className="field">
              <label htmlFor="search-cpf">
                CPF
              </label>

              <input
                id="search-cpf"
                value={searchCpf}
                onChange={(event) =>
                  setSearchCpf(event.target.value)
                }
                placeholder="000.000.000-00"
                autoComplete="off"
                required
              />

              <FieldError messages={fields.cpf} />
            </div>

            <button
              className="button button--primary"
              type="submit"
              disabled={searching}
            >
              <Search size={18} />

              {searching
                ? "Buscando..."
                : "Buscar paciente"}
            </button>
          </form>
        </section>

        <section className="data-card">
          <div className="data-card__header">
            <div>
              <h2>Cadastrar paciente</h2>

              <p>
                Informe os dados básicos do paciente.
              </p>
            </div>
          </div>

          <form
            onSubmit={handleSubmit}
            style={{ padding: "24px" }}
          >
            <div className="field">
              <label htmlFor="patient-name">
                Nome completo
              </label>

              <input
                id="patient-name"
                value={form.nome_completo}
                onChange={(event) =>
                  handleChange(
                    "nome_completo",
                    event.target.value,
                  )
                }
                autoComplete="name"
                required
              />

              <FieldError
                messages={fields.nome_completo}
              />
            </div>

            <div className="field">
              <label htmlFor="patient-cpf">
                CPF
              </label>

              <input
                id="patient-cpf"
                value={form.cpf}
                onChange={(event) =>
                  handleChange(
                    "cpf",
                    event.target.value,
                  )
                }
                placeholder="000.000.000-00"
                required
              />

              <FieldError messages={fields.cpf} />
            </div>

            <div className="field">
              <label htmlFor="patient-birth">
                Data de nascimento
              </label>

              <input
                id="patient-birth"
                type="date"
                value={form.data_nascimento}
                onChange={(event) =>
                  handleChange(
                    "data_nascimento",
                    event.target.value,
                  )
                }
                required
              />

              <FieldError
                messages={fields.data_nascimento}
              />
            </div>

            <div className="field">
              <label htmlFor="patient-phone">
                Telefone
              </label>

              <input
                id="patient-phone"
                type="tel"
                value={form.telefone}
                onChange={(event) =>
                  handleChange(
                    "telefone",
                    event.target.value,
                  )
                }
                placeholder="(00) 00000-0000"
                required
              />

              <FieldError messages={fields.telefone} />
            </div>

            <div className="field">
              <label htmlFor="patient-email">
                E-mail
              </label>

              <input
                id="patient-email"
                type="email"
                value={form.email}
                onChange={(event) =>
                  handleChange(
                    "email",
                    event.target.value,
                  )
                }
                placeholder="nome@exemplo.com"
              />

              <FieldError messages={fields.email} />
            </div>

            <button
              className="button button--primary"
              type="submit"
              disabled={loading}
            >
              <UserRoundPlus size={18} />

              {loading
                ? "Cadastrando..."
                : "Cadastrar paciente"}
            </button>
          </form>
        </section>
      </div>

      {patient && (
        <section
          className="data-card"
          style={{ marginTop: "24px" }}
        >
          <div className="data-card__header">
            <div>
              <h2>Paciente localizado</h2>

              <p>
                Dados cadastrados no sistema.
              </p>
            </div>
          </div>

          <div style={{ padding: "24px" }}>
            <div className="staff-row">
              <span
                className="avatar"
                aria-hidden="true"
              >
                <UserRound size={20} />
              </span>

              <div className="staff-row__identity">
                <strong>
                  {patient.nome_completo}
                </strong>

                <span>
                  CPF: {patient.cpf}
                </span>

                <span>
                  Nascimento:{" "}
                  {patient.data_nascimento}
                </span>

                <span>
                  Telefone: {patient.telefone}
                </span>

                {patient.email && (
                  <span>
                    E-mail: {patient.email}
                  </span>
                )}
              </div>
            </div>
          </div>
        </section>
      )}
    </div>
  );
}