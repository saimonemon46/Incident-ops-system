import { formatRelativeTime } from '../../../shared/utils/formatDate';

export default function BreachTimeline({ incidents }) {
  return (
    <section className="timeline">
      {incidents.map((incident) => (
        <article key={incident.id}>
          <strong>{incident.title}</strong>
          <span>{incident.severity} opened {formatRelativeTime(incident.created_at)}</span>
        </article>
      ))}
    </section>
  );
}
