import { apiGet, apiPost } from "./client";
import type { AnalysisReadiness } from "./readiness";

export interface AnalysisResult {
  resultId: string; indicatorCode: string; calculationStatus: "calculated" | "qualified" | "skipped" | "not_applicable" | "invalid";
  valueDecimal: string | null; valueText: string | null; unit: string | null; currency: string | null;
  displayValue: string | null; formulaCode: string | null; formulaVersion: string | null;
  inputFactIds: string[]; inputObservationIds: string[]; evidenceIds: string[]; explanation: string; reason: string | null;
}
export interface Finding {
  findingId: string; ruleCode: string; ruleVersion: string; findingType: string;
  severity: "info" | "low" | "medium" | "high" | "critical"; status: "active" | "unresolved" | "not_run" | "superseded";
  title: string; explanation: string; limitationNote: string | null; relatedIndicatorCodes: string[];
  inputFactIds: string[]; inputObservationIds: string[]; evidenceLinks: Array<{ evidenceId: string; role: "supports" | "contradicts" | "context"; note: string | null }>;
}
export interface AnalysisRunDetail {
  analysisRunId: string; caseId: string; runStatus: "completed" | "partial" | "failed";
  informationCutoffAt: string; startedAt: string; finishedAt: string | null;
  schemaVersion: string; formulaSetVersion: string; ruleSetVersion: string; softwareVersion: string;
  inputSnapshotHash: string; results: AnalysisResult[]; findings: Finding[];
  readiness: AnalysisReadiness; errorSummary: string | null;
}
export interface AnalysisRunSummary {
  analysisRunId: string; caseId: string; runStatus: "completed" | "partial" | "failed";
  informationCutoffAt: string; startedAt: string; finishedAt: string | null; inputSnapshotHash: string;
}
export function listAnalysisRuns(caseId: string): Promise<{ items: AnalysisRunSummary[]; total: number }> {
  return apiGet<{ items: AnalysisRunSummary[]; total: number }>(`/cases/${caseId}/analysis-runs`);
}
export function createAnalysisRun(caseId: string, informationCutoffAt: string): Promise<AnalysisRunDetail> {
  return apiPost<AnalysisRunDetail, { informationCutoffAt: string }>(`/cases/${caseId}/analysis-runs`, { informationCutoffAt });
}
export function getAnalysisRun(caseId: string, runId: string): Promise<AnalysisRunDetail> {
  return apiGet<AnalysisRunDetail>(`/cases/${caseId}/analysis-runs/${runId}`);
}
