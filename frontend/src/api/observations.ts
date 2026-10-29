import { apiGet, apiPost } from "./client";

export type SignalCategory = "issue_terms" | "company_financials" | "valuation" | "subscription_qib" | "subscription_nii" | "subscription_retail" | "gmp" | "market_context" | "company_events";
export type ObservationReviewStatus = "candidate" | "accepted" | "rejected" | "conflicted" | "superseded";

export interface ObservationRecord {
  observationId: string;
  caseId: string;
  indicatorCode: string;
  signalCategory: SignalCategory;
  segment: "QIB" | "NII" | "RETAIL" | null;
  rawValueText: string;
  valueNumeric: string | null;
  valueText: string | null;
  unit: string | null;
  currency: string | null;
  metricDefinition: string;
  observedAt: string | null;
  publishedAt: string | null;
  retrievedAt: string | null;
  recordedAt: string;
  sourceId: string | null;
  acquisitionAttemptId: string | null;
  evidenceId: string;
  entryMethod: "manual" | "extracted_candidate" | "imported" | "connector" | "derived";
  reviewStatus: ObservationReviewStatus;
  definitionMetadata: Record<string, unknown>;
  reviewedAt: string | null;
  reviewRationale: string | null;
  supersedesObservationId: string | null;
}

export function listObservations(caseId: string): Promise<{ items: ObservationRecord[]; total: number }> {
  return apiGet<{ items: ObservationRecord[]; total: number }>(`/cases/${caseId}/observations`);
}

export function createObservation(caseId: string, body: {
  indicatorCode: string;
  signalCategory: SignalCategory;
  segment?: "QIB" | "NII" | "RETAIL" | null;
  rawValueText: string;
  valueNumeric?: string | null;
  valueText?: string | null;
  unit?: string | null;
  currency?: string | null;
  metricDefinition: string;
  observedAt?: string | null;
  publishedAt?: string | null;
  retrievedAt?: string | null;
  evidenceId: string;
  definitionMetadata?: Record<string, unknown>;
}): Promise<ObservationRecord> {
  return apiPost<ObservationRecord, typeof body>(`/cases/${caseId}/observations`, body);
}

export function reviewObservation(caseId: string, observationId: string, action: "accept" | "reject" | "mark_conflicted" | "supersede", rationale?: string): Promise<ObservationRecord> {
  return apiPost<ObservationRecord, { action: typeof action; rationale?: string }>(
    `/cases/${caseId}/observations/${observationId}/review`,
    { action, ...(rationale ? { rationale } : {}) }
  );
}
