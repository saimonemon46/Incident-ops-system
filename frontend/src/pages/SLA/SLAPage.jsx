import BreachTimeline from '../../features/sla/components/BreachTimeline';
import EscalationRules from '../../features/sla/components/EscalationRules';
import SLAStatusCard from '../../features/sla/components/SLAStatusCard';
import { useIncidents } from '../../features/incidents/hooks/useIncidents';

export default function SLAPage() {
  const { incidents } = useIncidents();
  const active = incidents.filter((incident) => incident.status !== 'RESOLVED');

  return (
    <section className="page-section">
      <div>
        <p className="eyebrow">SLA Watch</p>
        <h2>Breach risk</h2>
      </div>
      <div className="sla-grid">
        {active.map((incident) => (
          <SLAStatusCard incident={incident} key={incident.id} />
        ))}
      </div>
      <EscalationRules />
      <BreachTimeline incidents={active} />
    </section>
  );
}
