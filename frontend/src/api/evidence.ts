import { apiGet, apiPost } from "./client";

export type EvidenceKind = "web_page" | "manual_note" | "manual_value" | "uploaded_document";

export interface EvidenceItem {
  evidenceId: string;
  caseId: string;
  sourceId: string | null;
  evidenceKind: EvidenceKind;
  title: string;
  sourceUrl: string | null;
  originalFileName: string | null;
  mimeType: string | null;
  sizeBytes: number | null;
  sha256: string | null;
  publishedAt: string | null;
  capturedAt: string;
  locator: string | null;
  verificationStatus: "unverified" | "user_verified" | "conflicting" | "rejected";
  notes: string | null;
  downloadUrl: string | null;
  localAvailable: boolean;
}

export interface EvidenceListResponse {
  items: EvidenceItem[];
  total: number;
}

export function listEvidence(caseId: string): Promise<EvidenceListResponse> {
  return apiGet<EvidenceListResponse>(`/cases/${caseId}/evidence`);
}

export function createEvidence(caseId: string, body: {
  evidenceKind: "web_page" | "manual_note" | "manual_value";
  title: string;
  sourceUrl?: string | null;
  publishedAt?: string | null;
  notes?: string | null;
}): Promise<EvidenceItem> {
  return apiPost<EvidenceItem, typeof body>(`/cases/${caseId}/evidence`, body);
}

export async function uploadEvidencePdf(caseId: string, file: File, metadata: {
  title?: string;
  sourceUrl?: string;
  notes?: string;
}): Promise<EvidenceItem> {
  const form = new FormData();
  form.set("file", file);
  if (metadata.title?.trim()) form.set("title", metadata.title.trim());
  if (metadata.sourceUrl?.trim()) form.set("source_url", metadata.sourceUrl.trim());
  if (metadata.notes?.trim()) form.set("notes", metadata.notes.trim());
  const response = await fetch(
    (import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ?? "http://127.0.0.1:8000/api/v1") +
      `/cases/${caseId}/evidence/files`,
    { method: "POST", headers: { Accept: "application/json" }, body: form }
  );
  if (!response.ok) {
    let message = "The evidence file could not be uploaded.";
    try {
      const payload = await response.json() as { error?: { message?: string }; detail?: string };
      message = payload.error?.message ?? payload.detail ?? message;
    } catch { /* Keep the safe fallback message. */ }
    throw new Error(message);
  }
  return response.json() as Promise<EvidenceItem>;
}
