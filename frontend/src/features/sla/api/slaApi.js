import { getSlaRemaining } from '../../incidents/utils/incidentHelpers';

export function calculateSlaState(incident) {
  const remainingMs = getSlaRemaining(incident);
  return {
    breached: remainingMs <= 0 && incident.status !== 'RESOLVED',
    remainingMs,
  };
}
