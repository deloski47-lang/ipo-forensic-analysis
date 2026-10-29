import { FormEvent, useCallback, useEffect, useState } from "react";
import { getHealth, type HealthResponse } from "../api/client";
import { createCase, listCases, type CaseSummary } from "../api/cases";

type ServiceState =
  | { kind: "loading" }
  | { kind: "available"; health: HealthResponse }
  | { kind: "unavailable"; message: string };

function HealthCard({ state }: { state: ServiceState }) {
  if (state.kind === "loading") {
    return <section className="status-card" aria-live="polite" aria-busy="true"><span className="status-dot status-dot-pending" /><div><p className="status-title">Checking local services</p><p className="muted">Contacting the Python API…</p></div></section>;
  }
  if (state.kind === "unavailable") {
    return <section className="status-card status-card-warning" role="status"><span className="status-dot status-dot-warning" /><div><p className="status-title">Local API unavailable</p><p className="muted">{state.message}</p><p className="status-hint">Start the backend using the repository README.</p></div></section>;
  }
  const { health } = state;
  const databaseReady = health.databaseStatus === "ok";
  const dataDirectoryReady = health.dataDirectoryStatus === "ok";
  return (
    <section className="status-card" aria-label="Local service status">
      <span className={"status-dot " + (health.status === "ok" ? "status-dot-good" : "status-dot-warning")} />
      <div className="status-content">
        <p className="status-title">{health.status === "ok" ? "Local API and database ready" : "Local services need attention"}</p>
        <p className="muted">API version {health.apiVersion} · checked at {new Date(health.timestamp).toLocaleTimeString()}</p>
        <div className="service-list">
          <span className={"service-pill " + (databaseReady ? "service-ready" : "service-pending")}>{databaseReady ? "✓" : "!"} Local database {databaseReady ? "ready" : "unavailable"}</span>
          <span className={"service-pill " + (dataDirectoryReady ? "service-ready" : "service-pending")}>{dataDirectoryReady ? "✓" : "!"} Data directory {dataDirectoryReady ? "available" : "unavailable"}</span>
        </div>
      </div>
    </section>
  );
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(new Date(value));
}

export default function CasesPage() {
  const [serviceState, setServiceState] = useState<ServiceState>({ kind: "loading" });
  const [cases, setCases] = useState<CaseSummary[]>([]);
  const [casesLoading, setCasesLoading] = useState(true);
  const [enteredName, setEnteredName] = useState("");
  const [customTitle, setCustomTitle] = useState("");
  const [formError, setFormError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  const refreshCases = useCallback(async () => {
    setCasesLoading(true);
    try {
      const result = await listCases();
      setCases(result.items);
      setLoadError(null);
    } catch (error) {
      setLoadError(error instanceof Error ? error.message : "Could not load saved research cases.");
    } finally {
      setCasesLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    getHealth()
      .then((health) => { if (active) setServiceState({ kind: "available", health }); })
      .catch((error: unknown) => {
        if (active) setServiceState({ kind: "unavailable", message: error instanceof Error ? error.message : "Could not connect to the local API." });
      });
    void refreshCases();
    return () => { active = false; };
  }, [refreshCases]);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFormError(null);
    const name = enteredName.trim();
    if (name.length < 2) {
      setFormError("Enter an IPO or issuer name (at least 2 characters).");
      return;
    }
    setCreating(true);
    try {
      const created = await createCase({ enteredName: name, ...(customTitle.trim() ? { title: customTitle.trim() } : {}) });
      setCases((previous) => [{ ...created, issueDisplayName: null }, ...previous]);
      setEnteredName("");
      setCustomTitle("");
    } catch (error) {
      setFormError(error instanceof Error ? error.message : "The case could not be saved.");
    } finally {
      setCreating(false);
    }
  }

  return (
    <main className="page-container">
      <section className="page-intro">
        <p className="eyebrow">RESEARCH / CASES</p>
        <h1>Your IPO research, grounded in evidence.</h1>
        <p className="lead">A private, local workspace for organizing Mainboard IPO evidence, checking financial and demand signals, and producing traceable research reports.</p>
      </section>

      <HealthCard state={serviceState} />

      <section className="cases-layout" aria-label="Research cases workspace">
        <div className="panel create-panel">
          <p className="eyebrow">NEW RESEARCH CASE</p>
          <h2>Start with an IPO name.</h2>
          <p className="muted">This creates a saved case, not a confirmed IPO identity. You’ll verify the exact Mainboard issue before analysis.</p>
          <form className="create-case-form" onSubmit={handleCreate}>
            <label htmlFor="ipo-name">IPO or issuer name <span aria-hidden="true">*</span></label>
            <input id="ipo-name" name="enteredName" autoComplete="off" maxLength={200} value={enteredName} onChange={(event) => setEnteredName(event.target.value)} placeholder="e.g. Example Industries IPO" required />
            <label htmlFor="case-title">Workspace title <span className="optional-label">(optional)</span></label>
            <input id="case-title" name="title" maxLength={160} value={customTitle} onChange={(event) => setCustomTitle(event.target.value)} placeholder="Defaults to the name above" />
            {formError && <p className="form-error" role="alert">{formError}</p>}
            <button className="button button-primary create-button" type="submit" disabled={creating || serviceState.kind !== "available" || serviceState.health.databaseStatus !== "ok"}>
              {creating ? "Saving case…" : "Create research case"}
            </button>
          </form>
        </div>

        <section className="panel cases-panel">
          <div className="panel-heading">
            <div><p className="eyebrow">YOUR WORKSPACE</p><h2>Saved cases <span className="count-pill">{cases.length}</span></h2></div>
            <button type="button" className="button button-secondary" onClick={() => void refreshCases()} disabled={casesLoading}>Refresh</button>
          </div>
          {loadError && <p className="form-error" role="alert">{loadError}</p>}
          {casesLoading ? <p className="muted" aria-live="polite">Loading cases from your local database…</p> :
            cases.length === 0 ? <div className="empty-cases"><span className="empty-icon" aria-hidden="true">＋</span><h3>No research cases yet</h3><p className="muted">Create your first case. It will remain here after you restart the app.</p></div> :
              <div className="case-list">{cases.map((item) => <article className="case-row" key={item.caseId}>
                <div className="case-row-main"><h3>{item.title}</h3><p className="case-entered-name">{item.enteredName}</p><p className="case-meta">Last activity {formatDate(item.lastActivityAt)}</p></div>
                <div className="case-row-status"><span className={"case-status status-" + item.caseStatus}>{item.caseStatus.replaceAll("_", " ")}</span><span className="identity-status">{item.identityStatus.replaceAll("_", " ")}</span></div>
              </article>)}</div>}
        </section>
      </section>

      <section className="guardrail-strip" aria-label="Product guardrails">
        <div><span className="guardrail-icon">01</span><p><strong>Mainboard only</strong><small>SME issues are out of scope</small></p></div>
        <div><span className="guardrail-icon">02</span><p><strong>Evidence before conclusions</strong><small>Unknown values stay unknown</small></p></div>
        <div><span className="guardrail-icon">03</span><p><strong>Local-first storage</strong><small>No cloud database or paid API</small></p></div>
      </section>
    </main>
  );
}
