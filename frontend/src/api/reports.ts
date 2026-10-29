import { apiGet, apiPost } from "./client";

export interface ReportSection {
  sectionCode: string; heading: string; bodyMarkdown: string;
  relatedEvidenceIds: string[]; relatedResultIds: string[]; relatedFindingIds: string[]; statusNote: string | null;
}
export interface ReportArtifact {
  artifactId: string; reportId: string; format: "html" | "docx"; sha256: string;
  sizeBytes: number; createdAt: string; downloadUrl: string;
}
export interface ReportDetail {
  reportId: string; caseId: string; analysisRunId: string; generatedAt: string;
  templateVersion: string; reportSnapshotHash: string; title: string; issueDisplayName: string;
  informationCutoffAt: string; sections: ReportSection[]; warnings: string[]; exportArtifacts: ReportArtifact[];
}
export function listReports(caseId: string): Promise<{ items: ReportDetail[]; total: number }> {
  return apiGet<{ items: ReportDetail[]; total: number }>(`/cases/${caseId}/reports`);
}
export function createReport(caseId: string, analysisRunId: string): Promise<ReportDetail> {
  return apiPost<ReportDetail, { analysisRunId: string }>(`/cases/${caseId}/reports`, { analysisRunId });
}
export function exportReport(caseId: string, reportId: string, format: "html" | "docx"): Promise<ReportArtifact> {
  return apiPost<ReportArtifact, { format: "html" | "docx" }>(`/cases/${caseId}/reports/${reportId}/exports`, { format });
}
