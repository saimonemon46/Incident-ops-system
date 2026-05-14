export default function EscalationRules() {
  return (
    <section className="rules-grid">
      <article>
        <strong>Critical</strong>
        <span>Escalate at 15 minutes, breach at 30 minutes.</span>
      </article>
      <article>
        <strong>High</strong>
        <span>Escalate at 60 minutes, breach at 2 hours.</span>
      </article>
      <article>
        <strong>Medium</strong>
        <span>Escalate at 4 hours, breach at 8 hours.</span>
      </article>
    </section>
  );
}
