import { INCIDENT_STATUSES } from '../../../shared/constants/incidentStatus';
import { SEVERITIES } from '../../../shared/constants/severity';
import Input from '../../../shared/components/ui/Input';
import { normalizeLabel } from '../utils/incidentHelpers';

export default function IncidentFilters({ filters, onChange }) {
  return (
    <section className="control-strip">
      <Input
        id="incident-search"
        label="Search"
        placeholder="Title, description, owner"
        value={filters.query}
        onChange={(event) => onChange({ ...filters, query: event.target.value })}
      />
      <div className="segmented" aria-label="Filter by status">
        {['ACTIVE', ...INCIDENT_STATUSES, 'ALL'].map((status) => (
          <button
            className={filters.status === status ? 'selected' : ''}
            key={status}
            type="button"
            onClick={() => onChange({ ...filters, status })}
          >
            {normalizeLabel(status)}
          </button>
        ))}
      </div>
      <label className="field" htmlFor="severity-filter">
        <span>Severity</span>
        <select
          id="severity-filter"
          value={filters.severity}
          onChange={(event) => onChange({ ...filters, severity: event.target.value })}
        >
          <option value="ALL">All severities</option>
          {SEVERITIES.map((severity) => (
            <option key={severity} value={severity}>
              {normalizeLabel(severity)}
            </option>
          ))}
        </select>
      </label>
    </section>
  );
}
