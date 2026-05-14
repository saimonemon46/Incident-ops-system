import { SLA_MINUTES_BY_SEVERITY } from '../../../shared/constants/severity';

export const sampleIncidents = [
  {
    id: 'sample-001',
    title: 'Payment gateway timeout spike',
    description: 'Checkout requests are timing out for cards issued by two banks.',
    severity: 'CRITICAL',
    status: 'OPEN',
    assigned_to: 'rahim',
    category: 'PAYMENT',
    suggested_fix: 'Fail over traffic to the secondary gateway and replay stuck callbacks.',
    ai_notes: 'Correlates with gateway p95 latency crossing 8s.',
    created_at: new Date(Date.now() - 1000 * 60 * 18).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 6).toISOString(),
  },
  {
    id: 'sample-002',
    title: 'Login OTP delivery delay',
    description: 'A segment of users are receiving OTP codes after the session expires.',
    severity: 'HIGH',
    status: 'IN_PROGRESS',
    assigned_to: 'nabila',
    category: 'AUTH',
    suggested_fix: 'Move OTP traffic to the priority SMS route until queue depth normalizes.',
    ai_notes: 'Similar incident resolved by provider route switch.',
    created_at: new Date(Date.now() - 1000 * 60 * 74).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 22).toISOString(),
  },
  {
    id: 'sample-003',
    title: 'Support dashboard export failures',
    description: 'CSV exports complete with empty rows for filtered ticket views.',
    severity: 'MEDIUM',
    status: 'RESOLVED',
    assigned_to: 'arif',
    category: 'DATABASE',
    suggested_fix: 'Patch export query to include scoped joins before pagination.',
    ai_notes: 'Blast radius limited to internal operations users.',
    created_at: new Date(Date.now() - 1000 * 60 * 210).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 32).toISOString(),
  },
  {
    id: 'sample-004',
    title: 'Webhook retries backing up',
    description: 'Partner webhooks are retrying after receiving intermittent 503 responses.',
    severity: 'LOW',
    status: 'OPEN',
    assigned_to: '',
    category: 'NETWORK',
    suggested_fix: 'Increase worker concurrency and drain dead-letter candidates.',
    ai_notes: 'No customer-facing transaction loss detected.',
    created_at: new Date(Date.now() - 1000 * 60 * 310).toISOString(),
    updated_at: new Date(Date.now() - 1000 * 60 * 115).toISOString(),
  },
];

export function normalizeLabel(value = '') {
  return value.replaceAll('_', ' ').toLowerCase();
}

export function getSlaDeadline(incident) {
  const createdAt = new Date(incident.created_at).getTime();
  const minutes = SLA_MINUTES_BY_SEVERITY[incident.severity] || SLA_MINUTES_BY_SEVERITY.LOW;
  return createdAt + minutes * 60 * 1000;
}

export function getSlaRemaining(incident) {
  return getSlaDeadline(incident) - Date.now();
}

export function filterIncidents(incidents, filters) {
  return incidents.filter((incident) => {
    const matchesSeverity = filters.severity === 'ALL' || incident.severity === filters.severity;
    const matchesStatus =
      filters.status === 'ALL' ||
      (filters.status === 'ACTIVE' && incident.status !== 'RESOLVED') ||
      incident.status === filters.status;
    const searchText = `${incident.title} ${incident.description} ${incident.assigned_to || ''}`.toLowerCase();
    return matchesSeverity && matchesStatus && searchText.includes(filters.query.toLowerCase());
  });
}

export function buildIncidentStats(incidents) {
  const active = incidents.filter((incident) => incident.status !== 'RESOLVED');

  return [
    { label: 'Active', value: active.length, tone: 'blue' },
    { label: 'Critical', value: active.filter((incident) => incident.severity === 'CRITICAL').length, tone: 'red' },
    { label: 'Unassigned', value: active.filter((incident) => !incident.assigned_to).length, tone: 'amber' },
    { label: 'Resolved', value: incidents.filter((incident) => incident.status === 'RESOLVED').length, tone: 'green' },
  ];
}
