import { useCallback, useEffect, useState } from "react";
import { createObservation, listObservations, reviewObservation, type ObservationRecord, type SignalCategory } from "../api/observations";
import type { EvidenceItem } from "../api/evidence";

export default function ObservationsPanel({ caseId, evidence }: { caseId: string; evidence: EvidenceItem[] }) {
  const [items, setItems] = useState<ObservationRecord[]>([]);
  const [choice, setChoice] = useState("DEM-01|subscription_qib|QIB");
  const [rawValue, setRawValue] = useState("");
  const [numericValue, setNumericValue] = useState("");
  const [unit, setUnit] = useState("multiple");
  const [definition, setDefinition] = useState("");
  const [evidenceId, setEvidenceId] = useState("");
  const [observedAt, setObservedAt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try { setItems((await listObservations(caseId)).items); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not load observations."); }
  }, [caseId]);
  useEffect(() => { void refresh(); }, [refresh]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError(null);
    try {
      const [indicatorCode, signalCategory, segment] = choice.split("|");
      const created = await createObservation(caseId, {
        indicatorCode,
        signalCategory: signalCategory as SignalCategory,
        segment: segment === "none" ? null : segment as "QIB" | "NII" | "RETAIL",
        rawValueText: rawValue.trim(),
        ...(numericValue.trim() ? { valueNumeric: numericValue.trim() } : {}),
        ...(unit.trim() ? { unit: unit.trim() } : {}),
        metricDefinition: definition.trim(),
        observedAt: observedAt ? new Date(observedAt).toISOString() : null,
        evidenceId,
        definitionMetadata: { enteredManually: true }
      });
      setItems(previous => [created, ...previous]);
      setRawValue(""); setNumericValue(""); setDefinition(""); setObservedAt("");
    } catch (e) { setError(e instanceof Error ? e.message : "Observation could not be saved."); }
    finally { setBusy(false); }
  }

  async function review(item: ObservationRecord, action: "accept" | "reject") {
    setBusy(true); setError(null);
    try {
      const updated = await reviewObservation(caseId, item.observationId, action, action === "accept" ? "Reviewed against linked evidence." : "Rejected during manual review.");
      setItems(previous => previous.map(current => current.observationId === updated.observationId ? updated : current));
    } catch (e) { setError(e instanceof Error ? e.message : "Observation review failed."); }
    finally { setBusy(false); }
  }

  return <section className="panel observations-panel">
    <div className="panel-heading"><div><p className="eyebrow">LISTING SIGNALS</p><h2>Manual observations <span className="count-pill">{items.length}</span></h2></div><button className="button button-secondary" type="button" onClick={() => void refresh()}>Refresh</button></div>
    <p className="muted">Enter timestamped subscription or GMP observations and link each to evidence. Values are saved as candidates; accepting one is a separate review action. Unknown observation times stay unknown.</p>
    {error && <p className="form-error" role="alert">{error}</p>}
    <form className="create-case-form observation-form" onSubmit={submit}>
      <label htmlFor="observation-indicator">Indicator</label>
      <select id="observation-indicator" value={choice} onChange={e => setChoice(e.target.value)}>
        <option value="DEM-01|subscription_qib|QIB">QIB subscription (DEM-01)</option>
        <option value="DEM-02|subscription_nii|NII">NII / HNI subscription (DEM-02)</option>
        <option value="DEM-03|subscription_retail|RETAIL">Retail subscription (DEM-03)</option>
        <option value="GMP-01|gmp|none">Unofficial GMP quote (GMP-01)</option>
        <option value="ISS-01|issue_terms|none">Issue terms (ISS-01)</option>
        <option value="FIN-01|company_financials|none">Financial indicator (FIN-01)</option>
        <option value="VAL-01|valuation|none">Valuation indicator (VAL-01)</option>
      </select>
      <label htmlFor="observation-raw">Raw value as reported</label><input id="observation-raw" value={rawValue} onChange={e => setRawValue(e.target.value)} maxLength={5000} placeholder="e.g. 4.25x or ₹15 GMP" required />
      <label htmlFor="observation-numeric">Numeric value (optional; decimal string)</label><input id="observation-numeric" value={numericValue} onChange={e => setNumericValue(e.target.value)} placeholder="e.g. 4.25 or -15" />
      <label htmlFor="observation-unit">Unit (optional)</label><input id="observation-unit" value={unit} onChange={e => setUnit(e.target.value)} maxLength={64} placeholder="multiple, INR/share, %, etc." />
      <label htmlFor="observation-time">Observed at (optional)</label><input id="observation-time" type="datetime-local" value={observedAt} onChange={e => setObservedAt(e.target.value)} />
      <label htmlFor="observation-definition">Metric definition / basis</label><textarea id="observation-definition" value={definition} onChange={e => setDefinition(e.target.value)} maxLength={2000} rows={3} placeholder="Preserve denominator, category rules, quote basis and caveats." required />
      <label htmlFor="observation-evidence">Linked evidence</label><select id="observation-evidence" value={evidenceId} onChange={e => setEvidenceId(e.target.value)} required><option value="">Choose evidence</option>{evidence.map(item => <option key={item.evidenceId} value={item.evidenceId}>{item.title}</option>)}</select>
      <button className="button button-primary create-button" disabled={busy || evidence.length === 0}>{busy ? "Saving observation…" : "Save observation as candidate"}</button>
    </form>
    {items.length === 0 ? <div className="empty-cases"><h3>No observations recorded</h3><p className="muted">Subscription and GMP readings appear here once entered and linked to evidence.</p></div> : <div className="evidence-list">{items.map(item => <article className="evidence-row" key={item.observationId}>
      <div className="evidence-main"><h3>{item.indicatorCode} · {item.rawValueText}</h3><p className="case-meta">{item.signalCategory.replaceAll("_", " ")} · {item.segment ?? "no segment"} · {item.observedAt ? "observed " + new Date(item.observedAt).toLocaleString() : "observation time unknown"}</p><p className="muted">{item.metricDefinition}</p><p className="case-meta">Linked evidence ID: {item.evidenceId}</p></div>
      <div className="case-row-status"><span className="case-status">{item.reviewStatus}</span>{item.reviewStatus === "candidate" && <><button className="button button-secondary" type="button" onClick={() => void review(item, "accept")} disabled={busy}>Accept</button><button className="button button-secondary" type="button" onClick={() => void review(item, "reject")} disabled={busy}>Reject</button></>}</div>
    </article>)}</div>}
  </section>;
}
