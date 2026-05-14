export default function SuggestedFixes({ incident }) {
  return (
    <article className="triage-block">
      <h3>Suggested fixes</h3>
      <p>{incident.suggested_fix || 'No response recommendation yet.'}</p>
    </article>
  );
}
