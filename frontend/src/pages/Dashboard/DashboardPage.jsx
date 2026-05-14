import { useMemo, useState } from 'react';
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import Loader from '../../shared/components/Loader';
import Card from '../../shared/components/ui/Card';
import IncidentDetails from '../../features/incidents/components/IncidentDetails';
import IncidentFilters from '../../features/incidents/components/IncidentFilters';
import IncidentList from '../../features/incidents/components/IncidentList';
import IncidentStats from '../../features/incidents/components/IncidentStats';
import { useIncidents } from '../../features/incidents/hooks/useIncidents';
import { filterIncidents } from '../../features/incidents/utils/incidentHelpers';

const chartColors = {
  LOW: '#16a34a',
  MEDIUM: '#d97706',
  HIGH: '#ea580c',
  CRITICAL: '#dc2626',
};

export default function DashboardPage() {
  const {
    incidents,
    isLoading,
    notice,
    selectedId,
    selectedIncident,
    setSelectedId,
    updateIncident,
  } = useIncidents();
  const [filters, setFilters] = useState({ query: '', severity: 'ALL', status: 'ACTIVE' });

  const filteredIncidents = useMemo(() => filterIncidents(incidents, filters), [filters, incidents]);
  const criticalIncidents = incidents.filter((incident) => incident.status !== 'RESOLVED' && incident.severity === 'CRITICAL');
  const chartData = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'].map((severity) => ({
    severity,
    count: incidents.filter((incident) => incident.severity === severity).length,
  }));

  return (
    <>
      {criticalIncidents.length > 0 && (
        <section className="critical-banner">
          <strong>{criticalIncidents.length} critical incident{criticalIncidents.length > 1 ? 's' : ''}</strong>
          <span>Immediate response required for active customer-impacting risk.</span>
        </section>
      )}
      <p className="notice" role="status">{isLoading ? 'Loading incidents...' : notice}</p>
      <IncidentStats incidents={incidents} />
      <Card className="chart-panel">
        <div>
          <p className="eyebrow">Severity mix</p>
          <h2>Incident volume</h2>
        </div>
        <ResponsiveContainer height={220} width="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="severity" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="count" radius={[6, 6, 0, 0]}>
              {chartData.map((item) => (
                <Cell fill={chartColors[item.severity]} key={item.severity} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </Card>
      <IncidentFilters filters={filters} onChange={setFilters} />
      {isLoading ? (
        <Loader />
      ) : (
        <div className="main-grid">
          <IncidentList incidents={filteredIncidents} selectedId={selectedId} onSelect={setSelectedId} />
          <IncidentDetails
            incident={selectedIncident}
            onStatusChange={(incident, status) => updateIncident(incident, { status })}
          />
        </div>
      )}
    </>
  );
}
