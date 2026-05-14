import { INCIDENT_STATUSES } from '../../../shared/constants/incidentStatus';
import Badge from '../../../shared/components/ui/Badge';
import Button from '../../../shared/components/ui/Button';
import { formatRelativeTime } from '../../../shared/utils/formatDate';
import SLAStatusCard from '../../sla/components/SLAStatusCard';
import TriagePanel from '../../triage/components/TriagePanel';
import { normalizeLabel } from '../utils/incidentHelpers';

export default function IncidentDetails({ incident, onStatusChange }) {
  if (!incident) {
    return null;
  }

  return (
    <aside className="detail-panel" aria-label="Selected incident details">
      <div className="detail-heading">
        <Badge tone={`severity-${incident.severity.toLowerCase()}`}>{normalizeLabel(incident.severity)}</Badge>
        <h2>{incident.title}</h2>
        <p>{incident.description}</p>
      </div>
      <dl className="detail-list">
        <div>
          <dt>Status</dt>
          <dd>{normalizeLabel(incident.status)}</dd>
        </div>
        <div>
          <dt>Owner</dt>
          <dd>{incident.assigned_to || 'Unassigned'}</dd>
        </div>
        <div>
          <dt>Category</dt>
          <dd>{normalizeLabel(incident.category || 'UNKNOWN')}</dd>
        </div>
        <div>
          <dt>Created</dt>
          <dd>{formatRelativeTime(incident.created_at)}</dd>
        </div>
      </dl>
      <div className="status-actions">
        {INCIDENT_STATUSES.map((status) => (
          <Button
            className={incident.status === status ? 'selected' : ''}
            key={status}
            tone="ghost"
            onClick={() => onStatusChange(incident, status)}
          >
            {normalizeLabel(status)}
          </Button>
        ))}
      </div>
      <SLAStatusCard incident={incident} />
      <TriagePanel incident={incident} />
    </aside>
  );
}
