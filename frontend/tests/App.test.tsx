import { cleanup, render, screen, waitFor } from "@testing-library/react";
import { fireEvent } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router";
import { AppRouter } from "../src/app/router";

const savedCase = {
  caseId: "b2a1cc8a-77de-41fd-9bce-4a4f5f9b2e1a",
  enteredName: "Acme Industries IPO",
  title: "Acme Industries IPO",
  caseStatus: "identity_pending",
  identityStatus: "unresolved",
  issueDisplayName: null,
  lastActivityAt: "2026-10-29T00:00:00Z",
  latestAnalysisRunId: null,
  latestReportId: null,
  warningCount: 0
};

describe("research cases workspace", () => {
  const fetchMock = vi.fn();

  beforeEach(() => {
    fetchMock.mockReset();
    fetchMock.mockImplementation(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      if (url.endsWith("/health")) {
        return new Response(JSON.stringify({
          status: "ok", appVersion: "0.1.0", apiVersion: "v1",
          databaseStatus: "ok", dataDirectoryStatus: "ok", timestamp: "2026-10-29T00:00:00Z"
        }), { status: 200, headers: { "Content-Type": "application/json" } });
      }
      if (url.endsWith("/cases") && init?.method === "POST") {
        const body = JSON.parse(String(init.body)) as { enteredName: string };
        return new Response(JSON.stringify({ ...savedCase, enteredName: body.enteredName, title: body.enteredName, issue: null, createdAt: savedCase.lastActivityAt, updatedAt: savedCase.lastActivityAt, caseChangedSinceLastRun: true, readinessSummary: null }), { status: 201, headers: { "Content-Type": "application/json" } });
      }
      if (url.endsWith("/cases")) {
        return new Response(JSON.stringify({ items: [savedCase], total: 1 }), { status: 200, headers: { "Content-Type": "application/json" } });
      }
      return new Response("Not found", { status: 404 });
    });
    vi.stubGlobal("fetch", fetchMock);
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("loads saved cases from the API", async () => {
    render(<MemoryRouter initialEntries={["/cases"]}><AppRouter /></MemoryRouter>);
    expect(screen.getByRole("heading", { name: /your ipo research, grounded in evidence/i })).toBeInTheDocument();
    expect(await screen.findByRole("heading", { name: "Acme Industries IPO" })).toBeInTheDocument();
    expect(screen.getByText(/local api and database ready/i)).toBeInTheDocument();
  });

  it("creates a case through the API and shows it only after the API responds", async () => {
    render(<MemoryRouter initialEntries={["/cases"]}><AppRouter /></MemoryRouter>);
    fireEvent.change(screen.getByLabelText(/ipo or issuer name/i), { target: { value: "New Mainboard IPO" } });
    fireEvent.submit(screen.getByRole("button", { name: /create research case/i }).closest("form")!);
    await waitFor(() => expect(fetchMock.mock.calls.some(([url, init]) =>
      String(url).endsWith("/cases") &&
      (init as RequestInit | undefined)?.method === "POST" &&
      (init as RequestInit | undefined)?.body === JSON.stringify({ enteredName: "New Mainboard IPO" })
    )).toBe(true));
    expect(await screen.findByRole("heading", { name: "New Mainboard IPO" })).toBeInTheDocument();
  });
});
