import { apiGet } from "./client";

export interface ReadinessIssue {
  code: string;
  severity: "blocker" | "warning" | "info";
  message: string;
  affectedIndicatorCodes: string[];
  affectedSignalCategories: string[];
  evidenceIds: string[];
  nextAction: string | null;
}

export interface AnalysisReadiness {
  caseId: string;
  status: "ready" | "qualified" | "blocked";
  checkedAt: string;
  informationCutoffAt: string;
  blockers: ReadinessIssue[];
  warnings: ReadinessIssue[];
  readyFormulaCodes: string[];
  skippedFormulaCodes: string[];
  eligibleFindingRuleCodes: string[];
  skippedFindingRuleCodes: string[];
  sourceCoverage: Array<{
    sourceId: string | null;
    sourceName: string;
    signalCategory: string;
    accessStatus: string;
    connectorStatus: string;
    latestCategoryStatus: string;
    latestAttemptAt: string | null;
    latestObservedAt: string | null;
    message: string;
    latestObservationIds: string[];
  }>;
}

export function getAnalysisReadiness(caseId: string): Promise<AnalysisReadiness> {
  return apiGet<AnalysisReadiness>(`/cases/${caseId}/analysis/readiness`);
}
