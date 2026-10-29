import { useCallback, useEffect, useState } from "react";
import { createFact, listFacts, reviewFact, type FactRecord } from "../api/facts";
import type { EvidenceItem } from "../api/evidence";

export default function FactsPanel({ caseId, evidence }: { caseId: string; evidence: EvidenceItem[] }) {
  const [items, setItems] = useState<FactRecord[]>([]);
  const [indicatorCode, setIndicatorCode] = useState("FIN-01");
  const [rawValueText, setRawValueText] = useState("");
  const [valueNumeric, setValueNumeric] = useState("");
  const [unit, setUnit] = useState("");
  const [periodStart, setPeriodStart] = useState("");
  const [periodEnd, setPeriodEnd] = useState("");
  const [evidenceId, setEvidenceId] = useState("");
  const [definitionNote, setDefinitionNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try { setItems((await listFacts(caseId)).items); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not load facts."); }
  }, [caseId]);
  useEffect(() => { void refresh(); }, [refresh]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError(null);
    try {
      const created = await createFact(caseId, {
        indicatorCode, rawValueText: rawValueText.trim(),
        ...(valueNumeric.trim() ? { valueNumeric: valueNumeric.trim() } : {}),
        ...(unit.trim() ? { unit: unit.trim() } : {}),
        ...(periodStart ? { periodStart } : {}),
        ...(periodEnd ? { periodEnd } : {}),
        evidenceId, ...(definitionNote.trim() ? { definitionNote: definitionNote.trim() } : {})
      });
      setItems(previous => [created, ...previous]);
      setRawValueText(""); setValueNumeric(""); setDefinitionNote("");
    } catch (e) { setError(e instanceof Error ? e.message : "Fact could not be saved."); }
    finally { setBusy(false); }
  }

  async function review(item: FactRecord, action: "accept" | "reject") {
    setBusy(true); setError(null);
    try {
      const updated = await reviewFact(caseId, item.factId, action, action === "accept" ? "Reviewed against linked evidence." : "Rejected during manual review.");
      setItems(previous => previous.map(current => current.factId === updated.factId ? updated : current));
    } catch (e) { setError(e instanceof Error ? e.message : "Fact review failed."); }
    finally { setBusy(false); }
  }

  return <section className="panel facts-panel">
    <div className="panel-heading"><div><p className="eyebrow">ISSUER FACTS</p><h2>Manual facts <span className="count-pill">{items.length}</span></h2></div><button className="button button-secondary" type="button" onClick={() => void refresh()}>Refresh</button></div>
    <p className="muted">Enter facts from documents and link the evidence. Numeric values are decimal strings, not JavaScript floating-point values. Each fact starts as a candidate and must be reviewed before use.</p>
    {error && <p className="form-error" role="alert">{error}</p>}
    <form className="create-case-form fact-form" onSubmit={submit}>
      <label htmlFor="fact-indicator">Indicator catalogue ID</label><select id="fact-indicator" value={indicatorCode} onChange={e => setIndicatorCode(e.target.value)}>
        <option value="ISS-01">ISS-01 — Issue structure</option><option value="FIN-01">FIN-01 — Financial performance</option><option value="FIN-02">FIN-02 — Earnings quality</option><option value="CON-01">CON-01 — Business concentration</option><option value="GOV-01">GOV-01 — Governance</option><option value="VAL-01">VAL-01 — Valuation</option>
      </select>
      <label htmlFor="fact-raw">Raw value from source</label><input id="fact-raw" value={rawValueText} onChange={e => setRawValueText(e.target.value)} maxLength={5000} required placeholder="Keep the source's original wording and units" />
      <label htmlFor="fact-numeric">Numeric value (optional)</label><input id="fact-numeric" value={valueNumeric} onChange={e => setValueNumeric(e.target.value)} placeholder="Decimal string, e.g. 125.50" />
      <label htmlFor="fact-unit">Unit (optional)</label><input id="fact-unit" value={unit} onChange={e => setUnit(e.target.value)} maxLength={64} placeholder="INR crore, %, shares…" />
      <div className="scenario-price-grid"><div><label htmlFor="fact-period-start">Period start (optional)</label><input id="fact-period-start" type="date" value={periodStart} onChange={e => setPeriodStart(e.target.value)} /></div><div><label htmlFor="fact-period-end">Period end (optional)</label><input id="fact-period-end" type="date" value={periodEnd} onChange={e => setPeriodEnd(e.target.value)} /></div></div>
      <label htmlFor="fact-evidence">Linked evidence</label><select id="fact-evidence" value={evidenceId} onChange={e => setEvidenceId(e.target.value)} required><option value="">Choose evidence</option>{evidence.map(item => <option key={item.evidenceId} value={item.evidenceId}>{item.title}</option>)}</select>
      <label htmlFor="fact-note">Definition note / caveat (optional)</label><textarea id="fact-note" value={definitionNote} onChange={e => setDefinitionNote(e.target.value)} maxLength={2000} rows={2} />
      <button className="button button-primary create-button" disabled={busy || evidence.length === 0}>{busy ? "Saving fact…" : "Save fact as candidate"}</button>
    </form>
    {items.length === 0 ? <div className="empty-cases"><h3>No facts recorded</h3><p className="muted">Manual facts will appear here with their source link and review status.</p></div> : <div className="evidence-list">{items.map(item => <article className="evidence-row" key={item.factId}><div className="evidence-main"><h3>{item.indicatorCode} · {item.rawValueText}</h3><p className="case-meta">{item.unit ?? "unit unknown"} · {item.periodStart ?? "period start unknown"} → {item.periodEnd ?? "period end unknown"}</p><p className="case-meta">Linked evidence ID: {item.evidenceId}</p>{item.definitionNote && <p className="muted">{item.definitionNote}</p>}</div><div className="case-row-status"><span className="case-status">{item.reviewStatus}</span>{item.reviewStatus === "candidate" && <><button className="button button-secondary" type="button" onClick={() => void review(item, "accept")} disabled={busy}>Accept</button><button className="button button-secondary" type="button" onClick={() => void review(item, "reject")} disabled={busy}>Reject</button></>}</div></article>)}</div>}
  </section>;
}
