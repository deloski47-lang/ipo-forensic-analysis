import { apiGet, apiPost } from "./client";

export interface FactRecord {
  factId: string;
  caseId: string;
  indicatorCode: string;
  rawValueText: string;
  valueNumeric: string | null;
  valueText: string | null;
  unit: string | null;
  currency: string | null;
  periodStart: string | null;
  periodEnd: string | null;
  asOfDate: string | null;
  evidenceId: string;
  entryMethod: "manual" | "extracted_candidate" | "imported" | "connector" | "derived";
  reviewStatus: "candidate" | "accepted" | "rejected" | "conflicted" | "superseded";
  definitionNote: string | null;
  recordedAt: string;
  createdAt: string;
  reviewedAt: string | null;
  reviewRationale: string | null;
  supersedesFactId: string | null;
}

export function listFacts(caseId: string): Promise<{ items: FactRecord[]; total: number }> {
  return apiGet<{ items: FactRecord[]; total: number }>(`/cases/${caseId}/facts`);
}

export function createFact(caseId: string, body: {
  indicatorCode: string;
  rawValueText: string;
  valueNumeric?: string | null;
  valueText?: string | null;
  unit?: string | null;
  currency?: string | null;
  periodStart?: string | null;
  periodEnd?: string | null;
  asOfDate?: string | null;
  evidenceId: string;
  definitionNote?: string | null;
}): Promise<FactRecord> {
  return apiPost<FactRecord, typeof body>(`/cases/${caseId}/facts`, body);
}

export function reviewFact(caseId: string, factId: string, action: "accept" | "reject" | "mark_conflicted" | "supersede", rationale?: string): Promise<FactRecord> {
  return apiPost<FactRecord, { action: typeof action; rationale?: string }>(
    `/cases/${caseId}/facts/${factId}/review`,
    { action, ...(rationale ? { rationale } : {}) }
  );
}
