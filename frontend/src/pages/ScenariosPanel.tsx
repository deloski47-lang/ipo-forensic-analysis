import { useCallback, useEffect, useState } from "react";
import { createScenario, listScenarios, previewScenario, type ScenarioDefinition, type ScenarioPreview } from "../api/scenarios";

export default function ScenariosPanel({ caseId }: { caseId: string }) {
  const [items, setItems] = useState<ScenarioDefinition[]>([]);
  const [label, setLabel] = useState("Base case");
  const [entryPrice, setEntryPrice] = useState("");
  const [exitPrice, setExitPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const [assumptionNote, setAssumptionNote] = useState("");
  const [preview, setPreview] = useState<ScenarioPreview | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try { setItems((await listScenarios(caseId)).items); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not load scenarios."); }
  }, [caseId]);
  useEffect(() => { void refresh(); }, [refresh]);

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError(null); setPreview(null);
    const body = {
      label: label.trim(), entryPrice: entryPrice.trim(), exitPrice: exitPrice.trim(),
      ...(quantity.trim() ? { quantity: Number(quantity) } : {}),
      ...(assumptionNote.trim() ? { assumptionNote: assumptionNote.trim() } : {})
    };
    try {
      const [saved, calculation] = await Promise.all([
        createScenario(caseId, body),
        previewScenario(caseId, body)
      ]);
      setItems(previous => [saved, ...previous]);
      setPreview(calculation);
    } catch (e) { setError(e instanceof Error ? e.message : "Scenario could not be saved or calculated."); }
    finally { setBusy(false); }
  }

  return <section className="panel scenarios-panel">
    <div className="panel-heading"><div><p className="eyebrow">LISTING-DAY EXIT</p><h2>Scenario calculator <span className="count-pill">{items.length} saved</span></h2></div></div>
    <p className="muted">Use hypothetical entry and exit prices. Gross arithmetic is deterministic; this is not a forecast or a recommendation. Net return remains unknown until costs and taxes are modelled.</p>
    {error && <p className="form-error" role="alert">{error}</p>}
    <form className="create-case-form scenario-form" onSubmit={submit}>
      <label htmlFor="scenario-label">Scenario name</label><input id="scenario-label" value={label} onChange={e => setLabel(e.target.value)} maxLength={100} required />
      <div className="scenario-price-grid"><div><label htmlFor="scenario-entry">Entry price (₹)</label><input id="scenario-entry" inputMode="decimal" value={entryPrice} onChange={e => setEntryPrice(e.target.value)} placeholder="e.g. 100.00" required /></div><div><label htmlFor="scenario-exit">Exit price (₹)</label><input id="scenario-exit" inputMode="decimal" value={exitPrice} onChange={e => setExitPrice(e.target.value)} placeholder="e.g. 125.50" required /></div></div>
      <label htmlFor="scenario-quantity">Quantity (optional)</label><input id="scenario-quantity" inputMode="numeric" value={quantity} onChange={e => setQuantity(e.target.value)} placeholder="e.g. 15 shares" />
      <label htmlFor="scenario-note">Assumption note (optional)</label><textarea id="scenario-note" value={assumptionNote} onChange={e => setAssumptionNote(e.target.value)} maxLength={2000} rows={2} placeholder="Why are you considering this exit price?" />
      <button className="button button-primary create-button" disabled={busy}>{busy ? "Calculating…" : "Save scenario and calculate gross return"}</button>
    </form>
    {preview && <div className="scenario-result"><p className="eyebrow">GROSS SCENARIO RESULT</p><div className="scenario-result-grid"><div><small>Gross return</small><strong>{preview.grossReturnPct}%</strong></div><div><small>Gross profit / loss</small><strong>{preview.grossProfitAmount === null ? "Quantity not provided" : "₹" + preview.grossProfitAmount}</strong></div><div><small>Net return</small><strong>Unknown</strong></div></div><p className="muted">{preview.limitationNote}</p></div>}
    {items.length > 0 && <div className="saved-scenarios"><h3>Saved assumptions</h3>{items.map(item => <article className="case-row" key={item.scenarioId}><div className="case-row-main"><h3>{item.label}</h3><p className="case-entered-name">Entry ₹{item.entryPrice} → exit ₹{item.exitPrice}{item.quantity ? " · " + item.quantity + " shares" : ""}</p><p className="case-meta">{item.assumptionNote ?? "No assumption note supplied."}</p></div></article>)}</div>}
  </section>;
}
