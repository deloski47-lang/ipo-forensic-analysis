import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router";
import { apiGet } from "../api/client";
import { listEvidence, createEvidence, uploadEvidencePdf, type EvidenceItem } from "../api/evidence";
import type { CaseDetail } from "../api/cases";

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

  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const [caseResult, evidenceResult] = await Promise.all([
        apiGet<CaseDetail>(`/cases/${caseId}`),
        listEvidence(caseId)
      ]);
      setResearchCase(caseResult);
      setEvidence(evidenceResult.items);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load this research case.");
    } finally {
      setLoading(false);
    }
  }, [caseId]);

  useEffect(() => { void refresh(); }, [refresh]);

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
        <p className="muted">No automatic identity lookup is enabled yet. Add source-backed evidence first; identity confirmation will be built on this evidence register.</p>
        <div className="detail-status-row"><span className="case-status status-identity_pending">{researchCase.caseStatus.replaceAll("_", " ")}</span><span className="identity-status">{researchCase.identityStatus.replaceAll("_", " ")}</span></div>
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
    <section className="panel evidence-list-panel">
      <div className="panel-heading"><div><p className="eyebrow">CASE EVIDENCE</p><h2>Evidence register <span className="count-pill">{evidence.length}</span></h2></div><button className="button button-secondary" type="button" onClick={() => void refresh()} disabled={loading}>Refresh</button></div>
      {evidence.length === 0 ? <div className="empty-cases"><h3>No evidence registered</h3><p className="muted">Add a source reference, a manual note, or a PDF. Nothing is treated as verified automatically.</p></div> :
        <div className="evidence-list">{evidence.map(item => <article className="evidence-row" key={item.evidenceId}>
          <div className="evidence-main"><h3>{item.title}</h3><p className="case-meta">{item.evidenceKind.replaceAll("_", " ")} · captured {new Date(item.capturedAt).toLocaleString()}</p>
            {item.sourceUrl && <a href={item.sourceUrl} target="_blank" rel="noreferrer">{item.sourceUrl}</a>}
            {item.originalFileName && <p className="case-entered-name">{item.originalFileName} · {item.sizeBytes?.toLocaleString()} bytes</p>}
            {item.sha256 && <p className="evidence-hash">SHA-256: {item.sha256}</p>}
            {item.notes && <p className="muted">{item.notes}</p>}
          </div>
          <div className="case-row-status"><span className="case-status">{item.verificationStatus.replaceAll("_", " ")}</span>{item.downloadUrl && <a className="button button-secondary" href={"http://127.0.0.1:8000" + item.downloadUrl}>Download PDF</a>}</div>
        </article>)}</div>}
    </section>
  </main>;
}
