import { Navigate, Route, Routes } from "react-router";
import CasesPage from "../pages/CasesPage";

function NotFoundPage() {
  return (
    <main className="page-container">
      <section className="panel">
        <p className="eyebrow">PAGE NOT FOUND</p>
        <h1>This page is not part of the current build.</h1>
        <p className="muted">Return to the local research workspace.</p>
        <a className="button button-primary" href="/cases">Go to workspace</a>
      </section>
    </main>
  );
}

export function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/cases" replace />} />
      <Route path="/cases" element={<CasesPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}
