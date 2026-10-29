import { apiGet, apiPost } from "./client";

export interface ScenarioDefinition {
  scenarioId: string;
  caseId: string;
  label: string;
  entryPrice: string;
  exitPrice: string;
  quantity: number | null;
  assumptionNote: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface ScenarioPreview {
  label: string;
  entryPrice: string;
  exitPrice: string;
  quantity: number | null;
  grossReturnPct: string;
  grossProfitAmount: string | null;
  netReturnPct: null;
  calculationStatus: "calculated" | "incomplete";
  limitationNote: string;
}

export interface CreateScenarioRequest {
  label: string;
  entryPrice: string;
  exitPrice: string;
  quantity?: number | null;
  assumptionNote?: string | null;
}

export function listScenarios(caseId: string): Promise<{ items: ScenarioDefinition[]; total: number }> {
  return apiGet<{ items: ScenarioDefinition[]; total: number }>(`/cases/${caseId}/scenarios`);
}

export function createScenario(caseId: string, body: CreateScenarioRequest): Promise<ScenarioDefinition> {
  return apiPost<ScenarioDefinition, CreateScenarioRequest>(`/cases/${caseId}/scenarios`, body);
}

export function previewScenario(caseId: string, body: CreateScenarioRequest): Promise<ScenarioPreview> {
  return apiPost<ScenarioPreview, CreateScenarioRequest>(`/cases/${caseId}/scenarios/preview`, body);
}
