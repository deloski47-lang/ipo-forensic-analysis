export interface ApiErrorDetail {
  field: string | null;
  issueCode: string | null;
  message: string;
}

export interface ApiErrorEnvelope {
  error?: {
    code?: string;
    message?: string;
    details?: ApiErrorDetail[];
    requestId?: string;
  };
  timestamp?: string;
}

export class ApiClientError extends Error {
  readonly status: number;
  readonly code: string;
  readonly details: ApiErrorDetail[];
  readonly requestId: string | null;

  constructor(
    message: string,
    status: number,
    code = "REQUEST_FAILED",
    details: ApiErrorDetail[] = [],
    requestId: string | null = null
  ) {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.code = code;
    this.details = details;
    this.requestId = requestId;
  }
}

export async function readApiError(response: Response): Promise<ApiClientError> {
  let payload: ApiErrorEnvelope | null = null;
  try {
    payload = (await response.json()) as ApiErrorEnvelope;
  } catch {
    // Non-JSON responses are normalized to a safe message below.
  }

  return new ApiClientError(
    payload?.error?.message ?? "The local API returned HTTP " + response.status + ".",
    response.status,
    payload?.error?.code ?? "REQUEST_FAILED",
    payload?.error?.details ?? [],
    payload?.error?.requestId ?? null
  );
}
