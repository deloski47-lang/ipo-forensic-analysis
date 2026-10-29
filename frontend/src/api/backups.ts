import { apiPost } from "./client";

export interface BackupResponse {
  backupId: string; createdAt: string; sizeBytes: number; sha256: string;
  caseCount: number; evidenceFileCount: number; downloadUrl: string;
}
export interface RestoreValidationResponse {
  validationId: string; status: "valid" | "invalid" | "incompatible";
  caseCount: number; evidenceFileCount: number; warnings: string[]; errors: string[]; validatedAt: string;
}
export interface RestoreResponse {
  status: "completed" | "failed"; restoredAt: string | null; safetyBackupId: string | null; message: string;
}

export function createBackup(): Promise<BackupResponse> {
  return apiPost<BackupResponse>("/local-data/backups");
}
export async function validateRestore(file: File): Promise<RestoreValidationResponse> {
  const form = new FormData();
  form.set("file", file);
  const base = import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ?? "http://127.0.0.1:8000/api/v1";
  const response = await fetch(base + "/local-data/restore/validate", { method: "POST", headers: { Accept: "application/json" }, body: form });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({})) as { error?: { message?: string }; detail?: string };
    throw new Error(payload.error?.message ?? payload.detail ?? "Backup validation failed.");
  }
  return response.json() as Promise<RestoreValidationResponse>;
}
export function restoreBackup(validationId: string, confirmationText: string): Promise<RestoreResponse> {
  return apiPost<RestoreResponse, { validationId: string; confirmationText: string }>("/local-data/restore", { validationId, confirmationText });
}
