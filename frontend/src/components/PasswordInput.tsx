import { Eye, EyeOff } from "lucide-react";
import { useState, type InputHTMLAttributes } from "react";

interface PasswordInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  hint?: string;
}

export function PasswordInput({ label, error, hint, id, ...props }: PasswordInputProps) {
  const [visible, setVisible] = useState(false);
  const inputId = id ?? "password";
  const helpId = `${inputId}-help`;

  return (
    <div className="field">
      <label htmlFor={inputId}>{label}</label>
      <div className={`password-field ${error ? "input--error" : ""}`}>
        <input
          {...props}
          id={inputId}
          type={visible ? "text" : "password"}
          aria-invalid={Boolean(error)}
          aria-describedby={error || hint ? helpId : undefined}
        />
        <button
          type="button"
          className="icon-button"
          aria-label={visible ? "Ocultar senha" : "Mostrar senha"}
          onClick={() => setVisible((current) => !current)}
        >
          {visible ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      </div>
      {(error || hint) && (
        <small id={helpId} className={error ? "field__error" : "field__hint"}>
          {error ?? hint}
        </small>
      )}
    </div>
  );
}

