import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { apiGet, apiPost } from "../api/client";
import { listEvidence, createEvidence, uploadEvidencePdf, reviewEvidence, type EvidenceItem } from "../api/evidence";
import { getAnalysisReadiness, type AnalysisReadiness } from "../api/readiness";
import type { CaseDetail } from "../api/cases";
import ObservationsPanel from "./ObservationsPanel";
import ScenariosPanel from "./ScenariosPanel";
import FactsPanel from "./FactsPanel";
import AnalysisReportsPanel from "./AnalysisReportsPanel";

export default function CaseDetailPage() {
  const { caseId = "" } = useParams();
  const [researchCase, setResearchCase] = useState<CaseDetail | null>(null);
  const [evidence, setEvidence] = useState<EvidenceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [kind, setKind] = useState<"manual_note" | "manual_value" | "web_page">("manual_note");
  const [title, setTitle] = useState("");
  const [sourceUrl, setSourceUrl] = useState("");
  const [notes, setNotes] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [issuerLegalName, setIssuerLegalName] = useState("");
  const [issueDisplayName, setIssueDisplayName] = useState("");
  const [identityEvidenceIds, setIdentityEvidenceIds] = useState<string[]>([]);
  const [readiness, setReadiness] = useState<AnalysisReadiness | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const [caseResult, evidenceResult, readinessResult] = await Promise.all([
        apiGet<CaseDetail>(`/cases/${caseId}`),
        listEvidence(caseId),
        getAnalysisReadiness(caseId)
      ]);
      setResearchCase(caseResult);
      setEvidence(evidenceResult.items);
      setReadiness(readinessResult);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load this research case.");
    } finally {
      setLoading(false);
    }
  }, [caseId]);

  useEffect(() => { void refresh(); }, [refresh]);

  async function refreshReadiness() {
    try { setReadiness(await getAnalysisReadiness(caseId)); }
    catch (e) { setError(e instanceof Error ? e.message : "Could not check analysis readiness."); }
  }

  async function markEvidenceReviewed(item: EvidenceItem) {
    setBusy(true); setError(null);
    try {
      const updated = await reviewEvidence(caseId, item.evidenceId, "verify", "Reviewed by user in the local research workspace.");
      setEvidence(previous => previous.map(current => current.evidenceId === updated.evidenceId ? updated : current));
      await refreshReadiness();
    } catch (e) { setError(e instanceof Error ? e.message : "Evidence review could not be saved."); }
    finally { setBusy(false); }
  }

  async function confirmIdentity(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const updated = await apiPost<CaseDetail, {
        manualIssue: { issuerLegalName: string; displayName: string; marketSegment: "MAINBOARD" };
        identityEvidenceIds: string[];
      }>(`/cases/${caseId}/identity/confirm`, {
        manualIssue: { issuerLegalName: issuerLegalName.trim(), displayName: issueDisplayName.trim(), marketSegment: "MAINBOARD" },
        identityEvidenceIds
      });
      setResearchCase(updated);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Identity could not be confirmed.");
    } finally {
      setBusy(false);
    }
  }

  async function addEvidence(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setBusy(true);
    try {
      let item: EvidenceItem;
      if (file) {
        item = await uploadEvidencePdf(caseId, file, { title, sourceUrl, notes });
        setFile(null);
        const input = document.getElementById("evidence-file") as HTMLInputElement | null;
        if (input) input.value = "";
      } else {
        item = await createEvidence(caseId, {
          evidenceKind: kind, title: title.trim(),
          ...(sourceUrl.trim() ? { sourceUrl: sourceUrl.trim() } : {}),
          ...(notes.trim() ? { notes: notes.trim() } : {})
        });
      }
      setEvidence((previous) => [item, ...previous]);
      setTitle("");
      setSourceUrl("");
      setNotes("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save evidence.");
    } finally {
      setBusy(false);
    }
  }

  if (loading) return <main className="page-container"><p className="muted">Loading research case…</p></main>;
  if (!researchCase) return <main className="page-container"><section className="panel"><h1>Research case unavailable</h1><p className="form-error">{error ?? "This case could not be found."}</p><Link to="/cases">Back to cases</Link></section></main>;

  return <main className="page-container">
    <p className="eyebrow"><Link to="/cases">RESEARCH / CASES</Link> / CASE DETAIL</p>
    <section className="page-intro"><h1>{researchCase.title}</h1><p className="lead">Entered name: {researchCase.enteredName}. The IPO identity is still {researchCase.identityStatus.replaceAll("_", " ")}; analysis stays unavailable until identity and evidence are reviewed.</p></section>
    {error && <p className="form-error" role="alert">{error}</p>}
    <section className="case-detail-grid">
      <div className="panel">
        <p className="eyebrow">IDENTITY</p><h2>Confirm the exact issue</h2>
        {researchCase.identityStatus === "confirmed" && researchCase.issue ? <div className="confirmed-identity"><h3>{researchCase.issue.displayName}</h3><p className="muted">{researchCase.issue.issuerLegalName} · Mainboard</p><p className="muted">Manual identity confirmation saved. Dates and price fields remain unknown unless entered.</p></div> : <>
          <p className="muted">No approved automatic identity source is enabled. Confirm manually only after adding source evidence and selecting it below.</p>
          <form className="create-case-form" onSubmit={confirmIdentity}>
            <label htmlFor="issuer-legal-name">Issuer legal name</label>
            <input id="issuer-legal-name" value={issuerLegalName} onChange={e => setIssuerLegalName(e.target.value)} maxLength={200} required />
            <label htmlFor="issue-display-name">IPO issue display name</label>
            <input id="issue-display-name" value={issueDisplayName} onChange={e => setIssueDisplayName(e.target.value)} maxLength={200} required />
            <fieldset className="identity-evidence-picker"><legend>Identity evidence (select at least one)</legend>
              {evidence.filter(item => item.verificationStatus === "reviewed").length === 0 ? <p className="muted">Add evidence and mark it reviewed first.</p> : evidence.filter(item => item.verificationStatus === "reviewed").map(item => <label key={item.evidenceId} className="identity-evidence-option"><input type="checkbox" checked={identityEvidenceIds.includes(item.evidenceId)} onChange={e => setIdentityEvidenceIds(prev => e.target.checked ? [...prev, item.evidenceId] : prev.filter(id => id !== item.evidenceId))} /> <span>{item.title} <small>({item.verificationStatus.replaceAll("_", " ")})</small></span></label>)}
            </fieldset>
            <p className="muted">This records your manual confirmation; it does not independently verify the document. Missing dates and financial terms stay unknown.</p>
            <button className="button button-primary create-button" disabled={busy || evidence.length === 0 || identityEvidenceIds.length === 0}>{busy ? "Confirming…" : "Confirm Mainboard identity"}</button>
          </form>
        </>}
        <div className="detail-status-row"><span className={"case-status status-" + researchCase.caseStatus}>{researchCase.caseStatus.replaceAll("_", " ")}</span><span className="identity-status">{researchCase.identityStatus.replaceAll("_", " ")}</span></div>
      </div>
      <div className="panel">
        <p className="eyebrow">ADD EVIDENCE</p><h2>Register a source or upload a PDF</h2>
        <form className="create-case-form" onSubmit={addEvidence}>
          <label htmlFor="evidence-kind">Evidence type</label>
          <select id="evidence-kind" value={kind} onChange={e => setKind(e.target.value as typeof kind)}>
            <option value="manual_note">Manual note</option><option value="manual_value">Manual value/source record</option><option value="web_page">Web page reference</option>
          </select>
          <label htmlFor="evidence-title">Title</label>
          <input id="evidence-title" value={title} onChange={e => setTitle(e.target.value)} maxLength={200} placeholder="e.g. RHP — risk factors" required />
          {(kind === "web_page" || sourceUrl) && <><label htmlFor="evidence-url">Source URL {kind === "web_page" ? "(required)" : "(optional)"}</label><input id="evidence-url" type="url" value={sourceUrl} onChange={e => setSourceUrl(e.target.value)} placeholder="https://…" required={kind === "web_page"} /></>}
          <label htmlFor="evidence-notes">Notes (optional)</label><textarea id="evidence-notes" value={notes} onChange={e => setNotes(e.target.value)} maxLength={10000} rows={3} placeholder="What does this evidence contain? Any caveats?" />
          <label htmlFor="evidence-file">PDF upload (optional)</label><input id="evidence-file" type="file" accept="application/pdf,.pdf" onChange={e => setFile(e.target.files?.[0] ?? null)} />
          <p className="muted">PDFs are stored locally as originals and SHA-256 hashed. Uploading a file creates an evidence item; it does not automatically validate facts.</p>
          {file && <p className="muted">Selected: {file.name} ({Math.ceil(file.size / 1024)} KB)</p>}
          <button className="button button-primary create-button" disabled={busy}>{busy ? "Saving evidence…" : "Save evidence"}</button>
        </form>
      </div>
    </section>
    <section className="panel readiness-panel"><div className="panel-heading"><div><p className="eyebrow">ANALYSIS PREFLIGHT</p><h2>Readiness check</h2></div><button className="button button-secondary" type="button" onClick={() => void refreshReadiness()}>Recheck</button></div>{readiness && <><p><span className={"case-status " + (readiness.status === "blocked" ? "status-identity_pending" : "status-active")}>{readiness.status}</span></p><p className="muted">Information cutoff: {new Date(readiness.informationCutoffAt).toLocaleString()}</p>{readiness.blockers.map(item => <div className="readiness-issue readiness-blocker" key={item.code}><strong>{item.message}</strong>{item.nextAction && <p className="muted">{item.nextAction}</p>}</div>)}{readiness.warnings.map(item => <div className="readiness-issue readiness-warning" key={item.code}><strong>{item.message}</strong>{item.nextAction && <p className="muted">{item.nextAction}</p>}</div>)}<p className="muted">No financial analysis has run. The approved formula register and external source connectors are not enabled; this check does not invent results.</p></>}</section><section className="panel evidence-list-panel">
      <div className="panel-heading"><div><p className="eyebrow">CASE EVIDENCE</p><h2>Evidence register <span className="count-pill">{evidence.length}</span></h2></div><button className="button button-secondary" type="button" onClick={() => void refresh()} disabled={loading}>Refresh</button></div>
      {evidence.length === 0 ? <div className="empty-cases"><h3>No evidence registered</h3><p className="muted">Add a source reference, a manual note, or a PDF. Nothing is treated as verified automatically.</p></div> :
        <div className="evidence-list">{evidence.map(item => <article className="evidence-row" key={item.evidenceId}>
          <div className="evidence-main"><h3>{item.title}</h3><p className="case-meta">{item.evidenceKind.replaceAll("_", " ")} · captured {new Date(item.capturedAt).toLocaleString()}</p>
            {item.sourceUrl && <a href={item.sourceUrl} target="_blank" rel="noreferrer">{item.sourceUrl}</a>}
            {item.originalFileName && <p className="case-entered-name">{item.originalFileName} · {item.sizeBytes?.toLocaleString()} bytes</p>}
            {item.sha256 && <p className="evidence-hash">SHA-256: {item.sha256}</p>}
            {item.notes && <p className="muted">{item.notes}</p>}
          </div>
          <div className="case-row-status"><span className="case-status">{item.verificationStatus.replaceAll("_", " ")}</span>{item.verificationStatus === "unverified" && <button className="button button-secondary" type="button" onClick={() => void markEvidenceReviewed(item)} disabled={busy}>Mark reviewed</button>}{item.downloadUrl && <a className="button button-secondary" href={"http://127.0.0.1:8000" + item.downloadUrl}>Download PDF</a>}</div>
        </article>)}</div>}
    </section>
    <FactsPanel caseId={caseId} evidence={evidence} />
    <ObservationsPanel caseId={caseId} evidence={evidence} />
    <ScenariosPanel caseId={caseId} />
    <AnalysisReportsPanel caseId={caseId} identityConfirmed={researchCase.identityStatus === "confirmed"} />
  </main>;
}
