import { useCallback, useEffect, useState } from "react";
import { getAnalysisReadiness } from "../api/readiness";
import { createAnalysisRun, listAnalysisRuns, type AnalysisRunDetail, type AnalysisRunSummary } from "../api/analysis";
import { createReport, exportReport, listReports, type ReportArtifact, type ReportDetail } from "../api/reports";

export default function AnalysisReportsPanel({ caseId, identityConfirmed }: { caseId: string; identityConfirmed: boolean }) {
  const [runs, setRuns] = useState<AnalysisRunSummary[]>([]);
  const [reports, setReports] = useState<ReportDetail[]>([]);
  const [selectedRun, setSelectedRun] = useState<AnalysisRunDetail | null>(null);
  const [selectedReport, setSelectedReport] = useState<ReportDetail | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const [runList, reportList] = await Promise.all([listAnalysisRuns(caseId), listReports(caseId)]);
      setRuns(runList.items); setReports(reportList.items);
    } catch (e) { setError(e instanceof Error ? e.message : "Could not load saved runs and reports."); }
  }, [caseId]);
  useEffect(() => { void refresh(); }, [refresh]);

  async function runAnalysis() {
    setBusy(true); setError(null);
    try {
      const readiness = await getAnalysisReadiness(caseId);
      const run = await createAnalysisRun(caseId, readiness.informationCutoffAt);
      setSelectedRun(run);
      setRuns(previous => [run, ...previous.filter(item => item.analysisRunId !== run.analysisRunId)]);
      await refresh();
    } catch (e) { setError(e instanceof Error ? e.message : "Analysis run was blocked."); }
    finally { setBusy(false); }
  }

  async function makeReport(runId: string) {
    setBusy(true); setError(null);
    try {
      const report = await createReport(caseId, runId);
      setSelectedReport(report);
      setReports(previous => [report, ...previous.filter(item => item.reportId !== report.reportId)]);
    } catch (e) { setError(e instanceof Error ? e.message : "Report could not be created."); }
    finally { setBusy(false); }
  }

  async function makeExport(report: ReportDetail, format: "html" | "docx") {
    setBusy(true); setError(null);
    try {
      const artifact = await exportReport(caseId, report.reportId, format);
      const updated = { ...report, exportArtifacts: [artifact, ...report.exportArtifacts] };
      setSelectedReport(updated);
      setReports(previous => previous.map(item => item.reportId === updated.reportId ? updated : item));
    } catch (e) { setError(e instanceof Error ? e.message : "Report export failed."); }
    finally { setBusy(false); }
  }

  return <section className="panel analysis-reports-panel">
    <div className="panel-heading"><div><p className="eyebrow">ANALYSIS & REPORTS</p><h2>Saved runs and reports</h2></div><button className="button button-primary" type="button" disabled={busy || !identityConfirmed} onClick={() => void runAnalysis()}>{busy ? "Working…" : "Run partial analysis"}</button></div>
    <p className="muted">The current engine calculates gross returns for saved user scenarios and records data-coverage limitations. It does not yet calculate full financial, valuation, subscription, GMP-trend or cross-signal conclusions.</p>
    {error && <p className="form-error" role="alert">{error}</p>}
    {!identityConfirmed && <p className="readiness-issue readiness-blocker">Confirm the IPO identity and save at least one scenario before running analysis.</p>}
    {selectedRun && <div className="analysis-run-card"><p className="eyebrow">LATEST RUN · {selectedRun.runStatus}</p><p className="case-meta">Cutoff: {new Date(selectedRun.informationCutoffAt).toLocaleString()}</p><p className="evidence-hash">Snapshot SHA-256: {selectedRun.inputSnapshotHash}</p>
      {selectedRun.results.map(result => <div className="result-row" key={result.resultId}><strong>{result.indicatorCode}</strong><span>{result.displayValue ?? result.valueText ?? "Unknown"}</span><p className="muted">{result.explanation}</p></div>)}
      {selectedRun.findings.map(finding => <div className="readiness-issue readiness-warning" key={finding.findingId}><strong>{finding.title}</strong><p className="muted">{finding.explanation}</p></div>)}
      <button className="button button-secondary" type="button" onClick={() => void makeReport(selectedRun.analysisRunId)} disabled={busy}>Create immutable report snapshot</button>
    </div>}
    <div className="saved-run-list"><h3>Analysis history ({runs.length})</h3>{runs.map(run => <button key={run.analysisRunId} className="history-row" type="button" onClick={async () => { setBusy(true); try { setSelectedRun(await (await import("../api/analysis")).getAnalysisRun(caseId, run.analysisRunId)); } catch (e) { setError(e instanceof Error ? e.message : "Could not reopen run."); } finally { setBusy(false); } }}><span>{run.runStatus} · {new Date(run.startedAt).toLocaleString()}</span><small>{run.inputSnapshotHash.slice(0, 12)}…</small></button>)}</div>
    <div className="saved-run-list"><h3>Reports ({reports.length})</h3>{reports.map(report => <article className="saved-report-row" key={report.reportId}><div><strong>{report.title}</strong><p className="case-meta">Snapshot {report.reportSnapshotHash.slice(0, 12)}…</p></div><div className="report-actions"><button className="button button-secondary" type="button" onClick={() => setSelectedReport(report)}>Preview</button><button className="button button-secondary" type="button" onClick={() => void makeExport(report, "html")} disabled={busy}>HTML</button><button className="button button-secondary" type="button" onClick={() => void makeExport(report, "docx")} disabled={busy}>DOCX</button></div></article>)}</div>
    {selectedReport && <div className="report-preview"><p className="eyebrow">IMMUTABLE REPORT PREVIEW</p><h3>{selectedReport.title}</h3><p className="muted">Information cutoff: {new Date(selectedReport.informationCutoffAt).toLocaleString()}</p>{selectedReport.warnings.map(warning => <p className="readiness-issue readiness-warning" key={warning}>{warning}</p>)}{selectedReport.sections.map(section => <section key={section.sectionCode}><h4>{section.heading}</h4><pre>{section.bodyMarkdown}</pre></section>)}<div className="report-actions">{selectedReport.exportArtifacts.map((artifact: ReportArtifact) => <a className="button button-secondary" key={artifact.artifactId} href={"http://127.0.0.1:8000" + artifact.downloadUrl}>{artifact.format.toUpperCase()} download</a>)}</div></div>}
  </section>;
}
