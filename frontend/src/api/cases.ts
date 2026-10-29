import { apiGet, apiPost, apiPatch } from "./client";

export type CaseStatus = "identity_pending" | "active" | "archived";
export type IdentityStatus = "unresolved" | "ambiguous" | "confirmed" | "out_of_scope" | "rejected";

export interface CaseSummary {
  caseId: string;
  enteredName: string;
  title: string;
  caseStatus: CaseStatus;
  identityStatus: IdentityStatus;
  issueDisplayName: string | null;
  lastActivityAt: string;
  latestAnalysisRunId: string | null;
  latestReportId: string | null;
  warningCount: number;
}

export interface CaseDetail extends Omit<CaseSummary, "issueDisplayName"> {
  issue: null;
  createdAt: string;
  updatedAt: string;
  caseChangedSinceLastRun: boolean;
  readinessSummary: "ready" | "qualified" | "blocked" | null;
}

export interface CaseListResponse {
  items: CaseSummary[];
  total: number;
}

export interface CreateCaseRequest {
  enteredName: string;
  title?: string | null;
}

export function listCases(): Promise<CaseListResponse> {
  return apiGet<CaseListResponse>("/cases");
}

export function createCase(payload: CreateCaseRequest): Promise<CaseDetail> {
  return apiPost<CaseDetail, CreateCaseRequest>("/cases", payload);
}

export function renameCase(caseId: string, title: string): Promise<CaseDetail> {
  return apiPatch<CaseDetail, { title: string }>(`/cases/${caseId}`, { title });
}
