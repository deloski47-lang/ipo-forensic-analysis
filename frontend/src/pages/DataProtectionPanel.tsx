import { useState } from "react";
import { createBackup, restoreBackup, validateRestore, type BackupResponse, type RestoreValidationResponse } from "../api/backups";

export default function DataProtectionPanel() {
  const [backup, setBackup] = useState<BackupResponse | null>(null);
  const [validation, setValidation] = useState<RestoreValidationResponse | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [confirmation, setConfirmation] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function makeBackup() {
    setBusy(true); setError(null); setMessage(null);
    try { setBackup(await createBackup()); setMessage("Backup created. Keep a copy outside this computer too."); }
    catch (e) { setError(e instanceof Error ? e.message : "Backup could not be created."); }
    finally { setBusy(false); }
  }
  async function validateFile(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) return;
    setBusy(true); setError(null); setMessage(null); setValidation(null); setConfirmation("");
    try { setValidation(await validateRestore(file)); }
    catch (e) { setError(e instanceof Error ? e.message : "Backup validation failed."); }
    finally { setBusy(false); }
  }
  async function doRestore() {
    if (!validation || validation.status !== "valid") return;
    setBusy(true); setError(null); setMessage(null);
    try {
      const result = await restoreBackup(validation.validationId, confirmation);
      setMessage(result.message + (result.safetyBackupId ? " Safety backup ID: " + result.safetyBackupId : ""));
      setValidation(null); setFile(null); setConfirmation("");
      const input = document.getElementById("restore-file") as HTMLInputElement | null;
      if (input) input.value = "";
      window.location.reload();
    } catch (e) { setError(e instanceof Error ? e.message : "Restore failed."); }
    finally { setBusy(false); }
  }

  return <section className="panel data-protection-panel">
    <div className="page-intro"><p className="eyebrow">LOCAL DATA SAFETY</p><h2>Backup and restore</h2><p className="muted">Backups include the SQLite database, original evidence files, report snapshots and exports. Restore validates the archive first and creates a safety backup before replacing live data.</p></div>
    {error && <p className="form-error" role="alert">{error}</p>}
    {message && <p className="status-hint" role="status">{message}</p>}
    <div className="backup-action-row"><button className="button button-primary" type="button" onClick={() => void makeBackup()} disabled={busy}>{busy ? "Working…" : "Create local backup"}</button>
      {backup && <div className="backup-result"><strong>Backup ready</strong><p className="case-meta">{backup.caseCount} cases · {backup.evidenceFileCount} evidence files · {(backup.sizeBytes / 1024 / 1024).toFixed(2)} MB</p><p className="evidence-hash">SHA-256: {backup.sha256}</p><a className="button button-secondary" href={"http://127.0.0.1:8000" + backup.downloadUrl}>Download backup ZIP</a></div>}
    </div>
    <form className="create-case-form restore-form" onSubmit={validateFile}>
      <label htmlFor="restore-file">Validate a backup ZIP before restore</label>
      <input id="restore-file" type="file" accept=".zip,application/zip" onChange={e => { setFile(e.target.files?.[0] ?? null); setValidation(null); }} required />
      <button className="button button-secondary" type="submit" disabled={busy || !file}>{busy ? "Validating…" : "Validate backup archive"}</button>
    </form>
    {validation && <div className={"restore-validation restore-" + validation.status}><div className="panel-heading"><strong>Validation: {validation.status}</strong><span>{validation.caseCount} cases · {validation.evidenceFileCount} evidence files</span></div>
      {validation.warnings.map((item, i) => <p className="muted" key={"w" + i}>Warning: {item}</p>)}
      {validation.errors.map((item, i) => <p className="form-error" key={"e" + i}>{item}</p>)}
      {validation.status === "valid" && <><p className="muted">Restoring replaces the current database and evidence/report files with the selected backup. A safety backup is created automatically first.</p><label htmlFor="restore-confirmation">Type RESTORE to confirm</label><input id="restore-confirmation" value={confirmation} onChange={e => setConfirmation(e.target.value)} autoComplete="off" /><button className="button button-primary" type="button" onClick={() => void doRestore()} disabled={busy || confirmation !== "RESTORE"}>Restore selected backup</button></>}
    </div>}
  </section>;
}
