import { ApiClientError, readApiError } from "./errors";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ??
  "http://127.0.0.1:8000/api/v1";

// Temporary Phase 0 health response type. Generate full resource types from OpenAPI
// with npm run api:types before implementing additional API resources.
export interface HealthResponse {
  status: "ok" | "degraded";
  appVersion: string;
  apiVersion: "v1";
  databaseStatus: "ok" | "error";
  dataDirectoryStatus: "ok" | "error";
  timestamp: string;
}

export async function apiGet<T>(path: string, timeoutMs = 5_000): Promise<T> {
  const controller = new AbortController();
  const timeoutId = globalThis.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(API_BASE_URL + path, {
      method: "GET",
      headers: { Accept: "application/json" },
      signal: controller.signal
    });
    if (!response.ok) throw await readApiError(response);
    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof ApiClientError) throw error;
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("The local API did not respond in time.");
    }
    throw new Error("Could not reach the local API. Check that the Python backend is running.");
  } finally {
    globalThis.clearTimeout(timeoutId);
  }
}

export function getHealth(): Promise<HealthResponse> {
  return apiGet<HealthResponse>("/health");
}
