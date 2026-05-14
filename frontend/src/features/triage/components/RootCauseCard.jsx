import { normalizeLabel } from '../../incidents/utils/incidentHelpers';

export default function RootCauseCard({ incident }) {
  return (
    <article className="triage-block">
      <h3>Likely category</h3>
      <p>{normalizeLabel(incident.category || 'UNKNOWN')}</p>
    </article>
  );
}
