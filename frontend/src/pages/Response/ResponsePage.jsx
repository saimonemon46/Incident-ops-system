import Badge from '../../shared/components/ui/Badge';
import Table from '../../shared/components/ui/Table';
import { useIncidents } from '../../features/incidents/hooks/useIncidents';
import { normalizeLabel } from '../../features/incidents/utils/incidentHelpers';

export default function ResponsePage() {
  const { incidents } = useIncidents();
  const active = incidents.filter((incident) => incident.status !== 'RESOLVED');

  return (
    <section className="page-section">
      <div>
        <p className="eyebrow">Response queue</p>
        <h2>Active ownership</h2>
      </div>
      <Table
        rows={active}
        getRowKey={(row) => row.id}
        columns={[
          { key: 'title', label: 'Incident' },
          { key: 'assigned_to', label: 'Owner', render: (row) => row.assigned_to || 'Unassigned' },
          { key: 'severity', label: 'Severity', render: (row) => <Badge tone={`severity-${row.severity.toLowerCase()}`}>{normalizeLabel(row.severity)}</Badge> },
          { key: 'status', label: 'Status', render: (row) => normalizeLabel(row.status) },
        ]}
      />
    </section>
  );
}
