import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router";
import { AppRouter } from "../src/app/router";

describe("application shell", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it("renders the local workspace without requiring the API to be online", () => {
    render(
      <MemoryRouter initialEntries={["/cases"]}>
        <AppRouter />
      </MemoryRouter>
    );
    expect(screen.getByRole("heading", { name: /your ipo research, grounded in evidence/i })).toBeInTheDocument();
    expect(screen.getByText(/phase 0 · local scaffold/i)).toBeInTheDocument();
  });
});
