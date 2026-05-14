import EmptyState from '../../../shared/components/EmptyState';
import IncidentCard from './IncidentCard';

export default function IncidentList({ incidents, selectedId, onSelect }) {
  if (!incidents.length) {
    return <EmptyState title="No incidents found" message="Try a different search or filter set." />;
  }

  return (
    <section className="incident-list" aria-label="Incident queue">
      {incidents.map((incident) => (
        <IncidentCard
          incident={incident}
          isSelected={selectedId === incident.id}
          key={incident.id}
          onSelect={() => onSelect(incident.id)}
        />
      ))}
    </section>
  );
}
