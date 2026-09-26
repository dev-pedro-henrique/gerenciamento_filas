import { Sprout } from "lucide-react";

export function Brand({ compact = false }: { compact?: boolean }) {
  return (
    <div className={`brand ${compact ? "brand--compact" : ""}`}>
      <span className="brand__mark" aria-hidden="true">
        <Sprout size={compact ? 19 : 24} strokeWidth={1.8} />
      </span>
      <span className="brand__copy">
        <strong>Clínica de Psicologia</strong>
        <small>Espaço de acolhimento</small>
      </span>
    </div>
  );
}

