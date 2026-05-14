import Card from '../../../shared/components/ui/Card';
import { buildIncidentStats } from '../utils/incidentHelpers';

export default function IncidentStats({ incidents }) {
  return (
    <section className="metric-grid" aria-label="Incident metrics">
      {buildIncidentStats(incidents).map((metric) => (
        <Card className={`metric metric-${metric.tone}`} key={metric.label}>
          <span>{metric.label}</span>
          <strong>{metric.value}</strong>
        </Card>
      ))}
    </section>
  );
}
