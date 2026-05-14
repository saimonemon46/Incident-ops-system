export default function AISummary({ incident }) {
  return (
    <article className="triage-block">
      <h3>AI summary</h3>
      <p>{incident.ai_notes || 'Run triage to generate investigation notes.'}</p>
    </article>
  );
}
