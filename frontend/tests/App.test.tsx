import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router";
import { AppRouter } from "../src/app/router";

describe("application shell", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            status: "degraded",
            appVersion: "0.1.0",
            apiVersion: "v1",
            databaseStatus: "error",
            dataDirectoryStatus: "ok",
            timestamp: "2026-10-29T00:00:00Z"
          }),
          { status: 200, headers: { "Content-Type": "application/json" } }
        )
      )
    );
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("renders the local workspace and displays the API status", async () => {
    render(
      <MemoryRouter initialEntries={["/cases"]}>
        <AppRouter />
      </MemoryRouter>
    );
    expect(screen.getByRole("heading", { name: /your ipo research, grounded in evidence/i })).toBeInTheDocument();
    expect(await screen.findByText(/python api connected/i)).toBeInTheDocument();
    expect(screen.getByText(/local database not initialized/i)).toBeInTheDocument();
  });
});
