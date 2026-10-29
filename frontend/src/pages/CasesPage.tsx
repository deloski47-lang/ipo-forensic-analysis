import { useEffect, useState } from "react";
import { getHealth, type HealthResponse } from "../api/client";

type ApiViewState =
  | { kind: "loading" }
  | { kind: "available"; health: HealthResponse }
  | { kind: "unavailable"; message: string };

function HealthCard({ state }: { state: ApiViewState }) {
  if (state.kind === "loading") {
    return (
      <section className="status-card" aria-live="polite" aria-busy="true">
        <span className="status-dot status-dot-pending" />
        <div>
          <p className="status-title">Checking local services</p>
          <p className="muted">Contacting the Python API…</p>
        </div>
      </section>
    );
  }

  if (state.kind === "unavailable") {
    return (
      <section className="status-card status-card-warning" role="status">
        <span className="status-dot status-dot-warning" />
        <div>
          <p className="status-title">Local API unavailable</p>
          <p className="muted">{state.message}</p>
          <p className="status-hint">Start the backend using the repository README.</p>
        </div>
      </section>
    );
  }

  const health = state.health;
  const databaseReady = health.databaseStatus === "ok";
  const dataDirectoryReady = health.dataDirectoryStatus === "ok";

  return (
    <section className="status-card" aria-label="Local service status">
      <span className={"status-dot " + (health.status === "ok" ? "status-dot-good" : "status-dot-warning")} />
      <div className="status-content">
        <p className="status-title">Python API connected</p>
        <p className="muted">API version {health.apiVersion} · checked at {new Date(health.timestamp).toLocaleTimeString()}</p>
        <div className="service-list">
          <span className={"service-pill " + (databaseReady ? "service-ready" : "service-pending")}>
            <span aria-hidden="true">{databaseReady ? "✓" : "!"}</span>
            Local database {databaseReady ? "ready" : "not initialized"}
          </span>
          <span className={"service-pill " + (dataDirectoryReady ? "service-ready" : "service-pending")}>
            <span aria-hidden="true">{dataDirectoryReady ? "✓" : "!"}</span>
            Data directory {dataDirectoryReady ? "available" : "unavailable"}
          </span>
        </div>
        {!databaseReady && (
          <p className="status-hint">
            Expected in Phase 0: database schema and migrations are part of the next build step.
          </p>
        )}
      </div>
    </section>
  );
}

export default function CasesPage() {
  const [apiState, setApiState] = useState<ApiViewState>({ kind: "loading" });

  useEffect(() => {
    let active = true;
    getHealth()
      .then((health) => {
        if (active) setApiState({ kind: "available", health });
      })
      .catch((error: unknown) => {
        const message = error instanceof Error
          ? error.message
          : "An unexpected connection error occurred.";
        if (active) setApiState({ kind: "unavailable", message });
      });
    return () => { active = false; };
  }, []);

  return (
    <main className="page-container">
      <section className="page-intro">
        <p className="eyebrow">RESEARCH / CASES</p>
        <h1>Your IPO research, grounded in evidence.</h1>
        <p className="lead">
          A private, local workspace for organizing Mainboard IPO evidence, checking financial and demand signals,
          and producing traceable research reports.
        </p>
      </section>

      <HealthCard state={apiState} />

      <section className="workspace-grid" aria-label="Build status">
        <article className="panel panel-large">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">CURRENT MILESTONE</p>
              <h2>Phase 0 · Local scaffold</h2>
            </div>
            <span className="status-label">IN PROGRESS</span>
          </div>
          <p className="muted">
            The frontend shell and health endpoint are the first foundation. Case creation, identity review,
            evidence upload and analysis will be added in their planned phases.
          </p>
          <div className="milestone-list">
            <div className="milestone-item">
              <span className="milestone-check" aria-hidden="true">✓</span>
              <div><strong>Frontend shell</strong><small>React + TypeScript + Vite</small></div>
            </div>
            <div className="milestone-item">
              <span className="milestone-check" aria-hidden="true">✓</span>
              <div><strong>Local API health route</strong><small>FastAPI · loopback only</small></div>
            </div>
            <div className="milestone-item milestone-pending">
              <span className="milestone-empty" aria-hidden="true" />
              <div><strong>Cases and local database</strong><small>Next implementation milestone</small></div>
            </div>
            <div className="milestone-item milestone-pending">
              <span className="milestone-empty" aria-hidden="true" />
              <div><strong>Evidence and manual facts</strong><small>After case persistence is validated</small></div>
            </div>
          </div>
        </article>

        <aside className="panel guardrail-panel">
          <p className="eyebrow">PRODUCT GUARDRAILS</p>
          <h2>Trust before automation.</h2>
          <dl className="guardrail-list">
            <div><dt>Coverage</dt><dd>Mainboard IPOs only</dd></div>
            <div><dt>Storage</dt><dd>Local-first</dd></div>
            <div><dt>Calculations</dt><dd>Deterministic Python</dd></div>
            <div><dt>Data gaps</dt><dd>Never treated as zero</dd></div>
            <div><dt>Cost</dt><dd>₹0 budget target</dd></div>
          </dl>
          <p className="guardrail-note">
            No broker execution, paid API, mandatory AI service or unapproved source adapter.
          </p>
        </aside>
      </section>
    </main>
  );
}
