import { AppRouter } from "./app/router";

export default function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <a className="brand" href="/cases" aria-label="IPO Forensic Analysis Engine home">
          <span className="brand-mark" aria-hidden="true">IF</span>
          <span className="brand-name">IPO Forensic Analysis Engine</span>
        </a>
        <span className="header-tag">LOCAL RESEARCH WORKSPACE</span>
      </header>
      <AppRouter />
      <footer className="app-footer">
        <span>Local-first · Evidence before conclusions</span>
        <span>Indian Mainboard IPOs only</span>
      </footer>
    </div>
  );
}
