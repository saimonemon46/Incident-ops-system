import IncidentDetails from '../../features/incidents/components/IncidentDetails';
import IncidentList from '../../features/incidents/components/IncidentList';
import { useIncidents } from '../../features/incidents/hooks/useIncidents';

export default function AITriagePage() {
  const { incidents, selectedId, selectedIncident, setSelectedId, updateIncident } = useIncidents();
  const needsTriage = incidents.filter((incident) => incident.status !== 'RESOLVED');

  return (
    <div className="main-grid">
      <IncidentList incidents={needsTriage} selectedId={selectedId} onSelect={setSelectedId} />
      <IncidentDetails incident={selectedIncident} onStatusChange={(incident, status) => updateIncident(incident, { status })} />
    </div>
  );
}
