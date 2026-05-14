import Badge from '../../../shared/components/ui/Badge';
import { formatRelativeTime } from '../../../shared/utils/formatDate';
import { severityColor } from '../../../shared/utils/severityColor';
import { cn } from '../../../shared/utils/cn';
import { normalizeLabel } from '../utils/incidentHelpers';

export default function IncidentCard({ incident, isSelected, onSelect }) {
  return (
    <button className={cn('incident-row', isSelected && 'selected')} type="button" onClick={onSelect}>
      <span className={`severity-dot severity-${severityColor(incident.severity)}`} />
      <span className="incident-summary">
        <strong>{incident.title}</strong>
        <span>{incident.description}</span>
      </span>
      <span className="row-meta">
        <Badge tone={`status-${incident.status.toLowerCase()}`}>{normalizeLabel(incident.status)}</Badge>
        <span>{formatRelativeTime(incident.updated_at || incident.created_at)}</span>
      </span>
    </button>
  );
}
