import { ApiClientError, readApiError } from "./errors";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/+$/, "") ??
  "http://127.0.0.1:8000/api/v1";

export interface HealthResponse {
  status: "ok" | "degraded";
  appVersion: string;
  apiVersion: "v1";
  databaseStatus: "ok" | "error";
  dataDirectoryStatus: "ok" | "error";
  timestamp: string;
}

async function request<T>(path: string, init: RequestInit = {}, timeoutMs = 8_000): Promise<T> {
  const controller = new AbortController();
  const timeoutId = globalThis.setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(API_BASE_URL + path, {
      ...init,
      headers: { Accept: "application/json", ...(init.body ? { "Content-Type": "application/json" } : {}), ...init.headers },
      signal: controller.signal
    });
    if (!response.ok) throw await readApiError(response);
    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof ApiClientError) throw error;
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error("The local API did not respond in time.", { cause: error });
    }
    throw new Error("Could not reach the local API. Check that the Python backend is running.", { cause: error });
  } finally {
    globalThis.clearTimeout(timeoutId);
  }
}

export function apiGet<T>(path: string, timeoutMs = 5_000): Promise<T> {
  return request<T>(path, {}, timeoutMs);
}

export function apiPost<T, B = unknown>(path: string, body?: B): Promise<T> {
  return request<T>(path, { method: "POST", ...(body === undefined ? {} : { body: JSON.stringify(body) }) });
}

export function apiPatch<T, B>(path: string, body: B): Promise<T> {
  return request<T>(path, { method: "PATCH", body: JSON.stringify(body) });
}

export function getHealth(): Promise<HealthResponse> {
  return apiGet<HealthResponse>("/health");
}
