import { Brand } from "./Brand";

export function LoadingScreen() {
  return (
    <main className="loading-screen" aria-live="polite">
      <Brand />
      <span className="spinner" aria-label="Carregando" />
    </main>
  );
}

