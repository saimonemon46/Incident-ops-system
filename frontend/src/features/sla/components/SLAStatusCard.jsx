import { useEffect, useState } from 'react';
import { formatClockTime } from '../../../shared/utils/formatDate';
import { calculateSlaState } from '../api/slaApi';

export default function SLAStatusCard({ incident }) {
  const [slaState, setSlaState] = useState(() => calculateSlaState(incident));

  useEffect(() => {
    setSlaState(calculateSlaState(incident));
    const timer = window.setInterval(() => setSlaState(calculateSlaState(incident)), 1000);
    return () => window.clearInterval(timer);
  }, [incident]);

  return (
    <section className={`sla-card ${slaState.breached ? 'sla-breached' : ''}`}>
      <span>SLA countdown</span>
      <strong>{slaState.breached ? 'Breached' : formatClockTime(slaState.remainingMs)}</strong>
    </section>
  );
}
