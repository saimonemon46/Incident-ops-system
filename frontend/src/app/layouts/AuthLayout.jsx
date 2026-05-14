export default function AuthLayout({ children, title, subtitle }) {
  return (
    <main className="auth-shell">
      <section className="auth-visual" aria-label="Incident Ops">
        <div className="brand-lockup">
          <span className="brand-mark">IO</span>
          <div>
            <strong>Incident Ops</strong>
            <span>Response command center</span>
          </div>
        </div>
        <div className="auth-copy">
          <p>Coordinate incidents, triage faster, and keep SLA pressure visible.</p>
        </div>
      </section>
      <section className="auth-panel">
        <div className="auth-card">
          <p className="eyebrow">Secure access</p>
          <h1>{title}</h1>
          <p className="muted">{subtitle}</p>
          {children}
        </div>
      </section>
    </main>
  );
}
